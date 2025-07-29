# add some lines to every file meeting a spec.
for file in *.md; do
  if [ -f "$file" ]; then
    sed -i '1i\'$'\n\n' "$file"
  fi
done
