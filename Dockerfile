FROM python:3.11.1-slim-bullseye

COPY ./requirements.txt /requirements.txt
RUN pip3 install -r /requirements.txt --no-cache-dir

COPY ./utils /utils
COPY ./filter_config.json /filter_config.json
COPY ./run.py /run.py

CMD ["python", "run.py"]
