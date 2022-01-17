# Speech To Text

Converts the audio of a file to text with use of Azure Cognitive Service.

<img src=https://user-images.githubusercontent.com/52599177/130236381-51f8305e-6962-4c6a-9d2f-798868f4e61b.png width="325">

## Requirements
- Python 3
- Instance of Azure Speech Service
- Recommended audio format:  
    - type: WAV
    - precision: 16-bit
    - sample rate: 8kHz or 16kHz
    - channel: Single channel (mono)

## Usage

### Install depencies
```shell
pip3 install -r requirements.txt
```

### Modify env_sample.txt
1. Add required values
2. Rename file to .env

### Run transcription
```shell
python3 src/transcription.py
```
