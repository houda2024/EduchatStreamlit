import streamlit as st
import os
import time  

from langchain.chains import ConversationChain, LLMChain
from langchain_core.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder,
)
from langchain_core.messages import SystemMessage
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from langchain_groq import ChatGroq

# Function to measure response time
def measure_response_time(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        response_time = end_time - start_time
        return result, response_time
    return wrapper

# Function to measure accuracy
# Function to measure accuracy based on user feedback
def measure_accuracy(user_feedback, response):
    if user_feedback in ["Very Satisfied", "Satisfied"]:
        accuracy = 100  # User considered the response as correct
    elif user_feedback == "Neutral":
        accuracy = 50   # User unsure about the response
    else:
        accuracy = 0    # User considered the response as incorrect
    return accuracy

# Function to track user engagement
def track_user_engagement():
    # Placeholder implementation, replace with actual tracking logic
    pass

def main():
    st.title("Educap Chatbot")

    # Customization options
    conversational_memory_length = st.sidebar.slider('Conversational memory length:', 1, 10, value=5)

    memory = ConversationBufferWindowMemory(k=conversational_memory_length, memory_key="chat_history", return_messages=True)

    user_question = st.text_input("Ask a question:")

    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    else:
        for message in st.session_state.chat_history:
            memory.save_context({'input': message['human']}, {'output': message['AI']})

    groq_chat = ChatGroq(
    groq_api_key="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",
    model_name='llama3-8b-8192'
)


    if user_question:
        # Determine the type of prompt to use based on the user question
        if "explain" in user_question.lower() or "describe" in user_question.lower():
            prompt_type = "FAQ"
        elif "quiz" in user_question.lower() or "test" in user_question.lower():
            prompt_type = "Quiz"
        elif "struggle" in user_question.lower() or "difficult" in user_question.lower():
            prompt_type = "Adaptive Learning"
        elif "recommend" in user_question.lower() or "resources" in user_question.lower():
            prompt_type = "Resource Recommendations"
        elif "plan" in user_question.lower() or "study" in user_question.lower():
            prompt_type = "Study Planning"
        else:
            prompt_type = "General"

        # Construct a chat prompt template based on the detected prompt type
        if prompt_type == "FAQ":
            system_message_content = "This is an FAQ prompt. Please provide a detailed and explanatory answer."
        elif prompt_type == "Quiz":
            system_message_content = "This is a quiz prompt. Please provide a question with multiple-choice answers."
        elif prompt_type == "Adaptive Learning":
            system_message_content = "This is an adaptive learning prompt. Please simplify the explanation as needed."
        elif prompt_type == "Resource Recommendations":
            system_message_content = "This is a resource recommendation prompt. Please suggest relevant articles or videos."
        elif prompt_type == "Study Planning":
            system_message_content = "This is a study planning prompt. Please provide a structured study plan."
        else:
            system_message_content = "Welcome to the Educational Chatbot! How can I assist you today?"

        prompt = ChatPromptTemplate.from_messages([
            SystemMessage(content=system_message_content),
            MessagesPlaceholder(variable_name="chat_history"),
            HumanMessagePromptTemplate.from_template("{human_input}"),
        ])

        conversation = LLMChain(
            llm=groq_chat,
            prompt=prompt,
            memory=memory
        )

        # Measure response time
        @measure_response_time
        def get_response(user_input):
            return conversation.predict(human_input=user_input)

        response, response_time = get_response(user_question)

        # Record conversation history
        message = {'human': user_question, 'AI': response}
        st.session_state.chat_history.append(message)

        # Display response and response time
        st.write("Chatbot:", response)
        st.write("Response Time:", response_time)
        

        

        # Track user engagement
        track_user_engagement()

        # Collect user feedback
        user_feedback = st.selectbox("How satisfied are you with the chatbot's response?", ["Very Satisfied", "Satisfied", "Neutral", "Dissatisfied", "Very Dissatisfied"])
        
        # Measure accuracy based on user feedback
        accuracy = measure_accuracy(user_feedback, response)
        st.write("Accuracy:", accuracy)

       

if __name__ == "__main__":
    main()
