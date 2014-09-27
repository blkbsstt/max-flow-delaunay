#/bin/bash

python max-flow-delaunay.py $@
neato -Tpdf out.dot > out.pdf
open out.pdf
