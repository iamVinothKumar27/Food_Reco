import os
import pyttsx3
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import google.generativeai as genai
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import LLMChain
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Google Generative AI
genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))

# Initialize embeddings


# Define the prompt template
prmt_temp = """
    You are a travel guide. Your tourist is feeling sleepy and also {emotion} around {location} at {time}. 
    They are driving a car and need some food to refresh.
    Suggest two food items for them: one vegan and one non-vegan. 
    Format the response as:
    example:
    "Hey buddy, why not a <food suggestion> at <restaurant near by> now?" or 
    "A cup of coffee would make you feel better." 

    The suggestion that you give should be catchy and make the driver feel freshened if you are suggesting two foods make it like you can choose either of these.
"""

# Initialize the Chat model
model = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0.7)

# Define the prompt with the correct input variables
prompt = PromptTemplate(template=prmt_temp, input_variables=["emotion", "location", "time"])

# Create the LLMChain with the correct document variable
llm_chain = LLMChain(llm=model, prompt=prompt)


# Define a function to get recommendations and read them aloud using Zira's voice
def get_food_recommendation(emotion: str, location: str, time: str):
    # Inputs for the LLM chain
    inputs = {
        "emotion": emotion,
        "location": location,
        "time": time
    }
    # Run the chain
    response = llm_chain.run(inputs)
    
    # Initialize the TTS engine
    engine = pyttsx3.init()
    
    # Set Microsoft Zira Desktop (Female) voice
    mac_voice_id = "com.apple.speech.synthesis.voice.Albert"  # Replace <voiceName> with your chosen voice
    engine.setProperty('voice', mac_voice_id)
    
    # Optional adjustments for speed and volume
    engine.setProperty('rate', 145)  # Speed
    engine.setProperty('volume', 1.0)  # Volume
    
    # Read aloud the recommendation
    engine.say(response)
    engine.runAndWait()
    
    return response

# Example usage
emotion = "happy"
location = "Hyderabadh"
time = "5:00 PM"
recommendation = get_food_recommendation(emotion, location, time)
print(recommendation)
