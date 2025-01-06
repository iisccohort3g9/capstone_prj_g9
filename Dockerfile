# pull python base image
FROM python:3.10

ADD requirements.txt requirements.txt


# update pip
RUN pip install --upgrade pip

# install dependencies
RUN pip install -r requirements.txt

# copy application files
COPY app/. app/.
COPY input_video.mp4 input_video.mp4

RUN git clone https://github.com/iisccohort3g9/Wav2Lip.git

# Move the cloned repository to the desired directory
RUN mv Wav2Lip app/Wav2Lip

RUN pip install -r app/Wav2Lip/requirements.txt

# expose port for application
EXPOSE 8001

# start fastapi application
CMD ["python", "app/api.py"]