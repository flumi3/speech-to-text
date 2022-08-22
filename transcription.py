import os
import sys
import time
import azure.cognitiveservices.speech as speechsdk
from dotenv import load_dotenv

load_dotenv()

# colors for colored output
BLUE = '\033[94m'
RED = '\033[91m'
GREEN = '\033[92m'
ENDC = '\033[0m'

API_KEY = os.getenv("API_KEY")
REGION = os.getenv("REGION")
INPUT_FILE_PATH = os.getenv("INPUT_FILE_PATH")
OUTPUT_FILE_PATH = os.getenv("OUTPUT_FILE_PATH")
LANGUAGE = os.getenv("LANGUAGE")


def check_config() -> None:
    print("Checking configuration ...")
    try:
        assert API_KEY
        assert REGION
        assert INPUT_FILE_PATH
        assert OUTPUT_FILE_PATH
        assert LANGUAGE
    except AssertionError:
        print(RED + f"Missing configuration parameter. Please check env file" + ENDC)
        sys.exit(1)

    # check whether the user wants to write to an existing file before starting with speech to text
    # because we only have five free audio hours per month and dont want to waste them
    if os.path.isfile(OUTPUT_FILE_PATH):
        print(RED + f"Specified output file already exists: {OUTPUT_FILE_PATH}" + ENDC)
        sys.exit(1)


def setup_speech_recognizer() -> speechsdk.SpeechRecognizer:
    print("Setting up speech recognition ...")
    try:
        speech_config = speechsdk.SpeechConfig(
            subscription=API_KEY,
            region=REGION,
            speech_recognition_language=LANGUAGE
        )
        audio_config = speechsdk.AudioConfig(filename=INPUT_FILE_PATH)
        speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)
    except Exception as e:
        print(RED + "Could not setup speech service" + ENDC)
        print(e)
        sys.exit(1)
    else:
        return speech_recognizer


def recognize(speech_recognizer: speechsdk.SpeechRecognizer) -> list:
    print("Starting speech recognition ...\n")
    done = False
    all_results = list()

    def stop_cb(evt):
        speech_recognizer.stop_continuous_recognition()
        nonlocal done
        done = True

        if evt.result.reason == speechsdk.ResultReason.Canceled:
            cancellation_details = evt.result.cancellation_details
            cancellation_reason = cancellation_details.reason
            print()
            if cancellation_reason == speechsdk.CancellationReason.Error:
                print(RED + "=== ERROR ===" + ENDC)
                print(f"Error code: {cancellation_details.error_code}")
                print(f"Error details: {cancellation_details.error_details}")
            elif cancellation_reason == speechsdk.CancellationReason.CancelledByUser:
                print(RED + "=== CANCELED BY USER ===" + ENDC)
            elif cancellation_reason == speechsdk.CancellationReason.EndOfStream:
                print(GREEN + "=== SUCCESS ===" + ENDC)

    def handle_final_result(evt):
        nonlocal all_results
        all_results.append(evt.result.text)

    # connect callbacks to the events fired by the speech recognizer
    speech_recognizer.recognized.connect(handle_final_result)
    speech_recognizer.recognizing.connect(lambda evt: print(f"RECOGNIZING: {evt}"))
    speech_recognizer.recognized.connect(lambda evt: print(f"RECOGNIZED: {evt}"))
    speech_recognizer.session_started.connect(lambda evt: print(f"SESSION STARTED: {evt}"))
    speech_recognizer.session_stopped.connect(lambda evt: print(f"SESSION STOPPED: {evt}"))
    speech_recognizer.canceled.connect(lambda evt: print(f"CANCELED: {evt}"))

    # stop continuous recognition on either session stopped or canceled events
    speech_recognizer.session_stopped.connect(stop_cb)
    speech_recognizer.canceled.connect(stop_cb)

    # start continuous speech recognition
    speech_recognizer.start_continuous_recognition()
    while not done:
        time.sleep(5)

    return all_results


def print_to_file(text_results: "list[str]") -> None:
    try:
        with open(OUTPUT_FILE_PATH, "w", encoding="utf-8") as output:
            for result in text_results:
                output.write(result + "\n")
    except Exception as e:
        print(RED + f"Could not write text into {OUTPUT_FILE_PATH}" + ENDC)
        print(e)
    else:
        print(f"Printed text to {OUTPUT_FILE_PATH}")


def main():
    check_config()
    speech_recognizer = setup_speech_recognizer()
    text_results = recognize(speech_recognizer)
    print_to_file(text_results)

    
if __name__ == "__main__":
    main()
