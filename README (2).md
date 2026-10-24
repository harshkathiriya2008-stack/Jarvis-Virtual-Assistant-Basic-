# Jarvis - Python Voice Assistant

A simple voice assistant for Windows built with Python. Speak a command and Jarvis will answer or perform the task.

## Features

- Greets you based on the time of day
- Searches Wikipedia and reads out the summary
- Opens YouTube, Google and Stack Overflow
- Plays music from a folder
- Tells the current time
- Opens VS Code
- Sends email to saved contacts using your voice
- Exit with "exit", "stop" or "bye"

## Requirements

- Windows 10/11
- Python 3.10 - 3.12 (3.11 recommended)
- A working microphone and internet connection

## Installation

```bash
# 1. Create a virtual environment
py -3.11 -m venv jarvis_env
jarvis_env\Scripts\activate

# 2. Upgrade tools
python -m pip install --upgrade pip setuptools wheel

# 3. Install modules
pip install pyaudio pyttsx3 SpeechRecognition wikipedia
```

Test your microphone:

```bash
python -m speech_recognition
```

## PyAudio Error Fix

If `pip install pyaudio` fails:

1. Check `python --version`. Python 3.13+ has no ready PyAudio wheel, so install Python 3.11.
2. Try pipwin:
   ```bash
   pip install pipwin
   pipwin install pyaudio
   ```
3. Or download the matching `.whl` file (for example `cp311` + `win_amd64`) and run:
   ```bash
   pip install PyAudio-0.2.14-cp311-cp311-win_amd64.whl
   ```

## Configuration

Open `jarvis.py` and edit the settings at the top:

```python
MUSIC_DIR = r"D:\Non Critical\songs\Favorite Songs2"
VSCODE_PATH = r"C:\Users\Haris\AppData\Local\Programs\Microsoft VS Code\Code.exe"
CONTACTS = {
    "harry": "harryyourEmail@gmail.com",
}
```

### Email setup

Gmail needs an **App Password** (not your normal password):

1. Google Account -> Security -> turn on 2-Step Verification
2. Create an App Password
3. Set environment variables, then reopen the terminal:

```bash
setx JARVIS_EMAIL "youremail@gmail.com"
setx JARVIS_APP_PASSWORD "your-16-char-app-password"
```

## Run

```bash
python jarvis.py
```

## Voice Commands

| Say | Action |
|-----|--------|
| "Wikipedia Python" | Reads a 2-line summary |
| "Open YouTube" | Opens YouTube |
| "Open Google" | Opens Google |
| "Open Stack Overflow" | Opens Stack Overflow |
| "Play music" | Plays the first song in your music folder |
| "What is the time" | Speaks the current time |
| "Open code" | Opens VS Code |
| "Email to Harry" | Records a message and sends it |
| "Exit" / "Stop" / "Bye" | Closes Jarvis |

## Build an .exe (optional)

```bash
pip install pyinstaller
pyinstaller --onefile jarvis.py
```

The executable will be in the `dist` folder.

## Troubleshooting

| Problem | Solution |
|---------|----------|
| PyAudio install error | Use Python 3.11 (see above) |
| "Say that again please..." | Speak clearly, check microphone and internet |
| Email not sending | Use a Gmail App Password and set the environment variables |
| Music/VS Code not opening | Fix the paths in the config section |
| `sapi5` error | `pyttsx3` with `sapi5` works only on Windows |

## Notes

- Speech recognition uses Google's online service, so internet is required.
- `os.startfile` and `sapi5` are Windows-only.
