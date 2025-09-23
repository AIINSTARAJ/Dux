from gtts import gTTS

import os
import sys

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"

import pygame
import time


def speak(text, name="app", lang="en", slow=False):

    tts = gTTS(text=text, lang=lang, slow=slow)

    filename = f"Speech/{name}.mp3"
    tts.save(filename)

    pygame.mixer.init()
    pygame.mixer.music.load(filename)
    pygame.mixer.music.play()


    while pygame.mixer.music.get_busy():
        time.sleep(0.5)

    sys.stderr = sys.__stderr__

content = "Hello! This is a simple text to speech demo using gTTS."
speak(content)

speak("Bonjour, je m'appelle Instaraj.", lang="fr", name="3")
speak("Reading slowly for clarity.", slow=True, name="4")

speak("I love you, Instaraj.", name="5")
