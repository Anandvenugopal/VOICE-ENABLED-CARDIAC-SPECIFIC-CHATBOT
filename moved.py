import os
import json
from groq import Groq

api_key = "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"
# Initialize the Groq client
client = Groq(api_key=api_key)

conversation_history = []

system_prompt = '''
You are a medical chatbot specializing in assisting post-angioplasty patients. Your primary role is to provide accurate, concise, and empathetic guidance on:  

1. Recovery process: Offer step-by-step instructions on post-procedure care.  
2. Medication guidelines: Explain usage, dosages, and adherence importance without mentioning side effects.  
3. Lifestyle recommendations: Provide advice on diet, exercise, stress management, and smoking cessation.  
4. Follow-up care: Guide patients on scheduling check-ups, monitoring symptoms, and communicating with healthcare providers.  

Ensure all responses are:  
- **Clear, concise, and medically sound**  
- **Supportive and reassuring**  

Avoid:  
- Mentioning side effects  
- Providing diagnoses or prescribing medications  
- Contradicting medical professionals  
'''

def get_chatbot_response(user_input, max_tokens=1000):
    conversation_history.append({"role": "user", "content": user_input})
    prompt = system_prompt
    for message in conversation_history:
        prompt += f"{message['role'].capitalize()}: {message['content']}\n"

    chat_completion = client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model="llama-3.3-70b-versatile",
        max_tokens=max_tokens
    )

    response_text = chat_completion.choices[0].message.content.strip()

    # Generate a separate 'voice_content'
    voice_prompt = f"Summarize this response in one sentence for voice output: {response_text}"
    voice_completion = client.chat.completions.create(
        messages=[{"role": "user", "content": voice_prompt}],
        model="llama-3.3-70b-versatile",
        max_tokens=50  # Keep it concise
    )
    voice_content = voice_completion.choices[0].message.content.strip()

    chatbot_response = {
        "main_content": response_text,
        "voice_content": voice_content
    }

    conversation_history.append({"role": "assistant", "content": chatbot_response})
    
    return json.dumps(chatbot_response, ensure_ascii=False, indent=2)




question = input("q: ")
print(get_chatbot_response(question))
