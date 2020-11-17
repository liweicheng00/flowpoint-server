FROM centos/python-36-centos7
COPY . /app
WORKDIR /app
ENV ENV="production"
USER root

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

#CMD gunicorn  -k gunicorn.workers.ggevent.GeventWorker -w 1 -b 0.0.0.0:8080 app:app
CMD gunicorn  -k gunicorn.workers.ggevent.GeventWorker -w 1 -b 0.0.0.0:$PORT app:app