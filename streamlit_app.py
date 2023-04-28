# Import required libraries
import streamlit as st
import yaml
import pandas as pd
import openai

from langchain.agents import (
    create_json_agent,
    AgentExecutor
)

from langchain.agents.agent_toolkits import JsonToolkit
from langchain.document_loaders import CSVLoader
from langchain.indexes import VectorstoreIndexCreator
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
from langchain.agents import create_csv_agent
from langchain.llms import OpenAI
from langchain.requests import TextRequestsWrapper
from langchain.tools.json.tool import JsonSpec
import os

openai.api_key = os.getenv('OPENAI_KEY')

with open("Crafty+GameRules.json") as f:
    data = yaml.load(f, Loader=yaml.FullLoader)
json_spec = JsonSpec(dict_=data, max_value_length=4000)
json_toolkit = JsonToolkit(spec=json_spec)


# Load the documents
loader = CSVLoader("Crafty+Database.csv")

# Create an index
index_creator = VectorstoreIndexCreator()
docsearch = index_creator.from_loaders([loader])

# QA Chain and Agent
chain = RetrievalQA.from_chain_type(llm=ChatOpenAI(temperature=0,model_name='gpt-3.5-turbo'), chain_type="stuff", retriever=docsearch.vectorstore.as_retriever(), input_key="question")
agent = create_csv_agent(OpenAI(temperature=0,model_name='gpt-3.5-turbo'), 'D:\Langchain-Crafty+\Crafty+Database.csv', verbose=True)
json_agent_executor = create_json_agent(
    llm=OpenAI(temperature=0),
    toolkit=json_toolkit,
    verbose=True
)
#json_agent_executor.run("How do I Play Crafty+?")
#agent.run("Tell me about Queen Priestess")

#Query
#query = "What is the stats of Queen Priestess"
#initial_response = chain({"question": query})
#print(initial_response)

# Function to handle user input and generate chatbot response
# Function to handle user input and generate chatbot response
def chatbot_response(user_input):
    # Your chatbot logic goes here
    cards_question = f"Answer any question regarding the card database: {user_input}"
    response = agent.run(cards_question)
    
    if isinstance(response, dict):
        try:
            df = pd.DataFrame.from_dict(response, orient='index', columns=['Value'])
            df.reset_index(inplace=True)
            df.rename(columns={'index': 'Key'}, inplace=True)
            return df
        except KeyError:
            return "Sorry, I could not find the information you're looking for."
    else:
        return pd.DataFrame({"Key": ["Response"], "Value": [response]})

def chatbot_rules_response(user_input):
    # Your chatbot logic goes here
    rules_question = f"Can you give me clear rules on {user_input}"
    response = json_agent_executor.run(rules_question)
    
    if isinstance(response, dict):
        try:
            df = pd.DataFrame.from_dict(response, orient='index', columns=['Value'])
            df.reset_index(inplace=True)
            df.rename(columns={'index': 'Key'}, inplace=True)
            return df
        except KeyError:
            return "Sorry, I could not find the information you're looking for."
    else:
        return pd.DataFrame({"Key": ["Response"], "Value": [response]})


# Main function for the Streamlit application
# Main function for the Streamlit application
# Main function for the Streamlit application
def main():
    # Application title and description
    st.title("Crafty+ Chatbot")
    st.write("This is a chatbot that can answer questions about Crafty+.")

    # Set display options for pandas dataframes
    pd.set_option('display.max_columns', None)  # Show all columns
    pd.set_option('display.expand_frame_repr', False)  # Don't wrap to multiple pages
    pd.set_option('display.max_rows', None)  # Show all rows

    # Get user input for card information
    user_input_card = st.text_input("What question do you have about your card?:")

    # When user presses 'Send' button for card information
    if st.button("Send Card Info"):
        # Call the chatbot_response function with user input
        response = chatbot_response(user_input_card)

        # Display the chatbot's response
        st.write(f"Chatbot:")
        st.write(response)

    # Get user input for rules question
    user_input_rules = st.text_input("Ask a Question about the rules:")

    # When user presses 'Ask' button for rules question
    if st.button("Ask Rules"):
        response = chatbot_rules_response(user_input_rules)
        st.write(f"Chatbot:")
        st.write(response)

# Run the main function
if __name__ == "__main__":
    main()
