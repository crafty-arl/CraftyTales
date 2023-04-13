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
    prompt = f"Human: A new adventure begins with a character named {character_name}, a {character_race} {character_class}. Introduce the beginning of their story in 25 words or less."

    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        temperature=0.7,
        max_tokens=65,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        stop=["Human:", "AI:"],
    )

    return response.choices[0].text.strip()

# Function to summarize story in one sentence
@st.cache_data
def summarize_story(story):
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=f"Summarize the following story in one sentence:\n\n{story}",
        temperature=0.3,
        max_tokens=30,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        stop=["\n"],
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
            st.session_state.story_generated = True

with col2:
    st.title("Story Generation")

    if st.session_state.get("story_generated", False):
        st.subheader("Story Introduction")
        story_intro = generate_story_intro(character_name, character_race, character_class)
        st.write(story_intro)

        # Generate story and summary
        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=f"Human: {story_intro}\nAI:",
            temperature=0.7,
            max_tokens=1024,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
            stop=["Human:", "AI:"],
        )
        story = story_intro + response.choices[0].text.strip()

        summary = summarize_story(story)
        st.write(story)

        # Tweet the story summary
        tweet_text = f"{summary} #CraftyTales @craftthefuture_ Craft Your Tale
