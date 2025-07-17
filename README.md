GEOMETRY FROM SILHOUETTE
========================

This repository contains a very simple script for generating a triangle mesh of a solid of revolution, described by a given sampled silhouette. 
This silhouette must be provided as list of values within [0,1) and the number of items in the list (i.e., sampling rate) determines the number of vertical mesh segments. 
The radial sampling rate can be provided as optional parameter.


## Usage

The script can be called like this:
```bash
python3 geometry-from-silhouette.py -c SILHOUETTE_FILE -t TEXTURE_FILE -o OUTPUT_FILE [--radial-segments=NUM_R_SEGMENTS]
```
Also see the simple example in `test.sh`. 
