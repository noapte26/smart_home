import cv2
import face_recognition
import dlib
import numpy as np
import os
import serial 
import customtkinter as ctk
import time
from PIL import Image, ImageTk
import gui1
import gui



''' deep learnong algorithm based face detector (convolutional neural network)'''
cnn_face_detector = dlib.cnn_face_detection_model_v1("mmod_human_face_detector.dat")

''' it's a deep learning model that uses neural network to generate embiddings
which is a 128-dimentional numerical vector having all the important features of the face
and is better used by the face recognition model to compare images instead of the normal image'''
embedding_model = dlib.face_recognition_model_v1("dlib_face_recognition_resnet_model_v1.dat")

''' this predictor model finds 68 crusial landscapes points on the image, like the eyes, nose, ...'''
shape_predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")


#ser = serial.Serial('COM1', 9600, timeout=1)  # get serial instance and set timeout to 1, it returns all available bytes after 1s
#print(ser.name)

def send_signal(signal):
    ser.write(signal.encode())
    print(f'sent {signal} to mc')
    
def recieve_message():
    while ser.in_waiting():   #when there is data available
        message_inBytes = ser.readline()
        message_string = message_inBytes.decode('utf-8').strip() #decode and strip away excess characters
        print(f'recieved {message_string} from mc ')
        return message_string


 


def adding_photoFolder_to_Dataset(folder_path, person_name, database_path = 'dataset'):
    photos = os.listdir(folder_path)
    count = 0
    conf_thresh = 0.6
    person_folder_path = os.path.join(database_path, person_name)
    for photo in photos:
        photo_path = os.path.join(folder_path, photo)   # or = f"{folder_path}/{photo}"
        img = cv2.imread(photo_path)
        rgb_photo = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        
        faces = cnn_face_detector(rgb_photo)
        
        for face in faces :
            
            face_conf = face.confidence
            if face_conf < conf_thresh:
                continue
            
            x1 = face.rect.left()
            y1 = face.rect.top()
            x2 = face.rect.right()
            y2 = face.rect.bottom()
            
            cv2.rectangle(img, (x1, y1), (x2, y2), (255, 0, 255), 2)
            
            extracted_face = img[y1:y2, x1:x2]
            extracted_face_path = f"{person_folder_path}/{person_name}_{count}.png"
            cv2.imwrite(extracted_face_path, extracted_face)
    
    generate_embeddings(person_name)
            



def capture_owners_face(name, database_path = 'dataset'):
    
    webcam = cv2.VideoCapture(0)
    
    if not os.path.exists(database_path):
        os.makedirs(database_path)
    if not os.path.exists(f"{database_path}/{name}"):
        os.makedirs(f"{database_path}/{name}")
        
    count = 0
    while 1:
        ret, imageframe = webcam.read()
        if not ret:   #in case of error in capturing
            break
        #img = cv2.resize(imageframe, (0,0, fx=0.5, fy=0.5))  # to make the processing take less time
        rgb_image = cv2.cvtColor(imageframe, cv2.COLOR_BGR2RGB)   #as cnn detector works with rgb
        faces = cnn_face_detector(rgb_image, 1)

        for i, face in enumerate(faces):   
            x1 = face.rect.left()   # get the cnn regtangle coordinates
            y1 = face.rect.top()
            x2 = face.rect.right()
            y2 = face.rect.bottom()

            cv2.rectangle(imageframe, (x1, y1), (x2, y2), (255, 0, 255), 2)  #draw a cv2 recatngle

            
            extracted_face = imageframe[y1:y2, x1:x2]
            face_file_path = f"{database_path}/{name}/{name}_{count}.png"
            cv2.imwrite(face_file_path, extracted_face)
            print(f"Saved {face_file_path}")

            count += 1

        cv2.imshow('Video', imageframe)
        
        # Press 'q' to quit capturing
        if cv2.waitKey(1) & 0xFF == ord('q'):
            webcam.release()
            cv2.destroyAllWindows()
            break

    
  
  
        
def generate_embeddings(name, database_path = 'dataset'):
    
    embeddings = []   #the array of embeddings
    
    faces_imgs = os.listdir(f"{database_path}/{name}")  #get all the stored faces in that folder
    
    for img in faces_imgs:
        img_path = f"{database_path}/{name}/{img}"
        image = cv2.imread(img_path)
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        faces = cnn_face_detector(rgb_image)   # to get the rectangle on the face
        
        for face in faces:
            print("Now, shape predictor is working...")
            face_landscapes =shape_predictor(rgb_image, face.rect)
            face_alligned = dlib.get_face_chip(rgb_image, face_landscapes) #uses the landscapes points to alligne the face to be easily processed
            face_embedding = embedding_model.compute_face_descriptor(face_alligned)
            print("Embedding generated:", face_embedding)
            embeddings.append(np.array(face_embedding))
    
    np.save(f"{database_path}/{name}_embeddings.npy", embeddings)
    


