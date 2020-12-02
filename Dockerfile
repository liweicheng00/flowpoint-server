FROM centos/python-36-centos7
COPY . /app
WORKDIR /app
ENV ENV="production"
ENV MONGO_URI="mongodb+srv://admin:ziQe2V5YdadTm1vy@flowpoint.ukamc.mongodb.net/flowpoint?retryWrites=true&w=majority"
ENV CLINET_ID="422430406019-4knnkh10lgpftp3a7hhi3cd17ljdnat2.apps.googleusercontent.com"

USER root

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

#CMD gunicorn  -k gunicorn.workers.ggevent.GeventWorker -w 1 -b 0.0.0.0:8080 app:app
CMD gunicorn  -k gunicorn.workers.ggevent.GeventWorker -w 1 -b 0.0.0.0:$PORT app:app