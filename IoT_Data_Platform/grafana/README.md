IMPORTANT! before running the container make sure you have a persistent volume called grafana-storage.
docker volume create grafana-storage

If you want to launch grafana on localhost:
sudo service start grafana-server

Note: If you want to launch this platform using docker-compose, the volume is going to be created when you
```docker-compose up --build``` and you don't need to do anything else.
