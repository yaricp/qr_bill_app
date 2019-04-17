#!/bin/bash
virtualenv venv
$PWD/venv/bin/pip install pip --upgrade
$PWD/venv/bin/pip install -r requirements.txt
