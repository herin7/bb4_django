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

---

BestBefore is a cutting-edge web application designed to streamline inventory management for users' daily needs, encompassing food, medicine, or any other essentials. The elegantly crafted homepage presents users with intuitive options, including adding items manually or seamlessly scanning them using Google's Gemini API.

In the "Add Food" feature, users can input details such as product name, type, quantity, and expiry date, ensuring meticulous record-keeping. Meanwhile, the "Scan to Add" function utilizes Gemini AI to automatically retrieve product details, setting expiry dates six months from the addition date, thus simplifying data entry.

The application's chatbot empowers users to effortlessly retrieve information from the stored database, enhancing user interaction and accessibility. Built on the Django framework with an SQLite3 database, the implementation ensures efficient data management and scalability.

Security is paramount, with dual authentication systems from Google and Github, safeguarding user accounts with keys from the respective organizations. Furthermore, a "Send Welcome Email" feature automatically welcomes users to the platform, fostering a seamless onboarding experience.

A standout feature is the "Notify Expiry" function, which notifies users via email of expired items, facilitating timely action. Additionally, the "Generate PDF" functionality enables users to print inventory lists directly from the frontend, enhancing convenience.

Moreover, the application boasts a "Delete Food Item" feature, allowing users to easily manage their inventory. BestBefore is accessible across both mobile and desktop devices, ensuring convenience and flexibility for users on the go.

In conclusion, BestBefore sets a new standard in inventory management, offering a comprehensive suite of features combined with intuitive design and robust functionality, making it an indispensable tool for users' daily lives.
