import sys
import tkinter as tk 
import threading
import speech_recognition  
import pyttsx3 as tts

from neuralintents import GenericAssistant



class Assistant:
    def  __init__(self):
         self.recognizer =  speech_recognition.Recognizer()
         self.speaker = tts.init("nsss")
         self.speaker.setProperty("rate", 150)
         self.assistant = GenericAssistant("intents.json", intent_methods={"file": self.create_file})
         self.assistant.train_model()
         self.root = tk.Tk()
         self.lable = tk.Label(text="Abdulah Rasol Loyar UAE",font=("Arial", 120, "bold"))
         self.lable.pack()
         threading.Thread(target=self.run_assistant).start()
         self.root.mainloop ()

    def create_file(self):     
         with open("somefile.txt", "w") as f:
              f.write("Abdula Rasol Loyar")
    def run_assistant(self):
         while True:
                try:
                   with speech_recognition.Microphone as mic:
                        self.recognizer.adjust_for_ambient_noise( mic, duration=5.0)
                        audio = self.recognizer.listen(mic)
                        text = self.recognizer.recognize_google(audio)
                        text = text.lower(text)
                        if "hey jack" in text : 
                             self.lable.config(fg="red")
                             audio = self.recognizer.listen(mic)
                             text = self.recognizer.recognize_google(audio)
                             text = text.lower()
                             if text == "stop": 
                                  self.speaker.say("Bye")
                                  self.speaker.runAndWait()
                                  self.speaker.stop()
                                  self.root.destroy()
                                  sys.exit()
                             else:
                                    if text is not None:
                                       response = self.assistant.request(text)
                                       if response is not None:
                                            self.speaker.say(response)
                                            self.speaker.runAndWait()
                                    self.lable.config(fg="black")  

                except : 
                     self.lable.config(fg="black")
                     continue                           
                                   

Assistant()
                   