# Deployment
If you want to clone this repo and launch the platform
I recommend to get over the docker-compose.yml file to see
what are the sensitive informations you need to add.

Mainly what you need to do is:
* create a directory /timescaleDB/secrets
* add 2 files: pguser_secret.txt, pgpassword_secret.txt which will
contain the user and the password the database is going to use.

```
docker-compose up --build
```

If you don't want to deploy using docker-compose, you will need to set certain
environment variables and create the necessary networks and volumes by yourself.
Please follow the docker-compose.yml file to understand what is needed for deployment.

## After deployment
If everything was successful, you should now be able to use the iot_gateway_simulator (or any other
client) to publish sensor data to localhost:1883. You should also have a grafana server running
on localhost:3000.