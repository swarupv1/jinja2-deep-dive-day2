# Challenge - Building a Docker Tools Container

The goal of this exercise is to build a new Docker container image with a few network automation tools and streamline the process by using either Make or Invoke.

## Exercise Overview

### Prerequisites

You will need to have [Docker installed](https://www.docker.com/get-started) and either Make (in WSL / Linux VM) or Python Invoke (any OS). 

> Note: A cleaner option is to use a Virtual Machine and install everything you need in there - you can start from an Ubuntu Desktop live CD (to have a Graphical Environment) or just via CLI with Ubuntu Server.

### Tasks

1. Ensure your Docker environment is working by `pulling` and `running` the official [Python docker image](https://hub.docker.com/_/python).
2. Create a `Dockerfile` to build a new Docker image starting from the `python:3` base.
    - Using a `requirements.txt` file, install the following python packages: `ansible, netmiko, napalm, ansible-lint, yamllint, black, netaddr, jmespath, requests`
    - Using the package manager (`apt-get`), install the following packages: `git, tree, curl, sshpass`
    - Add metadata (labels) for your new image: `maintainer, description, version`
    - Set the default command of the container to be `/bin/bash` (i.e. what's executed when you run the container)
3. Create a Makefile or an Invoke tasks file to perform the following tasks:
    - Build the container image from the Dockerfile (e.g. `make container`)
    - Delete the container image (e.g. `make clean-images`)
    - Run a fresh container with an interactive command line (bash) (e.g. `make run`)
    - Delete all stopped containers  (e.g. `make clean-stopped`)

> Hint: Run bash in the base container and validate your commands manually first. When you're happy that they work (in a non-interactive manner for the build process!) you can put them in the Dockerfile.

> Note: You should test that packages you installed in the container actually work - for example, try writing a simple Ansible playbook and then run it from the container. Remember, you can copy files to and from a container (be it running or stopped), but images are immutable once built.

Your solution should include these files: Dockerfile, Makefile/tasks.py and requirements.txt

### Useful links

- [Dockerfile Reference](https://docs.docker.com/engine/reference/builder/)
- [Docker Hub Python Image](https://hub.docker.com/_/python)
- [Make Docs](https://www.gnu.org/software/make/manual/make.html)
- [Invoke Docs](https://docs.pyinvoke.org/en/stable/index.html)

### Reference Enablement Material

- Developer Tooling & Navigation
- Development Environments - Lab Guide

> Note: Recordings of the relevant sessions can be found online at: https://training.networktocode.com/ 
