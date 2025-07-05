import os
from groq import Groq
from flask import Flask, request, jsonify, send_from_directory, Response, stream_with_context
from flask_cors import CORS
import httpx
import json

app = Flask(__name__)
CORS(app)

api_key = "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"
client = Groq(
    api_key=api_key,
    http_client=httpx.Client()
)

conversation_history = []

system_prompt = '''
You are a medical chatbot specializing in assisting post-angioplasty patients. Your primary role is to provide accurate, concise, and empathetic guidance on:  

1. **Recovery Process**:
   - Offer step-by-step instructions on post-procedure care
   - Emphasize the importance of following medical advice
   - Provide clear timelines for recovery milestones

2. **Medication Guidelines**:
   - Explain proper usage and dosages
   - Stress the importance of medication adherence
   - Focus on the benefits without mentioning side effects

3. **Lifestyle Recommendations**:
   - **Diet**: Suggest heart-healthy eating habits
   - **Exercise**: Recommend appropriate physical activities
   - **Stress Management**: Share effective relaxation techniques
   - **Smoking Cessation**: Provide supportive guidance if applicable

4. **Follow-up Care**:
   - Guide patients on scheduling check-ups
   - Help monitor symptoms effectively
   - Facilitate communication with healthcare providers

Always format your responses with:
- **Bold text** for important points and headers
- Bullet points for lists
- Clear paragraph breaks for readability
- Numbered steps for instructions

Ensure all responses are:
- **Clear, concise and medically sound**
- **Supportive and reassuring**

Avoid:
- Mentioning side effects
- Providing diagnoses or prescribing medications
- Contradicting medical professionals
'''

def get_chatbot_response(user_input, max_tokens=200):
    conversation_history.append({"role": "user", "content": user_input})
    prompt = system_prompt
    for message in conversation_history:
        prompt += f"{message['role'].capitalize()}: {message['content']}\n"

    chat_completion = client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model="llama-3.3-70b-versatile",
        max_tokens=max_tokens,
        stream=True
    )

    return chat_completion

@app.route('/')
def serve_index():
    return send_from_directory('.', 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('.', path)

@app.route('/api/chat', methods=['POST'])
def chat():
    if not request.is_json:
        return jsonify({'error': 'Content-Type must be application/json'}), 400
        
    data = request.json
    user_message = data.get('message', '')
    
    def generate():
        try:
            response_stream = get_chatbot_response(user_message)
            collected_message = ""
            
            for chunk in response_stream:
                if hasattr(chunk.choices[0], 'delta') and hasattr(chunk.choices[0].delta, 'content'):
                    content = chunk.choices[0].delta.content
                    if content:
                        collected_message += content
                        yield f"data: {json.dumps({'content': content})}\n\n"
            
            conversation_history.append({"role": "assistant", "content": collected_message})
            
        except Exception as e:
            print(f"Error in generate: {str(e)}")  # Debug print
            yield f"data: {json.dumps({'error': str(e)})}\n\n"
    
    return Response(stream_with_context(generate()), 
                   mimetype='text/event-stream',
                   headers={
                       'Cache-Control': 'no-cache',
                       'X-Accel-Buffering': 'no'
                   })

if __name__ == '__main__':
    app.run(debug=True, port=5000)