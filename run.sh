#!/bin/sh

while read p; do mkdir -p src/mo/$p/LC_MESSAGES && msgfmt -c src/po/$p.po -o src/mo/$p/LC_MESSAGES/io.github.unicornyrainbow.secrets.mo; done < src/po/LINGUAS
python3 src/secrets_main.py