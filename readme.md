# Configuration

1. Copy `config.sample.ini` and rename it to `config.ini`.
2. Replace `your_api_key` and `your_api_secret` with your actual Gemini API credentials.

## Adding API Keys for Chatbot

To make the chatbot work in the BB4 Django project, you need to add your own API key for the Gemini API. Follow these steps to add your API key:

### Get Your Gemini API Key:
1. Sign up for an account on the Gemini API website.
2. Generate an API key in your account settings.

### Create a Configuration File:
1. Navigate to the root directory of the project.
2. Create a file named `config.ini` if it doesn't already exist.

### Add Your API Key:
1. Open the `config.ini` file in a text editor.
2. Add the following lines to the file:

    ```ini
    [GENAI]
    API_KEY = YOUR_GEMINI_API_KEY
    CREDENTIALS_FILE_PATH = PATH_TO_GEN_LANG_CLIENT_JSON_FILE
    ```

    Replace `YOUR_GEMINI_API_KEY` with your actual Gemini API key and `PATH_TO_GEN_LANG_CLIENT_JSON_FILE` with the path to your `gen-lang-client JSON` file.

### Save the Configuration File:
1. Save the changes to the `config.ini` file.

### Start the Server:
1. Run the Django server.


## Guide for Gemini
1. run this code first in terminal to install GEMINI in your project:

    ```python
    pip install google-generativeai
    ```
2. Add Your own Gemini API Key in config.ini file under Section [GENAI]
3. Add following lines.

    ```ini
    [GENAI]
    API_KEY = YOUR_GEMINI_API_KEY
    CREDENTIALS_FILE_PATH = PATH_TO_GEN_LANG_CLIENT_JSON_FILE
    ```

#### For Text to Text Prompt

Gemini-pro version is used to generate prompt from Text,

1. Import Gemini-pro model with this:
    ```python
    model = genai.GenerativeModel("gemini-pro")
    ```

currently prompt is asked from user from console via this method

```python
prompt = input("What Kind of Dish You want to make? : ")
```

can be linked with frontend with dJango for Dynamic Propmts.

and the content is generated through prompt is by this method

```python
response = model.generate_content(f"How Do you make {prompt}")
```

Then the response can be used anywhere.

### For Image to Text Prompt

Gemini-pro-vision is used for the task for multimodal stream.

1. Import gemini-pro-vision:

    ```python
    model = genai.GenerativeModel('gemini-pro-vision')
    ```

2. Import your image: 

    ```python
    import PIL.Image
    img = PIL.Image.open('(Path to your Image.)')
    ```

3. Propmt to Gemini AI

    ```python
    response = model.generate_content(["Derive The Text", img], stream=True)
    response.resolve()
    ```

4. Get the response via ```Response.text``` And use it anywhere you want






