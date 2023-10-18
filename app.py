import face_recognition
import cv2
from sklearn import svm
from sklearn.metrics import accuracy_score
import numpy as np
import os
from datetime import datetime
import math


#Creating the lists to store encodings,names and classnames
encodings=[]
names=[]
className=[]

#Fetching the data to train the model from train_dir
train_dir=os.listdir('train_dir/')

#loop for fetching the folder for each image
for person in train_dir:
    print("Training model for : "+person)
    #creating a list to store all this folders
    pix=os.listdir("train_dir/"+person+"/")
    
    #loop to go thorough each folder and fetch images
    for person_img in pix:
        #loading the images to the algo
        face_img=face_recognition.load_image_file("train_dir/"+person+"/"+person_img)
        #Getting the face Locations for each image
        face_loc=face_recognition.face_locations(face_img)
        #the above function will retrun an array/List of tuples
        #Now if a face a single face is found in a image then one we will train our else we will discard that image
        if len(face_loc)==1:
            #Providing face to the algo to train
            face_enc=face_recognition.face_encodings(face_img)[0]
            #The above function will learing from the image and will remember the encodings
            #adding this encodings to the encoding list
            encodings.append(face_enc)
            #adding the name of the person to the names list
            names.append(person)
        #Checking the condition for more than one face
        elif len(face_loc)>1:
            print(person + "/" + person_img + " was skipped => More than one face was detected")
        #IF not face is detected then we can go to this  
        else:
            print(person + "/" + person_img + " was skipped => No face was detected")

#Creating and training the SVC classifier
clf =svm.SVC(gamma='scale')
clf.fit(encodings,names)
print("Training Complete")

def markAttendancePresent(name):
    with open('AttendancePresent.csv', 'r+') as f:
        myDataList = f.readlines()
        nameList = []
        for line in myDataList:
            entry = line.split(',')
            nameList.append(entry[0])
            if name not in nameList:
                now = datetime.now()
                dtString = now.strftime('%Y/%m/%d-%H:%M:%S')
                f.writelines(f'\n{name},{dtString}')
def markAttendanceAbsent(name):
    with open('AttendanceAbsent.csv', 'r+') as f:
        myDataList = f.readlines()
        nameList = []
        for line in myDataList:
            entry = line.split(',')
            nameList.append(entry[0])
            if name not in nameList:
                now = datetime.now()
                # print(now)
                dtString = now.strftime('%Y/%m/%d-%H:%M:%S')
                f.writelines(f'\n{name},{dtString}')
    
known_face_encodings = encodings
classNames=names
print('Encoding Complete')


def face_distance_to_conf(face_distance, face_match_threshold=0.6):
    if face_distance > face_match_threshold:
        range = (1.0 - face_match_threshold)
        linear_val = (1.0 - face_distance) / (range * 2.0)
        return linear_val
    else:
        range = face_match_threshold
        linear_val = 1.0 - (face_distance / (range * 2.0))
        return linear_val + ((1.0 - linear_val) * math.pow((linear_val - 0.5) * 2, 0.2))
video_capture = cv2.VideoCapture("http://192.168.55.43:81/stream")

name = "Unknown"
flag=False

while True:
    # Grab a single frame of video
    ret, frame = video_capture.read()

    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    rgb_frame = frame[:, :, ::-1]

    # Find all the faces and face enqcodings in the frame of video
    face_locations = face_recognition.face_locations(rgb_frame)
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)
   
    # Loop through each face in this frame of video
    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        # See if the face is a match for the known face(s)
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
        # Or instead, use the known face with the smallest distance to the new face
        face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
        best_match_index = np.argmin(face_distances)
        if matches[best_match_index]:
            # print(face_distances)
            acc=face_distance_to_conf(face_distances[best_match_index])
            if(acc>0.9):
                name = classNames[best_match_index]
                flag=True
        else:
            flag=False
            
        # Draw a box around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 255), 2)

        # Draw a label with a name below the face
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        if(flag):
            # For known
            percentage=round(acc,2) *100       
            f=name+"-"+str(percentage)
            cv2.putText(frame, f, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
            markAttendancePresent(name)

        else:
            #For unkown
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
        # marking attendence
            markAttendanceAbsent(name)
    # Display the resulting image
    cv2.imshow('Video', frame)

    # Hit 'q' on the keyboard to quit!c
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release handle to the webcam
video_capture.release()
cv2.destroyAllWindows()