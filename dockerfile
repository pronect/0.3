FROM python:alpine
COPY . /
RUN pip install flask
ENTRYPOINT python app/run.py
