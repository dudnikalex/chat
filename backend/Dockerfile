FROM python:3.10.9

WORKDIR /usr/src/app

COPY ./backend/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY ./backend .

CMD ["./run-dev.sh"]
