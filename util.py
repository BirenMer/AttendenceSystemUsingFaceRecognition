import datetime
import os
from stat import ST_CTIME
import face_recognition
import math
import cv2
import numpy as np
import codecs, json
import uuid
import ast
#Added for detection in pi

#Adding imports for requesting
import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder

#globals
unknown_manager = {
    "count":1,
    "lastUnknownCaptureTime":datetime.datetime.now()
}
user_list={}

def open_file(path):
    '''
    Function Name: open_file
    Args: 
        path: It is the path for the file to be opened 
    Usage: It is used to open a file via the path provided
    Returns: None
    '''
    with open(path,'r+') as f :
        contents=f.readlines()
        if contents==[]:
            print("Empty so nothing to update")
        else:
            temp_name=contents[-1]
            name=temp_name.split(' ')
            name_org=name[1].rstrip()
            user_list.update({name_org:temp_name})
        f.close()
def mark_logs_general(path,name,filename):
    '''
    Function Name: mark_logs_general
    Args: 
        path: Path for the file 
        name: Name for the detected person (name of the employee or unknown)
        filename: Name of the file in which we want to enter the log
    Usage: It is used to add mark general logs of the all the known users.
    Returns: None
    ''' 
    initial_headers="Device Id,Group Id,Employee Code,Confidence,No. of Person,Date Time,Known,Unknown,Image Path"+"\n"

    current_new_path=os.path.join(path,filename)
    current_new_path_folder=path
    temp_name=str(name)
    # print("Type check 1",type(name),type(temp_name))
    
    if(os.path.exists((current_new_path_folder))):
         print("Exits general")
    else:
         os.makedirs(current_new_path_folder)
    if(os.path.exists(current_new_path)):
            #  open_file(current_new_path)
             if (user_list=={}):
                 write_to_file(current_new_path,temp_name)
                 user_list.update({name:temp_name})
             else:
                 if(name in user_list and user_list[name]== temp_name):
                        return False
                 else:
                     write_to_file(current_new_path,temp_name)
                     user_list.update({name:temp_name})
    else:
             with open(current_new_path,'+a') as f:
                  f.write(initial_headers)
                  f.close()
            #  open_file(current_new_path)
             if (user_list=={}):
                 write_to_file(current_new_path,temp_name)
                 user_list.update({name:temp_name})
             else:
                 if(name in user_list and user_list[name]== temp_name):
                        return False
                 else:
                     write_to_file(current_new_path,temp_name)
                     user_list.update({name:temp_name})


def mark_logs_individual(path,name,log_name,filename):
    '''
    Function Name: mark_logs_individual
    Args: 
        path: Path for the file 
        name: Name for the detected person (name of the employee or unknown)
        log_name:Total log info string
        filename: Name of the file in which we want to enter the log
    Usage: It is used to add mark individual logs of the all the known users.
    Returns: None
    ''' 
    initial_headers="Device Id,Group Id,Employee Code,Confidence,No. of Person,Date Time,Known,Unknown,Image Path"+"\n"
    
    current_new_path=os.path.join(path,name,filename)
    current_new_path_folder=os.path.join(path,name)
    temp_name=log_name
    if(os.path.exists((current_new_path_folder))):
         print("Exits")
    else:
         os.makedirs(current_new_path_folder)
    if(os.path.exists(current_new_path)):
             open_file(current_new_path)

             if (user_list=={}):
                 write_to_file(current_new_path,temp_name)
                 user_list.update({name:temp_name})
             else:
                 if(name in user_list and user_list[name]== temp_name):
                        return False
                 else:
                     write_to_file(current_new_path,temp_name)
                     user_list.update({name:temp_name})
    else:
             with open(current_new_path,'+a') as f:
                    f.write(initial_headers)
                    f.close()
             open_file(current_new_path)
             if (user_list=={}):
                 write_to_file(current_new_path,temp_name)
                 user_list.update({name:temp_name})
             else:
                 if(name in user_list and user_list[name]== temp_name):
                        return False
                 else:
                     write_to_file(current_new_path,temp_name)
                     user_list.update({name:temp_name})

