#!/bin/bash

MY_DIR="$(dirname $0)"
APP_DIR=$MY_DIR/..
export PYTHONPATH=.:..
cd $APP_DIR
pip install -r requirements.txt

