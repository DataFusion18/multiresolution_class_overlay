import pandas as pd

import numpy as np

import gc

from geotiffio import readtif
from geotiffio import createtif
from geotiffio import writetif

from mo_functions import swapValues

gc.collect()

# read images (variable of interest and associated quality product) 
dataset,rows,cols,bands = readtif("D:/work/20161113_integridad250/MADMEX_NALCMS30m/madmex_lcc_landsat_2010_v4.3_rec_nalcms_final_roadnetwork_islands.tif")

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
	                           [1,2,5,6],\
	                           [3,4],\
	                           [7,8,11],\
	                           [10,12],\
	                           [13,16],\
	                           [14],\
	                           [9,15],\
	                           [17],\
	                           [18],\
	                           [19]
	                          ],\
							[1,2,3,4,5,6,7,8,9,10])

# 1,2,5,6 - 1 bosque
# 3,4     - 2 selvas
# 7,8,11  - 3 matorrales
# 10,12 - 4 pastizal 
# 13,16   - 5 suelo desnudo
# 14      - 6 humedal
# 9,15      - 7 agricultura
# 17      - 8 asentamiento humano
# 18      - 9 agua
# 19      - 10 nieve y hielo

band[gooddata_idx] = aggregated

# set up output
outData = createtif(driver, rows, cols, 1,"D:/work/20170928_reportes_auto_conanp/madmex_nalc_10c_30m_2010.tif",16)


writetif(outData,band, projection, transform)

# close dataset properly
outData = None	

	


