#!/bin/bash

env
echo "create $QR_PIC_DIR folder"
mkdir -p $QR_PIC_DIR

poetry run python3 /bot/main.py