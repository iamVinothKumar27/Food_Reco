from flask import Flask, request, jsonify, render_template
import pyttsx3
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
import google.generativeai as genai
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

app = Flask(__name__)
genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))

# Define the prompt template
prompt_template = """
You are a travel guide. Your tourist is feeling sleepy and also {emotion} around {location} at {time}.
They are driving a car and need some food to refresh.
Suggest two food items for them: one vegan and one non-vegan.
Format the response as:
"Hey buddy, why not a <food suggestion> at <restaurant nearby> now?" or
"A cup of coffee would make you feel better."
"""

# Initialize the Chat model
model = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0.7)
prompt = PromptTemplate(template=prompt_template, input_variables=["emotion", "location", "time"])
llm_chain = LLMChain(llm=model, prompt=prompt)

# Initialize TTS
engine = pyttsx3.init()
mac_voice_id = "com.apple.voice.compact.fr-FR.Thomas"
engine.setProperty('voice', mac_voice_id)
engine.setProperty('rate', 145)
engine.setProperty('volume', 1.0)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/recommend_food', methods=['POST'])
def recommend_food():
    data = request.json
    emotion = data['emotion']
    location = data['location']
    time = data['time']

    # Inputs for the LLM chain
    inputs = {
        "emotion": emotion,
        "location": location,
        "time": time
    }

    # Get recommendation from AI
    recommendation = llm_chain.run(inputs)

    # Speak the recommendation
    engine.say(recommendation)
    engine.runAndWait()

    # Return recommendation as a response
    return jsonify({"recommendation": recommendation})

if __name__ == '__main__':
    app.run(debug=True)
