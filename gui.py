import customtkinter as ctk 
import cv2
from customtkinter import CTkImage
from PIL import Image, ImageTk

# Global variable for correct password
correct_password = "12345678AS"

# Function to create the main application window
def create_app():
    app = ctk.CTk()
    app.title("Password and Camera GUI")
    app.geometry("800x600")
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("dark-blue")
    return app

# Function to create the password frame and related components
def create_password_frame(app):
    password_frame = ctk.CTkFrame(master=app)
    password_frame.pack(side="left", padx=20, pady=20, fill="y")
    
    password_label = ctk.CTkLabel(master=password_frame, text="Enter Password:", font=("Arial", 16))
    password_label.pack(pady=10)
    
    password_textbox = ctk.CTkTextbox(master=password_frame, width=200, height=30)
    password_textbox.pack(pady=10)

    check_button = ctk.CTkButton(master=password_frame, text="Submit", command=lambda: check_password(password_textbox))
    check_button.pack(pady=10)

    change_password_button = ctk.CTkButton(master=password_frame, text="Change Password", command=lambda: change_password_window(app))
    change_password_button.pack(pady=10)

# Function to check the password entered by the user
def check_password(password_textbox):
    global correct_password
    user_input = password_textbox.get("1.0", "end-1c").strip()
    if user_input == correct_password:
        print("Correct")
    else:
        print("False")

# Function to open the change password window
def change_password_window(app):
    change_window = ctk.CTkToplevel(app)
    change_window.title("Change Password")
    change_window.geometry("300x200")

    new_password_label = ctk.CTkLabel(master=change_window, text="Enter New Password:")
    new_password_label.pack(pady=10)

    new_password_textbox = ctk.CTkTextbox(master=change_window, width=200, height=30)
    new_password_textbox.pack(pady=10)

    save_button = ctk.CTkButton(master=change_window, text="Save Password", command=lambda: set_new_password(new_password_textbox, change_window))
    save_button.pack(pady=10)

# Function to set a new password
def set_new_password(new_password_textbox, change_window):
    global correct_password
    correct_password = new_password_textbox.get("1.0", "end-1c").strip()
    print("Password changed to:", correct_password)
    change_window.destroy()

# Function to create the camera frame and start the camera feed
def create_camera_frame(app):
    camera_frame = ctk.CTkFrame(master=app)
    camera_frame.pack(side="right", padx=20, pady=20, fill="both", expand=True)

    camera_label = ctk.CTkLabel(master=camera_frame)
    camera_label.pack()

    return camera_label

# Function to update the camera feed
def update_camera(camera_label, webcam):
    ret, frame = webcam.read()
    if ret:
        # Convert the image to RGB format
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Convert the OpenCV image to a PIL Image
        pil_image = Image.fromarray(rgb_frame)

        # Create CTkImage from PIL image and specify desired size
        ctk_image = CTkImage(pil_image, size=(camera_label.winfo_width(), camera_label.winfo_height()))

        # Update the camera label with the CTkImage
        camera_label.configure(image=ctk_image)
        camera_label.image = ctk_image  # Keep a reference to the image
        return frame


# Main function to run the app
def run_app():
    app = create_app()

    # Create password and camera frames
    create_password_frame(app)
    camera_label = create_camera_frame(app)

    # Start camera feed
    cap = cv2.VideoCapture(0)
    update_camera(camera_label, cap)

    # Run the application
    app.mainloop()

    # Release camera after closing the app
    cap.release()

# Entry point for running the application
#if name == "main":
 #   run_app()