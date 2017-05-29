#!/usr/bin/env python3.6
import argparse
from os.path import dirname, abspath, join, normpath
import sh

THIS_DIR = dirname(abspath(__file__))
REPO_DIR = abspath(join(THIS_DIR, "../../"))
IMAGE_NAME = "chaos"


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="chaos docker builder")
    parser.add_argument("-e", "--env", default="pc", choices=["pc", "rpi"])
    args = parser.parse_args()

    dockerfile = "Dockerfile"
    if args.env == "rpi":
        dockerfile = "Dockerfile.rpi"

    sh.cp(join(REPO_DIR, "requirements.txt"), ".")
    sh.docker.build("-t", IMAGE_NAME, "-f", dockerfile, ".", _fg=True)
    sh.rm("requirements.txt")

