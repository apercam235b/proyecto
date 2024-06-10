import pathlib
import textwrap
import speech_recognition as sr
import pyttsx3
import google.generativeai as genai

from IPython.display import display, Markdown

# Inicializar el motor de síntesis de voz
engine = pyttsx3.init()
engine.setProperty('rate', 150)  # Velocidad de la voz
engine.setProperty('volume', 1.0)  # Volumen de la voz

# Configurar la API de Google Generative AI
genai.configure(api_key='AIzaSyAKPxKVmVhuyKbdXVhdEIf43gTbuDhNxAk')
model = genai.GenerativeModel('gemini-1.5-flash')

def to_markdown(text):
    """Convierte el texto a formato Markdown y lo lee en voz alta."""
    text = text.replace('*', '')
    display(Markdown(text))
    engine.say(text)
    engine.runAndWait()

def recognize_speech():
    """Reconoce el habla del micrófono y devuelve el texto."""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Say Something...")
        audio = r.listen(source)
        try:
            pregunta = r.recognize_google(audio, language='en-EN')
            return pregunta
        except sr.UnknownValueError:
            print("I am sorry! I can not understand!")
            return None
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")
            return None

def generate_response(question):
    """Genera una respuesta utilizando el modelo de Generative AI de Google."""
    try:
        response = model.generate_content(question)
        return response.text
    except Exception as e:
        print(f"Error generating response: {e}")
        return None

def main():
    question = recognize_speech()
    if question:
        response = generate_response(question)
        if response:
            to_markdown(response)
        else:
            print("No response generated.")
    else:
        print("No question recognized.")

if __name__ == "__main__":
    main()
