import pandas as pd

import numpy as np

import gc

from geotiffio import readtif
from geotiffio import createtif
from geotiffio import writetif

from aggregate_raster_classes import swapValues

gc.collect()

# read images (variable of interest and associated quality product) 
dataset,rows,cols,bands = readtif("D:/Julian/64_ie_maps/madmex/madmex_lcc_landsat_2000_v4.3.1.tif")

# image metadata
projection = dataset.GetProjection()
transform = dataset.GetGeoTransform()
driver = dataset.GetDriver()
				
# make numpy array and flatten
band = dataset.GetRasterBand(1)
band = band.ReadAsArray(0, 0, cols, rows).astype(np.int16)
print("tamanio")
print(rows)
print(cols)
print(np.shape(band))
print("")
band = np.ravel(band)

print(np.shape(band))

# remove missing values from class swapping
gooddata_idx = band != 0
gooddata = band[gooddata_idx]

print(np.shape(gooddata))

# # raster with aggregated classes
# aggregated = swapValues(gooddata,[\
# 	                           #[1,2,3,4,5,6,7,8,9,10,11,12,13,16,17,18,19,21,22,23,],\
# 	                           #[14,15,20,24,25,26,],\
# 	                           [1],\
# 	                           [14],\
# 	                           [28],\
# 	                           [27],\
# 	                           [5],\
# 	                           [30],\
# 	                           [29],\
# 	                          ],\
# 							[1,2,3,4,5,6,7])

# print(np.shape(aggregated))

# band[gooddata_idx] = aggregated

# print(np.shape(band))

# set up output
outData = createtif(driver, rows, cols, 1,"D:/Julian/64_ie_maps/madmex/madmexipcc.tif",16)


writetif(outData,band, projection, transform, order='r')

# close dataset properly
outData = None	

	


