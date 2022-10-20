# Sampling Box
Tool to analyze a volume image regarding the vessel fraction in sampling boxes with adjustable edge length and at 
desired locations.

Needs an existing nrrd-file containing a label image and a .csv-file containing sampling locations as input. 

Output is a .csv-file containing number of foreground voxels (value != 0), background voxels (value = 0) and 
fraction of foreground voxels in the sample box.

## Requirements
Required packages are listed in requirements.txt and can be installed using pip as follows:\
`pip3 install -r requirements.txt`

## Usage
To use this program you need to supply a .nrrd-file which contains a volume image, a .csv-file with coordinates of 
the desired sampling box centres, separated by ',' (x, y, z) and one coordinate triplet per row and an integer edge 
length of the isometric sampling box (e.g. 100 voxels) used for analysis. As an optional argument output name file can 
be supplied, otherwise results will be written in results.csv.

`python3 sampling_box.py filename.nrrd sampling_points.csv 100 -o outputfile`
