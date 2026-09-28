# 🎓 Professor Detail Finder AI (CrewAI + Groq)

An automated multi-agent AI system built with **CrewAI**, **Groq LLMs**, and **DuckDuckGo Free Search** to find comprehensive details about professors, including their academic background, research interests, official university email addresses, phone numbers, and web profiles.

---

## ✨ Features

- 🌐 **Free Web Search**: Powered by DuckDuckGo (No paid Serper/Google Search API required).
- ⚡ **Ultra Fast & Flexible Groq LLMs**: Select between various Groq models directly from the UI (`Llama 3.3 70B`, `Llama 3.1 8B Instant`, `DeepSeek R1 Distill`, `Gemma 2`, `Mixtral`, etc.).
- 🎨 **Modern Local Web UI**: Sleek, dark-mode glassmorphic dashboard built with Streamlit.
- 👥 **Multi-Agent Architecture**:
  - **Academic Researcher Agent**: Finds department, designation, research topics, and web profiles.
  - **Contact Extractor Agent**: Finds official email, office contact, and university links.
- 💾 **Auto Report Export**: Automatically saves reports to `output/` folder and provides 1-click Download buttons (`.txt` & `.md`).

---

## 🚀 How to Run

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run with Web UI (Localhost Dashboard)
```bash
streamlit run app.py
```
Yeh command chalane ke baad aapka browser automatically open ho jayega (`http://localhost:8501`).

### 3. Run in Terminal (CLI Mode)
```bash
python -m src.main
```
"# professor-detail-finder-agent" 