def recognize_face(persons, tolerance=0.4):
    
    def add_visitor_toDatabase (visiotr_name, visitor_embeddings):
        if visiotr_name:
            np.save(f"dataset/{visiotr_name}_embeddings", visitor_embeddings)  # save the visitor embedding to the dataset)
            print(f"added {visiotr_name} to database...")
    
    def create_decision_window (visitor_embeddings):
        decision_window = gui1.create_app()
        decision_window.title("decision_window")
        label = ctk.CTkLabel(decision_window, text="A stranger detected!", font=('Arial',20), text_color="white")
        label.pack(pady=10)
        
        def button1_command():
            #send_signal('0')
            print('door not opened')
            decision_window.destroy()
        def button2_command():
            #send_signal('1')
            print("door opened")
            decision_window.destroy()
        def buuton3_command():
            #send_signal('1')
            print("door opened")
            
            def save_visitorName ():
                visitor_name = name_entry.get()
                add_visitor_toDatabase(visitor_name, visitor_embeddings)
                visitorName_window.destroy()
                #decision_window.destroy()
            
            visitorName_window = gui1.create_app()
            visitorName_window.title("hello there^^")
            name_label = ctk.CTkLabel(visitorName_window, text="Enter the visitor's name", font=('Arial', 20))
            name_label.pack(pady=10)
            name_entry = ctk.CTkEntry(visitorName_window)
            name_entry.pack(pady=10)
            save_button = ctk.CTkButton(visitorName_window, text='save', command=save_visitorName, width=200, height=50, font=("Arial",16))
            save_button.pack(pady=10)
            
            visitorName_window.mainloop()
            
            
        button1 = ctk.CTkButton(decision_window, text="Don't open", command=button1_command, width=200, height=50, font=("Arial",16))
        button1.pack(pady=10)
        buuton2 = ctk.CTkButton(decision_window, text="open", command=button2_command, width=200, height=50, font=("Arial",16))
        buuton2.pack(pady=10)
        button3 = ctk.CTkButton(decision_window, text='open and add visior to database', command=buuton3_command, width=200, height=50, font=("Arial",16))
        button3.pack(pady=10)
        
        decision_window.mainloop()
    
    #app = gui.create_app()
    #camera_label = gui.create_camera_frame(app)  # Create the camera frame
    
    webcam = cv2.VideoCapture(0)

    visitor_embeddings = []
    
    embeddings_data = {}   #making a dictionary of embeddings with the keys the person and the key value their embeddings array vector
    for person_name in persons:
        embeddings_data[person_name] = np.load(f"dataset/{person_name}_embeddings.npy")  #giving the person key it;s embeddings array
    
    while 1 :
        
        #gui.update_camera(camera_label, webcam)  # Update the camera feed
        
        ret, imageframe = webcam.read()  #take capture of the visitor's face
        if not ret:
            break
         
        small_frame = cv2.resize(imageframe, (0, 0), fx=0.5, fy=0.5)  # Resize to half the original size to speed up processing
         
        rgb_image = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)   #bec cnn works with rgb
        faces = cnn_face_detector(rgb_image, 1)  #detect the viisitor's face
        print("visitor face detection complete..")
       
        for i, face in enumerate(faces):
            face_landscapes = shape_predictor(rgb_image, face.rect)
            face_alligned = dlib.get_face_chip(rgb_image, face_landscapes)
            visitor_embedding = embedding_model.compute_face_descriptor(face_alligned)  # geberate the visitor's embedding
            print("visitor embedding generated")
            visitor_embeddings.append(visitor_embedding)
            print("visitor embedding added to it's embeddings array")

            recognized = 0
            for person_name, embeddings in embeddings_data.items():  # loop through each person array of embeddings
                for stored_embedding in embeddings:   #match the visitor embidding with each embedding in embeddings array
                    distance = np.linalg.norm(stored_embedding - visitor_embedding)  # getting the euclodean distance
                    if distance < tolerance:  
                    
                        # get the original scale
                        x1, y1, x2, y2 = int(face.rect.left() * 2), int(face.rect.top() * 2), int(face.rect.right() * 2), int(face.rect.bottom() * 2)
                        
                        cv2.rectangle(imageframe, (x1,y1), (x2, y2), (0,255,0), 3)
                        cv2.putText(imageframe, f"{person_name}", (x1, y1-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255,0, 0), 2)
                        cv2.imshow('visitor', imageframe)
                        recognized = 1
                        #send_signal('1')
                        break  #break from inner loop
                if recognized:
                    break   #break from the outer loop
                
            if not recognized:
                x1, y1, x2, y2 = int(face.rect.left() * 2), int(face.rect.top() * 2), int(face.rect.right() * 2), int(face.rect.bottom() * 2)
                cv2.rectangle(imageframe, (x1,y1), (x2, y2), (0,0,255), 3)
                cv2.putText(imageframe, "trespasser", (x1, y1-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0,255 ), 2)
                cv2.imshow("visitor", imageframe)
                create_decision_window(visitor_embeddings)
                
       
                
        if cv2.waitKey(1) & 0xFF == ord('q'):  # q to quit taking captures
            webcam.release()
            cv2.destroyAllWindows()
            break
        
        
        

