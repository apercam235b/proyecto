import pathlib
import textwrap

import google.generativeai as genai

from IPython.display import display
from IPython.display import Markdown

def to_markdown(text):
    text = text.replace('*','')
    print(text)


genai.configure(api_key='TU API KEY')

model = genai.GenerativeModel('gemini-1.5-flash')


response = model.generate_content('what is the meaning of life') #ejemplo de pregunta que se le lanza

to_markdown(response.text)