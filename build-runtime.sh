#!/bin/bash
set -e
set -x

cd "$(dirname "$0")"
HERE="$(pwd)"
ROOT="$(dirname "$HERE")"

docker build -t lindenlab.com/raml/pyraml-parser "$HERE"
