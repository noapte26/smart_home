import cv2
import customtkinter as ctk


ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

app = ctk.CTk()
app.geometry("400x240")
app.title("Hello there, Heba!")

def button_function():
    print("I Love You, Heba")

button  = ctk.CTkButton(master= app, fg_color=("red", "dark"),  text="press me ^^", command=button_function)
button.pack(pady = 20)

app.mainloop()
