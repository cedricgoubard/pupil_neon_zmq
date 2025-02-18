FROM python:3.11

RUN pip install --upgrade pip

RUN pip install pupil-labs-realtime-api pyyaml >=6.0.2

# OpenCV dependencies
RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y && rm -rf /var/lib/apt/lists/*

RUN 

WORKDIR /work
COPY . .

RUN pip install -e .

CMD bash