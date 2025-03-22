import os
import boto3
import json
import streamlit as st
import pyperclip
from openai import OpenAI
from botocore.exceptions import ClientError

# Amazon Bedrock client setup
def get_bedrock_client():
    return boto3.client(
        "bedrock-runtime",
        aws_access_key_id="aws_access_key_id_here",
        aws_secret_access_key="aws_secret_access_key_here",
        region_name="region_name_here"
    )

# OpenRouter client setup
def get_openrouter_client():
    return OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key="api_key_here",  # Replace with your actual API key
    )

# Available models
MODELS = {
    "Amazon Bedrock Titan": "amazon.titan-text-express-v1",
    "Gemini 2.0 Flash": "google/gemini-2.0-flash-thinking-exp-1219:free",
    "Mistral Small 3.1 24B": "mistralai/mistral-small-3.1-24b-instruct:free",
    "Microsoft Phi-3 Medium": "microsoft/phi-3-medium-128k-instruct:free",
    "DeepSeek V3": "deepseek/deepseek-chat:free",
    "Moonlight 16B": "moonshotai/moonlight-16b-a3b-instruct:free"
}

# Writing styles
WRITING_STYLES = {
    "Professional": "Write in a professional and formal tone suitable for business communication.",
    "Friendly": "Write in a warm, friendly tone while maintaining professionalism.",
    "Concise": "Write a brief, to-the-point response that addresses the key points.",
    "Detailed": "Provide a comprehensive response with detailed explanations.",
    "Empathetic": "Show understanding and empathy in the response."
}

# Generate response using Amazon Bedrock
def generate_bedrock_response(email_content, model_id, writing_style):
    try:
        client = get_bedrock_client()
        
        # Create prompt with email content and writing style
        prompt = f"""Generate a professional email response to the following email. {WRITING_STYLES[writing_style]}

Original Email:
{email_content}

Response:"""
        
        # Format the request payload
        body = json.dumps({
            "inputText": prompt,
            "textGenerationConfig": {
                "maxTokenCount": 512,
                "temperature": 0.7,
                "topP": 0.9
            }
        })
        
        # Invoke the model
        response = client.invoke_model(
            body=body,
            modelId=model_id,
            accept="application/json",
            contentType="application/json"
        )
        
        # Parse the response
        response_body = json.loads(response.get('body').read())
        generated_text = response_body.get('results')[0].get('outputText')
        
        # Clean up the response if needed
        if '\n' in generated_text:
            generated_text = generated_text[generated_text.index('\n')+1:]
        
        return generated_text.strip()
        
    except ClientError as e:
        return f"Error: {e.response['Error']['Message']}"
    except Exception as e:
        return f"An error occurred: {str(e)}"

# Generate response using OpenRouter models
def generate_openrouter_response(email_content, model_id, writing_style):
    try:
        client = get_openrouter_client()
        
        # Create prompt with email content and writing style
        prompt = f"""Generate a professional email response to the following email. {WRITING_STYLES[writing_style]}

Original Email:
{email_content}

Response:"""
        
        # Call the OpenRouter API
        completion = client.chat.completions.create(
            model=model_id,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        
        return completion.choices[0].message.content
        
    except Exception as e:
        return f"An error occurred: {str(e)}"

# Main function to generate response based on selected model
def generate_response(email_content, model_name, writing_style):
    if not email_content.strip():
        return "Please enter an email to generate a response."
    
    model_id = MODELS[model_name]
    
    # Use Bedrock for Amazon model, OpenRouter for others
    if model_name == "Amazon Bedrock Titan":
        return generate_bedrock_response(email_content, model_id, writing_style)
    else:
        return generate_openrouter_response(email_content, model_id, writing_style)

# Set page config
st.set_page_config(
    page_title="AI Email Response System",
    page_icon="✉️",
    layout="wide"
)

# App title and description
st.title("AI-Based Automated Email Response System")
st.markdown("Generate context-aware email replies using AI models from Amazon Bedrock and OpenRouter.")

# Create two columns for layout
col1, col2 = st.columns([1, 2])

with col1:
    st.markdown("### Settings")
    
    # Model selection dropdown
    model_name = st.selectbox(
        "Select AI Model",
        options=list(MODELS.keys()),
        index=0
    )
    
    # Writing style dropdown
    writing_style = st.selectbox(
        "Writing Style",
        options=list(WRITING_STYLES.keys()),
        index=0
    )
    
    # Generate button
    generate_button = st.button("Generate Response", type="primary")

with col2:
    # Email input area
    email_input = st.text_area(
        "Email Content",
        placeholder="Paste the email content here...",
        height=250
    )
    
    # Response output area
    response_output = st.empty()

# Handle generate button click
if generate_button and email_input:
    with st.spinner("Generating response..."):
        st.session_state.generated_response = generate_response(email_input, model_name, writing_style)

if 'generated_response' in st.session_state:
    response_output.text_area("Generated Response", 
                             value=st.session_state.generated_response, 
                             height=300,
                             key="response_textarea")
    
    # Copy button with Python-based functionality
    if st.button("Copy to Clipboard", help="Copy the generated response to clipboard"):
        try:
            # Copy the generated response to clipboard using pyperclip
            pyperclip.copy(st.session_state.generated_response)
            
            # Show success message
            st.success("Response copied to clipboard!", icon="✅")
        except Exception as e:
            # Show error message if copying fails
            st.error(f"Failed to copy: {str(e)}", icon="⚠️")

# Clear button
if st.button("Clear"):
    # Clear all session state variables
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()

# Instructions
st.markdown("### Instructions")
st.markdown("""
1. Paste the email content you received in the 'Email Content' box
2. Select an AI model from the dropdown menu
3. Choose a writing style that matches your needs
4. Click 'Generate Response' to create an AI-generated reply
5. Edit the generated response as needed
6. Use 'Copy to Clipboard' to copy the final response
""")