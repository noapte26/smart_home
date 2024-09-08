import cv2
import face_recognition
import dlib
import numpy as np
import os
import serial 

''' deep learnong algorithm based face detector (convolutional neural network)'''
cnn_face_detector = dlib.cnn_face_detection_model_v1("mmod_human_face_detector.dat")

''' it's a deep learning model that uses neural network to generate embiddings
which is a 128-dimentional numerical vector having all the important features of the face
and is better used by the face recognition model to compare images instead of the normal image'''
embedding_model = dlib.face_recognition_model_v1("dlib_face_recognition_resnet_model_v1.dat")

''' this predictor model finds 68 crusial landscapes points on the image, like the eyes, nose, ...'''
shape_predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")


ser = serial.Serial()  # get serial instance
ser.baudrate = 9600
ser.port = 'COM1'
print(ser.name)


def extract_face (image, x1, y1, x2, y2):  #extract the detected face from the image
    ''' making sure we are represinting the right coordinates'''
    minX = min(x1, x2)
    maxX = max(x1, x2)
    minY = min(y1, y2)
    maxY = max(y1, y2)
    face = image[minY : maxY, minX : maxX]   #slice this hight and width
    #resized_face = cv2.resize(face, (224, 224))
    BGR_face = cv2.cvtColor(face, cv2.COLOR_RGB2BGR)  #converting it again to be saved as cv2 works with BGR
    return BGR_face

def convert_and_trim(image, rect):  #converts dlib rectangle coordinates to the bounding box coordinates
    startX = rect.left()
    startY = rect.top()
    endX = rect.right()
    endY = rect.bottom()
    ''' making sure the bounding box coordinates fall within the image frame'''
    startX = max(0, startX)
    startY = max(0, startY)
    endX = min(endX, image.shape[1])
    endY = min(endY, image.shape[0])
    '''getting w and h'''
    w = endX - startX
    h = endY - startY
    return(startX, startY, w, h)


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
            y1 = face.recr.top()
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
    webcam = cv2.VideoCapture(0)
    
    visitor_embeddings = []
    
    embeddings_data = {}   #making a dictionary of embeddings with the keys the person and the key value their embeddings array vector
    for person_name in persons:
        embeddings_data[person_name] = np.load(f"dataset/{person_name}_embeddings.npy")  #giving the person key it;s embeddings array
    
    while 1:
        ret, imageframe = webcam.read()  #take capture of the visitor's face
        if not ret:
            break

        rgb_image = cv2.cvtColor(imageframe, cv2.COLOR_BGR2RGB)   #bec cnn works with rgb
        faces = cnn_face_detector(rgb_image, 1)  #detect the viisitor's face
        print("visitor face detection complete..")
       
        for i, face in enumerate(faces):
            face_landscapes = shape_predictor(rgb_image, face.rect)
            face_alligned = dlib.get_face_chip(rgb_image, face_landscapes)
            visitor_embedding = embedding_model.compute_face_descriptor(face_alligned)  # geberate the visitor's embedding
            print("visitor embedding generated")
            visitor_embeddings.append(visitor_embedding)

            recognized = 0
            for person_name, embeddings in embeddings_data.items():  # loop through each person array of embeddings
                for stored_embedding in embeddings:   #match the visitor embidding with each embedding in embeddings array
                    distance = np.linalg.norm(stored_embedding - visitor_embedding)  # getting the euclodean distance
                    if distance < tolerance:  
                        cv2.rectangle(imageframe, (face.rect.left(),face.rect.top()), (face.rect.right(), face.rect.bottom()), (0,255,0), 3)
                        cv2.putText(imageframe, f"{person_name}", (face.rect.left(), face.rect.top()-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255,0, 0), 2)
                        recognized = 1
                        # ser.write(b'1')
                        break  #break from inner loop
                if recognized:
                    break   #break from the outer loop
                
            if not recognized:
                cv2.rectangle(imageframe, (face.rect.left(),face.rect.top()), (face.rect.right(), face.rect.bottom()), (0,0,255), 3)
                cv2.putText(imageframe, "trespasser", (face.rect.left(), face.rect.top()-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0,255 ), 2)
                
                 #if case==1 :
                    #ser.write(b'0')
                #elif case ==2:
                    #ser.write(b'1')
                #elif case == 3:
                    # ser.write(b'1')
                    # np.save(f"dataset/{visitorName}_embeddings.npy", visitor_embeddings)  # save the visitor embedding to the dataset
                

        cv2.imshow('visitor', imageframe)

        if cv2.waitKey(1) & 0xFF == ord('q'):  # q to quit taking captures
            webcam.release()
            cv2.destroyAllWindows()
            break

def remove_person(person_name):    #remove a person from the dataset
    os.remove(f"dataset/{person_name}")
    os.remove(f"dataset/{person_name}_embeddings.npy")      
    
   
#persons = ["Heba"]  
#recognize_face(persons)
#print (face_recognition.__version__)

    
    