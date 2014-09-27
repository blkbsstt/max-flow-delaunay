#/bin/bash

python2 max-flow-delaunay.py $@
neato -Tpdf out.dot > out.pdf
open out.pdf
