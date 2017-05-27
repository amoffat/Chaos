#!/usr/bin/env python3.6
import argparse
from os.path import dirname, abspath, join, normpath
import sh

THIS_DIR = dirname(abspath(__file__))
REPO_DIR = abspath(join(THIS_DIR, "../../"))
IMAGE_NAME = "chaos"

# host port: container port
PORT_MAPPING = {
    8082: 80,
    8081: 8081,
}

def launch(image, entrypoint, port_mapping, repo_dir):
    args = []
    if entrypoint:
        entrypoint_arg = "--entrypoint=" + entrypoint
        args.append(entrypoint_arg)

    for host_port, container_port in port_mapping.items():
        args.append("-p")
        args.append("{hp}:{cp}".format(hp=host_port, cp=container_port))

    args.append(image)
    volume = "{repo}:/root/workspace/Chaos".format(repo=repo_dir)

    sh.docker.run("-it", "--rm", "-v", volume, *args, _fg=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="chaos docker helper")
    parser.add_argument("-s", "--shell", action="store_true", help="start a shell into the image")
    args = parser.parse_args()

    entrypoint = None
    if args.shell:
        entrypoint = "/bin/bash"

    launch(IMAGE_NAME, entrypoint, PORT_MAPPING, REPO_DIR)
