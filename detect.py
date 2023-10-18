"""Main script to run the object detection routine."""
import sys
import time
import cv2
from util import *

import os
#Creating the lists to store encodings,names and classnames
encodings=[]
names=[] 
class_names=[]
current_working_dir=os.getcwd()
file_name="encodings.txt"
file_path_for_encodings=os.path.join(current_working_dir,file_name)
encodings,names=retrive_encodings(file_path_for_encodings)
#Punch in/out path for know person images
punch_in_known_image_path,punch_out_known_image_path=folder_check_for_known_image()
#Punch in/out path for unknow person images
punch_in_unknown_image_path,punch_out_unknown_image_path=folder_check_for_unknown_image()
#Punch in/out path for person folder
punch_in_path_person,punch_out_path_person=folder_check_for_person()
punch_log_path_known=folder_check_for_known_logs()
punch_log_general_path_known=folder_check_for_known_logs_general()
punch_log_path_unknown=folder_check_for_unknown_logs()

def run(model,camera_ip, width, height, num_threads,enable_edgetpu,cam_number,window_name):
  """Continuously run inference on images acquired from the camera.
  Args:
    model: Name of the TFLite object detection model.
    camera_id: The camera id to be passed to OpenCV.
    width: The width of the frame captured from the camera.
    height: The height of the frame captured from the camera.
    num_threads: The number of CPU threads to run the model.
    enable_edgetpu: True/False whether the model is a EdgeTPU model.
  """
  test_path="" 
  # Variables to calculate FPS
  counter, fps = 0, 0
  group_count=0
  start_time = time.time()

  # Start capturing video input from the camera
  cap = cv2.VideoCapture(camera_ip)
  cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
  cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)


  # Continuously capture images from the camera and run inference
  while cap.isOpened():
    #Ask mohit
    current_date=datetime.datetime.today().strftime("%d-%m-%Y")
    group_count=group_count_reseter(group_count,current_date)
    
    success, image = cap.read()
    if not success:
      sys.exit(
          'ERROR: Unable to read from webcam. Please verify your webcam settings.'
      )

    counter += 1
    image = cv2.flip(image, 1)

    # Convert the image from BGR to RGB as required by the TFLite model.
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    #Resizing
    rgb_image=cv2.resize(image,(0,0),fx=1,fy=1)

    face_locations = face_recognition.face_locations(rgb_image,number_of_times_to_upsample=1,model="hog")
    total_faces=len(face_locations)
    if total_faces!=0:
          #checking the distance of the face deteced     
          group_count=group_count+1          
          print("face got") #if any frame is found the processing it
          if(cam_number==1):
            test_path=save_person_img(punch_in_path_person,image)

          else:
            test_path=save_person_img(punch_out_path_person,image)
          
      
          if(os.path.exists(test_path)):
              frame=cv2.imread(test_path)
              print("Calling detector")
              # person_count=person_detector_and_counter(test_path,'efficientdet_lite0.tflite',False,4)
              process_frame_with_face_locations(frame,encodings,names,1,total_faces,group_count)
          else:
            continue
    # Stop the program if the ESC key is pressed.
    # if( cv2.waitKey(1) == 27):
    #   break
    # cv2.imshow(window_name, image)

  cap.release()
  cv2.destroyAllWindows()
  if(test_path!=""):
    return test_path
  else:
    return ""

run('efficientdet_lite0.tflite', "http://192.168.55.17:81/stream", 640, 480,4, False,1,"Punch_In")
