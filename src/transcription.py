import os
import azure.cognitiveservices.speech as speechsdk
from dotenv import load_dotenv

# load .env file
load_dotenv()

SUBSCRIPTION_KEY = os.getenv("SUBSCRIPTION_KEY")
REGION = os.getenv("REGION")
INPUT_FILE_PATH = os.getenv("INPUT_FILE_PATH")
OUTPUT_FILE_PATH = os.getenv("OUTPUT_FILE_PATH")
LANGUAGE = os.getenv("LANGUAGE")

assert SUBSCRIPTION_KEY
assert REGION
assert INPUT_FILE_PATH
assert OUTPUT_FILE_PATH
assert LANGUAGE

SPEECH_CONFIG = speechsdk.SpeechConfig(
    subscription=SUBSCRIPTION_KEY,
    region=REGION
)


def from_file():
    print(f"=== Speech to text ===")
    print(f"input file: {INPUT_FILE_PATH}")
    print(f"output file: {OUTPUT_FILE_PATH}")
    print(f"recognition language: {LANGUAGE}")

    # convert speech of file to text
    audio_input = speechsdk.AudioConfig(filename=INPUT_FILE_PATH)
    SPEECH_CONFIG.speech_recognition_language = LANGUAGE
    speech_recognizer = speechsdk.SpeechRecognizer(
        speech_config=SPEECH_CONFIG,
        audio_config=audio_input
    )
    result = speech_recognizer.recognize_once_async().get()

    # check result
    if result.reason == speechsdk.ResultReason.NoMatch:
        print(f"No speech could be recognized: {result.no_match_details}")
    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = result.cancellation_details
        print(f"Speech recognition canceled: {cancellation_details}")
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            print(f"Error details: {cancellation_details.error_details}")
    else:
        return result


def print_to_file(text):
    try:
        with open(OUTPUT_FILE_PATH, "w", encoding="utf-8") as output:
            output.write(text)
    except Exception as e:
        print(f"Could not write text to file: {e}")
    else:
        print(f"Printed text to: {OUTPUT_FILE_PATH}")


# check whether the user wants to write to an existing file before starting
# with speech to text because we only 5 free audiohours per month and dont
# want to waste them
if os.path.isfile(OUTPUT_FILE_PATH):
    print(f"File already exsists: {OUTPUT_FILE_PATH}")

text = from_file()
if text:
    print_to_file(text)
