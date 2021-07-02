# Speech To Text

## Requirements
- Python 3
- Instance of Azure Speech Service
- Default audio format:  
    - type: WAV
    - bitrate: 16-bit
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
python3 transcription.py
```