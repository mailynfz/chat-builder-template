from openai import OpenAI
import streamlit as st
import time
from PIL import Image

# USER DEFINED VARIABLES

# Set the title and icon for the site
site_title = "Site Title"
site_icon = "😎"

page_heading = "Page Heading" # Page heading defaults to site_title if left blank

# Set the color of the heading text
heading_color = ""

# Set text for the main chat area
description = f"""Description"""
instructions = f"""Instructions"""
chat_box_text = f"""Chat box text"""

# Set text for the sidebar
sidebar_text = f"""Sidebar text"""
user_name = "User name"
user_email = "User email" 
footer_text = f"""Footer text"""

# Optional: Add a logo to the sidebar
image_filepath = "https://chat-lab-asssets.nyc3.cdn.digitaloceanspaces.com/Chat-lab-bubble-logo-no_tail-removebg-white_face.png"

# SET DEFAULT TEXT FOR WARNING AND ERROR MESSAGES
# DO NOT CHANGE THIS TEXT:
error_message = f"**ERROR:** Please enter your API key AND click \'Start New Chat\' to get started."        
# DO NOT CHANGE THIS TEXT:
ai_warning_text = f"**WARNING:** This app uses the same GPT models as ChatGPT, which can make mistakes. Please verify information from chat responses in this app and report any errors to [{user_name}](mailto:{user_email})."

# SET STREAMLIT PAGE CONFIGURATION
st.set_page_config(page_title= site_title, page_icon= site_icon)

# DEFINE CUSTOM CSS STYLES
if heading_color == "":
    heading_color = "rgba(31, 31, 31, 1)"

st.markdown("""
    <style>
    body .main .block-container h1 {
        color: {heading_color}; 
    }
    body .main .block-container h2 {
        color: {heading_color};
    }
    body .main .block-container h3 {
        color: red;
    }
    body .sidebar .block-container h1 {
        color: {heading_color}; 
    }
    body .sidebar .block-container h2 {
        color: {heading_color}; 
    }
    body .sidebar .block-container h3 {
        color: red;
    }   
    .element-container .stTextInput input::placeholder {
        color: #E5751F; 
    }
    .element-container .stTextInput input {
        color: black; 
    }
    footer {
        visibility: hidden;
    }
    </style>
    """, unsafe_allow_html=True)

# MAIN PAGE SETUP
st.markdown(f"# {page_heading}", unsafe_allow_html=True)
st.caption(description)
st.markdown(f"## Instructions", unsafe_allow_html=True)
st.markdown(instructions)
st.divider()

# DISPLAY SIDEBAR IMAGE
if image_filepath != "":
    if image_filepath.startswith("http"):
        html_str = f"""
                    <div style="text-align: center;">
                    <img src='{image_filepath}' style='height:150px;'/>
                    </div>
                    """
        st.sidebar.markdown(html_str, unsafe_allow_html=True)
        st.sidebar.divider()
else:
    image = Image.open(image_filepath)
    st.sidebar.image(image, use_column_width=True)
    st.sidebar.divider()

# DEFINE ENVIRONMENT VARIABLES FROM STREAMLIT SECRETS (IF AVAILABLE)
if st.secrets:
    if 'ASSISTANT_ID' in st.secrets:
        ASSISTANT_ID = st.secrets['ASSISTANT_ID']
    if 'OPENAI_API_KEY' in st.secrets:
        OPENAI_API_KEY = st.secrets['OPENAI_API_KEY']
    if 'PASSKEY' in st.secrets:
        PASSKEY = st.secrets['PASSKEY']

# DEFINE SESSION STATE VARIABLES
if "THREAD_ID" not in st.session_state:
    st.session_state.THREAD_ID = None

if "messages" not in st.session_state:
    st.session_state.messages = []

# USER INPUT FOR API KEY
API_KEY = st.sidebar.text_input("Enter your API key", type="password")

# INITIALIZE A NEW CHAT THREAD
if st.sidebar.button("Start New Chat"):
    if API_KEY == PASSKEY:
        API_KEY = OPENAI_API_KEY
    if API_KEY == "":
        st.error(error_message, icon="🚨")
    else:    
        try:
            client = OpenAI(api_key=API_KEY)
            thread = client.beta.threads.create()
            st.session_state.THREAD_ID = thread.id
            st.session_state.messages = []
            st.sidebar.warning(f"{ai_warning_text}", icon="⚠️")
        except:
            st.error(f"**Authentication Error:** Please enter a valid API key", icon="🚨")

# INSERT OPTIONAL SIDEBAR TEXT
st.sidebar.divider()
st.sidebar.markdown(f"{sidebar_text}", unsafe_allow_html=True)

# CHAT INTERFACE SETUP 

# Display existing messages in the chat
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Chat input for the user
if prompt := st.chat_input(chat_box_text):
    if st.session_state.THREAD_ID is None:
        st.error(error_message, icon="🚨") # ERROR MESSAGE IF THREAD HAS NOT BEEN INITIALIZED
    else:
        format_prompt = prompt.replace("$", "\\$")
        # Add user message to the state and display it
        st.session_state.messages.append({"role": "user", "content": format_prompt})
        with st.chat_message("user"):
            st.write(str(format_prompt))

        # Add the user's message to the existing thread
        client.beta.threads.messages.create(
            thread_id = st.session_state.THREAD_ID,
            role="user",
            content=prompt
        )
        # Create a run with additional instructions
        run = client.beta.threads.runs.create(
            thread_id = st.session_state.THREAD_ID,
            assistant_id=st.session_state.ASSISTANT_ID
        )
        # Poll for the run to complete and retrieve the assistant's messages
        while run.status != 'completed':
            time.sleep(.5)
            run = client.beta.threads.runs.retrieve(
                thread_id = st.session_state.THREAD_ID,
                run_id=run.id
            )
        # Retrieve messages added by the assistant
        messages = client.beta.threads.messages.list(
            thread_id =  st.session_state.THREAD_ID, 
            order="asc"
        )
        # Process and display assistant messages
        assistant_messages_for_run = [
            message for message in messages 
            if message.run_id == run.id and message.role == "assistant"
        ]
        for message in assistant_messages_for_run:
            response = message.content[0].text.value
            st.session_state.messages.append({"role": "assistant", "content": response})
            with st.chat_message("assistant"):
                st.markdown(f"{response}", unsafe_allow_html=True)


# DEFINE FOOTER
def footer(text):
    footer_html = f"""
    <style>
    .footer {{
        position: fixed;
        left: 10;
        bottom: 0;
        width: 100%;
        background-color: rgba(241, 241, 241, 0);
        color: rgba(117, 120, 123, 1);
        text-align: left;
        font-size: 8px;
        }}
    </style>
    <div class='footer'>
        <p>{text}</p>
    </div>
    """
    st.sidebar.markdown(footer_html, unsafe_allow_html=True)

footer(footer_text)
