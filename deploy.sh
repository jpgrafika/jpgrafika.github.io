#!/bin/sh
python3.8 jpgrafika.py build
git add --all
git commit -m "automatic deploy"
git push -u origin master