FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Set this to your local timezone
ENV TZ=Europe/Berlin
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

WORKDIR /app
COPY requirements.txt config.py ./

# System deps for Chromium - Required for Html2Img
RUN set -eux; \
  apt-get update; \
  apt-get install -y --no-install-recommends \
    chromium \
    chromium-driver \
    fonts-liberation \
    libasound2 \
    libatk-bridge2.0-0 \
    libatk1.0-0 \
    libcups2 \
    libdbus-1-3 \
    libgdk-pixbuf-2.0-0 \
    libnspr4 \
    libnss3 \
    libx11-xcb1 \
    libxcomposite1 \
    libxdamage1 \
    libxrandr2 \
    libxss1 \
    libxtst6 \
    libayatana-appindicator3-1 \
    libu2f-udev \
    libvulkan1 \
    libxshmfence1 \
    xdg-utils; \
  rm -rf /var/lib/apt/lists/*

RUN ln -s /usr/bin/chromium /usr/bin/chromium-browser

RUN pip install --no-cache-dir -r requirements.txt
COPY . .

ENV CHROMIUM_EXECUTABLE_PATH=/usr/bin/chromium-browser
CMD ["python", "app.py"]
