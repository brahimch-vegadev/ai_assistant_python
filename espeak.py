import json
import speech_recognition as sr
import espeakng
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

# Initialize eSpeakNG
def initialize_espeak():
    speaker = espeakng.Speaker()
    speaker.voice = "ar"
    return speaker

# Speak a message
def speak(speaker, message):
    speaker.say(message)

# Load data from JSON file
def load_data():
    with open("data.json") as json_file:
        data = json.load(json_file)
    return data

# Display logo on LCD
def display_logo():
    lcd.clear()
    lcd.message("Your Logo\nHere")

# Main function
def main():
    # Initialize eSpeakNG
    speaker = initialize_espeak()

    # Load data from JSON file
    data = load_data()

    # Initialize the speech recognizer for Arabic language
    recognizer = sr.Recognizer()

    # Set language to Arabic
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)

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
            query = recognizer.recognize_google(audio, language="ar-EG").lower()
            print("User:", query)

            # Check if the query matches any commands
            if query in data:
                response = data[query]["response"]
                display_message = data[query].get("display_message", "")
                if display_message:
                    lcd.clear()
                    lcd.message(display_message)
                    time.sleep(3)  # Display message for 3 seconds
                speak(speaker, response)
            else:
                speak(speaker, "آسف، لم أفهم ذلك.")

        except sr.UnknownValueError:
            print("آسف، لم أتمكن من فهم صوتك.")
            speak(speaker, "آسف، لم أتمكن من فهم صوتك.")
        except sr.RequestError as e:
            print("لم استطع الوصول إلى الخدمة؛ {0}".format(e))
            speak(speaker, "لم استطع الوصول إلى الخدمة. يرجى المحاولة مرة أخرى في وقت لاحق.")

if __name__ == "__main__":
    main()
