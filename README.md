# Speech To Text

Converts the audio of a file to text with use of Azure Cognitive Service.

<img src=https://user-images.githubusercontent.com/52599177/130236381-51f8305e-6962-4c6a-9d2f-798868f4e61b.png width="325">

## Requirements
- Python 3
- Instance of Azure Speech Service
- Recommended audio format:  
    - type: WAV (required)
    - precision: 16-bit
    - sample rate: 8kHz or 16kHz
    - channel: mono

## Getting started

### Azure Cognitive Services

This script uses the Azure Speech service which provides an API to transcribe audible speech into readable, searchable text. Therefore, it is
necessary to create an instance of that if you don't have one. Then, in order to give the script access to your Speech service, you have to pass your
subscription key and the region of the instance.

Infos on how to create a free instance of Azure Speech (5 audio hours per month) and how to get the subscription key and region can be found
[here](https://docs.microsoft.com/en-us/azure/cognitive-services/speech-service/overview).

### Prepare the audio

The default audio format for the recognition to work is WAV (16 kHz or 8 kHz, 16-bit, and mono PCM). You can easily convert your audio
[here](https://online-audio-converter.com/).

### Install the dependencies

Create a virutal environment for installing the dependencies:
```shell
python3 -m venv venv
```

Activate the virtual environment:
```shell
source venv/bin/activate  # On Linux
./venv/Scripts/activate  # On Windows
```

Install the dependencies:
```shell
pip install -r requirements.txt
```

### Provide your configuration

As mentioned above, for the script to work, you have to provide the subscription key and the region of your Azure Speech instance. Also you have to
specify the path of your audio file and the path of your output file (which has to be a .txt).

1. Add all required values into the env_sample.txt file
2. Rename the file to .env

### Run transcription
```shell
python3 src/transcription.py
```
