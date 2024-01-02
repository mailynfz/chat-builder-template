# Chat Builder Template

## Introduction

This template enables professors and educators to easily create their own teaching assistant chatbots. It leverages Streamlit for web interfacing and OpenAI's Assistants API for chat functionality, offering customizable features to suit various teaching needs.

This is the template used by Chat-Lab.AI's *Chat Builder*.

### Requirements

- Python installation.
- An API key from OpenAI.
- Streamlit installed (pip install streamlit).
- A GitHub account for deployment.

## Setup Instructions

### Filling the Template

- `site_title`: Enter the title of your chatbot site.
- `site_icon`: Choose an icon for your site (e.g., an image path or emoji).
- `page_heading`: Set the main heading of the page; defaults to site_title if left blank.
- `heading_color`: Choose the color for the heading text.
- `description`: Write a brief description for your chatbot.
- `instructions`: Provide instructions or guidelines for using the chatbot.
- `chat_box_text`: User should enter the text for the chat box.
- `sidebar_text`: User should provide text for the sidebar.
- `user_name`: User should enter a name.
- `user_email`: User should enter an email address.
- `footer_text`: User should provide text for the footer.
- `heading_color`: Choose a color for the heading text using Hex numbers. If not specified, headings default to black otherwise.

Refer to this image to see where these text variables will appear on the chat interface.

<img src="https://chat-builder.nyc3.cdn.digitaloceanspaces.com/app-marked-up.png" alt="Alt text" style="max-width: 100%; height: auto; border-radius: 10px; box-shadow: 5px 5px 10px rgba(0,0,0,0.3);">

### Uploading to GitHub

- Create a new repository on GitHub.
- Upload the modified `streamlit-app.py` and `requirements.txt` file to your repository.
- The `requirements.txt` list all necessary Python packages, including streamlit and any others used in your template.

### Deploying on Streamlit Cloud

- Sign in to Streamlit Cloud using your GitHub account.
- Connect your GitHub repository containing the chatbot template and requirements.txt.

#### Important! Update your OpenAI variables in the app's settings  

**Before deploying**, add your OpenAI API key and Assistant ID as "secrets" in the app’s settings:

- Navigate to your app settings on Streamlit Cloud.  
- Go to the `Secrets` section.
- Copy and paste the following text exactly:  

    ```python
    OPENAI_API_KEY='your_api_key_here'
    ASSISTANT_ID='your_assistant_id'
    PASSKEY='your_own_password or your_api_key'
    ```

Replace the text inside the quotes for each variable added to the secrets settings. Please be careful not to remove the `'` quotation marks, as they are part of the code.

- `your_api_key_here` = replace this text with your own API key
- `your_assistant_id` = replace this text with the Assistant ID for the Assistant that you will be using with this chat interface. You can find the Assistant ID on the Assistants page in the OpenAI platform. You can also find it using the Assistants Lab on Chat-Lab.AI, just enter your API key, select your assistant, and navigate to the Assistant Details tab.
- `your_own_password or your_api_key` = this text gives you the option of creating a password and using that with the interface instead of your API key. Setting your own password has a few benefits, not the least of which is that you don't have to look up your API key everytime you want to use the app. It also lets you share the app and pay for the API costs, if you choose to do so. For instance, if your department will reimburse you for student usage, this would be the easiest way to share the app with students. Otherwise, bright, but wily students could begin incurring API costs outside of this app on your dime. If you don't wish to enable a password, then you should set this variable to your API key. This value should not be left blank. Also, it should not be this default value, unless you want to incur additional API charges from anyone who knows how to crack passwords.

### Deploy your chatbot

Streamlit Cloud will automatically host it based on the contents of your repository.

### Customization Tips

- You can further customize the chat interface, such as adding more interactive elements or changing the theme.
- Experiment with different settings to find what works best for your educational needs.

## Support

For further assistance or queries, please refer to the [Chat-Lab.AI documentation](https:docs.chat-lab.ai).  

## Video Tutorial

Here is an excellent video tutorial by [@DataProfessor (YouTube)](https://www.youtube.com/channel/UCV8e2g4IWQqK71bbzGDEI4Q) on how to deploy your Streamlit app to the Streamlit Cloud using the procedure I outline here. I cannot improve upon this video, so I'm just going to share it with you all here. Hat tip to the [Data Professor (GitHub)](https://github.com/dataprofessor/).

[![Video](https://img.youtube.com/vi/HKoOBiAaHGg/maxresdefault.jpg)][def]

[def]: https://youtu.be/HKoOBiAaHGg?si=PIk10_1EF9F7gus0
