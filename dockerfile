FROM python:alpine
COPY . /
RUN pip install flask
RUN pip install flask_sqlalchemy
CMD /bin/sh ./autohold.sh
ENV FLASK_APP=/app/run.py
ENTRYPOINT flask run --host=0.0.0.0

