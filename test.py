import json
import speech_recognition as sr
import pyttsx3
import time
import Adafruit_CharLCD as LCD

# Initialize LCD
lcd_rs = 25
lcd_en = 24
lcd_d4 = 23
lcd_d5 = 17
lcd_d6 = 18
lcd_d7 = 22
lcd_backlight = 4
lcd_columns = 16
lcd_rows = 2
lcd = LCD.Adafruit_CharLCD(
    lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7, lcd_columns, lcd_rows, lcd_backlight
)

# Initialize text-to-speech engine
engine = pyttsx3.init()
voices = engine.getProperty('voices')
arabic_female_voice_id = None
for voice in voices:
    if "female" in voice.name.lower() and "arabic" in voice.languages:
        arabic_female_voice_id = voice.id
        break
if arabic_female_voice_id:
    engine.setProperty('voice', arabic_female_voice_id)
    engine.setProperty('rate', 150)  # Adjust the rate as needed
    engine.setProperty('textnorm', 'arabic')  # Set text normalization for Arabic
else:
    print("No suitable Arabic female voice found.")
# Load data from JSON file
def load_data():
    with open("data.json") as json_file:
        data = json.load(json_file)
    return data

# Save data to JSON file
def save_data(data):
    with open("data.json", "w") as json_file:
        json.dump(data, json_file, indent=4)

# Display logo on LCD
def display_logo():
    lcd.clear()
    lcd.message("Your Logo\nHere")

# Speak a message
def speak(message):
    engine.say(message)
    engine.runAndWait()

# Main function
def main():
    # Load data from JSON file
    data = load_data()

    # Initialize the speech recognizer
    recognizer = sr.Recognizer()

    # Display logo on LCD
    display_logo()

    # Main loop
    while True:
        # Listen for voice input
        with sr.Microphone() as source:
            print("Listening...")
            audio = recognizer.listen(source)

        try:
            # Recognize speech
            query = recognizer.recognize_google(audio).lower()
            print("User:", query)

            # Check if the query matches any commands
            if query in data:
                response = data[query]["response"]
                display_message = data[query].get("display_message", "")
                if display_message:
                    lcd.clear()
                    lcd.message(display_message)
                    time.sleep(3)  # Display message for 3 seconds
                speak(response)
            else:
                speak("Sorry, I didn't understand that.")

        except sr.UnknownValueError:
            print("Sorry, I could not understand your voice.")
            speak("Sorry, I could not understand your voice.")
        except sr.RequestError as e:
            print("Could not request results; {0}".format(e))
            speak("Could not request results. Please try again later.")

if __name__ == "__main__":
    main()
