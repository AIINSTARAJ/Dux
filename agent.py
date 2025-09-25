import os
import time

from gtts import gTTS
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from termcolor import colored
from datetime import datetime

from elevenlabs.client import ElevenLabs
from elevenlabs.play import play
from elevenlabs import VoiceSettings

import pyttsx3

Engine = pyttsx3.init()

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"

load_dotenv()

import pygame

client = ElevenLabs(
    api_key= os.environ.get("LABS_API_KEY")
)


def speak(text, name="app", lang="en", slow=True):
    """
    Synthesize text -> Speech/{name}.mp3 and play it using pygame.
    """
    os.makedirs("Speech", exist_ok=True)

    filename = f"Speech/{name}.mp3"

    tts = gTTS(text=text, lang=lang, tld="com.au", slow=slow)
    tts.save(filename)

    try:
        pygame.mixer.init()
    except Exception:
        pass

    pygame.mixer.music.load(filename)
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        time.sleep(0.2)


def speak_(text):
    """
    Synthesize text -> Speech and play it using ELEVEN LABS.
    """
    audio = client.text_to_speech.convert(
        text=text,
        voice_id="c1uwEpPUcC16tq1udqxk",
        model_id="eleven_multilingual_v2",
        output_format="mp3_44100_128",
        voice_settings= VoiceSettings(
            stability=0.5, similarity_boost=0.6, style=0.2, use_speaker_boost=True
        )
    )

    play(audio)

def _speak(text,filename, rate=200):
    """
    Synthesize text -> Speech and play it using pyttsx3.
    """

    Engine.setProperty("rate", rate) 

    Engine.say(text)

    Engine.runAndWait()

model = os.environ.get("BASE_MODEL", "gemini-2.0-flash")

llm = ChatGoogleGenerativeAI(model=model, temperature=0.2)

Prompt = """
    You are a world-class content strategist, master storyteller, and elite voice performer with decades of experience across broadcast media, educational platforms, and entertainment industries.
    
    Mission: Architect a masterful {format} that transforms the given topic into an unforgettable auditory experience using cutting-edge narrative psychology and persuasion techniques.
    
    Core Parameters:
    - Emotional Tone: {tone} (weave this consistently through every word choice and rhythm)
    - Precise Length: exactly {length} or more sentence
    - Communication Style: {style} (completely adapt linguistic patterns, cognitive load, and cultural resonance)
    
    Advanced Architecture:
    
    OPENING MASTERY: Deploy a magnetic hook using one of these proven techniques:
    - Provocative question that challenges assumptions
    - Startling statistic or counterintuitive fact  
    - Vivid scenario that places listener in the moment
    - Bold statement that reframes their perspective
    - REFERENCES where possible
    
    CORE DEVELOPMENT: Build compelling narrative momentum through:
    - Multi-sensory examples that create mental movies
    - Unexpected analogies that bridge familiar to unfamiliar
    - Personal anecdotes or case studies that humanize concepts
    - Pattern interrupts that maintain cognitive engagement
    
    CLOSING IMPACT: Deliver a crystalline takeaway that:
    - Provides immediate, actionable next steps
    - Creates lasting behavioral change potential
    - Leaves them with quotable wisdom they'll remember and share
    
    Technical Excellence Standards:
    - Engineer for pure audio consumption with natural speech cadence
    - Dont include things like Pause, *, or anything the model will misinterpret as words.
    - Embed strategic micro-pauses and emphasis anchors
    - Eliminate all text-based formatting and structural artifacts  
    - Create seamless thought-to-thought bridges using transitional mastery
    - Calibrate complexity, references, and assumptions to match specified style perfectly
    - Use sensory-rich language that activates multiple learning channels
    - Incorporate subtle repetition and callback techniques for memory retention
    - It is going to be printed in the CLI, so optimize the output structure

    NOTE: 
    - Don't make it too robotic
    - Ensure it reflects human style of writing
    - Nothing like * in text
    
    Topic Focus: {topic}
"""

def generate_content(topic: str, tone: str = "Friendly", length: int = 12, fmt: str = "advanced content", style: str = "casual") -> str:
    """
    AI Integration
    """
    prompt = Prompt.format(format=fmt,
                            tone=tone, 
                            length=length, 
                            style=style, 
                            topic=topic
                        )
    
    response = llm.invoke(prompt)

    text = getattr(response, "content", None)

    if text is None:
        text = str(response)

    return text.strip()


def main_loop():

    print(colored("vTTS 💎💎💎. Type 'exit' to quit.","cyan",attrs=["bold"]))

    while True:

        topic = input("\nEnter topic: ").strip()
        if not topic or topic.lower() in ("exit", "quit"):
            break

        tone = input("Tone: ").strip() or "friendly"
        style = input("Style: ").strip() or "casual"

        try:
            length = int(input("Approx sentences (8-∞): ").strip() or 8)
        except ValueError:
            length = 8

        print(colored("\n⚡ Generating content... please wait ⚡", "cyan", attrs=["bold"]))

        try:
            content = generate_content(topic=topic, tone=tone, length=length, fmt="Advanced spoken content", style=style)
        except Exception as e:
            print(colored(f"❌ Generation failed: {e}", "red", attrs=["bold"]))
            continue

        print(colored(f"AI: {content}", "white"))
        print(colored("\n🔊 Speaking now...", "green", attrs=["bold"]))

        safe_name = "".join(c if c.isalnum() else "_" for c in "_".join(topic.split()))[:40]

        filename = f"{safe_name}_{datetime.now().strftime('%Y-%m-%d_%H-%M')}"
        
        _speak(content,filename)

        print(colored("🔊 TTS complete.", "green", attrs=["bold"]))

if __name__ == "__main__":
    main_loop()