# Chalice PynamoDB Docker REST API Starter Kit

This code is/was originally from: [Chalice-PynamoDB-Docker-Starter-Kit](https://github.com/DevOps-Nirvana/Chalice-PynamoDB-Docker-Starter-Kit/)

This repo makes a great boilerplate/foundation/bootstrap/starter kit to help you get started with AWS's [DynamoDB](https://aws.amazon.com/dynamodb/), Python's [PynamoDB](https://github.com/pynamodb/PynamoDB/), and [AWS's Chalice](https://github.com/aws/chalice) quickly which orchestrates creating and deploying an REST API on [AWS Lambda](https://aws.amazon.com/lambda/) and [AWS API Gateway](https://aws.amazon.com/api-gateway/).  Combined, this makes an easy to use boilerplate for architecting an application on AWS using technologies that are serverless-friendly and operate at very little cost.

This is my personal boilerplate for numerous personal and professional serverless applications on AWS.  This repository is an example of my work and of numerous best-practices of both my own and of the industry.

 * An example of [Dockerfile best-practices](https://docs.docker.com/develop/develop-images/dockerfile_best-practices/) see [Dockerfile](./Dockerfile)
 * An example of Docker Compose best-practices for ease of understanding, support, development, migrations, services, health checks, auto-restarting upon failures, auto-reload upon code changes, and keeping your Docker Compose file as DRY as possible with all the features and complexity with [YAML anchors](https://www.educative.io/blog/advanced-yaml-syntax-cheatsheet#anchors).  See [docker-compose.yml](./docker-compose.yml)
 * An example of using Python, an ORM layer, models, [AWS DynamoDB](https://aws.amazon.com/dynamodb/) via [PynamoDB](https://github.com/pynamodb/PynamoDB/), [AWS Chalice](https://github.com/aws/chalice)


## Requirements
Because of Docker, you don't even need to have Python installed, all you need is...

* To have installed and running [Docker](https://docs.docker.com/get-docker/)
* Install Docker Compose (via [plugin](https://docs.docker.com/compose/install/#scenario-two-install-the-compose-plugin) or [standalone](https://docs.docker.com/compose/install/other/))


## How to use this repo

There are 2 modes in which you can run the application in, primarily though, this codebase is meant for local docker development and experimentation.

### 1. Docker-Compose Local Development Mode
With Docker Compose we can run a local development version of the entire stack, the main purpose of this codebase.  This will spin up the various services needed such as an SMTP server, S3 Server (optional/disabled), DynamoDB server, an DynamoDB web admin, run database migrations, and then startup our application.

```bash
# Simply run this if you installed Docker Compose as a plugin
docker compose up
# or this if you installed Docker Compose standalone
docker-compose up
```

### 2. Cloud-Hosted / Production Mode
Simply run `chalice deploy` to deploy this into your AWS account.  Your AWS CLI must be setup and configured to talk to your desired AWS Account.  Note: This will require you install Python and Chalice on your computer, or that you shell into your "app" container and run it from there.

**WARNING**: If you are to use this in production/cloud mode, you will need to remove the `host = "http://dynamodb:8000"` in every model for it to be able to talk to AWS's hosted DynamoDB properly.

```bash
# First, you'll need to create the tables...
export AWS_DEFAULT_REGION=us-west-2
export AWS_REGION=us-west-2
python3 migrate.py -s dev -r us-west-2
# Then you'll deploy to the dev stage
chalice deploy --stage dev
# Then you should be able to paste the URL it gives you instead of OUR_URL below in examples of usage and use it!
```

## Examples of usage
Once your docker compose application is up, some of the following examples will highlight the features/examples/foundation in this codebase

```bash
# If using local...
export OUR_URL=http://localhost:8002
# If deploying to AWS copy/paste from output of chalice deploy, minus the last /
export OUR_URL=https://dlxlj8umy3.execute-api.us-west-2.amazonaws.com/api  #<---- NOTE REPLACE-ME-AFTER-YOU-DEPLOY-TO-AWS!!!

# Trying to create a user with missing data
curl --verbose --location -X POST "${OUR_URL}/users" --header 'Content-Type: application/json' --data-raw '{"email": "invalid.email.address", "password": "test"}'
# Trying an invalid email, showing exception handling
curl --verbose --location -X POST "${OUR_URL}/users" --header 'Content-Type: application/json' --data-raw '{"email": "invalid.email.address", "password": "test", "name": "tester"}'
# Trying with an valid email...
curl --verbose --location -X POST "${OUR_URL}/users" --header 'Content-Type: application/json' --data-raw '{"email": "user@test.com", "password": "test", "name": "tester"}'
curl --verbose --location -X POST "${OUR_URL}/users" --header 'Content-Type: application/json' --data-raw '{"email": "user2@test.com", "password": "test", "name": "tester2"}'
# To show login works, automatically put session id into variable (requires you have jq installed)
export SESSION_ID=`curl --verbose --location -X POST "${OUR_URL}/login" --header 'Content-Type: application/json' --data-raw '{"email": "user@test.com", "password": "test"}' | jq --raw-output .id`
export SESSION2_ID=`curl --verbose --location -X POST "${OUR_URL}/login" --header 'Content-Type: application/json' --data-raw '{"email": "user2@test.com", "password": "test"}' | jq --raw-output .id`
# Show it worked...
echo "Session ID 1: $SESSION_ID"
echo "Session ID 2: $SESSION2_ID"
# To show using an logged in endpoint works, lookup who we are without session id first...
curl --verbose --location "${OUR_URL}/whoami" --header 'Content-Type: application/json'  # This will fail, on purpose
# Now lets show logged in works...
curl --verbose --location "${OUR_URL}/whoami" --header 'Content-Type: application/json' -H "Authorization: $SESSION_ID"
# Then try to lookup who we are with our session id, setting it into an environment variable with jq
export USER_ID=`curl --verbose --location "${OUR_URL}/whoami" --header 'Content-Type: application/json' -H "Authorization: $SESSION_ID" | jq --raw-output .id`
export USER2_ID=`curl --verbose --location "${OUR_URL}/whoami" --header 'Content-Type: application/json' -H "Authorization: $SESSION2_ID" | jq --raw-output .id`
# Show it worked...
echo "User ID 1: $USER_ID"
echo "User ID 2: $USER2_ID"
# To show LIST works
curl --verbose --location "${OUR_URL}/users/" -H "Authorization: $SESSION_ID"
# To show GET works, but only for ourself...
curl --verbose --location "${OUR_URL}/users/$USER_ID" -H "Authorization: $SESSION_ID"
curl --verbose --location "${OUR_URL}/users/$USER2_ID" -H "Authorization: $SESSION_ID"  # This will fail, on purpose
# To show patch/put works, but only for ourself...
curl --verbose --location -X PATCH "${OUR_URL}/users/$USER_ID" -H "Authorization: $SESSION_ID" --header 'Content-Type: application/json' --data-raw '{"email": "new@new.com"}'
curl --verbose --location -X PATCH "${OUR_URL}/users/$USER2_ID" -H "Authorization: $SESSION_ID" --header 'Content-Type: application/json' --data-raw '{"email": "new@new.com"}'  # This will fail, on purpose
# To show error handling works, try patch with an invalid id, should return FORBIDDEN same as wrong id
curl --verbose --location -X PATCH "${OUR_URL}/users/INVALID_VALUE" -H "Authorization: $SESSION_ID" --header 'Content-Type: application/json' --data-raw '{"email": "new@new.com"}'
# To show input validation works on patch...
curl --verbose --location -X PATCH "${OUR_URL}/users/$USER_ID" -H "Authorization: $SESSION_ID" --header 'Content-Type: application/json' --data-raw '{"email": "INVALID_EMAIL"}'
# To show DELETE works, first try to delete the wrong one, then ours
curl --verbose --location -X DELETE "${OUR_URL}/users/$USER2_ID" -H "Authorization: $SESSION_ID"  # This will fail on purpose, wrong user id with session
curl --verbose --location -X DELETE "${OUR_URL}/users/$USER_ID" -H "Authorization: $SESSION_ID"
curl --verbose --location -X DELETE "${OUR_URL}/users/$USER2_ID" -H "Authorization: $SESSION2_ID"
```


# What this codebase does
* It adds some Django-like fixtures to the PynamoDB Model metadata `required_fields, read_only_fields, validate_fields` via [BaseModel](https://github.com/DevOps-Nirvana/Chalice-PynamoDB-Docker-Starter-Kit/blob/master/models/BaseModel.py)
* A classmethod helper to create from a dictionary automatically, respecting private/require fields (eg: for POST via REST endpoint)
* A helper to set attributes based on an input dict (with input validation)
* A classmethod helper to search through a GSI (GlobalSecondaryIndex) on this model, provided you follow the naming scheme of columnname__index
* A classmethod helper scan through table's column->contains (simplified)
* A simplified example of login and using an authorizer (via API keys)
* Has a working example of how to deploy and use this on AWS directly
* Add automated code to automatically create the DynamoDB tables on AWS needed for this stack (stolen from the [chalice-workshop](https://chalice-workshop.readthedocs.io))
* A simplified permissions model (allowing a user to only manage their own User object(s))
* Make all this repo's table names automatically optionally prefixed by a "stage" name (eg: dev__modelName)
* Auto-detects what AWS region you've deployed into and uses that in the model region
* Automatically adds all routes from the routes folder, a nice(r) way to keep an chalice app DRY and simple to support/develop on


# What this codebase doesn't do (yet) / TODO

These are various TODOs that are things that could be improved, changed, etc.  Contributions are welcome for any of these, but this is mostly a personal list of things I'd like to adjust/improve in this codebase for all our sake/sanity.

* Add example endpoint to send an email
* Add example endpoint to send/receive data from S3 service
* Setup swagger - https://github.com/samuelkhtu/aws-chalice-swagger
* Add postman based on swagger
* Add testing, ideally fully automated, add Github Action for it?
* Add example of SQS topic usage and (ideally) automated creation
* Enable 2FA if user wants to
* It (currently) doesn't provide an robust example of deploying into production in AWS (eg: Terraform, autoscaling DynamoDB)
* It does not deal with advanced permissions/roles/group models



## Support / Author

This codebase was originally authored by [Farley](https://github.com/andrewfarley/) loosely inspired by this [DynamoDB Python Docker Compose Starter Kit](https://github.com/CT83/DynamoDB-Python-Docker-Compose-Starter-Kit).  Feel free to [leave an issue](https://github.com/DevOps-Nirvana/Chalice-PynamoDB-Docker-Starter-Kit/issues) on this codebase if you have any questions or problems, or feel free to email me or contact me via any of the channels below.

| Author   | Contact Details                                                       |
|----------|-----------------------------------------------------------------------|
| Author   | Farley Farley (yes, that's my name)                                   |
| GitHub   | [/andrewfarley](https://github.com/andrewfarley/) (my old legal name) |
| Email    | _farley_ **at** neonsurge __dot__ com                                 |
| LinkedIn | [/in/farley-farley/](http://linkedin.com/in/farley-farley/)           |
| Angelist | [/u/farleyfarley](http://angel.co/u/farley-farley)                    |
