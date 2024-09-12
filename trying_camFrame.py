import cv2
import numpy as np
import dlib
import customtkinter as ctk
from threading import Thread
from PIL import Image, ImageTk

class FaceRecognitionApp:
    def _init_(self, root):
        self.root = root
        self.root.title("Face Recognition System")

        # Create a frame for the camera feed
        self.camera_frame = ctk.CTkFrame(self.root, width=640, height=480)
        self.camera_frame.pack(pady=20, padx=20)

        # Create a label to display the camera feed
        self.camera_label = ctk.CTkLabel(self.camera_frame)
        self.camera_label.pack()

        # Create buttons for starting and stopping the recognition
        self.start_button = ctk.CTkButton(self.root, text="Start Recognition", command=self.start_recognition, width=200, height=50, font=("Arial", 16))
        self.start_button.pack(pady=10)

        self.stop_button = ctk.CTkButton(self.root, text="Stop Recognition", command=self.stop_recognition, width=200, height=50, font=("Arial", 16))
        self.stop_button.pack(pady=10)

        self.cap = None
        self.recognition_thread = None
        self.running = False

        # Load models
        self.cnn_face_detector = dlib.cnn_face_detection_model_v1('mmod_human_face_detector.dat')
        self.shape_predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')
        self.embedding_model = dlib.face_recognition_model_v1('dlib_face_recognition_resnet_model_v1.dat')
        
        # Example persons and their embeddings
        self.persons = ['person1', 'person2']
        self.embeddings_data = {}
        for person_name in self.persons:
            self.embeddings_data[person_name] = np.load(f"dataset/{person_name}_embeddings.npy")

    def start_recognition(self):
        if not self.running:
            self.running = True
            self.cap = cv2.VideoCapture(0)
            self.recognition_thread = Thread(target=self.recognize_face)
            self.recognition_thread.start()
            self.update_camera()

    def stop_recognition(self):
        if self.running:
            self.running = False
            if self.cap:
                self.cap.release()
            if self.recognition_thread:
                self.recognition_thread.join()
            cv2.destroyAllWindows()

    def update_camera(self):
        if self.cap and self.running:
            ret, frame = self.cap.read()
            if ret:
                # Convert to RGB
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                # Convert to ImageTk format
                image = Image.fromarray(rgb_frame)
                image_tk = ImageTk.PhotoImage(image=image)
                self.camera_label.configure(image=image_tk)
                self.camera_label.image = image_tk

            self.root.after(30, self.update_camera)

    def recognize_face(self):
        tolerance = 0.4
        visitor_embeddings = []

        while self.running:
            ret, image_frame = self.cap.read()
            if not ret:
                break
            
            small_frame = cv2.resize(image_frame, (0, 0), fx=0.5, fy=0.5)
            rgb_image = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
            faces = self.cnn_face_detector(rgb_image, 1)
            
            for face in faces:
                face_landmarks = self.shape_predictor(rgb_image, face.rect)
                face_aligned = dlib.get_face_chip(rgb_image, face_landmarks)
                visitor_embedding = self.embedding_model.compute_face_descriptor(face_aligned)
                visitor_embeddings.append(visitor_embedding)

                recognized = False
                for person_name, embeddings in self.embeddings_data.items():
                    for stored_embedding in embeddings:
                        distance = np.linalg.norm(np.array(stored_embedding) - np.array(visitor_embedding))
                        if distance < tolerance:
                            x1, y1, x2, y2 = [int(coord * 2) for coord in (face.rect.left(), face.rect.top(), face.rect.right(), face.rect.bottom())]
                            cv2.rectangle(image_frame, (x1, y1), (x2, y2), (0, 255, 0), 3)
                            cv2.putText(image_frame, person_name, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2)
                            cv2.imshow('Visitor', image_frame)
                            recognized = True
                            break
                    if recognized:
                        break

                if not recognized:
                    x1, y1, x2, y2 = [int(coord * 2) for coord in (face.rect.left(), face.rect.top(), face.rect.right(), face.rect.bottom())]
                    cv2.rectangle(image_frame, (x1, y1), (x2, y2), (0, 0, 255), 3)
                    cv2.putText(image_frame, "Trespasser", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 255), 2)
                    cv2.imshow("Visitor", image_frame)
                    self.create_decision_window(visitor_embeddings)
        
    def create_decision_window(self, visitor_embeddings):
        decision_window = ctk.CTk()
        decision_window.title("Decision Window")

        label = ctk.CTkLabel(decision_window, text="A stranger detected!", font=('Arial', 20), text_color="white")
        label.pack(pady=10)

        def button1_command():
            print('Door not opened')
            decision_window.destroy()

        def button2_command():
            print("Door opened")
            decision_window.destroy()

        def button3_command():
            def save_visitor_name():
                visitor_name = name_entry.get()
                self.add_visitor_to_database(visitor_name, visitor_embeddings)
                visitor_name_window.destroy()

            visitor_name_window = ctk.CTk()
            visitor_name_window.title("Enter Visitor's Name")

            name_label = ctk.CTkLabel(visitor_name_window, text="Enter the visitor's name", font=('Arial', 20))
            name_label.pack(pady=10)
            name_entry = ctk.CTkEntry(visitor_name_window)
            name_entry.pack(pady=10)
            save_button = ctk.CTkButton(visitor_name_window, text='Save', command=save_visitor_name, width=200, height=50, font=("Arial", 16))
            save_button.pack(pady=10)

            visitor_name_window.mainloop()

        button1 = ctk.CTkButton(decision_window, text="Don't Open", command=button1_command, width=200, height=50, font=("Arial", 16))
        button1.pack(pady=10)
        button2 = ctk.CTkButton(decision_window, text="Open", command=button2_command, width=200, height=50, font=("Arial", 16))
        button2.pack(pady=10)
        button3 = ctk.CTkButton(decision_window, text='Open and Add Visitor to Database', command=button3_command, width=200, height=50, font=("Arial", 16))
        button3.pack(pady=10)

        decision_window.mainloop()

    def add_visitor_to_database(self, visitor_name, visitor_embeddings):
        if visitor_name:
            np.save(f"dataset/{visitor_name}_embeddings.npy", visitor_embeddings)
            print(f"Added {visitor_name} to database...")

if _name_ == "_main_":
    root = ctk.CTk()
    app = FaceRecognitionApp(root)
    root.protocol("WM_DELETE_WINDOW", app.stop_recognition)  # Ensure resources are cleaned up
    root.mainloop()