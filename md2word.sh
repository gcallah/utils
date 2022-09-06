#!/bin/sh
pandoc -o $1.docx -f markdown -t docx $1.md
