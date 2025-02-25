FROM alpine:latest
RUN apk add --no-cache --update ffmpeg py3-numpy py3-pillow py3-psycopg2 py3-lxml libwebp libwebp-dev libffi libffi-dev libc-dev gcc libxslt-dev neofetch libjpeg-turbo-dev git python3 python3-dev sqlite chromium chromium-chromedriver py3-pip bash postgresql-dev musl-dev postgresql
RUN git clone https://github.com/vusalold/OldUserBot /root/OldUserBot
RUN mkdir /root/OldUserBot/bin/
WORKDIR /root/OldUserBot/
COPY ./sample_config.env ./userbot.session* ./config.env* /root/OldUserBot/
ENV TZ=Europe/Azerbaijan
RUN pip3 install wheel
RUN pip3 install -r requirements.txt
CMD ["python3","main.py"]