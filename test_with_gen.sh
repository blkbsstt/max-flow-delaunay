#/bin/bash

python2 $@ > out.in
python2 P2.py out.in
neato -Tpdf out.dot > out.pdf
open out.pdf
