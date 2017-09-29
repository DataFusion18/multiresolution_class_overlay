from osgeo import gdal

from geotiffio import readtif
from geotiffio import createtif
from geotiffio import writetif

import numpy as np

filename = r"D:/work/20170901_madmex_hansen/hansen_loss/hansen_forest_loss_v1_3.tif"
input_raster = gdal.Open(filename)
output_raster = r"D:/work/20170928_reportes_auto_conanp/hansen_forest_loss_v1_3_lcc.tif"
gdal.Warp(output_raster,input_raster,dstSRS="+proj=lcc +lat_1=17.5 +lat_2=29.5 +lat_0=12 +lon_0=-102 +x_0=2500000 +y_0=0 +datum=WGS84 +units=m +no_defs +ellps=WGS84 +towgs84=0,0,0",multithread=True)

# read images (variable of interest and associated quality product) 
dataset,rows,cols,bands = readtif("D:/work/20170928_reportes_auto_conanp/hansen_forest_loss_v1_3_lcc.tif")

# image metadata
projection = dataset.GetProjection()
transform = dataset.GetGeoTransform()
driver = dataset.GetDriver()
				
# make numpy array and flatten
band = dataset.GetRasterBand(1)
band = band.ReadAsArray(0, 0, cols, rows).astype(np.int16)
band = np.ravel(band)

# set up output
outData = createtif(driver, rows, cols, 1,"D:/work/20170928_reportes_auto_conanp/hansen_forest_loss_v1_3_lcc.tif",16)

writetif(outData,band, projection, transform)

# close dataset properly
outData = None	