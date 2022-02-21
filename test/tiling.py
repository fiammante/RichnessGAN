import cv2
import os, os.path
import shutil
import tempfile
import numpy as np

# reduce image richness using KMeans
def reduce_richness(img):
    Z = img.reshape((-1,3))
    # convert to np.float32
    Z = np.float32(Z)
    # define criteria, number of clusters(K) and apply kmeans()
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
    K = 32 # number of colors
    ret,label,center=cv2.kmeans(Z,K,None,criteria,10,cv2.KMEANS_RANDOM_CENTERS)
    # Now convert back into uint8, and make original image
    center = np.uint8(center)
    res = center[label.flatten()]
    res2 = res.reshape((img.shape))
    return res2

# input and output paths
ipath = "C:/projets/oktal-se/sourceimages/"
opathe = "C:/projets/oktal-se/tiles_richness"
opathle = "C:/projets/oktal-se/tiles_less_richness"

# now loop on source images to create pairs

for ifile,f in enumerate(os.listdir(ipath)):
   
    print("processing source image",f)
    # make sure to read files with unicode characters in name
    filename, file_extension = os.path.splitext(f)
    file=ipath+file_extension
    shutil.copy(ipath+"/"+f, file)
    im =   cv2.imread(file)
    # reduce image richness with KMeans
    reduced=reduce_richness(im)
    # Current Image height and width
    imgheight=im.shape[0]
    imgwidth=im.shape[1]
    # Shift for clipping to image size
    verticalshift = 255
    horizontalshift = 255
    # image size as a factor of stride span
    w=16*60
    h=16*42
    for y in range(0,imgheight-h,verticalshift):
        for x in range(0, imgwidth-w+1, horizontalshift):
            source_tile = im[y:y+h,x:x+w]
            reduced_tile = reduced[y:y+h,x:x+w]
            cv2.imwrite(opathe+ "/img" + str(ifile)+'_' + str(x) + '_' + str(y)+".png",source_tile)
            cv2.imwrite(opathle+ "/img" + str(ifile)+'_' + str(x) + '_' + str(y)+".png",reduced_tile)
