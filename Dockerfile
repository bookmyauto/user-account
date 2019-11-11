FROM python:3.7.4-alpine
COPY requirements.txt /opt
WORKDIR /opt
RUN ls
RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev
RUN pip3 install -r requirements.txt
EXPOSE 80
CMD ["python3", "main.py"]


