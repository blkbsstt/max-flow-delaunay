#/bin/bash

python2 $@ > out.in
python2 max-flow-delaunay.py out.in
neato -Tpdf out.dot > out.pdf
open out.pdf