def write_to_file(file_path,name):
    '''
    Function Name: write_to_file
    Args: 
        file_path: Path for the file in which we want to write
        name: detected name
    Usage: It is used to write the provided argument in the file with the give file_path.
    Returns: None
    # '''    
    name=str(name)
    
    with open(file_path, 'a') as f:  
        f.write(name)
        f.close()

def unkonwn_capture(frame,path):
    global unknown_manager
    '''
    Function Name: unkonwn_capture
    Args: 
        frame: Image to be saved
        path: Path for saving the image
    Usage: It is used to capture the unknown faces and saves them to the porvided path
    Returns: None 
    '''
    print("path",path)
    dir_list=lastest_created(path)
    temp_date_time = datetime.datetime.now()
    capture_time=datetime.datetime.now().strftime("%d-%m-%Y_%H:%M")
    is_written = False
    if dir_list==[]:
        print('Capturing 1st image')
        temp_path=capture_time+' Unknown_1.jpg'
        new_path=os.path.join(path,temp_path)
        is_written = cv2.imwrite(new_path, frame)
        unknown_manager['count'] = unknown_manager['count'] + 1
        write_path=new_path
    else:
        # if countx != 1:
        temp = unknown_manager['lastUnknownCaptureTime'] + datetime.timedelta(seconds=1)
        
        if  temp_date_time.time() > temp.time() or unknown_manager['count'] == 1:
            temp_path=capture_time+' Unknown_'+str(unknown_manager['count'])+'.jpg'

            write_path=path+"/"+temp_path
            is_written = cv2.imwrite(write_path, frame)
            unknown_manager['count'] = unknown_manager['count'] + 1
            unknown_manager['lastUnknownCaptureTime'] = temp_date_time
            # print(unknown_manager['count'])
    if is_written:
        print("Image Saved")
        return write_path
    else:
        return ""
def lastest_created(main_folder_path):
        '''
        Function Name: lastest_created
        Args: 
            main_folder_path: Path for the folder where we want to check for the lastest file
        Usage: It is used to find the folder/file with the latest creation time and retrun the file path 
        Returns: temp_path (path for the latest found folder)
        '''
        dir_path = main_folder_path
        folder_timestamp=[]
        # get all entries in the directory
        folder_list = tuple((os.path.join(dir_path,file_name) for file_name in os.listdir(dir_path)))
        if (folder_list==()):
            #It returns a empty list if no file is found inside a folder
            return []
        else:
        # Get their stats
            folder_list = tuple(((os.stat(path), path) for path in folder_list))
        # leave only regular files, insert creation date
            folder_list = tuple(((stat[ST_CTIME], path)
                   for stat, path in folder_list ))
            for x in folder_list:
                folder_timestamp.append(x[0])
            sorted_folder_timestamp=sorted(folder_timestamp)
            for j in folder_list:
                    if sorted_folder_timestamp[-1]==j[0]:
                        temp_path=j[1]
            return temp_path 
def folder_check_for_unknown_image():
    '''
        Function Name: folder_check_for_unknown_image
        Args: None
        Usage: It is used to create punch in and punch out path to save the images of any unknonw person detected
        Returns: punch_in_path, punch_out_path
    '''
    current_date=datetime.date.today()
    current_path=os.getcwd()
    punch_path=os.path.join(current_path,"unknown_capture",str(current_date),"punch")    
    if(os.path.exists(punch_path)):
                return punch_path
    else:
        os.makedirs(punch_path)
        return punch_path
#fucntion to check all the know paths of the folder 
def folder_check_for_known_image():
    '''
        Function Name: folder_check_for_known_image
        Args: None
        Usage: It is used to create punch in and punch out path to save the images of any knonw person detected
        Returns: punch_in_path, punch_out_path
    ''' 
    current_path=os.getcwd()  
    current_date=datetime.date.today()
    punch_path=os.path.join(current_path,"attendance_capture",str(current_date),"punch")
    
    if(os.path.exists(punch_path)):
        return punch_path
    else:
        os.makedirs(punch_path)
        return punch_path
