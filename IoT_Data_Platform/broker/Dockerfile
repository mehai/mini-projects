FROM eclipse-mosquitto:latest
LABEL maintainer="Mihai Zanfir"
ADD ./mosquitto.conf /mosquitto/config/mosquitto.conf
VOLUME ["/mosquitto/config", "/mosquitto/data", "/mosquitto/log"]
EXPOSE 1883


