import os
import time

from gtts import gTTS
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from termcolor import colored

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

PROMPT_TEMPLATE = """
    You are a helpful creative assistant and voice actor.
    Task: Produce a {format} about the topic below.
    Constraints:
    - Tone: {tone} (e.g. friendly, serious, excited, calm)
    - Length: approx {length} sentences
    - Add one short opening line (1 sentence) that hooks the listener.
    - Add 1–2 short examples or metaphors to illustrate the idea (keep them concise).
    - End with a single-sentence actionable takeaway.
    Do NOT include any markup or section headers — produce continuous spoken-style text.

    Topic: {topic}
"""

def generate_content(topic: str, tone: str = "friendly", length: int = 3, fmt: str = "short paragraph") -> str:
    """
    Create the filled prompt, invoke Gemini and return text content.
    """
    prompt = PROMPT_TEMPLATE.format(format=fmt, tone=tone, length=length, topic=topic)
    response = llm.invoke(prompt)

    text = getattr(response, "content", None)

    if text is None:
        text = str(response)

    return text.strip()


def main_loop():
    colored("vTTS 💎💎💎. Type 'exit' to quit.","blue",attrs=["bold"])

    while True:

        topic = input("\nEnter topic: ").strip()
        if not topic or topic.lower() in ("exit", "quit"):
            break

        tone = input("Tone (friendly/serious/excited/calm) [friendly]: ").strip() or "friendly"
        try:
            length = int(input("Approx sentences (1-8) [3]: ").strip() or 3)
        except ValueError:
            length = 3

        print("\nGenerating... (this may take a second)")
        try:
            content = generate_content(topic=topic, tone=tone, length=length, fmt="spoken paragraph")
        except Exception as e:
            print("Generation failed:", e)
            continue

        print("\n--- GENERATED TEXT ---\n")
        print(content)
        print("\nSpeaking now...")

        safe_name = "".join(c if c.isalnum() else "_" for c in topic)[:40]

        speak(content, name=f"{safe_name}_{int(time.time())}")
        
        print("Done speaking.")

if __name__ == "__main__":
    main_loop()
