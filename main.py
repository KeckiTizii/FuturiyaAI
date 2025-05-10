import os
import asyncio
import edge_tts
import speech_recognition as sr

from g4f.client import AsyncClient
from g4f.Provider.PollinationsAI import PollinationsAI
from mss import mss
from colorama import Style, Fore
from pydub import AudioSegment, playback

r = sr.Recognizer()
m = sr.Microphone()

messages_log=[]

OUTPUT_EDGE_TTS = "audio/futuriya-edge.wav"
VOICE = "vi-VN-HoaiMyNeural"
    
async def edgetts(response_message):
    communicate = edge_tts.Communicate(response_message, VOICE, rate = "+50%")
    await communicate.save(OUTPUT_EDGE_TTS)

async def chat():
    response_message = ""
    client = AsyncClient(provider=PollinationsAI)

    try:
        if "màn hình" in speech:
            with mss() as sct:
                sct.shot(output='screenshot/screenshot.png')

            with open("screenshot/screenshot.png", "rb") as image:
                stream = client.chat.completions.stream(
                    model="openai",
                    messages=messages_log,
                    image=image
                )
                async for chunk in stream:
                    if chunk.choices and chunk.choices[0].delta.content:
                        response_message += chunk.choices[0].delta.content
        else:
            stream = client.chat.completions.stream(
                model="openai",
                messages=messages_log,
            )
            async for chunk in stream:
                if chunk.choices and chunk.choices[0].delta.content:
                    response_message += chunk.choices[0].delta.content

    except Exception as e:
        response_message = f"Error in streaming"
        print("Error in streaming:", e)

    await edgetts(response_message)
    print(f'Futuriya: {response_message}')
    try:
        PLAY_EDGE_TTS = AudioSegment.from_file(OUTPUT_EDGE_TTS)
        playback.play(PLAY_EDGE_TTS)
    except Exception as e:
        print("Error while trying play sound", e)

def starting():
    cl = lambda: os.system('cls')
    cl()
    print(Fore.RESET + Style.BRIGHT +"""
███████╗██╗   ██╗████████╗██╗   ██╗██████╗ ██╗██╗   ██╗ █████╗     ██████╗ ██████╗  ██████╗      ██╗███████╗ ██████╗████████╗
██╔════╝██║   ██║╚══██╔══╝██║   ██║██╔══██╗██║╚██╗ ██╔╝██╔══██╗    ██╔══██╗██╔══██╗██╔═══██╗     ██║██╔════╝██╔════╝╚══██╔══╝
█████╗  ██║   ██║   ██║   ██║   ██║██████╔╝██║ ╚████╔╝ ███████║    ██████╔╝██████╔╝██║   ██║     ██║█████╗  ██║        ██║   
██╔══╝  ██║   ██║   ██║   ██║   ██║██╔══██╗██║  ╚██╔╝  ██╔══██║    ██╔═══╝ ██╔══██╗██║   ██║██   ██║██╔══╝  ██║        ██║   
██║     ╚██████╔╝   ██║   ╚██████╔╝██║  ██║██║   ██║   ██║  ██║    ██║     ██║  ██║╚██████╔╝╚█████╔╝███████╗╚██████╗   ██║   
╚═╝      ╚═════╝    ╚═╝    ╚═════╝ ╚═╝  ╚═╝╚═╝   ╚═╝   ╚═╝  ╚═╝    ╚═╝     ╚═╝  ╚═╝ ╚═════╝  ╚════╝ ╚══════╝ ╚═════╝   ╚═╝   
                                                                                                                             
""")
    print(Fore.RESET + Style.BRIGHT + "              By: KenkiTizi")


try:
    starting()
    print(Style.RESET_ALL + "A moment of silence, please...")
    with m as source: r.adjust_for_ambient_noise(source)
    print("Set minimum energy threshold to {}".format(r.energy_threshold))
    while True:
        print("Say something!")
        with m as source: audio = r.listen(source)
        print("Got it! Now to recognize it...")
        try:
            global speech
            speech = r.recognize_google(audio, language="vi-VN", show_all= False)
            messages_log.append({"role": "user", "content": speech})
            print("You: {}".format(speech))
            asyncio.run(chat())
        except sr.UnknownValueError:
            print("Oops! Didn't catch that")
        except sr.RequestError as e:
            print("Uh oh! Couldn't request results from Google Speech Recognition service; {0}".format(e))
except KeyboardInterrupt:
    print('Closing Futuriya... \n Thanks For Using.')
