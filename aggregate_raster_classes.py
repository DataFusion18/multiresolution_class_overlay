import pandas as pd

import numpy as np

from geotiffio import readtif
from geotiffio import createtif
from geotiffio import writetif

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
