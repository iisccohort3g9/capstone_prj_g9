# pull python base image
FROM python:3.10

RUN apt-get -y update
RUN apt-get -y upgrade
RUN apt-get install -y ffmpeg

ADD requirements.txt requirements.txt

# update pip
RUN pip install --upgrade pip

# install dependencies
RUN pip install -r requirements.txt


# copy application files
COPY app/. app/.

RUN python -m spacy download en_core_web_sm
COPY input_video.mp4 input_video.mp4
COPY front-end/. front-end/.


RUN git clone https://github.com/iisccohort3g9/Wav2Lip.git

# Move the cloned repository to the desired directory
RUN mv Wav2Lip app/Wav2Lip

RUN pip install -r app/Wav2Lip/requirements.txt

# expose port for application
EXPOSE 8001
EXPOSE 8080
EXPOSE 7860
EXPOSE 9091


# start fastapi application
CMD ["python", "app/api.py", ";", "python", "front-end/app.py", ";", "python", "app/clearml_exporter.py"]