import tkinter as tk
from tkinter import scrolledtext, filedialog
from PIL import Image, ImageTk
import google.generativeai as genai
import os
import speech_recognition
import pyttsx3
import asyncio

class ChatbotInterface:
    def __init__(self, root):
        self.root = root
        self.root.title("Quang Anh GPT")
        self.root.geometry("800x600")
        self.selected_image = None
        self.selected_message= None
        self.photo = None
        self.create_widgets()

    def create_widgets(self):
        # Create a chat window
        self.chat_window = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, width=50, height=20)
        self.chat_window.pack(pady=10, padx=10, expand=True, fill=tk.BOTH)

        # Create input area
        self.input_area = tk.Text(self.root, wrap=tk.WORD, height=5)
        self.input_area.pack(pady=10, padx=10, expand=True, fill=tk.X)
        
        # Bind enter and shift+enter key presses
        self.input_area.bind("<Return>", self.send_inputs)
        self.input_area.bind("<Shift-Return>", self.insert_line_break)
        
        # Create buttons
        # Send button
        self.send_button = tk.Button(self.root, text="Send", command=self.send_inputs)
        self.send_button.pack(side=tk.RIGHT, pady=10, padx=10)
        
        # Image input button
        self.image_button = tk.Button(self.root, text="Upload Image", command=self.upload_image)
        self.image_button.pack(side=tk.RIGHT, pady=10, padx= 10)
        
        # Record button
        self.record_button = tk.Button(self.root, text="Record", command=self.start_recording)
        self.record_button.pack(side=tk.RIGHT, pady=10, padx=10)

    def send_inputs(self, event=None):
        os.environ['GOOGLE_API_KEY'] = "AIzaSyB1P1T9GlcJFRmtQLieCKL9v5eUXSil6bM" #input your API key
        genai.configure(api_key = os.environ['GOOGLE_API_KEY'])
        # Config & model pro
        generation_config_pro = {"temperature": 0.9, "top_p": 1, "max_output_tokens": 8192}
        model_pro = genai.GenerativeModel("gemini-pro", generation_config= generation_config_pro)
        # Config & model pro vision
        generation_config_pro_vision = {"temperature": 0.4, "top_p": 1, "top_k": 32, "max_output_tokens": 2048}
        model_pro_vision = genai.GenerativeModel("gemini-pro-vision", generation_config= generation_config_pro_vision)
        
        message = self.input_area.get("1.0", tk.END).strip()
        self.selected_message= message
        
        self.display_message(f"User: {message}")
        if self.selected_image is not None and self.selected_message is None:
            response = model_pro_vision.generate_content(self.photo)
        elif self.selected_image is not None and self.selected_message is not None:
            response = model_pro_vision.generate_content([message, self.photo])
        elif self.selected_image is None and self.selected_message is not None:
            response = model_pro.generate_content(message)
        
        self.display_message(f"Chatbot: {response.text}")
        # Clear the input area
        self.input_area.delete("1.0", tk.END)

    def insert_line_break(self, event=None):
        self.input_area.insert(tk.END, "\n")

    def display_message(self, message):
        self.chat_window.insert(tk.END, f"{message}\n")
        self.chat_window.yview(tk.END)  

    def start_recording(self):
        robot_ear = speech_recognition.Recognizer()
        robot_brain = ""
        robot_mouth = pyttsx3.init()
        with speech_recognition.Microphone() as mic:
            robot_ear.adjust_for_ambient_noise(mic)
            self.display_message("Chatbot: I'm listening...")
            audio = robot_ear.record(mic,duration=5)
        self.display_message("Processing...")
        try:
            you = robot_ear.recognize_google(audio)
        except:
            you = ""
        self.display_message(f"User: {you}")
        if you == "":
            robot_brain = "I can't hear you"
        else:
            os.environ['GOOGLE_API_KEY'] = "AIzaSyB1P1T9GlcJFRmtQLieCKL9v5eUXSil6bM" #input your API key
            genai.configure(api_key = os.environ['GOOGLE_API_KEY'])
            # Config & model pro
            generation_config_pro = {"temperature": 0.9, "top_p": 1, "max_output_tokens": 8192}
            model_pro = genai.GenerativeModel("gemini-pro", generation_config= generation_config_pro)
            # Config & model pro vision
            generation_config_pro_vision = {"temperature": 0.4, "top_p": 1, "top_k": 32, "max_output_tokens": 2048}
            model_pro_vision = genai.GenerativeModel("gemini-pro-vision", generation_config= generation_config_pro_vision)
            if self.selected_image is None:
                robot_brain = model_pro.generate_content(you)
            else:
                robot_brain = model_pro_vision.generate_content([you, self.photo])
            self.display_message(f"Chatbot: {robot_brain.text}")
            robot_mouth.say(robot_brain.text)
            robot_mouth.runAndWait()
            # Clear the input area
            self.input_area.delete("1.0", tk.END)
            
    def upload_image(self):
        file_path = filedialog.askopenfilename(title="Select an image file", filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
        self.selected_image = file_path
        if file_path:
            image = Image.open(file_path)
            self.photo = image
            self.display_image(image)

    def display_image(self, image):
        image = image.resize((200, 200))
        tk_image = ImageTk.PhotoImage(image)
        image_window = tk.Toplevel(self.root)
        image_label = tk.Label(image_window, image=tk_image)
        image_label.pack()
        image_window.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    chatbot_interface = ChatbotInterface(root)
    root.mainloop()
