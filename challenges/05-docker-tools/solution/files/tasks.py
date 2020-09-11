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
