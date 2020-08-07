FROM ubuntu:16.04
MAINTAINER Lucas Gärtner
FROM python:3.7


WORKDIR /app

COPY ./requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

RUN apt-get update \
    && apt-get install -y \
        vim \
	poppler-utils \
	tesseract-ocr \
	python-pip python-dev build-essential

RUN apt update && apt install -y libsm6 libxext6
RUN mkdir templates
RUN mkdir uploads
RUN mkdir skripte
RUN mkdir model
RUN mkdir corpora

COPY ./templates /app/templates
COPY ./skripte /app/skripte
COPY ./uploads /app/uploads
COPY ./model /app/model
COPY ./app.py /app
COPY ./nltk_download.py /app/uploads/joined_text/nltk
#COPY ./corpora /app/uploads/joined_text/nltk

RUN mkdir /app/uploads/joined_text/nltk/corpora

COPY ./corpora/wordnet  /app/uploads/joined_text/nltk/corpora/wordnet
#COPY ./corpora/wordnet.zip  /app/uploads/joined_text/nltk/corpora

ENV FLASK_APP=app:app
ENTRYPOINT [ "python" ]

CMD [ "/app/uploads/joined_text/nltk/nltk_download.py" ]

CMD ["app.py"]