def folder_check_for_known_logs():
    '''
        Function Name: folder_check_for_known_logs
        Args: None
        Usage: It is used to create punch in and punch out path to save the logs of any knonw person detected
        Returns: punch_in_path, punch_out_path
    ''' 
    current_path=os.getcwd()  
    current_date=datetime.date.today()
    punch_path=os.path.join(current_path,"logs",str(current_date),"punch_logs")
    if(os.path.exists(punch_path)):
        return punch_path
    else:
        os.makedirs(punch_path)
        return punch_path
def folder_check_for_known_logs_general():
    '''
        Function Name: folder_check_for_known_logs_general
        Args: None
        Usage: It is used to create punch in and punch out path to save the general logs of all the knonw person detected
        Returns: punch_in_path, punch_out_path
    ''' 
    current_path=os.getcwd()  
    current_date=datetime.date.today()
    punch_path=os.path.join(current_path,"logs",str(current_date),"general","punch_logs")
    
    if(os.path.exists(punch_path)):
        return punch_path
    else:
        os.makedirs(punch_path)
        return punch_path

def folder_check_for_unknown_logs():
      '''
        Function Name: folder_check_for_unknown_logs
        Args: None
        Usage: It is used to create punch in and punch out path to save the  logs of all the unknonw person detected
        Returns: punch_in_path, punch_out_path
      ''' 
      current_path=os.getcwd()  
      current_date=datetime.date.today()
      punch_path=os.path.join(current_path,"logs",str(current_date),"Unknown","punch_in")
      if(os.path.exists(punch_path)):
           return punch_path
      else:
        os.makedirs(punch_path)
        return punch_path
           
def save_images_known(path,name,img_format,frame):
    '''
        Function Name: save_images_known
        Args: path,name,img_format,frame
        Usage: It is used to save the images of the know persons to the provided path
        Returns: None
    '''
    check_path=os.path.join(path,name)
    capture_time=datetime.datetime.now().strftime("%d-%m-%Y_%H:%M:%S")
    temp_name=capture_time+' '+name+img_format
    is_written=False
    if(os.path.exists(check_path)):
        check_list=os.listdir(check_path)
        if(temp_name in check_list):
            print("name exists")
        else:
            temp_path=os.path.join(check_path,temp_name)
            is_written = cv2.imwrite(temp_path, frame)
    else:
        os.makedirs(check_path)
        temp_path=os.path.join(check_path,temp_name)
        is_written = cv2.imwrite(temp_path, frame)
    if is_written:
        print("Image for {} saved".format(name))
        return temp_path
    else:
        return ""
def folder_check_for_captured():
      '''
        Function Name: folder_check_for_person
        Args: None
        Usage: It is used create the path for sameing the images of the detected person
        Returns: punch_in_path,punch_out_path
      '''
      current_path=os.getcwd()  
      current_date=datetime.date.today()
      punch_in_path=os.path.join(current_path,"capture",str(current_date),"punch_in")
      if(os.path.exists(punch_in_path)):
        return punch_in_path
      else:
        os.makedirs(punch_in_path)
        return punch_in_path
def save_person_img(path,image):
    '''
        Function Name: save_images_known
        Args: path,images
        Usage: It is used to save the images of the detected persons to the provided path
        Returns: person_img_save_path
    '''
    current_path=path
    current_timestamp=datetime.datetime.now().strftime("%d-%m-%Y_%H:%M:%S")
    temp_name=str(uuid.uuid1())+"_"+str(current_timestamp)+"_person.jpg"
    person_img_save_path=os.path.join(current_path,temp_name)
    is_written=False    
    is_written=cv2.imwrite(person_img_save_path,image)
    if(is_written):
        print("Saved successfully")
    
