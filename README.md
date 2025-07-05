
# 🩺 Voice-Enabled Cardiac Specific Chatbot (LLama 3 + TTS/STT + RAG)

This is a multimodal healthcare chatbot that allows users to **speak** with an AI system specialized in **cardiac-related queries**. It responds back using voice and is fine-tuned on **domain-specific cardiac data**. The system uses **LLaMA 3** as the base model, integrates **speech-to-text (STT)** and **text-to-speech (TTS)**, and retrieves relevant context using a **RAG pipeline** powered by LangChain.

---

## ✨ Features

- 🎤 **Voice Input Support** – Users can interact with the chatbot using natural speech.
- 🔊 **Voice Output** – The chatbot responds using text-to-speech, enabling full voice-based conversations.
- 🧠 **LLama 3-Based Core** – Powered by Meta’s LLaMA 3 model, fine-tuned on curated cardiac healthcare data.
- 📚 **RAG Integration** – Uses LangChain to retrieve relevant documents before generating answers.
- 🧾 **Medical-Grade Domain Knowledge** – Specialized in handling cardiac symptoms, treatment options, and lifestyle advice.
- 🌐 **Web-Based Interface** – User-friendly web interface built using Flask and HTML/CSS.

---

## 🔧 Installation

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/your-username/voice-cardiac-chatbot.git
cd voice-cardiac-chatbot
```

### 2️⃣ Create a Virtual Environment (Optional but Recommended)
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 4️⃣ Run the Application
```bash
python app.py
```

➡️ Open [http://127.0.0.1:5000](http://127.0.0.1:5000) in your browser to start chatting!

---

## 🛠️ Technologies Used

- `Python`  
- `LLaMA 3` – Large language model core  
- `LangChain` – For RAG-based document retrieval  
- `Flask` – Web server  
- `SpeechRecognition` – Voice input (STT)  
- `gTTS` or `pyttsx3` – Voice output (TTS)  
- `HuggingFace Transformers` – Model handling  
- `ChromaDB` – Document vector store for RAG  

---

## 📈 Future Enhancements

- ✅ Add user authentication  
- ✅ Store conversation history in a database  
- ✅ Enable support for multiple languages  
- ✅ Deploy on cloud with SSL & scalable APIs

---

## 📄 License

This project is licensed under the **MIT License**.
