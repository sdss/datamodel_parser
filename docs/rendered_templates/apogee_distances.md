
# Data Model: APOGEE_Distances



#### General Description
The APOGEE Distance Catalog contains four sets of distances (BPG, NAOC,
  NICE, NMSU) for the stars associated with DR14
  (apogee_distances-DR14.fits; 31 columns, 277,731 rows).  Note that
  distance values have not been provided for all DR14 stars.  Additionally,
  the distance determinations rely upon the DR14 calibrated stellar atmospheric
  parameters.  Further information may be found in the <a href="http://www.sdss.org/vac/apogee-dr14-based-distance-estimations/">DR14
  Documentation</a> and, when applicable, in the specified publication.<br/><br/>


#### Naming Convention
<code>apogee_distances-DR14.fits</code>


#### Approximate Size
277371 entries; 86 MB


#### File Type
FITS


## Page Contents
* [HDU0: NULL EXTENSION](#hdu0-null-extension)
* [HDU1: APOGEE DISTANCE CATALOG](#hdu1-apogee-distance-catalog)

## HDU0: NULL EXTENSION
This is a null header.




## HDU1: APOGEE DISTANCE CATALOG
HDU 1 contains the catalog as a binary table documented below. The
  table includes distance estimates from 4 groups labeled as BPG,
  NAOC, NICE, and NMSU). Both the APOGEE_ID and the ASPCAP_ID (<a href="https://data.sdss.org/datamodel/files/APOGEE_REDUX/APRED_VERS/APSTAR_VERS/ASPCAP_VERS/RESULTS_VERS/allStar.html">allStar</a>
  catalog) are given for each table entry.

### HDU Type
IMAGE



		Columns


| **Key** | **Value** | **Type** | **Comment** |
| :--- | :----- | :---- | :------- |
| **APOGEE_ID** | Char[20] | 		 | 2MASS-STYLE Object Name | 
| **ASPCAP_ID** | Char[50] | 		 | ASPCAP ID | 
| **BPG_dist05** | Float32 | kpc | BPG StarHorse 5th posterior distance percentile (Bayesian; Santiago et al. 2016, Queiroz et al. 2017) | 
| **BPG_dist16** | Float32 | kpc | BPG StarHorse 16th posterior distance percentile (Bayesian; Santiago et al. 2016, Queiroz et al. 2017) | 
| **BPG_dist50** | Float32 | kpc | BPG StarHorse median posterior distance (Bayesian; Santiago et al. 2016, Queiroz et al. 2017) | 
| **BPG_dist84** | Float32 | kpc | BPG StarHorse 84th posterior distance percentile (Bayesian; Santiago et al. 2016, Queiroz et al. 2017) | 
| **BPG_dist95** | Float32 | kpc | BPG StarHorse 95th posterior distance percentile (Bayesian; Santiago et al. 2016, Queiroz et al. 2017) | 
| **BPG_meandist** | Float32 | kpc | BPG StarHorse mean posterior distance (Bayesian; Santiago et al. 2016, Queiroz et al. 2017) | 
| **BPG_diststd** | Float32 | kpc | BPG StarHorse posterior distance standard deviation (Bayesian; Santiago et al. 2016, Queiroz et al. 2017) | 
| **BPG_AV05** | Float32 | kpc | BPG StarHorse 5th posterior A(V) percentile (Bayesian; Santiago et al. 2016, Queiroz et al. 2017) | 
| **BPG_AV16** | Float32 | kpc | BPG StarHorse 16th posterior A(V) percentile (Bayesian; Santiago et al. 2016, Queiroz et al. 2017) | 
| **BPG_AV50** | Float32 | kpc | BPG StarHorse median posterior A(V) (Bayesian; Santiago et al. 2016, Queiroz et al. 2017) | 
| **BPG_AV84** | Float32 | kpc | BPG StarHorse 84th posterior A(V) percentile (Bayesian; Santiago et al. 2016, Queiroz et al. 2017) | 
| **BPG_AV95** | Float32 | kpc | BPG StarHorse 95th posterior A(V) percentile (Bayesian; Santiago et al. 2016, Queiroz et al. 2017) | 
| **BPG_meanAV** | Float32 | kpc | BPG StarHorse mean posterior A(V) (Bayesian; Santiago et al. 2016, Queiroz et al. 2017) | 
| **BPG_AVstd** | Float32 | kpc | BPG StarHorse posterior A(V) standard deviation (Bayesian; Santiago et al. 2016, Queiroz et al. 2017) | 
| **BPG_INPUTFLAGS** | char[80] | 		 | BPG StarHorse Inputflags (Queiroz et al. 2017) | 
| **BPG_OUTPUTFLAGS** | char[50] | 		 | BPG StarHorse Outputflags (Queiroz et al. 2017) | 
| **NAOC_dist** | Float32 | kpc | NAOC Distance (Bayesian; Wang et al. 2016) | 
| **NAOC_err_dist** | Float32 | kpc | NAOC Distance Error (Bayesian; Wang et al. 2016) | 
| **NAOC_parallax** | Float32 | mas | NAOC Parallax (Bayesian; Wang et al. 2016) | 
| **NAOC_err_parallax** | Float32 | mas | NAOC Parallax Error (Bayesian; Wang et al. 2016) | 
| **NAOC_AK** | Float32 | mag | NAOC Extinction A_Ks (Bayesian; Wang et al. 2016) | 
| **NAOC_err_AK** | Float32 | mag | NAOC Extinction Error (Bayesian; Wang et al. 2016) | 
| **NICE_dist** | Float32 | kpc | NICE Distance (Isochrone Matching; Schultheis et al. 2014) | 
| **NICE_err_dist** | Float32 | kpc | NICE Distance Error (Isochrone Matching; Schultheis et al. 2014) | 
| **NICE_E_JK** | Float32 | mag | NICE Reddening E_JK (Isochrone Matching; Schultheis et al. 2014) | 
| **NMSU_dist** | Float64 | kpc | NMSU Distance (Bayesian; Holtzman et al.) | 
| **NMSU_dist_err** | Float64 | kpc | NMSU Distance Error (Bayesian; Holtzman et al.) | 
| **NMSU_dist_prior** | Float64 | kpc | NMSU Distance with density model prior (Bayesian; Holtzman et al.) | 
| **NMSU_dist_prior_err** | Float64 | kpc | NMSU Distance Error with density model prior (Bayesian; Holtzman et al.) | 




