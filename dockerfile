FROM python:3.10.11
WORKDIR /usr/src/app

COPY . /usr/src/app
# Install OpenCV dependencies
RUN apt-get update && \
    apt-get install -y libgl1-mesa-glx

RUN pip install -r requirements.txt

CMD uvicorn main:app --port=8000 --host=0.0.0.0 
# CMD [ "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "15400" ] 