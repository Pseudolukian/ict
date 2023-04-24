#!/bin/bash
cd $PWD
pipenv run python3 -m pytest "$@"