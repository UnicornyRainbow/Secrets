#!/bin/sh

xgettext \
  --language=Glade \
  --output=src/po/io.github.unicornyrainbow.secrets.pot \
  $(find src -name '*.ui')

while read p; do
  msgmerge --update --backup=none \
    src/po/$p.po \
    src/po/io.github.unicornyrainbow.secrets.pot
done < src/po/LINGUAS
