# Analysis routines for "An integrated framework for quantifying immune-tumour interactions in a 3D co-culture model"

## Usage notes
Matlab routines (TcellTraffickingAnalysis.m) perform the segmentation-based trafficking analysis.
Edit lines 6-10 for the path to the data. The code assumes files will in separate folders for each experiment and time point, and each each folder files will be listed by group and sample.

The code stores several trafficking measures in tables than can be accesed through Matlab's variable explorer.

Python routines (kmeans.py) perform the k-means based analysis. It uses background.py to access the data files and extract the relevant information (e.g. vector of red levels across the image).
 - `do_iterations_mp` trains a k-means model using the images in `imlist` (file names) and the starting value `means`. It uses Python's `multiprocessing` to speed up the process.
 - `my_trafficking` compute the trafficking measure for a given image `im` and a trained k-means model `km`. 

The code can be easily scripted to produce tables of results for a collection of images


### Code authorship:
E. Campillo-Funollet, F. Yang 
