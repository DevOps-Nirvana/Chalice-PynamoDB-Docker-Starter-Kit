# Chalice PynamoDB Docker REST API Bootstrap

This code is/was originally from: [Chalice-PynamoDB-Docker-Bootstrap](https://github.com/DevOps-Nirvana/Chalice-PynamoDB-Docker-Bootstrap/)

This repo makes a great bootstrap/starter kit to help you get started with AWS's [DynamoDB](https://aws.amazon.com/dynamodb/), Python's [PynamoDB](https://github.com/pynamodb/PynamoDB/), and AWS's [Chalice](https://github.com/aws/chalice) quickly which orchestrates creating and deploying an REST API on AWS Lambda.  Combined, this makes a  easy to use boilerplate for architecting an application on AWS using technologies that are serverless-friendly and operate at very little cost.

This is my personal boilerplate for numerous personal and professional serverless applications on AWS.

This repository is an example of my work and of numerous best-practices of both my own and of the industry
 * [Dockerfile best-practices](https://docs.docker.com/develop/develop-images/dockerfile_best-practices/) see [Dockerfile](./Dockerfile)
 * Docker Compose best-practices for ease of understanding, support, development, migrations, services, health checks, auto-restarting upon failures, auto-reload upon code changes, and keeping your Docker Compose file as DRY as possible with all the features and complexity with [YAML anchors](https://www.educative.io/blog/advanced-yaml-syntax-cheatsheet#anchors).  See [docker-compose.yml](./docker-compose.yml)
 * An example of using Python, ORM, Models, [AWS DynamoDB](https://aws.amazon.com/dynamodb/), [PynamoDB](https://github.com/pynamodb/PynamoDB/), [AWS Chalice](https://github.com/aws/chalice)


## Requirements
Because of Docker, you don't even need to have Python installed, all you need is...

* To have installed and running [Docker](https://docs.docker.com/get-docker/)
* Install Docker Compose (via [plugin](https://docs.docker.com/compose/install/#scenario-two-install-the-compose-plugin) or [standalone](https://docs.docker.com/compose/install/other/))


## How to use this repo

There are 2 modes in which you can run the application in...

### 1. Docker-Compose Local Development Mode
Using Docker Compose we can run a local development version of the entire stack, the main purpose of this codebase.  This will spin up the various services needed such as an SMTP server, DynamoDB server, an DynamoDB web admin, run database migrations, and then startup our application.

```bash
# Simply run this if you installed Docker Compose as a plugin
docker compose up
# or this if you installed Docker Compose standalone
docker-compose up
```

### 2. Cloud-Hosted / Production Mode
Simply run `chalice deploy` to deploy this into your AWS account.  Your AWS CLI must be setup and configured to talk to your desired AWS Account.  Note: This will require you install Python and Chalice on your computer, or that you shell into your "app" container and run it from there.

**WARNING**: If you are to use this in production/cloud mode, you will need to remove the `host = "http://dynamodb:8000"` in every model for it to be able to talk to AWS's hosted DynamoDB properly.


## Examples of usage
Once your docker compose application is up, some of the following examples will highlight the features/examples/foundation in this codebase

```bash
# Trying an invalid email, showing solid exception handling
curl --verbose --location -X POST "http://localhost:8002/users" --header 'Content-Type: application/json' --data-raw '{"sid": "test", "email": "invalid.email.address"}'
# Trying with an valid email...
curl --verbose --location -X POST "http://localhost:8002/users" --header 'Content-Type: application/json' --data-raw '{"sid": "test", "email": "1234567891123222@test.com"}'
# To show GET works, copy/paste the ID from above
curl --verbose --location "http://localhost:8002/users/PASTEIDHERE"
# To show patch/put works, copy/paste the ID from above into this
curl --verbose --location -X PATCH "http://localhost:8002/users/PASTEIDHERE" --header 'Content-Type: application/json' --data-raw '{"email": "new@new.com"}'
# To show error handling works, try patch with an invalid id
curl --verbose --location -X PATCH "http://localhost:8002/users/invalid_id" --header 'Content-Type: application/json' --data-raw '{"email": "new@new.com"}'
# To show input validation works on patch...
curl --verbose --location -X PATCH "http://localhost:8002/users/PASTEIDHERE" --header 'Content-Type: application/json' --data-raw '{"email": "INVALID_EMAIL"}'
# To show DELETE works
curl --verbose --location -X DELETE "http://localhost:8002/users/PASTEIDHERE"
```


## TODO
These are various TODOs that are things that could be improved, changed, etc.  Contributions are welcome for any of these, but this is mostly a personal list of things I'd like to adjust/improve in this codebase for all our sake/sanity.

* Make this repo production-friendly by dynamically choosing the "host" variable intelligently (detecting if on AWS)
* Add working examples of this deploying onto AWS directly
* Add automated code to automatically create the DynamoDB tables needed for this stack
* Add example of SQS topic usage and (ideally) automated creation
* Make all this repo's table names automatically optionally prefixed by a "stage" name (eg: dev__modelName)


## Support / Author

This codebase was originally authored by [Farley](https://github.com/andrewfarley/) loosely inspired by this [DynamoDB Python Docker Compose Starter Kit](https://github.com/CT83/DynamoDB-Python-Docker-Compose-Starter-Kit).  Feel free to [leave an issue](https://github.com/DevOps-Nirvana/Chalice-PynamoDB-Docker-Bootstrap/issues) on this codebase if you have any questions or problems, or feel free to email me or contact me via any of the channels below.

| Author   | Contact Details                                                       |
|----------|-----------------------------------------------------------------------|
| Author   | Farley Farley (yes, that's my name)                                   |
| GitHub   | [/andrewfarley](https://github.com/andrewfarley/) (my old legal name) |
| Email    | _farley_ **at** neonsurge __dot__ com                                 |
| LinkedIn | [/in/farley-farley/](http://linkedin.com/in/farley-farley/)           |
| Angelist | [/u/farleyfarley](http://angel.co/u/farley-farley)                    |