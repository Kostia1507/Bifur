FROM python:3.12
WORKDIR /Bifur
COPY requirements.txt /Bifur/
RUN pip install -r requirements.txt
RUN apt-get update
RUN apt-get install -y ffmpeg
COPY . /Bifur
CMD python main.py
