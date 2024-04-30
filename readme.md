## Configuration

1. Copy `config.sample.ini` and rename it to `config.ini`.
2. Replace `your_api_key` and `your_api_secret` with your actual Gemini API credentials.


Adding API Keys for Chatbot
To make the chatbot work in the BB4 Django project, you need to add your own API key for the Gemini API. Follow these steps to add your API key:

Get Your Gemini API Key:
Sign up for an account on the Gemini API website.
Generate an API key in your account settings.
Create a Configuration File:
Navigate to the root directory of the project.
Create a file named config.ini if it doesn't already exist.
Add Your API Key:
Open the config.ini file in a text editor.
Add the following lines to the file:
ini
Copy code
[GENAI]
API_KEY = YOUR_GEMINI_API_KEY
CREDENTIALS_FILE_PATH = PATH_TO_GEN_LANG_CLIENT_JSON_FILE
Replace YOUR_GEMINI_API_KEY with your actual Gemini API key and PATH_TO_GEN_LANG_CLIENT_JSON_FILE with the path to your gen-lang-client JSON file.
Save the Configuration File:
Save the changes to the config.ini file.
Start the Server:
Run the Django server.