def final_log_marker(known_list,unknown_list,known_counter,unknown_counter,name,unknown_path_image,known_path_image):
        '''
         Function Name: final_log_marker
         Args: known_list,unknown_list,face_count,person_count,known_faces_count,unknown_faces_count
         Usage: It is used to process and mark logs for all users when the detection part is completed.
         Returns: None 
        '''
        ##Declaring the paths for logging 
        date=datetime.datetime.now().strftime("%d-%m-%Y")
        file_name=str(date)+".csv"
        unknown_path=folder_check_for_unknown_logs()
        general_path=folder_check_for_known_logs_general()
        individual_path=folder_check_for_known_logs()

        if(len(known_list)>0):
            for i in known_list:
                 temp_string=i+","+str(known_counter)+","+str(unknown_counter)+","+str(known_path_image)+"\n"
                 mark_logs_general(general_path,temp_string,"general_log.csv")
                 mark_logs_individual(individual_path,name,temp_string,file_name)
        if(len(unknown_list)>0):
            for j in unknown_list:
                 temp_string=j+","+str(known_counter)+","+str(unknown_counter)+","+str(unknown_path_image)+"\n"
                 mark_logs_general(general_path,temp_string,"general_log.csv")
                 mark_logs_individual(unknown_path,name,temp_string,file_name)


def group_count_reseter(groupcounter,date):
    current_date=datetime.datetime.now().strftime("%d-%m-%Y")
    if(current_date!=date):
        groupcounter=0
        return groupcounter
    else:
        return groupcounter
# Adding API request 
def api_caller(image_path):
    dt_string=datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")

    image_path=image_path
    url = "http://localhost:8000/api/v1/recognition/recognize"

    params = {
            "face_plugins": "landmarks,gender, age"
        }

    mp_encoder = MultipartEncoder(
        fields={
            # plain file object, no filename or mime type produces a
            # Content-Disposition header with just the part name
            'file': ('1.jpg', open(image_path, 'rb'), 'image/jpeg'),
        }
    )

    response = requests.post(url,params=params, data=mp_encoder,headers={'Content-Type': mp_encoder.content_type, "x-api-key": "fdd2d586-a3fa-4e7a-a029-b549a50dbe16"})
    print(response)
        # Check the response status
    if response.status_code == 200:
            # API call successful
            print("API call successful!")
            # print(response.json())
            return response,dt_string
    else:
            # API call failed
            print(response.status_code)
            print("API call failed!")
            print(response.text)
            return "",""
    
def response_logger(frame,response,group_counter,device_id,date_time):
    # print("Entered Logger")
    print("Response type",type(response))
    # print("REsults",response[0].json())
    data = response.json()

    unkonwn_capture_path=folder_check_for_unknown_image()
    known_capture_path=folder_check_for_known_image()
    
    known_list=[]
    unknown_list=[]
    known_counter=0
    unknown_counter=0
    name="unkonwn"
    unknonw_flag=False
    knonw_flag=False
    known_path_image="None"
    unknown_path_image="None"

    if response!="":
        person=len(data['result'])
        for i in data['result']:
            for j in i['subjects']:
                 if(j['similarity']>0.90):  
                    temp_string=str(device_id)+","+str(group_counter)+","+str(j['subject'])+","+str(j['similarity'])+","+str(person)+","+str(date_time)
                    known_list.append(temp_string)
                    known_counter=known_counter+1
                    name=str(j['subject'])
                    knonw_flag=True
                 else:
                    temp_string=str(device_id)+","+str(group_counter)+","+"Unknown"+","+str(j['similarity'])+","+str(person)+","+str(date_time)
                    unknown_list.append(temp_string)
                    unknown_counter=unknown_counter+1
                    unknonw_flag=True
            if(unknonw_flag):
                 unknown_path_image=unkonwn_capture(frame,unkonwn_capture_path)
            if(knonw_flag):
                 known_path_image=save_images_known(known_capture_path,str(date_time),'.jpg',frame)
        final_log_marker(known_list,unknown_list,known_counter,unknown_counter,name,unknown_path_image,known_path_image) 
                 