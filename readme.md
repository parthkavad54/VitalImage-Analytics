# VitalImage Analytics 👨‍⚕️

VitalImage Analytics is an intelligent Streamlit web application that uses Google's Gemini model to analyze medical images and provide detailed finding reports, recommendations, and next steps in multiple languages.

## Features
- **Instant Analysis**: Upload any medical image to get an AI-generated analysis.
- **Multi-language Support**: View reports in English, Hindi, Gujarati, Spanish, and French.
- **User-friendly UI**: Built with Streamlit for a fast, responsive, and clean user experience.

## Installation

1. Clone the repository:
   ```bash
   git clone <your-repo-url>
   cd medical_image_detection_app
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Setup your API Key:
   - Create a file named `api_key.py` in the root directory.
   - Add your Google Gemini API key to it:
     ```python
     api_key = "YOUR_API_KEY_HERE"
     ```

4. Run the app:
   ```bash
   streamlit run app.py
   ```

## Note
**Disclaimer:** This tool is for educational purposes only. Always consult with a qualified medical doctor before making any medical decisions.
