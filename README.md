# AI-Based Automated Email Response System

This application uses AI models from Amazon Bedrock and OpenRouter to generate context-aware email responses based on the content of received emails.

## Features

- Email content analysis using AI models
- Context-aware reply generation
- Multiple AI model options (Amazon Bedrock Titan and various OpenRouter models)
- Customizable writing styles (Professional, Friendly, Concise, Detailed, Empathetic)
- User-friendly interface for approving and editing AI-generated responses

## Setup

1. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Configure your API keys:
   - For Amazon Bedrock: The AWS credentials are already configured in the application
   - For OpenRouter: Replace the placeholder API key in the `email_response_system.py` file

3. Run the application:
   ```
   python email_response_system.py
   ```

## Usage

1. Paste the email content you received in the 'Email Content' box
2. Select an AI model from the dropdown menu
3. Choose a writing style that matches your needs
4. Click 'Generate Response' to create an AI-generated reply
5. Edit the generated response as needed
6. Use 'Copy to Clipboard' to copy the final response

## Models

The application supports the following AI models:

- Amazon Bedrock Titan
- Gemini 2.0 Flash
- Mistral Small 3.1 24B
- Microsoft Phi-3 Medium 128K
- DeepSeek V3
- Moonlight 16B A3B

## Writing Styles

You can customize the tone of the generated response by selecting one of these writing styles:

- Professional: Formal tone suitable for business communication
- Friendly: Warm tone while maintaining professionalism
- Concise: Brief, to-the-point responses
- Detailed: Comprehensive responses with explanations
- Empathetic: Responses that show understanding and empathy