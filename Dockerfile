###############################################################################
#
#       Frontend Dev Image
#
###############################################################################

FROM ghcr.io/srh-sloan/fsd-base-dev:latest as frontend-dev

RUN apt-get update && apt-get install -y redis-tools
WORKDIR /app

COPY . .

RUN python3 -m pip install --upgrade pip && pip install -r requirements.txt
RUN python3 -m pip install werkzeug==2.2.3 flask==2.2.3 debugpy==1.6.7

###############################################################################
#
#       Frontend Runtime Image
#
###############################################################################

FROM ghcr.io/srh-sloan/fsd-base:latest as frontend

WORKDIR /app

# TODO filter out test files etc.
COPY . .

RUN python3 -m pip install --upgrade pip && pip install -r requirements.txt

EXPOSE 8080
CMD ["flask", "run", "--port", "8080", "--host", "0.0.0.0"]
