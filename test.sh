#!/bin/bash
# Simple dummy example for testing. 


NUM_V_SEGMENTS=15
NUM_R_SEGMENTS=20
SAMPLE_SILHOUETTE_FILE="sample-contour.lst"
SIMPLE_TEXTURE_FILE="simple_texture.png"
ADVANCED_TEXTURE_FILE="advanced_texture.png"
CHECKERBOARD_STRIDE=100

# Creates a very simple rudimentary silhouette 
python3 -c "import numpy as np; print('\n'.join((-(np.linspace(0, 1, $NUM_V_SEGMENTS)-0.5)**2 + 0.5).astype(str)))" > $SAMPLE_SILHOUETTE_FILE
python3 geometry-from-silhouette.py -c $SAMPLE_SILHOUETTE_FILE -t $SIMPLE_TEXTURE_FILE \
	--radial-segments=$NUM_R_SEGMENTS -o simple.ply

# Creates a slightly more advanced silhouette 
python3 -c "import numpy as np; x=np.linspace(0, 1, $NUM_V_SEGMENTS); print('\n'.join((-(x-0.5)**2 + 0.5 + 0.2*np.cos(10*x)).astype(str)))" > $SAMPLE_SILHOUETTE_FILE
python3 geometry-from-silhouette.py -c $SAMPLE_SILHOUETTE_FILE -t $ADVANCED_TEXTURE_FILE \
	--radial-segments=$NUM_R_SEGMENTS -o advanced.ply
python3 -c "import numpy as np; import cv2;
tex = cv2.imread('$ADVANCED_TEXTURE_FILE', cv2.IMREAD_GRAYSCALE)
cols,rows = np.meshgrid(np.arange(tex.shape[1]), np.arange(tex.shape[0]))
tex &= 255*(((cols/$CHECKERBOARD_STRIDE).astype(int)==np.round(cols/$CHECKERBOARD_STRIDE)) & ((rows/$CHECKERBOARD_STRIDE).astype(int)==np.round(rows/$CHECKERBOARD_STRIDE))).astype(np.uint8)
cv2.imwrite('$ADVANCED_TEXTURE_FILE', tex)
"


rm $SAMPLE_SILHOUETTE_FILE
