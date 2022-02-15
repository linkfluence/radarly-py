#!/bin/bash
CURRENT_VERSION=$(cat setup.py | grep version | sed "s/version='//g" | sed "s/',//g" | tr -d '[:space:]')
PYPI_LATEST_VERSION=$(curl https://pypi.org/project/radarly-py/  | grep -E -o 'radarly-py [0-9]\.[0-9]\.[0-9][^[:space:]]+' | sed 's/radarly-py //g' | tr -d '[:space:]')

if [[ ${CURRENT_VERSION} == ${PYPI_LATEST_VERSION} ]]
then
    echo "current version match pypi version"
    exit 1
fi