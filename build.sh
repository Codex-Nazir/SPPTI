#!/usr/bin/env bash

# Install system dependency
apt-get update
apt-get install -y libzbar0

# Install python dependencies
pip install -r requirements.txt
