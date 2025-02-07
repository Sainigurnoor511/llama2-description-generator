import streamlit as st
import replicate
import os

# App title
st.set_page_config(page_title= "🍕Dish Description Generator")

# Replicate Credentials
with st.sidebar:
    st.title("🍕Dish Description Generator")
    if 'REPLICATE_API_TOKEN' in st.secrets:
        st.success('API key already provided!', icon='✅')
        replicate_api = st.secrets['REPLICATE_API_TOKEN']
    else:
        replicate_api = st.text_input('Enter Replicate API token:', type='password')
        if not (replicate_api.startswith('r8_') and len(replicate_api)==40):
            st.warning('Please enter your credentials!', icon='⚠️')
        else:
            st.success('Proceed to entering your prompt message!', icon='👉')
    os.environ['REPLICATE_API_TOKEN'] = replicate_api

    st.subheader('Models and parameters')
    selected_model = st.sidebar.selectbox('Choose a Llama2 model', ['Llama2-7B', 'Llama2-13B'], key='selected_model')
    if selected_model == 'Llama2-7B':
        llm = 'a16z-infra/llama7b-v2-chat:4f0a4744c7295c024a1de15e1a63c880d3da035fa1f49bfd344fe076074c8eea'
    elif selected_model == 'Llama2-13B':
        llm = 'a16z-infra/llama13b-v2-chat:df7690f1994d94e96ad9d568eac121aecf50684a0b0963b25a41cc40061269e5'

    temperature = 0.70
    top_p = 0.26
    max_length = st.sidebar.slider('max_length', min_value=5, max_value=125, value=20, step=5)

# Function for generating LLaMA2 response
def generate_llama2_response(dish_name, keywords):

    string_dialogue = f"You are product description assistant. Please provide a product description for Dish Name: {dish_name}\nKeywords: {keywords}\n in maximum of {max_length} words."

    #TODO: remove later
    # prompt_input = f"Dish Name: {dish_name}\nKeywords: {keywords}\n"
    # string_dialogue = "You are product description assistant. Please provide a product description for "
    
    output = replicate.run(llm,input={"prompt": f"{string_dialogue}",
                                    #   "temperature":temperature, 
                                    #   "top_p":top_p, 
                                    #   "max_length":max_length, 
                                    #   "repetition_penalty":1
                                    })

    return output

# User inputs for dish name and keywords
dish_name = st.text_input("Enter the dish name:")
keywords = st.text_input("Enter keywords (comma-separated):")

if st.button("Generate Response", disabled=not replicate_api):
    if dish_name and keywords:
        with st.spinner("Generating..."):
            response = generate_llama2_response(dish_name, keywords)
            placeholder = st.empty()
            full_response = ''
            for item in response:
                full_response += item
                placeholder.markdown(full_response)
            placeholder.markdown(full_response)
    else:
        st.warning("Please enter both dish name and keywords!", icon='⚠️')

# Clear chat history button
def clear_chat_history():
    st.session_state.messages = [{"role": "assistant", "content": "How may I assist you today?"}]
st.sidebar.button('Clear Chat History', on_click=clear_chat_history)