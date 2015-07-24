#!/bin/sh

coverage run test_htree.py && coverage report -m --include=htree.py && flake8 --max-line-length=119 htree.py test_htree.py
