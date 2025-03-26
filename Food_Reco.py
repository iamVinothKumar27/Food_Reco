
from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv
import google.generativeai as genai
from gtts import gTTS
import os

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Configure Gemini model
genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
model = genai.GenerativeModel("gemini-1.5-flash")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/recommend_food', methods=['POST'])
def recommend_food():
    data = request.json
    emotion = data['emotion']
    location = data['location']
    time = data['time']

    prompt = f"""
    You are a travel guide. Your tourist is feeling sleepy and also {emotion} around {location} at {time}.
    They are driving a car and need some food to refresh.
    Suggest two food items for them: one vegan and one non-vegan.
    Format the response as:
    "Hey buddy, why not a <food suggestion> at <restaurant nearby> now?" or
    "A cup of coffee would make you feel better."
    """

    response = model.generate_content(prompt)
    recommendation = response.text.strip()

    # Convert to speech with gTTS
    tts = gTTS(recommendation, lang="en")
    audio_path = "static/voice.mp3"
    tts.save(audio_path)

    return jsonify({
        "recommendation": recommendation,
        "audio_url": "/" + audio_path
    })

if __name__ == '__main__':
    app.run(debug=True)
