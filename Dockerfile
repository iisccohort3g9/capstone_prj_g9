# pull python base image
FROM python:3.10

RUN apt-get update && apt-get install -y ffmpeg


# copy application files
COPY app/. app/.
COPY input_video.mp4 input_video.mp4
COPY front-end/. front-end/.
ADD requirements.txt requirements.txt
ADD clearml.conf /root/clearml.conf
# RUN git clone https://github.com/iisccohort3g9/Wav2Lip.git
COPY Wav2Lip/. Wav2Lip/.

# update pip
RUN pip install --upgrade pip
# install dependencies
RUN pip install -r requirements.txt
RUN pip install -r Wav2Lip/requirements.txt
# RUN chmod +x /app/install_models.sh
RUN python -m spacy download en_core_web_sm
RUN mkdir -p /tmp/gradio
RUN chmod -R 777 /tmp/gradio


# Environmrnt values


# expose port for application
EXPOSE 8000
EXPOSE 7860


# start fastapi application
CMD ["sh", "-c", "python app/api.py & python front-end/app.py"]