import os
import sys
import time
import azure.cognitiveservices.speech as speechsdk
from dotenv import load_dotenv

load_dotenv()

SUBSCRIPTION_KEY = os.getenv("SUBSCRIPTION_KEY")
REGION = os.getenv("REGION")
INPUT_FILE_PATH = os.getenv("INPUT_FILE_PATH")
OUTPUT_FILE_PATH = os.getenv("OUTPUT_FILE_PATH")
LANGUAGE = os.getenv("TRANSCRIPTION_LANGUAGE")

assert SUBSCRIPTION_KEY
assert REGION
assert INPUT_FILE_PATH
assert OUTPUT_FILE_PATH
assert LANGUAGE

SPEECH_CONFIG = speechsdk.SpeechConfig(
    subscription=SUBSCRIPTION_KEY,
    region=REGION,
    speech_recognition_language=LANGUAGE
)


def continuous_recognition_from_file():
    print("=== Speech to text ===")
    print(f"input file: {INPUT_FILE_PATH}")
    print(f"output file: {OUTPUT_FILE_PATH}")
    print(f"recognition language: {LANGUAGE}\n")

    # convert speech of file to text
    audio_config = speechsdk.AudioConfig(filename=INPUT_FILE_PATH)  
    speech_recognizer = speechsdk.SpeechRecognizer(
        speech_config=SPEECH_CONFIG,
        audio_config=audio_config
    )

    done = False

    def stop_cb(evt):
        print(f"Stopping continuous speech recognition on {evt}")
        speech_recognizer.stop_continuous_recognition()
        nonlocal done
        done = True

    all_results = list()

    def handle_final_result(evt):
        nonlocal all_results
        all_results.append(evt.result.text)

    # Connect callbacks to the events fired by the speech recognizer
    speech_recognizer.recognized.connect(handle_final_result)
    speech_recognizer.recognizing.connect(lambda evt: print(f"RECOGNIZING: {evt}"))
    speech_recognizer.recognized.connect(lambda evt: print(f"RECOGNIZED: {evt}"))
    speech_recognizer.session_started.connect(lambda evt: print(f"SESSION STARTED: {evt}"))
    speech_recognizer.session_stopped.connect(lambda evt: print(f"SESSION STOPPED: {evt}"))
    speech_recognizer.canceled.connect(lambda evt: print("CANCELED: {evt}"))

    # stop continuous recognition on either session stopped or canceled events
    speech_recognizer.session_stopped.connect(stop_cb)
    speech_recognizer.canceled.connect(stop_cb)

    # start continuous speech recognition
    speech_recognizer.start_continuous_recognition()
    while not done:
        time.sleep(5)

    return all_results


def print_to_file(text_results):
    try:
        with open(OUTPUT_FILE_PATH, "w", encoding="utf-8") as output:
            for result in text_results:
                output.write(result + "\n")
    except Exception as e:
        print(f"Could not write text to file: {e}")
    else:
        print(f"Printed text to: {OUTPUT_FILE_PATH}")


# check whether the user wants to write to an existing file before starting
# with speech to text because we only have five free audiohours per month and
# dont want to waste them
if os.path.isfile(OUTPUT_FILE_PATH):
    print(f"Output file already exsists: {OUTPUT_FILE_PATH}")
    sys.exit(1)

text_results = continuous_recognition_from_file()
if text_results:
    print_to_file(text_results)
