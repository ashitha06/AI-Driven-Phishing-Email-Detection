import streamlit as st
import joblib
import re
import string
import nltk
from datetime import datetime
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

# Load model and vectorizer
model = joblib.load("model/phishing_model.pkl")
vectorizer = joblib.load("model/tfidf_vectorizer.pkl")

# Download NLTK resources
nltk.download("stopwords")
nltk.download("wordnet")

stop_words = set(stopwords.words("english"))
lemmatizer = WordNetLemmatizer()

# Text preprocessing function
def clean_text(text):
    text = text.lower()
    text = re.sub(r"http\S+|www\S+", "", text)
    text = re.sub(r"<.*?>", "", text)
    text = re.sub(r"\d+", "", text)
    text = text.translate(str.maketrans("", "", string.punctuation))
    words = text.split()
    words = [lemmatizer.lemmatize(word) for word in words if word not in stop_words]
    return " ".join(words)

# Streamlit UI
st.set_page_config(
    page_title="AI Phishing Detection",
    page_icon="📧",
    layout="centered"
)

st.title("📧 AI-Driven Phishing Email Detection")
st.write("Enter an email below to check whether it is **Safe** or **Phishing**.")
st.markdown("""
**Example emails**

🔴 Phishing:
> Verify your account immediately by clicking this link.

🟢 Safe:
> Your electricity bill has been generated successfully.
""")
# Sidebar

st.sidebar.title("📌 About")

st.sidebar.success("🟢 Model Status: Ready")

st.sidebar.markdown("""
### Project Information

**Model:** MLP Classifier

**Vectorizer:** TF-IDF

**Accuracy:** 96.81%

**Dataset:** Phishing Email Dataset
""")


email = st.text_area("Email Text")

st.caption("⚠️ Predictions are generated using a machine learning model and should be used as a decision-support tool, not as the sole basis for security decisions.")


predict = st.button("Predict")


if predict:

    clean_email = clean_text(email)
    email_vector = vectorizer.transform([clean_email])

    with st.spinner("🔍 Analyzing email...Please wait..."):
        prediction = model.predict(email_vector)

    probability = model.predict_proba(email_vector)[0]
    confidence = max(probability) * 100

    if prediction[0] == 1:
     st.error("🚨 Phishing Email")
     st.info(f"📊 Confidence: {confidence:.2f}%")
    else:
     st.success("✅ Safe Email")
     st.info(f"📊 Confidence: {confidence:.2f}%")
    st.caption(f"🕒 Prediction Time: {datetime.now().strftime('%d-%m-%Y %I:%M:%S %p')}") 
    st.markdown("### 📊 Email Statistics")
    st.write(f"**Characters:** {len(email)}")
    st.write(f"**Words:** {len(email.split())}")

with st.expander("ℹ️ How does this application work?"):
    st.write("""
1. The email is cleaned using NLP preprocessing.
2. TF-IDF converts the text into numerical features.
3. A trained MLP Neural Network analyzes the email.
4. The model predicts whether the email is Safe or Phishing.
5. The confidence score indicates how certain the model is.
""")
st.markdown("---")
st.caption("AI-Driven Phishing Email Detection | IICT Summer Internship Project")
