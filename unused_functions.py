# def stream(video_capture,known_face_encodings,class_names,Camera_number):
#     '''
#     Function Name: stream
#     Args: video_capture,known_face_encodings,class_names,Cam
#     Usage: It is used to call the process_frame function 
#     Returns: Void
#     '''
#     # Camera_number=Camera_number #Removing this for optimization
#     while True:
#         ret, frame = video_capture.read()
#         process_frame(ret,frame,known_face_encodings,class_names,Camera_number)
#         cv2.imshow('Video_cam', frame)
#         # Hit 'q' on the keyboard to quit!c
#         if cv2.waitKey(1) & 0xFF == ord('q'):
#             break
#         # Release handle to the webcam
#     video_capture.release()
#     cv2.destroyAllWindows()

# def process_frame(ret,frame,known_face_encodings,class_names,camera_number):
#     '''
#     Function Name: process_frame
#     Args: ret,frame,known_face_encodings,class_names,Cam
#     Usage: It is used to compare the faces in the live stream with the previosly encoded faces.
#     Returns: void 
#     '''
#     # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    
#     small_frame=cv2.resize(frame,(0,0),fx=1,fy=1)
#     # rgb_small_frame = small_frame[:, :, ::-1] #Well this is removed as it causes wierd behaviour in the code and give error as soon as any face is detected.
#     rgb_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)


#     # Find all the faces and face enqcodings in the frame of video
#     face_locations = face_recognition.face_locations(rgb_frame,number_of_times_to_upsample=1,model="hog")
#     face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)
   
#     # Loop through each face in this frame of video
#     for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
#         # See if the face is a match for the known face(s)
#         matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
#         # Or instead, use the known face with the smallest distance to the new face
#         face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
#         best_match_index = np.argmin(face_distances)
#         name = "Unknown" #using the default name as unkonwn
#         flag=False #creating a flag if the identified person is unknown
#         if matches[best_match_index]:
#             # print(face_distances)
#             acc=face_distance_to_conf(face_distances[best_match_index])
#             if(acc>0.9):
#                 name = class_names[best_match_index] #if the person is identified then settign the name accordingly
#                 flag=True #setting the flag to true if the person is know 
#         else:
#             flag=False #else trying to reset the flag also checking the flag for each frame to avoid conflict
            
#         # Draw a box around the face
#         cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 255), 2)

#         # Draw a label with a name below the face
#         cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
#         font = cv2.FONT_HERSHEY_DUPLEX
#         #Setting paths
#         punch_in_path_known,punch_out_path_known=folder_check_for_known_image()
#         punch_in_log_path_known,punch_out_log_path_known=folder_check_for_known_logs()
#         unknown_punch_in_log_path,unknown_punch_out_log_path=folder_check_for_unknown_logs()
#         unkonwn_image_punch_in_path,unkonwn_image_punch_out_path=folder_check_for_unknown_image()

#         if(flag):
#             # For known
#             percentage=round(acc,2) *100       
#             f=name+"-"+str(percentage)
#             cv2.putText(frame, f, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
#             if (camera_number==1): #checkign the flag for camera if cam is one then we mark punch in else punch out
#                 mark_logs(punch_in_log_path_known,name,"punch_in.csv")
#                 save_images_known(punch_in_path_known,name,".jpg",frame)
#             else:
#                 mark_logs(punch_out_log_path_known,name,"punch_out.csv")
#                 save_images_known(punch_out_path_known,name,".jpg",frame)

#         else:
#             #For unkown
#             cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
#             # marking attendence
#             if (camera_number==1):
#                 unkonwn_capture(frame,unkonwn_image_punch_in_path)
#                 mark_logs(unknown_punch_in_log_path,name,"unkonwn_punch_in.csv")
#             else:
#                 unkonwn_capture(frame,unkonwn_image_punch_out_path)
#                 mark_logs(unknown_punch_out_log_path,name,"unkonwn_punch_out.csv")
#         # cv2.imshow('frame1', frame)  