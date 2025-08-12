#!/bin/bash
set -ex
echo "STARTING MAIN.SH!"
echo "RUNNING SRC/MAIN.PY"
python3 src/main.py
echo "CD PUBLIC & RUN HTTP SERVER PORT 8888"
cd public && python3 -m http.server 8888
echo "DONE!"ls -