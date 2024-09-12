import customtkinter as ctk

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
    append_text()
    

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

# Function to start the app
def start_app():
    app.mainloop()