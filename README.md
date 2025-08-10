# RuneScape 3 D&D Notifier

This python module allows sending D&D alerts for various D&Ds in
RuneScape over several social media platforms.

## Setup & Execution

- Copy the `.env.example` file to the path `.env` and fill the required values.
- Create the python virtual environment:

```bash
python3 -m venv .venv

# Linux
source ./.venv/bin/activate
# Windows
./venv/Scripts/activate.ps1

# Install requirements
pip3 install -r requirements.txt --no-cache

# Run app
python3 app.py
```

This start a blocking scheduler from `APScheduler` which searches for D&D data
on a daily and hourly schedule and sends messages accordingly.

## HTML Renderer

Some modules offer an optional HTML Renderer for sending images.
To enable this, a chromium driver must be installed.

In linux, it is enough to install the chromium browser and set `CHROMIUM_EXECUTABLE_PATH=/usr/bin/chromium-browser`.

In Windows, please download a chrome demo browser from `https://googlechromelabs.github.io/chrome-for-testing` and set
the path to the downloaded folder's `chrome.exe` file. For example: `./chrome-win32/chrome.exe`.

## Current Events

| D&D Event Name          | Implemented?   |
|-------------------------|----------------|
| Rune Goldberg Machine   | Yes            |
| Wilderness Flash Events | In-Development |

More to be added soon

## Social Media Adapters

| Communication Channel | Implemented?   |
|-----------------------|----------------|
| Telegram              | Yes            |
| Discord               | In-Development |
| WhatsApp              | Planned        |
| Signal                | Maybe          |

## Collaboration

If you have any suggestions, feel free to open issues and join the development effort.
This software is meant as an open-source alternative for Alt-1 with direct notifications to one's phone.
