# docker-tutorial

Docker Core Part

## Flask Application Practice

First, we'll create a simple Flask application to demonstrate Docker usage.


### Note: All source code already exists in the flask_demo_site folder. Here we only show the content of app.py to help you follow along step by step and experience the joy of building it yourself (doge)


Create a file named `app.py` with the following content:

```python
from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return "Hello, Docker!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```

I won't go into detail about the Python content since the focus of this weekly session is Docker, not Python.

You can look up the relevant content on your own.

### Dockerfile

To let Docker know how to build an image, we need to create a Dockerfile in the project (no extension).

The Dockerfile must be in the same directory as app.py.

```dockerfile
#1. basic information
FROM python:3.10-slim

#2. set workspace
WORKDIR /app

#3. install dependencies
RUN pip install flask

#4. copy app.py to /app dir in the container
COPY app.py /app/

#5. set environment variables
ENV PYTHONUNBUFFERED=1  
#let python print log immediately

#6. define the command to run in default when container starts
CMD ["python", "app.py"]

```

Explanation of the code above:

- `FROM`: Specifies the base environment required for the project (such as Python version or C++ version)

- `WORKDIR`: Specifies the root directory of the project's workspace in the container

- `RUN`: Executes commands, here used to install Flask dependencies

- `COPY`: Copies files from the current folder (same level as Dockerfile) to the specified location in the container

- `ENV`: Adds environment variables

- `CMD`: Defines the default command to run when the container starts

With this Dockerfile, Docker knows what the corresponding image should look like and can build the image you want.

### Basic Image Operations

#### Create

How do we create an image?

We can create an image by running the following command:

`Must run in the directory where the Dockerfile is located`

```bash
docker build -t my-flask-app:v1 .
```

Where:

- `-t` specifies the name of the image, generally in the format: `name:version`

#### View

If you want to see how many images currently exist, you can run the following command:

```bash
docker images
```

The terminal will return all image information

#### Package

Package the image as a tar file (for physical transfer across devices):

You can think of it as a zip compressed file, except its extension is .tar

```bash
docker save -o my-flask-app-v1.tar my-flask-app:v1
```

Where `-o` means output, followed by the tar file name you want to output, then the image name you want to package

This will generate the corresponding tar file

#### Import tar package

You can import a tar file into docker with the following command:

```bash
docker load -i my-flask-app-v1.tar
```

docker will import the image from the tar file to the local machine, and you can check if it was successfully imported with `docker images`

#### Delete

You can delete an image with the following command:

```bash
docker rmi -f my-flask-app:v1
```

Where `-f` means force delete, normally you don't need to add -f (because docker will prompt you to confirm the deletion)

---

There's another way to clean up unused images:

```bash
docker image prune -a # -a: clean up all unused images
```

---

After operating on images, it's natural to operate on containers.

---

### Basic Container Operations

Commands related to containers are as follows:

#### Create Container

```bash
docker run -d --name my-flask-container -p 8080:5000 my-flask-app:v1
```

Regarding the above command, here are some points that need explanation (or you can look them up yourself):

- `-d`: Run in the background, don't show the simulated terminal in real-time

- `--name`: Custom container name (you can write whatever you want)

- `-p`: Port mapping (not needed if the packaged project doesn't involve network content like flask)

The function of this command is to map port 5000 in the container to port 8080 on the host, so we can access port 5000 in the container through port 8080 on the host.

#### View Container Status

```bash
docker ps # View running containers

docker ps -a # View all containers
```

#### Start Container

```bash
docker start my-flask-container
```

Just add your own container name after start

#### Run Internal Programs

```bash
# Enter the container's interactive terminal
docker exec -it my-flask-container /bin/bash

# Exit the container's interactive terminal
exit
```

#### Execute Commands in Container

```bash
# Execute a single command in the container
docker exec my-flask-container ls -la
```

You can replace ls -la with the command you want to execute, for example:

```bash
docker exec my-flask-container python -m flask run
```

All are feasible.

---

As a programmer, how can you not look at logs? (*^_^*) 

#### View Container Logs

```bash
docker logs my-flask-container

# View logs in real-time
docker logs -f my-flask-container
```

#### Stop Container

There are two ways to stop a container:

1. Graceful stop (recommended):

```bash
docker stop my-flask-container
```

2. Forced stop (only when necessary):

```bash
docker kill my-flask-container
```

#### Restart Container

```bash
docker restart my-flask-container
```

#### Delete Container

Like images, there are two ways to delete containers:

```bash
docker rm -f my-flask-container # Force delete specified container

docker container prune # Clean up all stopped containers
```

Where -f means force delete, if you want a gentler way, just remove -f.

---

#### Data Volume Operations

Data volumes are a mechanism in Docker for persisting data, which can share data between containers or between the host and containers.

```bash
# Create folder (will be used later)
mkdir ./data

# Create data volume
docker volume create my-volume

# View data volumes
docker volume ls

# View data volume details
docker volume inspect my-volume

# Mount data volume when running container
docker run -d --name my-flask-container -v my-volume:/app/data my-image

# Mount host directory to container
docker run -d --name my-flask-container -v ./data:/app/data my-image

# Delete data volume
docker volume rm my-volume

# Clean up unused data volumes
docker volume prune
```

Here, the role of `-v` is to specify the mapping relationship between the directory in the container and the directory on the host, for example:

```bash
docker run -d --name my-flask-container -v ./data:/app/data my-image
```

This means that the `/app/data` directory in the container and the `./data` directory on the host are in a mapping relationship. File changes in the container will be synchronized to the host, and file changes on the host will also be synchronized to the container.

---

I mentioned earlier that containers are isolated processes.

But our program has network requests, how can it survive without network? (sad)

Fortunately, Docker has long considered this, so Docker provides multiple network modes for communication between containers.

---

## Docker Network

Docker provides multiple network modes for communication between containers:

- **bridge mode**: Default network mode, containers communicate with the host through virtual network bridge
- **host mode**: Containers directly use the host network, best performance but poor isolation
- **none mode**: Containers have no network connection
- **overlay mode**: Used for multi-host Docker clusters

```bash
# Create network
docker network create my-network

# View networks
docker network ls

# Specify network when running container
docker run -d --name my-flask-container --network my-network my-image

# Connect container to network
docker network connect my-network my-flask-container

# Disconnect container from network
docker network disconnect my-network my-flask-container

# Delete network
docker network rm my-network
```

`Note`: After using port mapping, the container will automatically use bridge network mode.

Therefore, in most cases, no special configuration is needed unless you need containers to communicate with each other.

~~`Anyway, we don't need it for this weekly session (^_^)`~~

---

Finally, we have learned some basic Docker operations.

## But

Have you ever thought about a question:

Take `docker run` as an example:

Every time I want to create a container, do I have to take a deep breath and type the whole command:

```bash
docker run -d --name my-flask-container -p 8080:5000 my-image
```

Exhausted after typing it all?

## Would the legendary laziest programmers be willing to endure such humiliation! ! ! (╯‵□′)╯︵┻━┻

For the specific solution, please look forward to the second part of this weekly session:


## Docker Compose

