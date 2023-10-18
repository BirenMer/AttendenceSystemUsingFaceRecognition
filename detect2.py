"""Main script to run the object detection routine."""
import sys
import time
import cv2
from util import *

import os

punch_in_known_log_path=folder_check_for_known_logs()
#Punch in/out path for unknow person Logs
punch_unknown_log_path=folder_check_for_unknown_logs()
#Punch in/out path for person folder
punch_path_person=folder_check_for_captured()

def run(camera_ip, width, height, cam_number,window_name):
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
  group_count=0
  # start_time = time.time()

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

    image = cv2.flip(image, 1)

    # Convert the image from BGR to RGB as required by the TFLite model.
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    #Resizing
    rgb_image = cv2.resize(image,(0,0),fx=1,fy=1)
    group_count=group_count+1
    face_locations = face_recognition.face_locations(rgb_image,number_of_times_to_upsample=1,model="hog")
    total_faces=len(face_locations)
    if total_faces>0:
      print("face got") #if any frame is found the processing it
      test_path=save_person_img(punch_path_person,image) 
      response,date_time=api_caller(test_path)
      # print("Response type",type(response.data))
      if response!="":
        response_logger(rgb_image,response,group_count,0,date_time)
              # process_frame_with_face_locations(frame,encodings,names,1,total_faces)
  # Stop the program if the ESC key is pressed.
    if( cv2.waitKey(1) == 27):
      break
    cv2.imshow(window_name, image)

  cap.release()
  cv2.destroyAllWindows()
  
    
# run("http://192.168.3.143:4747/video", 640, 480,0,"Punch_Out")
run(0, 640, 480,0,"Punch_Out")

