# NTC DevEnv Workshop - Lab Guide

You will now practice some of the concepts that were demonstrated in the first part of the workshop by the instructor on your own cloud hosted virtual machine. This guide provides all the necessary commands and tasks in this lab guide should be performed in order, as they might depend on files and packages installed beforehand.


## CONFIDENTIAL

### This material is owned by Network to Code, LLC.

**You are NOT permitted to distribute the material, content, slides, labs, and other related material outside of the program.**

Copyright 2020, Network to Code, LLC.


## Setting Up for Remote Development

You should perform this step together with your instructor at the beginning of the session. The goal here is to be able to perform all the subsequent lab tasks inside of a VSCode session running on the lab VM.

Start up your VSCode, go to the Extensions tab, and ensure the "Remote - SSH" extension from Microsoft is installed. If you need to install it, type "Remote" in the search bar up top and locate it in the populated results below (VSCode needs to be able to access the Internet for this).

You will also need a compatible SSH client - the VSCode documentation provides instructions for all of the major platforms [here](https://code.visualstudio.com/docs/remote/troubleshooting#_installing-a-supported-ssh-client).

With the prerequisites installed, you should now have a green `><` sign in the bottom left corner of your VSCode window. You may click on it to open a selection of Remote-SSH actions.

> You may also open the command palette (`Ctrl-Shift-P`) and type `remote-ssh`.
> For a full list of shortcuts, go to File->Preferences->Keyboard Shortcuts.

First, you need to set up your remote SSH host. Select `Remote-SSH: Open Configuration File...` and choose the first option, depending on your operating system it will look like `path/to/home/folder/.ssh/config`. In this file, add a new entry (replacing the IP address):

```
Host devenv-workshop-vm
    HostName 192.0.2.1
    User ntc
```

Save this file and close it. From the `Remote-SSH` menu, now select the `Connect to host...` action. In the list that appears, you should find `devenv-workshop-vm` - select it. A new VSCode window will open, asking you for the password (unless otherwise instructed, it is `ntc123`). This window is now fully remote, giving you access to the files on the remote host. 

In the menu, open `File -> Add Folder to Workspace...`, then select `lab` under the `/home/ntc` path. The remote VSCode window may reopen, asking you to input the password again. You should now see the lab folder on the left-hand side `Explorer` panel. 

Expand the `lab` folder and open `lab_guide.md` from within. You may read it like this or use the `Markdown: Open Preview` option from the `Command Palette` (Ctrl-Shift-P or F1) to view an HTML render of the file.

If not already open, you may start a terminal inside this window by going to the `Terminal->New Terminal` menu item.

Congratulations, you are all set up!

### Backup option

`!!!` Only use this if you cannot get VSCode + Remote SSH to work. `!!!`

You can replicate the same functionality using the following tools:

- your SSH client of choice - [PuTTY](https://putty.org/), [SecureCRT](https://www.vandyke.com/products/securecrt/) etc.
- your code editor of choice - [SublimeText3](https://www.sublimetext.com/), [VSCode](https://code.visualstudio.com/), [Notepad++](https://notepad-plus-plus.org/), VIM/nano etc.
- a file sync client - [CyberDuck](https://cyberduck.io/) or [WinSCP](https://winscp.net/)

You should try to keep this lab guide and an SSH terminal on the lab VM side by side (or on separate monitors) to help you focus on the lab tasks.


## Task 1 - Using Python Remotely

### Step 1

In your terminal, ensure you are in the `/home/ntc/lab/` folder. Create a new folder here called `webserver` and change into it.

```
ntc devenv-01 ~ $ cd /home/ntc/lab/
ntc devenv-01 ~/lab $ mkdir webserver
ntc devenv-01 ~/lab $ cd webserver/
ntc devenv-01 ~/lab/webserver $ 
```

### Step 2

Create an `index.html` file with containing the following text: `<h1>Hello there!</h1>`. You may use VSCode for this or run the command shown below.

```
ntc devenv-01 ~/lab/webserver $ echo '<h1>Hello there!</h1>' > index.html
```

### Step 3

Start a simple python3 webserver. Here you are calling the `http.server` module directly from the command line, a very useful feature when you need to quickly start a development webserver.

```
ntc devenv-01 ~/lab/webserver $ python3 -m http.server
Serving HTTP on 0.0.0.0 port 8000 (http://0.0.0.0:8000/) ...
```

### Step 4

In your web browser of choice, open the following website: `http://YOUR_VM_IP:8000` replacing your VM's IP as appropriate. You should now see a "Hello there!" message on the page.

### Step 5

The webserver was started by using a module that ships with python. You will now create a separate python script that works as a web client, using a third-party library called `requests`.

Leave the webserver running in the current terminal and open a new one. You may do this using the `Terminal -> New Terminal` menu or by clicking the `+` sign in the top right section of the terminal panel.

### Step 6

Create a new folder called `webclient` inside of `/home/ntc/lab`, then change into it.

```
ntc devenv-01 ~/lab $ mkdir webclient
ntc devenv-01 ~/lab $ cd webclient/
ntc devenv-01 ~/lab/webclient $ 
```

### Step 7

Since you want to keep your lab VM "clean", you decide to install the `requests` library inside of a python virtual environment. This also allows for easier future packaging of your application.

Create a `requirements.txt` file containing the word `requests`. This will tell `pip` what to install. Verify its contents and location as per the output below.

```
ntc devenv-01 ~/lab/webclient $ cat requirements.txt 
requests
```

### Step 8

In the `webclient` folder, create a new python virtual environment called `venv` and activate it. Confirm that the python interpreter is running out of this new environment.

```
ntc devenv-01 ~/lab/webclient $ python3 -m venv venv
ntc devenv-01 ~/lab/webclient $ source venv/bin/activate
(venv) ntc devenv-01 ~/lab/webclient $ which python
/home/ntc/lab/webclient/venv/bin/python
```

### Step 9

Check what additional python packages are installed using `pip list`, then install your project's dependencies using `pip install -r requirements.txt`

```
(venv) ntc devenv-01 ~/lab/webclient $ pip list
Package       Version
------------- -------
pip           20.0.2 
pkg-resources 0.0.0  
setuptools    44.0.0 

(venv) ntc devenv-01 ~/lab/webclient $ pip install -r requirements.txt 
Collecting requests
  Downloading requests-2.24.0-py2.py3-none-any.whl (61 kB)
     |████████████████████████████████| 61 kB 349 kB/s 
Collecting chardet<4,>=3.0.2
  Downloading chardet-3.0.4-py2.py3-none-any.whl (133 kB)
     |████████████████████████████████| 133 kB 27.9 MB/s 
Collecting certifi>=2017.4.17
  Downloading certifi-2020.6.20-py2.py3-none-any.whl (156 kB)
     |████████████████████████████████| 156 kB 46.2 MB/s 
Collecting urllib3!=1.25.0,!=1.25.1,<1.26,>=1.21.1
  Downloading urllib3-1.25.10-py2.py3-none-any.whl (127 kB)
     |████████████████████████████████| 127 kB 54.9 MB/s 
Collecting idna<3,>=2.5
  Downloading idna-2.10-py2.py3-none-any.whl (58 kB)
     |████████████████████████████████| 58 kB 8.2 MB/s 
Installing collected packages: chardet, certifi, urllib3, idna, requests
Successfully installed certifi-2020.6.20 chardet-3.0.4 idna-2.10 requests-2.24.0 urllib3-1.25.10
```

### Step 10

Create a new file in the `/home/ntc/lab/webclient` folder called `get.py`. In it, place the following code:

```py
import requests

response=requests.get(url='http://localhost:8000')

print(response.text)
```

### Step 11

Making sure that you are still in the terminal that has the virtual environment active, execute the script using the `python3 get.py` interpreter. 

> You can always check whether the virtualenv is active by looking for the bash prompt (venv) prepended name or by using the `which python` command.

```
(venv) ntc devenv-01 ~/lab/webclient $ python3 get.py 
<h1>Hello there!</h1>
```

Success!


## Task 2 - Automating Common Python Tasks

Since running the `get.py` web client script requires a virtual environment with dependencies installed, it's common practice to use other tools to automate the creation, activation and updates of these dependencies.

You will use the `GNU Make` utility to manage the virtualenv and run the application. 

### Step 1

In the `/home/ntc/lab/webclient` folder, create a new file named `Makefile` and copy/paste in the following contents:

```Makefile
.PHONY: clean run

default: run

run: venv
    . venv/bin/activate; python3 get.py

venv: venv/bin/activate

venv/bin/activate: requirements.txt
    test -d venv || python3 -m venv venv
    . venv/bin/activate; pip3 install -Ur requirements.txt
    touch venv/bin/activate

clean:
    rm -rf venv
```

In VSCode, open the `Command Palette` (Ctrl-Shift-P) and select `Convert Indentation to Tabs`. Save the file.

> Most code editors convert tabs to spaces by default, but Makefiles require tabs for indentation, otherwise they will not work.

### Step 2 

Review the makefile. It defines the following "targets" or actions:

- run (the default): it activates the virtualenv and executes the `get.py` python script
- venv (a shorcut for venv/bin/activate): it ensures that the virtualenv is created and the dependencies specified in the `requirements.txt` file are installed
- clean: it removes the virtualenv

### Step 3

Open a fresh terminal and navigate to the `/home/ntc/lab/webclient` folder. Do NOT activate the virtualenv!

```
ntc devenv-01 ~ $ cd lab/webclient/
ntc devenv-01 ~/lab/webclient $
```

### Step 4

Use the command `make` without any arguments. It will execute the `run` default target.

```
ntc devenv-01 ~/lab/webclient $ make
. venv/bin/activate; python3 get.py
<h1>Hello there!</h1>
```

### Step 5

Run the command `make clean` to delete the virtual environment. Confirm by using `ls`.

```
ntc devenv-01 ~/lab/webclient $ make clean
rm -rf venv
ntc devenv-01 ~/lab/webclient $ ls
Makefile  get.py  requirements.txt
```

### Step 6

Now run `make` again. It will detect that the virtualenv is missing, create it, and then run the script successfully.

```
ntc devenv-01 ~/lab/webclient $ make
test -d venv || python3 -m venv venv
. venv/bin/activate; pip3 install -Ur requirements.txt
Collecting requests
  Using cached requests-2.24.0-py2.py3-none-any.whl (61 kB)
Collecting urllib3!=1.25.0,!=1.25.1,<1.26,>=1.21.1
  Using cached urllib3-1.25.10-py2.py3-none-any.whl (127 kB)
Collecting chardet<4,>=3.0.2
  Using cached chardet-3.0.4-py2.py3-none-any.whl (133 kB)
Collecting idna<3,>=2.5
  Using cached idna-2.10-py2.py3-none-any.whl (58 kB)
Collecting certifi>=2017.4.17
  Using cached certifi-2020.6.20-py2.py3-none-any.whl (156 kB)
Installing collected packages: urllib3, chardet, idna, certifi, requests
Successfully installed certifi-2020.6.20 chardet-3.0.4 idna-2.10 requests-2.24.0 urllib3-1.25.10
touch venv/bin/activate
. venv/bin/activate; python3 get.py
<h1>Hello there!</h1>
```

Feel free to play around with the various make targets (i.e. run, clean, venv).


## Task 3

Invoke is a python task execution tool & library that offers a pythonic way of implementing make functionality.

You will use `invoke` to automate code formatting and linting for your webclient application. The `black` uncompromising python formatter and the linter `pylint` are already installed on the machine.

### Step 1

In the `/home/ntc/lab/webclient` folder, execute the `black` formatter in check and diff mode. It should show you output as below if you did not modify the `get.py` code.

```
ntc devenv-01 ~/lab/webclient $ black --check --diff get.py 
--- get.py      2020-08-06 20:02:29.024221 +0000
+++ get.py      2020-08-06 20:39:26.787799 +0000
@@ -1,6 +1,6 @@
 import requests
 
-response=requests.get(url='http://localhost:8000')
+response = requests.get(url="http://localhost:8000")
 
 print(response.text)
 
would reformat get.py
Oh no! 💥 💔 💥
1 file would be reformatted.
```

As you can see, it would add some spacing around the `=` sign and convert the single quotes into double quotes.

### Step 2

In the `/home/ntc/lab/webclient` folder, execute `pylint` against the `get.py` file. It should show you output as below:

```
ntc devenv-01 ~/lab/webclient $ pylint get.py 
************* Module get
get.py:3:8: C0326: Exactly one space required around assignment
response=requests.get(url='http://localhost:8000')
        ^ (bad-whitespace)
get.py:1:0: C0114: Missing module docstring (missing-module-docstring)

------------------------------------------------------------------
Your code has been rated at 3.33/10 (previous run: 3.33/10, +0.00)
```

### Step 3

Before fixing the issues, first create the equivalent of a Makefile for `invoke`. This is the `tasks.py` file (you will need to create it). In it, you define two tasks, one that runs `black` and the other that runs `pylint`, just as you did in the previous steps.

```
ntc devenv-01 ~/lab/webclient $ cat tasks.py 
from invoke import task

@task
def black(context):
    context.run("black --check --diff get.py")

@task
def pylint(context):
    context.run("pylint get.py")
```

### Step 4

Now run `invoke`, listing the tasks it supports.

```
ntc devenv-01 ~/lab/webclient $ invoke --list
Available tasks:

  black
  pylint

```

### Step 5

Ask `invoke` to execute the `black` task.

```
ntc devenv-01 ~/lab/webclient $ invoke black
--- get.py      2020-08-06 20:02:29.024221 +0000
+++ get.py      2020-08-06 20:47:49.437627 +0000
@@ -1,6 +1,6 @@
 import requests
 
-response=requests.get(url='http://localhost:8000')
+response = requests.get(url="http://localhost:8000")
 
 print(response.text)
 
would reformat get.py
Oh no! 💥 💔 💥
1 file would be reformatted.
```

### Step 6

Ask `invoke` to execute the `pylint` task.

```
ntc devenv-01 ~/lab/webclient $ invoke pylint
************* Module get
get.py:3:8: C0326: Exactly one space required around assignment
response=requests.get(url='http://localhost:8000')
        ^ (bad-whitespace)
get.py:1:0: C0114: Missing module docstring (missing-module-docstring)

------------------------------------------------------------------
Your code has been rated at 3.33/10 (previous run: 3.33/10, +0.00)
```

### Step 7

Let's fix the code. Let `black` actually reformat the code, instead of reporting the changes it would make. Run the command `black get.py`.

```
ntc devenv-01 ~/lab/webclient $ black get.py 
reformatted get.py
All done! ✨ 🍰 ✨
1 file reformatted.
```

> Remember: if you run black without any parameters, it will reformat the files without asking any questions.

### Step 8

Run `invoke black` again to check that it now succeeds.

```
ntc devenv-01 ~/lab/webclient $ invoke black
All done! ✨ 🍰 ✨
1 file would be left unchanged.
```

It is now, indeed, happy. Well done!









## Task 4 - Using Docker Commands

You are now going to practice using some of the most common docker commands to perform operations on a docker host - that is, a VM that can build and run containers.

Tools and applications are nowadays also distributed as containers, making them more portable and reducing the time it takes to get them running. The goal of this task is for you to become comfortable at consuming such applications and, later on, even build a container of your own.


### Step 1

In a terminal on the lab VM, confirm your docker version and test that the daemon is running. The `docker` command connects to the local docker daemon running on the lab VM.

```
ntc devenv-01 ~/lab $ docker -v
Docker version 19.03.12, build 48a66213fe

ntc devenv-01 ~/lab $ docker ps
CONTAINER ID        IMAGE               COMMAND             CREATED             STATUS              PORTS               NAMES
```

> The `docker ps` command is the short version of the `docker container ls` command and shows a list of all the running (and optionally stopped) containers.


### Step 2

Run the command `docker run ubuntu echo Hello World!`. It will download and run the command `echo Hello World!` inside of a container image called `ubuntu`.

```
ntc devenv-01 ~/lab $ docker run ubuntu echo Hello World!
Unable to find image 'ubuntu:latest' locally
latest: Pulling from library/ubuntu
3ff22d22a855: Pull complete 
e7cb79d19722: Pull complete 
323d0d660b6a: Pull complete 
b7f616834fd0: Pull complete 
Digest: sha256:5d1d5407f353843ecf8b16524bc5565aa332e9e6a1297c73a92d3e754b8a636d
Status: Downloaded newer image for ubuntu:latest
Hello World!
```

> By default, if you don't explicitly specify a registry address, the docker command will connect to `https://hub.docker.com/`, a public repository of containers. In the example above, it downloads [this container](https://hub.docker.com/_/ubuntu).

### Step 3

The `ubuntu` image is now stored locally in docker's image repository on disk. Use the `docker image ls` command to view its contents.

```
ntc devenv-01 ~/lab $ docker image ls
REPOSITORY          TAG                 IMAGE ID            CREATED             SIZE
ubuntu              latest              1e4467b07108        13 days ago         73.9MB
```

> You can see container image names, sizes, and their tag (or version).

### Step 4

Containers can contain any programs, be it short-lived shell commands or long-lived services. You ran an `echo` command in the `bash` shell, so after it printed the message the container finished its execution. Run `docker ps -a` to view a list of all (running and stopped) containers.

```
ntc devenv-01 ~/lab $ docker ps -a
CONTAINER ID        IMAGE               COMMAND               CREATED             STATUS                     PORTS               NAMES
73cd9fe02d18        ubuntu              "echo Hello World!"   6 minutes ago       Exited (0) 6 minutes ago                       stupefied_gagarin
```

> `docker ps` only shows running containers by default, of which now you have none. Try it!

### Step 5

Containers that finished their execution are still there, as you may want to inspect them, do operations with their filesystems, or restart them. They take up space on disk though, so if you are sure you don't need them any more, you can use the `docker container prune` command to clean up.

```
ntc devenv-01 ~/lab $ docker container prune
WARNING! This will remove all stopped containers.
Are you sure you want to continue? [y/N] y
Deleted Containers:
73cd9fe02d187da994310f933fc2d3c99b572cca685f148ff79dc6c7f421b5cc

Total reclaimed space: 0B
ntc devenv-01 ~/lab $ docker ps -a
CONTAINER ID        IMAGE               COMMAND             CREATED             STATUS              PORTS               NAMES
```

### Step 6

When you want to run multiple commands in a container, it is common to start a shell (similar to how you start in a terminal on a remote host). In order to interact with this shell from the command line, you need to tell docker to start an interactive terminal `-it`. Optionally, you can provide the `--rm` flag to tell docker to delete (or prune) the container once it finishes running.

Run the `docker run -it --rm ubuntu bash` command. When you are done with the shell, type exit to return to the docker host.

```
ntc devenv-01 ~/lab $ docker run -it --rm ubuntu bash
root@0a83b24e5ec4:/# 
root@0a83b24e5ec4:/# 
root@0a83b24e5ec4:/# echo Hello World!
Hello World!
root@0a83b24e5ec4:/# exit
exit
ntc devenv-01 ~/lab $
```

### Step 7

If you want the container to keep running in the background, you can provide the `-d` or detach flag. Optionally, you can give your running container a name (it must be unique!).

Run the `docker run -itd --name test ubuntu bash` command now.

```
ntc devenv-01 ~/lab $ docker run -itd --name test ubuntu bash
cd68687c0816b9fb2eb07f27d2351c60e4bc8e9caaeb2cc6531a984b43c64f84
ntc devenv-01 ~/lab $
```

The result is a unique id of the running container and the docker command returns you to your shell, while the container is still executing in the background. This is commonly done with containers that provide services which are not interactive.

### Step 8

Run the `docker ps` command. You will now see your `test` container in the running state.

```
ntc devenv-01 ~/lab $ docker ps
CONTAINER ID        IMAGE               COMMAND             CREATED             STATUS              PORTS               NAMES
cd68687c0816        ubuntu              "bash"              2 seconds ago       Up 1 second                             test
```

### Step 9

To execute commands in an already running container, use the `docker exec` command. You may run one-shot commands or interactive (`-it`) sessions as you can see below for `bash`.

```
ntc devenv-01 ~/lab $ docker exec test echo Hello again!
Hello again!

ntc devenv-01 ~/lab $ docker exec -it test bash
root@cd68687c0816:/# #This is a new shell
root@cd68687c0816:/# ps a  
    PID TTY      STAT   TIME COMMAND
      1 pts/0    Ss+    0:00 bash
     63 pts/1    Ss     0:00 bash
     71 pts/1    R+     0:00 ps a
root@cd68687c0816:/# exit
exit
ntc devenv-01 ~/lab $
```

> In this case you know the name of your container, but if you didn't, you can find out the name or the ID from the `docker ps` output.

> The very first command you start a container with will always be PID 1. This is the first process and, when it ends, the container execution ends as well. Your second bash shell has a PID of 63 and will stop when you type `exit`

### Step 10

You can copy files from and to a container using the `docker cp` command. Copy the `webserver/index.html` file into the `test` container and then check it is there.

```
ntc devenv-01 ~/lab $ docker cp webserver/index.html test:/index.html
ntc devenv-01 ~/lab $ docker exec test cat /index.html
<h1>Hello there!</h1>
ntc devenv-01 ~/lab $
```

### Step 11

If you want to stop a running container, you may use the `docker stop` command. Run the commands as shown below.

```
ntc devenv-01 ~/lab $ docker ps
CONTAINER ID        IMAGE               COMMAND             CREATED             STATUS              PORTS               NAMES
cd68687c0816        ubuntu              "bash"              21 minutes ago      Up 21 minutes                           test

ntc devenv-01 ~/lab $ docker stop test
test

ntc devenv-01 ~/lab $ docker ps
CONTAINER ID        IMAGE               COMMAND             CREATED             STATUS              PORTS               NAMES
```

### Step 12

You can start a stopped container again. Run the `docker start test` command, then look at the output of `docker ps`.

```
ntc devenv-01 ~/lab $ docker start test
test

ntc devenv-01 ~/lab $ docker ps
CONTAINER ID        IMAGE               COMMAND             CREATED             STATUS              PORTS               NAMES
cd68687c0816        ubuntu              "bash"              23 minutes ago      Up 1 second                             test
```

> Docker still has the full configuration and state of the container as it was not deleted.

### Step 13

Since this is the same container as earlier, try to get the contents of the `/index.html` file.

```
ntc devenv-01 ~/lab $ docker exec test cat /index.html
<h1>Hello there!</h1>
```

### Step 14

Now stop and delete your `test` container by running the commands shown below.

```
tc devenv-01 ~/lab $ docker stop test
test
ntc devenv-01 ~/lab $ docker rm test
test
ntc devenv-01 ~/lab $ docker ps -a
CONTAINER ID        IMAGE               COMMAND             CREATED             STATUS              PORTS               NAMES
```

> Your container named `test` is now gone forever. Any changes from the `ubuntu` image, such as copied files, are also lost. Containers as ephemeral by design and you need explicit actions to preserve state.

### Step 15

Start a new `ubuntu` container named `test` and check its filesystem. As expected, the `/index.html` is not there anymore, since you started the container from the base unmodified image.

```
ntc devenv-01 ~/lab $ docker run -it --rm ubuntu bash

root@98a1f4a0b5d7:/# cat /index.html
cat: /index.html: No such file or directory
root@98a1f4a0b5d7:/# exit
exit

ntc devenv-01 ~/lab $
```




## Task 5 - Containerizing a Python Web Server

One common usage for docker containers is to package applications for distribution and portability. Here, you will use a different container image called `python` to run your simple webserver from within a container and serve the `index.html` page.

### Step 1

Retrieve version (or tag) `3.8-slim` of the `python` container image using the `docker pull python:3.8-slim` command.

```
ntc devenv-01 ~/lab $ docker pull python:3.8-slim
3.8-slim: Pulling from library/python
bf5952930446: Pull complete 
385bb58d08e6: Pull complete 
ab14b629693d: Pull complete 
7a5d07f2fd13: Pull complete 
56745e40505a: Pull complete 
Digest: sha256:f7edd1bb431a224e7f4f3e23cbb22738e82f4895a6d28f86294ce006177360c3
Status: Downloaded newer image for python:3.8-slim
docker.io/library/python:3.8-slim
```

### Step 2

Test start a new container using this image as show below. Notice you get dropped into a `python 3.8` interpreter by default.

```
ntc devenv-01 ~/lab $ docker run -it python:3.8-slim 
Python 3.8.5 (default, Aug  4 2020, 16:24:08) 
[GCC 8.3.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> exit()
ntc devenv-01 ~/lab $
```

### Step 3

Change to the `/home/ntc/lab` folder. Check that you have the `index.html` file in the `/home/ntc/lab/webserver` folder.

```
ntc devenv-01 ~/lab $ cd /home/ntc/lab/
ntc devenv-01 ~/lab $ cat webserver/index.html 
<h1>Hello there!</h1>
```

### Step 4

Run the following command to start a containerized python webserver and then confirm it is running.

```
ntc devenv-01 ~/lab $ docker run -d --rm --name pyweb -v $PWD/webserver:/webserver -p8888:8000 python:3.8-slim python3 -m http.server --directory /webserver/
53f1bc49d06df7f0bedbd08e49ff348dd32f93ea01dde87046bff4797f337b8b

ntc devenv-01 ~/lab $ docker ps
CONTAINER ID        IMAGE               COMMAND                  CREATED             STATUS              PORTS                    NAMES
53f1bc49d06d        python:3.8-slim     "python3 -m http.ser…"   3 seconds ago       Up 1 second         0.0.0.0:8888->8000/tcp   pyweb
```

Let's disect the command:

- `-d` start container in detached mode (run it as a service)
- `--rm` delete the container once it stops
- `--name pyweb` give it the name `pyweb`
- `-v $PWD/webserver:/webserver` mount the local `webserver` folder contents in the container at `/webserver`
- `-p8888:8000` create port forwarding to publish the container internal port 8000 to the docker host's port 8888
- `python:3.8-slim` the container image
- `python3 -m http.server --directory /webserver/` the command to start a python web server

In your web browser of choice, open the following website: `http://YOUR_VM_IP:8888` replacing your VM's IP as appropriate. You should now see a "Hello there!" message on the page.

### Step 5

Open the `/home/ntc/lab/webserver/index.html` file in your editor and change the message to "Hello from Docker!". Save the file and refresh your web browser `http://YOUR_VM_IP:8888` page.

Since this file is mounted into the container, the change will be instantly reflected and you should see the new message displayed.

Congratulations, you have containerized your first application!



## Task 6 - Create a Network Development Container Image

You will now get started on the path of creating your own container images pre-loaded with libraried and tools that you often use. Here, you will build upon the `python` docker container image to create a `netdev` container that has `ansible` and a few other network automation libraries (netmiko, napalm, textfsm) installed.

### Step 1

Create the `/home/ntc/lab/netdev` folder and change into it.

```
ntc devenv-01 ~/lab $ mkdir -p /home/ntc/lab/netdev
ntc devenv-01 ~/lab $ cd /home/ntc/lab/netdev
ntc devenv-01 ~/lab/netdev $
```

### Step 2

Create a new file in the `netdev` folder named `Dockerfile`. It should have the following contents:

```
ntc devenv-01 ~/lab/netdev $ cat Dockerfile 
FROM python:3.8-slim
LABEL maintainer="Yours Truly" description="Python based tooling" version="0.1"

RUN pip3 install --no-cache-dir ansible netmiko napalm textfsm
CMD ["/bin/bash"]
```

### Step 3

Run the command `docker build -t netdev:0.1 .` to build a new container image named `netdev` and tag it with version `0.1`. Mind the dot at the end of the command!

You will now see the build process that executes the commands as specified in the Dockerfile and produces a container image at the end if successful.

```
ntc devenv-01 ~/lab/netdev $ docker build -t netdev:0.1 .
Sending build context to Docker daemon  2.048kB
Step 1/4 : FROM python:3.8-slim
 ---> 07ea617545cd
Step 2/4 : LABEL maintainer="Yours Truly" description="Python based tooling" version="0.1"
 ---> Running in 99a9ca79ed31
Removing intermediate container 99a9ca79ed31
 ---> 1d0a17bf2d07
Step 3/4 : RUN pip3 install --no-cache-dir ansible netmiko napalm textfsm
 ---> Running in dcecc818fb84
Collecting ansible
  Downloading ansible-2.9.11.tar.gz (14.2 MB)
Collecting netmiko
  Downloading netmiko-3.2.0-py2.py3-none-any.whl (157 kB)
Collecting napalm
  Downloading napalm-3.1.0-py2.py3-none-any.whl (229 kB)
Collecting textfsm
  Downloading textfsm-1.1.0-py2.py3-none-any.whl (37 kB)
Collecting jinja2
  Downloading Jinja2-2.11.2-py2.py3-none-any.whl (125 kB)
Collecting PyYAML
  Downloading PyYAML-5.3.1.tar.gz (269 kB)
Collecting cryptography
  Downloading cryptography-3.0-cp35-abi3-manylinux2010_x86_64.whl (2.7 MB)
Requirement already satisfied: setuptools>=38.4.0 in /usr/local/lib/python3.8/site-packages (from netmiko) (49.2.1)
Collecting scp>=0.13.2
  Downloading scp-0.13.2-py2.py3-none-any.whl (9.5 kB)
Collecting paramiko>=2.4.3
  Downloading paramiko-2.7.1-py2.py3-none-any.whl (206 kB)
Collecting pyserial
  Downloading pyserial-3.4-py2.py3-none-any.whl (193 kB)
Collecting junos-eznc>=2.2.1
  Downloading junos-eznc-2.5.1.tar.gz (154 kB)
Collecting future
  Downloading future-0.18.2.tar.gz (829 kB)
Collecting cffi>=1.11.3
  Downloading cffi-1.14.1-cp38-cp38-manylinux1_x86_64.whl (409 kB)
Collecting ciscoconfparse
  Downloading ciscoconfparse-1.5.19-py3-none-any.whl (93 kB)
Collecting netaddr
  Downloading netaddr-0.8.0-py2.py3-none-any.whl (1.9 MB)
Collecting pyeapi>=0.8.2
  Downloading pyeapi-0.8.3.tar.gz (137 kB)
Collecting lxml>=4.3.0
  Downloading lxml-4.5.2-cp38-cp38-manylinux1_x86_64.whl (5.4 MB)
Collecting requests>=2.7.0
  Downloading requests-2.24.0-py2.py3-none-any.whl (61 kB)
Collecting six
  Downloading six-1.15.0-py2.py3-none-any.whl (10 kB)
Collecting MarkupSafe>=0.23
  Downloading MarkupSafe-1.1.1-cp38-cp38-manylinux1_x86_64.whl (32 kB)
Collecting pynacl>=1.0.1
  Downloading PyNaCl-1.4.0-cp35-abi3-manylinux1_x86_64.whl (961 kB)
Collecting bcrypt>=3.1.3
  Downloading bcrypt-3.1.7-cp34-abi3-manylinux1_x86_64.whl (56 kB)
Collecting ncclient>=0.6.3
  Downloading ncclient-0.6.8.tar.gz (117 kB)
Collecting yamlordereddictloader
  Downloading yamlordereddictloader-0.4.0.tar.gz (3.3 kB)
Collecting pyparsing
  Downloading pyparsing-2.4.7-py2.py3-none-any.whl (67 kB)
Collecting transitions
  Downloading transitions-0.8.2-py2.py3-none-any.whl (76 kB)
Collecting ntc_templates
  Downloading ntc_templates-1.5.0-py3-none-any.whl (254 kB)
Collecting pycparser
  Downloading pycparser-2.20-py2.py3-none-any.whl (112 kB)
Collecting colorama
  Downloading colorama-0.4.3-py2.py3-none-any.whl (15 kB)
Collecting dnspython
  Downloading dnspython-2.0.0-py3-none-any.whl (208 kB)
Collecting passlib
  Downloading passlib-1.7.2-py2.py3-none-any.whl (507 kB)
Collecting chardet<4,>=3.0.2
  Downloading chardet-3.0.4-py2.py3-none-any.whl (133 kB)
Collecting idna<3,>=2.5
  Downloading idna-2.10-py2.py3-none-any.whl (58 kB)
Collecting certifi>=2017.4.17
  Downloading certifi-2020.6.20-py2.py3-none-any.whl (156 kB)
Collecting urllib3!=1.25.0,!=1.25.1,<1.26,>=1.21.1
  Downloading urllib3-1.25.10-py2.py3-none-any.whl (127 kB)
Building wheels for collected packages: ansible, PyYAML, junos-eznc, future, pyeapi, ncclient, yamlordereddictloader
  Building wheel for ansible (setup.py): started
  Building wheel for ansible (setup.py): finished with status 'done'
  Created wheel for ansible: filename=ansible-2.9.11-py3-none-any.whl size=16176769 sha256=31b32a79e61708e9eefa87072490cf73e4f6dd91ff71e340576c3903d9aa1f60
  Stored in directory: /tmp/pip-ephem-wheel-cache-docsw7ec/wheels/96/b5/fc/646cc0302950f9dd85ce04f1108809447c7c1c20ebf23f587b
  Building wheel for PyYAML (setup.py): started
  Building wheel for PyYAML (setup.py): finished with status 'done'
  Created wheel for PyYAML: filename=PyYAML-5.3.1-cp38-cp38-linux_x86_64.whl size=44617 sha256=4481668e74b87ce7437c0bab4445e1542b5604c96ec697b49150cc55ececdcb2
  Stored in directory: /tmp/pip-ephem-wheel-cache-docsw7ec/wheels/13/90/db/290ab3a34f2ef0b5a0f89235dc2d40fea83e77de84ed2dc05c
  Building wheel for junos-eznc (setup.py): started
  Building wheel for junos-eznc (setup.py): finished with status 'done'
  Created wheel for junos-eznc: filename=junos_eznc-2.5.1-py3-none-any.whl size=190451 sha256=ac4e0a41ee9a9999dd92f240dbd6175c87e2b99517c1181dcb48044371afe99f
  Stored in directory: /tmp/pip-ephem-wheel-cache-docsw7ec/wheels/f0/4d/a0/fb9cbe8e782460ad05434b83389823c990f0ff12758700d44e
  Building wheel for future (setup.py): started
  Building wheel for future (setup.py): finished with status 'done'
  Created wheel for future: filename=future-0.18.2-py3-none-any.whl size=491058 sha256=5d78a73e00494f3141a94fa759b509b80f3d7ca911c9d6257be94804d42b247a
  Stored in directory: /tmp/pip-ephem-wheel-cache-docsw7ec/wheels/8e/70/28/3d6ccd6e315f65f245da085482a2e1c7d14b90b30f239e2cf4
  Building wheel for pyeapi (setup.py): started
  Building wheel for pyeapi (setup.py): finished with status 'done'
  Created wheel for pyeapi: filename=pyeapi-0.8.3-py3-none-any.whl size=90262 sha256=8ef9fdb2e2f203eb897faf88a101e510509ec3ae799c9e394b1636ffb565fce9
  Stored in directory: /tmp/pip-ephem-wheel-cache-docsw7ec/wheels/d1/56/be/60a2a048f7510cc33f862dafa06471e928494ebdf0a0558ec0
  Building wheel for ncclient (setup.py): started
  Building wheel for ncclient (setup.py): finished with status 'done'
  Created wheel for ncclient: filename=ncclient-0.6.8-py2.py3-none-any.whl size=103305 sha256=084051777bba962dc3c5393575964dc667bdf7d7eab4d3df91aaad43dbabefa3
  Stored in directory: /tmp/pip-ephem-wheel-cache-docsw7ec/wheels/02/03/15/2fc281ba0891ebe5f1632a0bdfc6c96e6b023baf5270e715e8
  Building wheel for yamlordereddictloader (setup.py): started
  Building wheel for yamlordereddictloader (setup.py): finished with status 'done'
  Created wheel for yamlordereddictloader: filename=yamlordereddictloader-0.4.0-py3-none-any.whl size=4052 sha256=51d614302245f4b6b2d90089d13de3fe6e8bd6d9072796f461180098056a07bd
  Stored in directory: /tmp/pip-ephem-wheel-cache-docsw7ec/wheels/50/9a/6f/9cb3312fd9cd01ea93c3fdc1dbee95f5fa0133125d4c7cb09a
Successfully built ansible PyYAML junos-eznc future pyeapi ncclient yamlordereddictloader
Installing collected packages: MarkupSafe, jinja2, PyYAML, pycparser, cffi, six, cryptography, ansible, future, textfsm, pynacl, bcrypt, paramiko, scp, pyserial, netmiko, lxml, ncclient, netaddr, yamlordereddictloader, pyparsing, transitions, ntc-templates, junos-eznc, colorama, dnspython, passlib, ciscoconfparse, pyeapi, chardet, idna, certifi, urllib3, requests, napalm
Successfully installed MarkupSafe-1.1.1 PyYAML-5.3.1 ansible-2.9.11 bcrypt-3.1.7 certifi-2020.6.20 cffi-1.14.1 chardet-3.0.4 ciscoconfparse-1.5.19 colorama-0.4.3 cryptography-3.0 dnspython-2.0.0 future-0.18.2 idna-2.10 jinja2-2.11.2 junos-eznc-2.5.1 lxml-4.5.2 napalm-3.1.0 ncclient-0.6.8 netaddr-0.8.0 netmiko-3.2.0 ntc-templates-1.5.0 paramiko-2.7.1 passlib-1.7.2 pycparser-2.20 pyeapi-0.8.3 pynacl-1.4.0 pyparsing-2.4.7 pyserial-3.4 requests-2.24.0 scp-0.13.2 six-1.15.0 textfsm-1.1.0 transitions-0.8.2 urllib3-1.25.10 yamlordereddictloader-0.4.0
Removing intermediate container dcecc818fb84
 ---> c691651da2be
Step 4/4 : CMD ["/bin/bash"]
 ---> Running in 8cf9db0ab6db
Removing intermediate container 8cf9db0ab6db
 ---> 83e955040d82
Successfully built 83e955040d82
Successfully tagged netdev:0.1
```

### Step 4

Check the list of docker images using `docker image ls`. Notice you now have a `netdev` image.

```
ntc devenv-01 ~/lab/netdev $ docker image ls
REPOSITORY          TAG                 IMAGE ID            CREATED              SIZE
netdev              0.1                 83e955040d82        About a minute ago   281MB
python              3.8-slim            07ea617545cd        2 days ago           113MB
ubuntu              latest              1e4467b07108        13 days ago          73.9MB
```

### Step 5

Create a new container from the freshly baked `netdev:0.1` image and try running `ansible` inside of it!

```
ntc devenv-01 ~/lab/netdev $ docker run -it --rm netdev:0.1
root@1d0325082173:/# ansible --version
ansible 2.9.11
  config file = None
  configured module search path = ['/root/.ansible/plugins/modules', '/usr/share/ansible/plugins/modules']
  ansible python module location = /usr/local/lib/python3.8/site-packages/ansible
  executable location = /usr/local/bin/ansible
  python version = 3.8.5 (default, Aug  4 2020, 16:24:08) [GCC 8.3.0]
```

Congratulations, your new network development tools container is functional!

> In the future you may want to share this container image with your colleagues. You may share the Dockerfile so they can build their own from it or push the image to a Docker registry.
