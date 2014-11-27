#!/bin/bash
RAML="$1"
RAML_FILE="$(basename "$1")"
RAML_FQN="$(pwd)/$RAML"

docker run --rm -v "$RAML_FQN":"/$RAML_FILE" lindenlab.com/raml/pyraml-parser "/$RAML_FILE"
