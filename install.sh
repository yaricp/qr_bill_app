#!/bin/bash
virtualenv venv
python3 -m venv venv3
$PWD/venv/bin/pip install pip --upgrade
$PWD/venv/bin/pip install -r requirements.txt
$PWD/venv3/bin/pip install pip --upgrade
$PWD/venv3/bin/pip install -r requirements3.txt
