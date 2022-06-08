# Speech To Text

This simple python project lets you convert the audio of a file into searchable text by using cloud computing resources from Azure Cognitive Services.

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

### Setup the Azure Speech service

1. Create free [Azure Subscripition](https://azure.microsoft.com/de-de/free/cognitive-services/)
2. Create free instance of [Speech service](https://ms.portal.azure.com/#create/Microsoft.CognitiveServicesSpeechServices) (5 audio hours per month) 

### Prepare the audio

The default audio format for the recognition to work is WAV (16 kHz or 8 kHz, 16-bit, and mono PCM). You can convert your audio
with this [Online Audio Converter](https://online-audio-converter.com/).

### Setup the environment

1. Create virutal environment for installing the dependencies
    ```shell
    python3 -m venv venv
    ```

2. Activate virtual environment
    ```shell
    # Linux
    source venv/bin/activate

    # Windows
    ./venv/Scripts/activate
    ```

3. Install dependencies
    ```shell
    pip install -r requirements.txt
    ```

### Provide your configuration

1. Get the API key and the region of your Speech service resource
    - <img src=https://user-images.githubusercontent.com/52599177/172724399-13edeae6-7a34-4327-b9b5-2acb538b83c7.png width=240>
3. Enter key and location into *./src/env_sample.txt*
4. Enter path and language of your audio input file into *./src/env_sample.txt*
5. Rename the file to *.env*

### Run the transcription
```shell
python3 src/transcription.py
```
