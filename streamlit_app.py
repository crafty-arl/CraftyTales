import streamlit as st
import openai
import tweepy
import os

# Retrieve the OpenAI Key from the environment variables
openai.api_key = os.getenv('OPENAI_KEY')

# Set up the Twitter API client
twitter_consumer_key = os.getenv('CONSUMER_KEY')
twitter_consumer_secret = os.getenv('CONSUMER_SECRET')
twitter_access_token = os.getenv('ACCESS_TOKEN')
twitter_access_token_secret = os.getenv('ACCESS_TOKEN_SECRET')

auth = tweepy.OAuthHandler(twitter_consumer_key, twitter_consumer_secret)
auth.set_access_token(twitter_access_token, twitter_access_token_secret)
api = tweepy.API(auth)


# Function to generate story introduction
@st.cache_data
def generate_story_intro(character_name, character_race, character_class):
    prompt = (f"A new adventure begins with a character named {character_name},"
              f"a {character_race} {character_class}. "
              f"Introduce the beginning of their story.")

    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=150,
        n=1,
        stop=None,
        temperature=0.7,
    )

    return response.choices[0].text.strip()


# Character creation interface
st.title("Character Creation for Adventure Story")

character_name = st.text_input("Enter your character's name:")
race_options = ["Human", "Elf", "Dwarf", "Orc", "Tiefling"]
character_race = st.selectbox("Select your character's race:", race_options)
class_options = ["Warrior", "Mage", "Rogue", "Cleric", "Ranger"]
character_class = st.selectbox("Select your character's class:", class_options)

if character_name and character_race and character_class:
    st.subheader("Character Summary")
    st.write(f"Name: {character_name}")
    st.write(f"Race: {character_race}")
    st.write(f"Class: {character_class}")

    # Generate and display story introduction
    st.subheader("Story Introduction")
    story_intro = generate_story_intro(character_name, character_race, character_class)
    st.write(story_intro)

    # Tweet the story
    tweet_url = f"https://twitter.com/intent/tweet?text=Check+out+this+story%3A+{story_intro}+%23ChooseYourOwnAdventure+_craftthefuture"
    tweet_button = f'<a href="{tweet_url}" target="_blank">Tweet</a>'
    st.markdown(tweet_button, unsafe_allow_html=True)
