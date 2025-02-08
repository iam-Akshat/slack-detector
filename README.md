# slack-detector
(Warning : The code is badly written and needs to be cleaned up)
A productivity monitoring tool that helps you stay focused by detecting when you might be slacking off. It uses screen monitoring and AI-powered analysis to provide real-time feedback on your work habits.

## Features

- Real-time screen monitoring
- AI-powered slack detection using Google's Gemini model
- Visual and audio alerts when slacking is detected
- Intelligent screenshot comparison to reduce unnecessary AI calls
- Multi-monitor support

## Prerequisites

- Python 3.8 or higher
- Google Gemini API key

## Installation

1. Clone the repository:
```bash
git clone git@github.com:iam-Akshat/slack-detector.git
cd slack-detector
```

2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

3. Set up your Gemini API key:
```bash
export GEMINI_API_KEY="your-api-key-here"
```

## Required Files

- `alert.mp3`: An audio file that plays when slacking is detected
- `alert.jpg`: An image to display when slacking is detected

Place these files in the project root directory.

## Usage

Run the main script:
```bash
python main.py
```

The program will:
1. Monitor your screen activity
2. Take periodic screenshots
3. Use AI to analyze if you're working or slacking
4. Show alerts if you're detected to be slacking

## How it Works

1. The program captures screenshots of your monitors every 5 seconds
2. It compares new screenshots with previous ones using structural similarity (SSIM)
3. If significant changes are detected, the screenshot is analyzed by Gemini AI
4. If slacking is detected, visual and audio alerts are triggered

## Configuration

The program uses several thresholds that can be modified in the code:
- Screenshot interval: 5 seconds (adjustable in `main.py`)
- Similarity threshold: 0.9 (adjustable in `main.py`)
