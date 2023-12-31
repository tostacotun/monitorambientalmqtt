FROM python:3.11.6-alpine
LABEL authors="williamdavidsuarezarevalo"
WORKDIR /usr/src/app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY main.py .
COPY mqttcon.py .
COPY .env .
CMD ["python","-u","main.py"]
#ENTRYPOINT ["top", "-b"]