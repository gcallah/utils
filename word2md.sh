#!/bin/sh
pandoc -o $1.md -f docx -t markdown $1.docx
