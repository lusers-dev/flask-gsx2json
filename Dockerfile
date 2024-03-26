# Base image is alpine
FROM alpine:latest as builder

COPY sample_docker_requirements.txt requirements.txt

RUN apk update \
    && apk upgrade \
    && apk add --update --no-cache python3 \
    && python3 -m ensurepip \
    && pip3 install -r requirements.txt


FROM alpine:latest
WORKDIR /python-flask-gsx2json
COPY --from=builder / / 
COPY . .
ENTRYPOINT [ "python3", "-m", "flask", "run", "--host=0.0.0.0" ]
