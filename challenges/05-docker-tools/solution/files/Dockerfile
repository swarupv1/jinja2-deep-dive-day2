FROM python:3
LABEL maintainer="Jane Smith" description="Python based tooling" version="0.1"

COPY requirements.txt /tmp

RUN pip3 install --no-cache-dir -r /tmp/requirements.txt
RUN apt-get update && apt-get install -y git tree curl sshpass

CMD ["/bin/bash"]
