#import needed modules
import streamlit as st
import pathlib as path
import google.generativeai as genai
from google.generativeai import types

#configure api
try:
    # This will work when deployed to Streamlit Cloud
    api_key = st.secrets["GOOGLE_API_KEY"]
except Exception:
    # This will work on your local machine
    try:
        from api_key import api_key
    except ImportError:
        st.error("API key not found! Please set GOOGLE_API_KEY in your Streamlit secrets or create api_key.py locally.")
        st.stop()

#configure genai
genai.configure(api_key=api_key)
#set up our model
generation_configure={
    "temperature":0.4,
    "top_p":1,
    "top_k":1,
    "max_output_tokens":4096
}
#apply safety settings
safety_settings = [
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE",
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE",
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE",
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE",
    },
]
#system promt
system_prompt="""
    As a highly skilled medical practitioner specializing in image analysis, you are tasked with examining medical images for a renowed hospital. Your expertise is crucial in identifiying any anomalies, diseases, or health issue that may be present in the images.

Your Responsibilities include:
1. Detailed Analysis: Thoroughly analyze each image, focusing on identifying any abnormal findings.
2. Findings Report: Document all observed anomalies or signs of disease. Clearly articulate these findings in a structured format.
3. Recommendations and Next Steps: Based on your analysis, suggess potential next steps, including further tests or treatmets.
4. Treatment Suggestions: If appropriate, recommend possible treatment options or interventions.

Important Notes:
1. Scope of Response: Only respond if the image pertains to human health issues.
2. Clarity of Image: In cases where the image quality impedes clear analysis, note that certain aspects are 'Unable to be determined based on the provided image.'
3. Disclaimer: Accompany your analysis with the disclaimer: "Consult with Doctor before making any medical decisions."
4. Your Insight are Invaluable in guiding clinical decisions. Please proceed with the analysis, adhering to the structured approach outlined above.

Please provide me an output response with these 4 headings Detailed Analysis, Findings Report, Recommendations and Next Steps, Treatment Suggestions. And for each headings, use bold text to highlight the heading.
"""

#model configuration
model = genai.GenerativeModel("gemini-3.8-flash",
                                generation_config=generation_configure,
                                safety_settings=safety_settings)



#setup page configuration
st.set_page_config(page_title="VitalImage Analytics", page_icon="🏥", layout="wide")

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1E88E5;
        font-weight: 700;
        margin-bottom: 0;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #555555;
        margin-top: 0;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar for settings and info
with st.sidebar:
    st.image("logo.png", width=150)
    st.markdown("### ⚙️ Settings")
    # Language selection
    language = st.selectbox(
        "🌐 Report Language", 
        ["English", "Hindi", "Gujarati", "Spanish", "French"]
    )
    st.markdown("---")
    st.markdown("💡 **How it works:**\nUpload a medical image and our AI will analyze it to provide detailed findings and next steps.")
    st.markdown("⚠️ **Disclaimer:**\n*Consult with a Doctor before making any medical decisions.*")

# Main page
st.markdown('<p class="main-header">👨‍⚕️ VitalImage Analytics</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">An intelligent assistant to analyze medical images</p>', unsafe_allow_html=True)
st.markdown("---")

# Upload file
uploaded_file = st.file_uploader("📤 Upload a Medical Image (JPG, PNG, JPEG)", type=["jpg", "png", "jpeg"])

if uploaded_file:
    # Create two columns for a better UI layout (give more space to the report)
    col1, col2 = st.columns([1, 1.5])
    
    with col1:
        st.subheader("🖼️ Uploaded Image")
        st.image(uploaded_file, use_container_width=True)
        
    with col2:
        st.subheader("📋 Analysis Report")
        with st.spinner(f"Analyzing image and generating report in {language}..."):
            # Process the uploaded image
            image_data = uploaded_file.getvalue()
        
            image_parts = [
                {
                    "mime_type": uploaded_file.type,
                    "data": image_data
                }
            ]
        
            # Update the prompt with the requested language
            localized_prompt = system_prompt + f"\n\nIMPORTANT: Please generate the entire response in the {language} language."
        
            try:
                # Generate content
                response = model.generate_content([
                    image_parts[0],
                    localized_prompt
                ])
                
                st.success("✅ Analysis Complete!")
                st.write(response.text)
            except Exception as e:
                st.error(f"An error occurred while generating the report: {e}")


   
