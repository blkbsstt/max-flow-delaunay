#/bin/bash

python $@ > out.in
python max-flow-delaunay.py out.in
neato -Tpdf out.dot > out.pdf
open out.pdf
