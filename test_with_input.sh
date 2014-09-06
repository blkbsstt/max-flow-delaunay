#/bin/bash

python2 P2.py $@
neato -Tpdf out.dot > out.pdf
open out.pdf
