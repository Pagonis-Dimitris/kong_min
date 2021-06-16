FROM python:3.7 as pyserver

COPY ./requirements.txt /home/app/
WORKDIR /home/app/

RUN apt-get update -y
RUN pip install -r requirements.txt

FROM pyserver

ENV PYTHONDONTWRITEBYTECODE 1

COPY . /home/app/
WORKDIR /home/app/

RUN chmod +x ./main.py

ENTRYPOINT ["./runserver.sh"]
