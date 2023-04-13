import streamlit as st
import openai
import os
import webbrowser
import urllib.parse
from PIL import Image

# Retrieve the OpenAI Key from the environment variables
openai.api_key = os.getenv('OPENAI_KEY')
img_path = "craftytales.png"
img = Image.open(img_path).resize((500, 500))

# Function to generate story introduction
@st.cache_data
def generate_story_intro(character_name, character_race, character_class):
    prompt = f"Human: A new adventure begins with a character named {character_name}, a {character_race} {character_class}. Introduce the beginning of their story in 250 charcters or less."

    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        temperature=0.7,
        max_tokens=75,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        stop=["Human:", "AI:"],
    )

    return response.choices[0].text.strip()

# Character creation interface
st.set_page_config(layout='wide')
col1, col2 = st.beta_columns(2)

with col1:
    st.image(img, caption="A Digital Storytelling Companion")

    st.title("Character Creation")
    character_name = st.text_input("Enter your character's name:")
    race_options = ["Human", "Elf", "Dwarf", "Orc", "Tiefling"]
    character_race = st.selectbox("Select your character's race:", race_options)
    class_options = ["Warrior", "Mage", "Rogue", "Cleric", "Ranger"]
    character_class = st.selectbox("Select your character's class:", class_options)

    if st.button("Submit"):
        if character_name and character_race and character_class:
            st.subheader("Character Summary")
            st.write(f"Name: {character_name}")
            st.write(f"Race: {character_race}")
            st.write(f"Class: {character_class}")

with col2:
    st.title("Story Generation")

    if character_name and character_race and character_class:
        st.subheader("Story Introduction")
        story_intro = generate_story_intro(character_name, character_race, character_class)
        st.write(story_intro)

        # Tweet the story
        tweet_text = f"Check out this story: {story_intro} #CraftyTales @_craftthefuture"
        tweet_url = "https://twitter.com/intent/tweet?text=" + urllib.parse.quote(tweet_text)
        tweet_button = f'<a href="{tweet_url}" target="_blank">Tweet</a>'
        st.markdown(tweet_button, unsafe_allow_html=True)
