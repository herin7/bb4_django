import google.generativeai as genai
import configparser

config = configparser.ConfigParser()
config.read("./config.ini")
api_key = config["GENAI"]["API_KEY"]
genai.configure(api_key=api_key)

prompt = input("What Kind of Dish You want to make? : ")

model = genai.GenerativeModel("gemini-pro")

response = model.generate_content(f"How Do you make {prompt}")

print(response.text)