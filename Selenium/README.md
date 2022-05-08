# Docker images for the Selenium Grid Server

https://github.com/SeleniumHQ/docker-selenium


## Standalone mode
```
docker run -d -p 4444:4444 --shm-size="2g" selenium/standalone-firefox:4.1.2-20220317
docker run -d -p 4444:4444 --shm-size="2g" selenium/standalone-chrome:4.1.2-20220317
docker run -d -p 4444:4444 --shm-size="2g" selenium/standalone-edge:4.1.2-20220317
```
- flag **--shm-size=2g** to use the host's shared memory
- health check **/wd/hub/status**
- retrieve files **-v /home/ubuntu/files:/home/seluser/files**
```chown 1200:1201 /home/ubuntu/files```



## Hub / Node mode
### Same Host
```
docker network create grid
docker run -d -p 4442-4444:4442-4444 --net grid --name selenium-hub selenium/hub:4.1.2-20220317
docker run -d --net grid -e SE_EVENT_BUS_HOST=selenium-hub \
    --shm-size="2g" \
    -e SE_EVENT_BUS_PUBLISH_PORT=4442 \
    -e SE_EVENT_BUS_SUBSCRIBE_PORT=4443 \
    selenium/node-chrome:4.1.2-20220317
```
### Different Host
#### Hub host
```
docker run -d -p 4442-4444:4442-4444 --name selenium-hub selenium/hub:4.1.2-20220317
```

#### Node host
```
docker run -d -p 5555:5555 \
    --shm-size="2g" \
    -e SE_EVENT_BUS_HOST=<ip-from-machine-1> \
    -e SE_EVENT_BUS_PUBLISH_PORT=4442 \
    -e SE_EVENT_BUS_SUBSCRIBE_PORT=4443 \
    -e SE_NODE_HOST=<ip-from-machine-2> \
    selenium/node-chrome:4.1.2-20220317
```

## Dynamic Grid mode
Grid 4 has the ability to start Docker containers on demand, this means that it starts a Docker container in the background for each new session request, the test gets executed there, and when the test completes, the container gets thrown away.

## Build selenium
```docker build . -t selenium-python:v1```




