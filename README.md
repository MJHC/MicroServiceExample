# Microservices Docker Compose and Swarm example

This is a simple microservices example using docker

## Creating SSL Certification
self signed certificates should not beused in production

```
mkdir ./cert
cd ./cert
openssl genpkey -algorithm RSA -out cert.key
openssl req -new -key cert.key -out cert.csr
openssl req -x509 -key cert.key -in cert.csr -out cert.crt -days 365
```
## files

- `docker-compose.yaml` is used for development and testing
- `docker-swarm.yaml` is used for production
  - in a production application, the database should not be a docker container, but it is in this example

Passwords and other sensitive data should also not be in the environments but in docker secrets

## Compose:
test locally with:
```
docker compose -f docker-compose.yaml up
```

## Swarm
creating swarm
```
docker swarm init
```

Join on other machines and then:

```
docker compose -f docker-swarm.yaml build
docker stack deploy -c docker-swarm.yaml testapp
```

### Scaling
```
docker service scale testapp_service_a=5
```

### Shutdown
```
docker stack rm testapp
```

### Leave Swarm
```
docker swarm leave
```

if node is a manager use `--force`

then the `Swarm` attribute in `docker info` should be `Swarm: inactive`