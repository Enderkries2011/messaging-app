import tkinter as tk
import requests
from tkinter import messagebox
import os

message_server = 'put_your_message_server_url_here'

# Determine the directory where the Python script is located
script_dir = os.path.dirname(os.path.abspath(__file__))
config_folder = os.path.join(script_dir, "config")

# Check if the config folder exists; if not, create it
if not os.path.exists(config_folder):
    os.makedirs(config_folder)

# Check if the config.txt file exists; if not, ask for a username and save it
config_file = os.path.join(config_folder, "config.txt")
if not os.path.isfile(config_file):
    # Initialize the tkinter window for username input
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
root.title("Ender's Messaging App")

frame = tk.Frame()

# Function to send a message
def save_message(event=None):
    message = entry.get()
    if message:
        try:
            data = {
                'username': username,
                'message': message
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

# Bind the Enter key to the save_message function
root.bind('<Return>', save_message)

# Function to load and display messages
def load_messages():
    try:
        response = requests.get(message_server + '/get_messages')
        if response.status_code == 200:
            messages = response.json()
            messages_text.config(state=tk.NORMAL)
            messages_text.delete('1.0', tk.END)
            for message in messages:
                messages_text.insert(tk.END, f"{message['username']}: {message['message']}\n")
            messages_text.config(state=tk.DISABLED)
            # Scroll to the end of the text widget
            messages_text.see(tk.END)
        else:
            messagebox.showerror('Error', 'Failed to load messages.')
    except Exception as e:
        messagebox.showerror('Error', f'Error loading messages: {str(e)}')

# Create an entry widget for typing messages
entry = tk.Entry(frame, width=40, font=("Arial", 16))
entry.pack(pady=10)

# Create a button to save the message
save_button = tk.Button(frame, text='Send', command=save_message)
save_button.pack()

# Create a text widget to display messages
messages_text = tk.Text(frame, width=40, height=10, state=tk.DISABLED)
messages_text.pack()

# Load and display messages
load_messages()

frame.pack()

# Start the tkinter main loop
root.mainloop()
