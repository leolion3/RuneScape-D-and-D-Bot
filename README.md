
# RuneScape 3 D&D Notifier

This python module allows sending D&D alerts for various D&Ds in
RuneScape over several social media platforms.

## Setup (Docker-Compose)

- Download the [`docker-compose.yml`](https://raw.githubusercontent.com/leolion3/RuneScape-D-and-D-Bot/refs/heads/main/docker-compose.yml) file.
- Download the [`.env.example`](https://raw.githubusercontent.com/leolion3/RuneScape-D-and-D-Bot/refs/heads/main/.env.example) file and rename it to `.env`
- Adjust the parameters as necessary (see more below). **Ignore the chromium browser path** - this gets set automatically.
- Pull the docker image:

```bash
docker pull ghcr.io/leolion3/runescape-d-and-d-bot:latest
```

- Start the Application with docker compose::

```bash
sudo docker compose up --build -d
```

## Setup & Execution (Python3 + Virtual Env)

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

| D&D Event Name (Link)   | Implemented? |
|-------------------------|--------------|
| [Rune Goldberg Machine](https://github.com/leolion3/RuneScape-D-and-D-Bot/tree/main/daily_dnds/rune_goldberg)   | Yes          |
| [Wilderness Flash Events](https://github.com/leolion3/RuneScape-D-and-D-Bot/tree/main/hourly_dnds/wilderness_flash_events) | Yes          |

More to be added soon

## Social Media Adapters

| Communication Channel | Implemented?   |
|-----------------------|----------------|
| Telegram              | Yes            |
| Discord               | In-Development |
| WhatsApp              | Not yet        |
| Signal                | Maybe          |

## Collaboration

If you have any suggestions, feel free to open issues and join the development effort.
This software is meant as an open-source alternative for Alt-1 with direct notifications to one's phone.
