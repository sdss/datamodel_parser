
# Data model: all ecam files



#### General Description
The engineering camera data is structured the same as that of the
<a href="/datamodel/files/GCAM_DATA/">guider</a>, but usually with no proc-gimg
files, as ecam data was not processed through the guider pipeline until MJD
57141. The proc-gimg files do not have the plate-view related HDUs, but HDU
1 and 2 are the same (processed image, mask).


