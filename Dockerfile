FROM python:3.8-slim-buster

# Always must have 'ps' for debugging otherwise sysadmins (like me) will hate you, and curl for health check/debugging
RUN apt-get update && \
    apt-get install procps curl -y && \
    rm -rf /var/lib/apt/lists/*

# Do our requirements first for layer caching
WORKDIR /app
ADD requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Then grab our entire app
COPY . .

# And setup our default entrypoint, for local development basically only since Chalice is meant to be deployed to AWS Serverless
# Meaning, we will never "push" this image anywhere and will never use it (eg: in Kubernetes)
EXPOSE 8002
ENTRYPOINT ["chalice", "local", "--host", "0.0.0.0", "--port", "8002", "--autoreload"]

# NOTE: If we were to ever push this image for use in Kubernetes/Docker/CICD/etc we should use this instead...
# ENTRYPOINT ["chalice", "local", "--host", "0.0.0.0", "--port", "8002"]
