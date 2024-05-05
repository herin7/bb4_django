import PIL.Image
import google.generativeai as genai
import configparser

config = configparser.ConfigParser()
config.read('./config.ini')
api_key = config['GENAI']['API_KEY']
genai.configure(api_key=api_key)

img = PIL.Image.open('./bb4main/image.jpg')
img

model = genai.GenerativeModel('gemini-pro-vision')

response = model.generate_content(["Derive The Text", img], stream=True)
response.resolve()

print(response.text)