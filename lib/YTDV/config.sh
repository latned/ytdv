#!/bin/bash

set -e 

mkdir -p ~/.YTDV

if [ ! -f ~/.YTDV/settings.json ]; then
  touch ~/.YTDV/settings.json
  echo '{"quality": "-HIGH-", "theme": "-DARK-", "path": ""}' > ~/.YTDV/settings.json
fi

