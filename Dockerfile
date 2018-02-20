FROM python:3

WORKDIR /usr/src

#COPY requirements.txt ./
#RUN pip install --no-cache-dir -r requirements.txt

RUN pip install Django

VOLUME /usr/src/gpm-accumul

WORKDIR gpm-accumul/erds_server

#RUN django-admin startproject app

#WORKDIR app

EXPOSE 8000

CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]