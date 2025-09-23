import os
import time

from gtts import gTTS
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from termcolor import colored
from datetime import datetime

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"

load_dotenv()

import pygame


def speak(text, name="app", lang="en", slow=False):
    """
    Synthesize text -> Speech/{name}.mp3 and play it using pygame.
    """
    os.makedirs("Speech", exist_ok=True)

    filename = f"Speech/{name}.mp3"

    tts = gTTS(text=text, lang=lang, slow=slow)
    tts.save(filename)

    try:
        pygame.mixer.init()
    except Exception:
        pass

    pygame.mixer.music.load(filename)
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        time.sleep(0.2)



model = os.environ.get("BASE_MODEL", "gemini-1.5-flash")

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
    - Embed strategic micro-pauses and emphasis anchors
    - Eliminate all text-based formatting and structural artifacts  
    - Create seamless thought-to-thought bridges using transitional mastery
    - Calibrate complexity, references, and assumptions to match specified style perfectly
    - Use sensory-rich language that activates multiple learning channels
    - Incorporate subtle repetition and callback techniques for memory retention
    
    Topic Focus: {topic}
"""

def generate_content(topic: str, tone: str = "friendly", length: int = 12, fmt: str = "advanced content", style: str = "casual") -> str:
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

    print(colored("vTTS 💎💎💎. Type 'exit' to quit.","blue",attrs=["bold"]))

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
            content = generate_content(topic=topic, tone=tone, length=length, fmt="advanced spoken content", style=style)
        except Exception as e:
            print(colored(f"❌ Generation failed: {e}", "red", attrs=["bold"]))
            continue

        print(colored(f"AI: {content}", "white"))
        print(colored("\n🔊 Speaking now...", "green", attrs=["bold"]))

        safe_name = "".join(c if c.isalnum() else "_" for c in "_".join(topic.split()))[:40]

        filename = f"{safe_name}_{datetime.now().strftime('%Y-%m-%d_%H-%M')}"
        speak(content, name=filename)

        print(colored("🔊 TTS complete.", "green", attrs=["bold"]))

if __name__ == "__main__":
    main_loop()