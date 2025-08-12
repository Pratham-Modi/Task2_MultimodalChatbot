# 🤖 Task 2: Multimodal Chatbot (Text + Image Captioning)

This project is a smart and simple **multimodal chatbot** that can:

- 💬 Respond to **text queries**
- 🖼️ Generate **captions for uploaded images**
- 🖼️💬 Answer **questions about uploaded images**

It leverages the **Gemini 1.5 Flash API** (Google), with a clean UI built using **Streamlit**.

---

## 🚀 Built With

- 🖥️ `Streamlit` – Interactive frontend for the chatbot  
- 🤖 `google-generativeai` – Gemini 1.5 Flash API integration  
- 🖼️ `Pillow` – Image upload and handling  
- 🔐 `python-dotenv` – Secure API key management via `.env`

---

## ✨ Features

✅ Text-based chatbot powered by Gemini  
✅ Image captioning via uploaded images  
✅ Image + prompt response (multimodal)  
✅ Clean and simple Streamlit UI  
✅ Free-tier friendly (Gemini API)

---

## 🧪 Testing & Evaluation

The chatbot was tested manually with various text and image prompts to ensure relevant and coherent responses. Users can view past interactions within the app’s chat history tabs.

---

## 🔒 Security

The `.env` file containing sensitive API keys is included in `.gitignore` to prevent accidental sharing of credentials.

---

## 🧱 Folder Structure

Task2_MultimodalChatbot/
│
├── app.py # Main Streamlit application
├── requirements.txt # Required Python packages
├── .env # API keys (DO NOT SHARE)
├── README.md # Project overview (this file)

---

## 🔧 Setup Instructions

### 1. Clone the repository
git clone https://github.com/your-username/Task2_MultimodalChatbot.git
cd Task2_MultimodalChatbot
### 2. Install dependencies
pip install -r requirements.txt
### 3. Set API Key in .env
Create a .env file in the root directory and add your key:
GOOGLE_API_KEY=your_gemini_key_here
### 4. Run the Streamlit app
streamlit run app.py

---

## 📸 Example Use

💬 Text Mode
Input: What is the capital of France?
Gemini Response: Paris

🖼️ Image Mode
Upload: dog.jpg
Gemini Caption: A golden retriever puppy is sitting on green grass with a happy expression.

🖼️ + 💬 Image + Prompt Mode
Upload: car.jpg
Prompt: What brand is this car?
Gemini Response: This appears to be a Tesla Model 3 based on the logo and design.

---

## 📦 requirements.txt

- streamlit
- pillow
- google-generativeai
- python-dotenv

---

## 📌 Notes

⚠️ Free-tier API usage is limited — upgrade for heavier workloads

🔒 Keep your .env file private (it is ignored by Git)

☁️ This app runs fully online — no GPU required locally

---

## 👨‍💻 Developed by
Pratham Modi
📅 July 2025
