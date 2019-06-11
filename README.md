# Employee Registry Api

## Introduction

This project is about a server-side API developed in Python with the Flask framework, and its extension Flask Resful.
The server-side API is currently not served served by database engine, but instead, a flat file database. 

The user interacts with the api by sending http requests to the server, upon which the corresponding CRUD operations detailed below are performed:

Create an employee in the database associated with a role <Manager | !Manager>

Read the details of an employee refered to by an ID.

Update the details of an employee reffered to by an ID.

Delete the employee reffered to by an ID.

This project is developed solely for tesing purposes, monkey test and penetration tests among others. Once a feature is added different vulnerabilities and issues will be tested and reported, prior to merge on the development branch.

The goal of the project is purely educational, as it is to observe the common vulnerabilities and pitfalls to beware of during backend development. Future releases will include different database engines and vulnerability fixes.

## How to install and interact with API

You would need python version X to contribute to this code. The API is hard coded to run on port XYZ1. There are two different ways of installing the dependencies explained below.

### Pip 
Project dependencies are stated in the requirements.txt file. The command below installs the dependencies:
`pip install -r requirements.txt`

### Docker
Project dependencies will also be listed in the docker-compose.yml and Dockerfile once it is ready.
The command below will then build the docker image, and run the docker container.

`docker-compose -f docker-compose.yml up --build -d`

## How to test

### Postman

### Pytest


## How to contribute

### Branching

#### Master

#### Develop

  ##### Feature-branches
  The current convention for branch name is <GRP | DLT>-X, where X is the feature id genereated by the card.


### Code review

### Devops
