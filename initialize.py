import cv2
import face_recognition
import dlib
import numpy as np
import os

''' deep learnong algorithm based face detector (convolutional neural network)'''
cnn_face_detector = dlib.cnn_face_detection_model_v1("mmod_human_face_detector.dat")

''' it's a deep learning model that uses neural network to generate embiddings
which is a 128-dimentional numerical vector having all the important features of the face
and is better used by the face recognition model to compare images instead of the normal image'''
embedding_model = dlib.face_recognition_model_v1("dlib_face_recognition_resnet_model_v1.dat")

''' this predictor model finds 68 crusial landscapes points on the image, like the eyes, nose, ...'''
shape_predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")


def extract_face (image, x1, y1, x2, y2):  #extract the detected face from the image
    ''' making sure we are represinting the right coordinates'''
    minX = min(x1, x2)
    maxX = max(x1, x2)
    minY = min(y1, y2)
    maxY = max(y1, y2)
    face = image[minX : maxX, minY : maxY]
    face = cv2.resize(face, (224,224))
    return face

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

def face_detection_for_database(name, database_path = 'dataset'):
    
    if not os.path.exists(database_path):
        os.makedirs(database_path)
    if not os.path.exists(f"{database_path}/{name}"):
        os.makedirs(f"{database_path}/{name}")
    
    webcam = cv2.VideoCapture(0) #0 adress of the camera
    i = 0
    
    while(1):
        _, imageFrame = webcam.read()
        image = cv2.resize(imageFrame, (0,0), fx=0.5, fy=0.5)  #resizing to speed up the processing
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB) #dlib works with rgb
    
        faces = cnn_face_detector(rgb_image,1)  #upsamble the image once in order ro detect small faces if there's any
        
        for face in faces:
            x1 = face.rect.left()
            y1 = face.rect.top()
            x2 = face.rect.right()
            y2 = face.rect.bottom()
            extracted_face = extract_face(imageFrame, x1, y1, x2, y2)
            face_path = f"{database_path}/{name}/{name}_{i}.png"
            cv2.imwrite(face_path, extracted_face)
        i = i+1
        
        cv2.imshow("me", imageFrame)
        
        if cv2.waitKey(10) & 0XFF == ord('q'):
           webcam.release()
           cv2.destroyAllWindows()
           break
  
  
        
def extract_embeddings(name, database_path = 'dataset'):
    
    embeddings = []   #the array of embeddings
    
    faces_imgs = os.listdir(f"{database_path}/{name}")  #get all the stored faces in that folder
    
    for img in faces_imgs:
        img_path = f"{database_path}/{name}/{img}"
        image = cv2.imread(img_path)
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        faces = cnn_face_detector(img)   # to get the rectangle on the face
        
        for face in faces:
            face_landscapes =shape_predictor(rgb_image, face.rect)
            face_alligned = dlib.get_face_chip(rgb_image, face_landscapes) #allignes the face to be easily processed
            face_embedding = embedding_model.compute_face_descriptor(face_alligned)
            embeddings.append(np.array(face_embedding))
    
    np.save(f"{database_path}/{name}_embeddings.npy", embeddings)
   



'''def face_detection(image):
    image = cv2.resize(image, (0,0), fx=0.5, fy=0.5)  #resizing to speed up the processing
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB) #dlib works with rgb
    
    faces = cnn_face_detector(rgb_image,1)  #upsamble the image once in order ro detect small faces if there's any
    for face in faces :
        x, y, w, h = convert_and_trim(image, face.rect)
        cv2.rectangle(image, (x, y), (x+w, y+h), (255,0,255), 2)
        cv2.imshow("step1", image)
        x1, y1, x2, y2 = (face.rect.left(), face.rect.top(), face.rect.right(), face.rect.bottom()) 
        face_region = dlib.rectangle(x1, y1, x2, y2)  #extracting the face region'''
    

    
    

#print (face_recognition.__version__)

    
    