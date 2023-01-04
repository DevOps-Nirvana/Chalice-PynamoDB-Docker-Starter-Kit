FROM python:3.8-slim-buster

# Always must have 'ps' for debugging otherwise sysadmins (like me) will hate you, and curl for health check/debugging
RUN apt-get update && \
    apt-get install procps curl -y && \
    rm -rf /var/lib/apt/lists/*

# Do our requirements first for layer caching
WORKDIR /app
ADD requirements.txt requirements.txt
RUN pip install -r requirements.txt && \
    pip install awscli

# Then grab our entire app
COPY . .

# And setup our default entrypoint, for local development basically only since Chalice is meant to be deployed to AWS Serverless
# Meaning, we will never "push" this image anywhere and will never use it (eg: in Kubernetes)
EXPOSE 8002

# NOTE: By default docker images should be ready to push upstream and be used in production, so
#       we shouldn't have stuff like autoreload enabled by default. We will specify this in our
#       docker-compose.yaml file instead
ENTRYPOINT ["chalice", "local", "--host", "0.0.0.0", "--port", "8002"]
