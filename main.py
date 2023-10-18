import cv2
from sklearn import svm
import os
# from stat import ST_CTIME
from  util  import *
from datetime import datetime
import threading

#Creating the lists to store encodings,names and classnames
encodings=[]
names=[] 
className=[]

#Fetching the data to train the model from train_dir
# train_dir=os.listdir('train_dir/')

# thread_pool=[]
# #Loop for fetching the folder for each image
# for person in train_dir:
#     #print("Training model for : "+person)
#     #creating a list to store all this folders
#     pix=os.listdir("train_dir/"+person+"/")
    
#     #loop to go thorough each folder and fetch images
#     for person_img in pix:
#         #loading the images to the algo
#         # thread_pool.append(threading.Thread(target=processlist,args=(person,person_img,encodings,names)))
#         processlist(person,person_img,encodings,names)
current_working_dir=os.getcwd()
file_name="encodings.txt"
file_path_for_encodings=os.path.join(current_working_dir,file_name)
encodings,names=retrive_encodings(file_path_for_encodings)
punch_in_known_image_path,punch_out_known_image_path=folder_check_for_known_image()
punch_in_unknown_image_path,punch_out_unknown_image_path=folder_check_for_unknown_image()
punch_in_known_log_path,punch_out_known_log=folder_check_for_known_logs()
punch_in_unknown_log_path,punch_out_unknown_log_path=folder_check_for_unknown_logs()

clf=svm.SVC(gamma='scale')
clf.fit(encodings,names)
print("Training Complete")
    
# known_face_encodings = encodings
# classNames=names
print('Encoding Complete')

# video_capture = cv2.VideoCapture("http://192.168.55.37:81/stream")
video_capture = cv2.VideoCapture(0)

count=0

while True:
    dt=datetime.now()
    # print("Fetching image ",dt)
    # Grab a single frame of video
    ret, frame = video_capture.read()
    # dtx=datetime.now()

    # print("done fetching image ",dtx)
    # if(count%3==0):
        # threading.Thread(target=process_frame,args=(ret,frame,known_face_encodings,class_names)).start()
    if(ret==False):
        print("Stopped excection")
    else:
        process_frame(ret,frame,encodings,names,1)

        cv2.imshow('Video_cam', frame)

            # Hit 'q' on the keyboard to quit!c
        if cv2.waitKey(1) & 0xFF == ord('q'):
                break

# Release handle to the webcam
video_capture.release()
cv2.destroyAllWindows()