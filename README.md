# AI Agent 1: Gemini Multi-Agent Araştırma Asistanı

Kaynak: Building a Multi-Agent System using Gemini API (Aman Kharwal) - https://amanxai.com/2025/09/16/building-a-multi-agent-system-using-gemini-api/

- `MultiAgent_Gemini.ipynb`: makaledeki kod, Colab için (Secrets'a `GOOGLE_API_KEY` ekleyin).
- `agents.py` + `app.py`: aynı ajanların Streamlit sürümü. Çalıştırmadan önce `GOOGLE_API_KEY` ortam değişkenini ayarlayın.

Not: Makaledeki kod `gemini-1.5-pro-latest` modelini ve `google-generativeai` paketini kullanıyor. Google bu eski modelleri ve arama aracı biçimini kaldırmış olabilir. 404/model bulunamadı hatası alırsanız `configure()` içindeki model adını güncel bir Gemini modeliyle değiştirin.