def remove_person(person_name):    #remove a person from the dataset
    if os.path.exists(f"dataset/{person_name}"):
        os.remove(f"dataset/{person_name}")
    
    if os.path.exists(f"dataset/{person_name}_embeddings.npy"):
        os.remove(f"dataset/{person_name}_embeddings.npy")      
    
def create_control_interface():
    control_interface = gui1.create_app()
    control_interface.title("control_interface")
    def delete_buuton_command():
        getName_window = gui1.create_app()
        getName_window.title("Hello there^^")
        
        def save_button_command():
            deleted_name = name_entry.get()
            remove_person(deleted_name)
            print(f"{deleted_name}, removed from database")
            getName_window.destroy()
        
        name_label = ctk.CTkLabel(getName_window, text="Enter the name you want to remove", font=('Arial', 20))
        name_label.pack(pady=10)
        name_entry = ctk.CTkEntry(getName_window)
        name_entry.pack(pady=10)
        save_button = ctk.CTkButton(getName_window, text='save', command=save_button_command, width=200, height=50, font=("Arial",16))
        save_button.pack(pady=10)
        getName_window.mainloop()
    
    label1 = ctk.CTkLabel(control_interface,text="To enter the password, press *", font=('Arial', 20) )
    label1.pack(pady=20)
    label2 = ctk.CTkLabel(control_interface,text="To change the password, press # ", font=('Arial', 20) )
    label2.pack(pady=20)
    delete_button = ctk.CTkButton(control_interface, text="remove person from database", command=delete_buuton_command, width=300, height=50, font=('Arial', 20))
    delete_button.pack(pady=40)
    control_interface.mainloop()

def notifications_window () :
    # Initialize the main application window
    app = ctk.CTk()
    app.title("notifications")
    app.geometry("800x600")

    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("dark-blue")

    # Create a parent frame to manage the layout
    main_frame = ctk.CTkFrame(master=app)
    main_frame.pack(fill="both", expand=True)

    # Frame with a "Continue" button (1/3 of the width)
    button_frame = ctk.CTkFrame(master=main_frame, width=200)
    button_frame.pack(side="left", fill="y", padx=20, pady=20)

    # Global variable to store user input
    user_input_data = "None"

    # Function to handle "Continue" button click
    def on_continue_click():
        while recieve_message():
            message = recieve_message()
            append_text(message)
        

    # Create the "Continue" button
    continue_button = ctk.CTkButton(master=button_frame, text="Continue", command=on_continue_click)
    continue_button.pack(pady=20)

    # Frame at the bottom with a large textbox (2/3 of the width)
    bottom_frame = ctk.CTkFrame(master=main_frame)
    bottom_frame.pack(side="right", fill="both", padx=20, pady=20, expand=True)

    # Create the textbox
    bottom_textbox = ctk.CTkTextbox(master=bottom_frame, wrap='word')
    bottom_textbox.pack(fill="both", expand=True, padx=10, pady=10)

    # Function to append text to the textbox
    def append_text(new_text):
        bottom_textbox.insert(ctk.END, new_text + "\n")
        bottom_textbox.see(ctk.END)  # Scroll to the end

    #  start the app
    append_text("Starting the application...")
    append_text("Welcome to the notifications window")
    app.mainloop()
    
    



#notifications_window()  


persons = ["Heba", "Manar"]  #list of owners' names in the dataset to compare with their embeddings
recognize_face(persons)


#create_control_interface()
    
