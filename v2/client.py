import tkinter as tk
import requests
from tkinter import messagebox, colorchooser
import os

message_server = 'http://212.132.99.175:5000'

# Determine the directory where the Python script is located
script_dir = os.path.dirname(os.path.abspath(__file__))
config_folder = os.path.join(script_dir, "config")

# Check if the config folder exists; if not, create it
if not os.path.exists(config_folder):
    os.makedirs(config_folder)

# Check if the config.txt file exists; if not, ask for a username and save it
config_file = os.path.join(config_folder, "config.txt")
if not os.path.isfile(config_file):
    username_window = tk.Tk()
    username_window.title('Username Selection')

    def save_username():
        global username
        username = username_entry.get()
        if username:
            with open(config_file, "w") as file:
                file.write(username)
            username_window.destroy()
        else:
            messagebox.showerror('Error', 'Username cannot be empty.')

    username_label = tk.Label(username_window, text="Enter your username:")
    username_label.pack(pady=10)

    username_entry = tk.Entry(username_window, width=40)
    username_entry.pack(pady=10)

    save_username_button = tk.Button(username_window, text='Save Username', command=save_username)
    save_username_button.pack()

    username_window.mainloop()
else:
    with open(config_file, "r") as file:
        username = file.read()

# Continue with the main application
root = tk.Tk()
root.title("Message Application")

frame = tk.Frame()

# Initialize selected color and message ID
selected_color = "#000000"  # Default color (black)
last_message_id = 0  # Track the last message ID

# Function to send a message
def save_message(event=None):
    global last_message_id
    message = entry.get()
    if message:
        last_message_id += 1  # Increment the message ID
        try:
            data = {
                'username': username,
                'message': message,
                'color': selected_color,  # Include the selected color
                'id': last_message_id  # Include the message ID
            }
            response = requests.post(message_server + '/store_message', json=data)
            if response.status_code == 200:
                entry.delete(0, 'end')
                load_messages()
            else:
                messagebox.showerror('Error', 'Failed to save message.')
        except Exception as e:
            messagebox.showerror('Error', f'Error saving message: {str(e)}')
    else:
        messagebox.showerror('Error', 'Message cannot be empty.')

# Function to load and display messages
def load_messages():
    global last_message_id
    try:
        response = requests.get(message_server + '/get_messages')
        if response.status_code == 200:
            messages = response.json()
            messages_text.config(state=tk.NORMAL)
            messages_text.delete('1.0', tk.END)
            for message in messages:
                # Insert the message and apply the color tag
                messages_text.insert(tk.END, f"{message['username']}: {message['message']}\n", message['id'])
                # Configure the tag for the color if it doesn't exist
                if message['id'] not in messages_text.tag_names():
                    messages_text.tag_config(message['id'], foreground=message['color'])
                # Update the last message ID
                last_message_id = max(last_message_id, message['id'])
            messages_text.config(state=tk.DISABLED)
            messages_text.see(tk.END)
        else:
            messagebox.showerror('Error', 'Failed to load messages.')
    except Exception as e:
        messagebox.showerror('Error', f'Error loading messages: {str(e)}')

# Function to choose a color
def choose_color():
    global selected_color
    color = colorchooser.askcolor()[1]  # Get the hex color code
    if color:
        selected_color = color
        draw_circle()  # Update the circle color

# Function to draw a filled circle
def draw_circle():
    color_circle.delete("all")  # Clear previous drawings
    color_circle.create_oval(5, 5, 30, 30, fill=selected_color, outline=selected_color)  # Draw a circle

# Create an entry widget for typing messages
entry = tk.Entry(frame, width=40, font=("Arial", 16))
entry.pack(pady=10)

# Create a circular color selector
color_circle = tk.Canvas(frame, width=35, height=35, bg='white', highlightthickness=0)
color_circle.pack(pady=10)
color_circle.bind("<Button-1>", lambda e: choose_color())  # Change color on click
draw_circle()  # Initial draw

# Create a button to save the message
save_button = tk.Button(frame, text='Send', command=save_message)
save_button.pack()

# Create a text widget to display messages
messages_text = tk.Text(frame, width=40, height=10, state=tk.DISABLED)
messages_text.pack()

# Load and display messages
load_messages()

# Function to refresh messages every 5 seconds
def refresh_messages():
    load_messages()
    root.after(5000, refresh_messages)  # Schedule the next refresh

# Start refreshing messages
refresh_messages()

frame.pack()

# Start the tkinter main loop
root.mainloop()
