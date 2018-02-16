FROM python:3

WORKDIR /usr/src

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

VOLUME /usr/src/gpm-accumul

WORKDIR gpm-accumul/erds_server

EXPOSE 8000

CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]