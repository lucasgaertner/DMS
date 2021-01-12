# DMS


DMS is a microservice-Architecture, based on an AI-model with an offline-storage, Python3 powered and HTML5 Markdown.

  - Upload a document
  - Storing document type and document in the background
  - Save time and space without tons of paper

You can also:
  - Import and save files from anywhere in your Network
  - Upload PDF, tiff, jpg or png documents
  - Export documents as base64 encoded 

DMS is a lightweight tool based on natural language processed. You are able

> The overriding design goal for DMS
> is to make your home as paperless
> as possible. The idea is that
> documents should be stored without taking
> physical space and waste as little time as possible.

This text you see here is *actually* written in Markdown! To get a feel for Markdown's syntax, type some text into the left window and watch the results in the right.

### Tech

DMS uses a number of open source projects to work properly:

* [Docker] - microservice Archicture
* [Python3]
* [flask] - great Web-Frameworks for modern web apps
* [pickle] - model saving
* [base64] - fast encoding(BLOB's)


### Installation

Install and start the server with:

```sh
$ docker-compose up
```
