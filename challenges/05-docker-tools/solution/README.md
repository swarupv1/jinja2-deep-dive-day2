# Challenge Exercise Solution Guide

## Building a Docker Tools Container

The goal of this exercise is to build a new Docker container image with a few network automation tools and streamline the process by using either Make or Invoke.

## Solution Walkthrough

First, grab the latest docker image for the `python:3` container as instructed.

```
vagrant ants /vagrant docker pull python:3
3: Pulling from library/python
d6ff36c9ec48: Pull complete
c958d65b3090: Pull complete
edaf0a6b092f: Pull complete
80931cf68816: Pull complete
bc1b8aca3825: Pull complete
edfe96a4dd20: Pull complete
4e7c0e94bdeb: Pull complete
8dffdfc294e3: Pull complete
036c588c629e: Pull complete
Digest: sha256:2c1045587e4452d49544c6dce92efe21c3b4b33864cfb56fdee66a2c8585c769
Status: Downloaded newer image for python:3
docker.io/library/python:3

vagrant ants /vagrant docker image ls
REPOSITORY          TAG                 IMAGE ID            CREATED             SIZE
python              3                   79cc46abd78d        2 weeks ago         882MB
```

Then, test that you can run the container - by default you will get a Python interpreter prompt.

```
vagrant ants /vagrant docker run -it python:3
Python 3.8.5 (default, Aug  5 2020, 08:22:02)
[GCC 8.3.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>>
```

### Building the container

In preparation for the build, you need a Dockerfile, which specifies which operations Docker should apply to the base image to arrive at your desired result. Create a file called `Dockerfile` with the following contents.

```Dockerfile
FROM python:3
LABEL maintainer="Jane Smith" description="Python based tooling" version="0.1"

COPY requirements.txt /tmp

RUN pip3 install --no-cache-dir -r /tmp/requirements.txt
RUN apt-get update && apt-get install -y git tree curl sshpass

CMD ["/bin/bash"]
```

Labels are just text that helps others understand what your container image is about - feel free to modify to suit your use case.

The Challenge tells you to use a `requirements.txt` file to install python packages, so you first have to copy it from the host *into* the container. Then, you pass it to the `pip` command to install all the needed packages.

You are also instructed to install some other tools, namely `git tree curl sshpass` - first you need to `apt-get update` to fetch up to date information about system packages, then install them.

Finally, as per the instructions, override the starting command of the container so that it is `CMD ["/bin/bash"]`. As you have seen earlier, the `python:3` container starts by default a python interpreter, not bash.

The contents of the requirements file should be as follows:

```
ansible
netmiko
napalm
ansible-lint
yamllint
black
netaddr
jmespath
requests
```

You can now build the container manually by running the build command.

```
vagrant ants /vagrant/solution/files docker build -t netdev/tools:0.1 .
Sending build context to Docker daemon   5.12kB
Step 1/6 : FROM python:3
 ---> 79cc46abd78d
Step 2/6 : LABEL maintainer="Jane Smith" description="Python based tooling" version="0.1"
 ---> Running in 8381907f4054
Removing intermediate container 8381907f4054
 ---> b579972c232e
Step 3/6 : COPY requirements.txt /tmp
 ---> 358ff7034290
Step 4/6 : RUN pip3 install --no-cache-dir -r /tmp/requirements.txt
 ---> Running in bf2be560fe99
Collecting ansible
  Downloading ansible-2.9.12.tar.gz (14.3 MB)
...
OUTPUT SNIPPED
...
Successfully built ad3a33f6cf40
Successfully tagged netdev/tools:0.1
```

Now run the container and enjoy its functionality!

```
vagrant ants /vagrant/solution/files docker run -it netdev/tools:0.1
root@01efba168042:/# ansible --version
ansible 2.9.12
  config file = None
  configured module search path = ['/root/.ansible/plugins/modules', '/usr/share/ansible/plugins/modules']
  ansible python module location = /usr/local/lib/python3.8/site-packages/ansible
  executable location = /usr/local/bin/ansible
  python version = 3.8.5 (default, Aug  5 2020, 08:22:02) [GCC 8.3.0]
```

### The Makefile

Included below is a Makefile example that uses variables to reduce repetition and help you with versioning and naming of your containers.

```
NAME = "netdev/tools"
VERSION = "0.1"

.PHONY: container run clean-images clean-stopped
default: container


container:
	docker build -t $(NAME):$(VERSION) .

run:
	docker run -it $(NAME):$(VERSION)

clean-images:
	docker image rm -f $(NAME):$(VERSION)

clean-stopped:
	docker container prune -f
```

### The Invoke tasks file

The same functionality as exposed in the Makefile is implemented here using Python's Invoke library.

There's only one gotcha - the `run` function needs to be told to execute its command through a terminal `pty=True` rather than just directly as a process in order for the `docker run -it` command to work interactively.

```
from invoke import task

NAME = "netdev/tools"
VERSION = "0.1"

@task
def container(context):
    context.run(f"docker build -t {NAME}:{VERSION} .")

@task
def run(context):
    context.run(f"docker run -it {NAME}:{VERSION}", pty=True)

@task
def clean_images(context):
    context.run(f"docker image rm -f {NAME}:{VERSION}")

@task
def clean_stopped(context):
    context.run(f"docker container prune -f")
```
