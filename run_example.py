import pandas as pd

import numpy as np

import gc

from geotiffio import readtif
from geotiffio import createtif
from geotiffio import writetif

from mo_functions import swapValues

gc.collect()

# read images (variable of interest and associated quality product) 
dataset,rows,cols,bands = readtif("E:/work/20150731_multi_scale_classif/madmex_lcc_landsat_2000_v4.3.1.tif")

# image metadata
projection = dataset.GetProjection()
transform = dataset.GetGeoTransform()
driver = dataset.GetDriver()
				
# make numpy array and flatten
band = dataset.GetRasterBand(1)
band = band.ReadAsArray(0, 0, cols, rows).astype(np.int16)
band = np.ravel(band)

# remove missing values from class swapping
gooddata_idx = band != 0
gooddata = band[gooddata_idx]

# raster with aggregated classes
aggregated = swapValues(gooddata,[\
	                           [1,2,3,8,9,10,11,12,13,16],\
	                           [4,5,6,7,17,18,19,21,22,23],\
	                           [14,15,20,24,25,26],\
	                           [27],\
	                           [28],\
	                           [29],\
	                           [30],\
	                           [31],\
	                          ],\
							[1,2,3,4,5,6,7,8])


band[gooddata_idx] = aggregated

# set up output
outData = createtif(driver, rows, cols, 1,"E:/work/20150731_multi_scale_classif/madmexipcc_8_2.tif",16)


writetif(outData,band, projection, transform)

# close dataset properly
outData = None	

	


