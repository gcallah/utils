#!/bin/sh

# add some lines to every file meeting a spec.
for file in *.md; do
  if [ -f "$file" ]; then
      awk 'BEGIN {print "\n========"} {print}' "$file" > "$file.tmp" && mv "$file.tmp" "$file"
  fi
done
