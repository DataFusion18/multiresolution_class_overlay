import pandas as pd

import numpy as np

from geotiffio import readtif
from geotiffio import createtif
from geotiffio import writetif

from osgeo import gdal
from osgeo.gdalconst import GA_ReadOnly 
from osgeo.gdalconst import GDT_Float32
from osgeo.gdalconst import GDT_Int16

gdal.UseExceptions()

def swapValues(flattenedNumpyArray,listOfInLists,listOfSwappingValues):
	'''

	takes each list in tlistOfInLists and swaps it by the
	corresponding value in listOfSwappingValues

	'''
	aux=flattenedNumpyArray
	if len(listOfInLists)!=len(listOfSwappingValues):
		print("lists must be of the same length")
	else:
		for i in xrange(len(listOfInLists)):
			# list to numpy array
			nparray = np.array(listOfInLists[i])
			print(nparray)
			found_idx = np.in1d(flattenedNumpyArray,nparray)
			print(listOfSwappingValues[i])
			aux[found_idx]=listOfSwappingValues[i]
	return(aux)


def multispectralToBits(multispec_raster_path,class_ids=[1,2,3,4,5,6,7,8]):
	# Get data from raster with classifications
	ds = gdal.Open(multispec_raster_path)
	band = ds.GetRasterBand(1)
	class_ar = band.ReadAsArray()
	gt = ds.GetGeoTransform()
	pj = ds.GetProjection()
	ds = band = None  # close

	# Define the raster values for each class, to relate to each band
	class_ids =  class_ids

	# Make a new bit rasters
	drv = gdal.GetDriverByName('GTiff')
	ds = drv.Create('bit_raster.tif', class_ar.shape[1], class_ar.shape[0],
		len(class_ids), gdal.GDT_Byte, ['NBITS=1'])
	ds.SetGeoTransform(gt)
	ds.SetProjection(pj)
	for bidx in range(ds.RasterCount):
		print(bidx)
		band = ds.GetRasterBand(bidx + 1)
		# create boolean result where 0 == no and 1 == yes
		selection = (class_ar == class_ids[bidx]).astype("u1")
		band.WriteArray(selection)
	ds = band = None  # save, close