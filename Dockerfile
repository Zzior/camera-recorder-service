FROM python:3.11-bookworm

WORKDIR /usr/src/video_bot

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python", "/usr/src/video_bot/src/bot/main.py"]
 
