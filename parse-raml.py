#!/usr/bin/env python
from pyraml import parser, model
import sys

try:
	p = parser.load(sys.argv[1])
except model.ValidationError as e:
	print repr(e)
	sys.exit(1)
print p
