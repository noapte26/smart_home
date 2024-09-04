import cv2
import face_recognition

print (face_recognition.__version__)
webcam = cv2.VideoCapture(0) #0 adress of the camera

while(1):

    _, imageFrame = webcam.read()

    cv2.imshow("camera",imageFrame)

    if cv2.waitKey(10) & 0xFF == ord('q'):
        webcam.release()
        cv2.destroyAllWindows()
        break
    cv2.imwrite("image.png", imageFrame)