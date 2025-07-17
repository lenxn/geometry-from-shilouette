#!/bin/bash
# Simple dummy example for testing. 


NUM_V_SEGMENTS=20
NUM_R_SEGMENTS=20
SAMPLE_SILHOUETTE_FILE="sample-contour.lst"
SAMPLE_TEXTURE_FILE="Lenna.png"

# Creates a very simple rudimentary silhouette 
python3 -c "import numpy as np; print('\n'.join((-(np.linspace(0, 1, $NUM_V_SEGMENTS)-0.5)**2 + 0.5).astype(str)))" > $SAMPLE_SILHOUETTE_FILE
python3 geometry-from-silhouette.py -c $SAMPLE_SILHOUETTE_FILE -t $SAMPLE_TEXTURE_FILE \
	--radial-segments=$NUM_R_SEGMENTS -o simple.ply

# Creates a slightly more advanced silhouette 
python3 -c "import numpy as np; x=np.linspace(0, 1, $NUM_V_SEGMENTS); print('\n'.join((-(x-0.5)**2 + 0.5 + 0.2*np.cos(10*x)).astype(str)))" > $SAMPLE_SILHOUETTE_FILE
python3 geometry-from-silhouette.py -c $SAMPLE_SILHOUETTE_FILE -t $SAMPLE_TEXTURE_FILE \
	--radial-segments=$NUM_R_SEGMENTS -o advanced.ply
rm $SAMPLE_SILHOUETTE_FILE
