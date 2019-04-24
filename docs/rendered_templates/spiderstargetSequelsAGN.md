
# Datamodel: spiderstargetSequelsAGN



#### General Description
The spiderstargetAGN file contains information about SPIDERS AGN
  targets. It contains information on the X-ray origin of the targets
  as extracted from the RASS <a href="http://www.xray.mpe.mpg.de/rosat/survey/rass-bsc/">Bright</a> (Voges et
  al. 1999) and the <a href="http://www.xray.mpe.mpg.de/rosat/survey/rass-fsc/">Faint</a> (Voges et al. 2000) Source catalogues.


#### Naming Convention
spiderstargetSequelsAGN-{TARGET_TYPE}-{version}


#### Approximate Size
75 KB


#### File Type
FITS


## Page Contents
* [HDU1: TARGETING METADATA](#hdu1-targeting-metadata)
* [HDU2: TARGET INFORMATION](#hdu2-target-information)

## HDU1: TARGETING METADATA
This HDU contains a few information relative to the targeting process.

### HDU Type
IMAGE




		Required Data Table Columns


| **Name** | **Type** | **Unit** | **Description** |
| :--- | :----- | :---- | :------- |
| **TARGET_TYPE** | string | 		 | The target type |
| **TARGET_RUN** | string | 		 | The date of the targeting |
| **X_RAY** | string | 		 | Type of X-ray data |
| **NOBJ** | int32 | 		 | Number of objects in the file |


## HDU2: TARGET INFORMATION
This HDU contains the actual information on the targets

### HDU Type
IMAGE




		Required Data Table Columns


| **Name** | **Type** | **Unit** | **Description** |
| :--- | :----- | :---- | :------- |
| **RA** | float64 | deg | RA (from the SDSS DR9 imaging catalogue) |
| **DEC** | float64 | deg | DEC (from the SDSS DR9 imaging catalogue) |
| **FIBER2MAG** | float32[5] | 		 | fiber2
  magnitudes (u,g,r,i,z) (from the SDSS DR9 imaging catalogue) |
| **RUN** | int32 | 		 | (from the SDSS DR9 imaging catalogue) |
| **RERUN** | string | 		 | (from the SDSS DR9 imaging catalogue) |
| **CAMCOL** | int32 | 		 | (from the SDSS DR9 imaging catalogue) |
| **FIELD** | int32 | 		 | (from the SDSS DR9 imaging catalogue) |
| **ID** | int32 | 		 | (from the SDSS DR9 imaging catalogue) |
| **PRIORITY** | int32 | 		 | Internal SPIDERS
  targeting priority (highest=0 ... 50=lowest) |
| **RASS_SRC_NAME** | string | 		 | Name of the
  original RASS source |
| **RASS_RA** | float64 | deg | RA (J2000) of the
  original RASS source |
| **RASS_DEC** | float64 | deg | DEC (J2000) of the
  original RASS source |
| **RASS_RADEC_ERR** | float32 | arcsec | The
  positional uncertainty of the RASS source |
| **XRAY_FLUX** | float64 | ergs/s/cm^2 | The estimated [0.1-2.4] keV flux derived from the observed count rate using
  a conversion factor based on a model consisting of a power law with
  spectral index=2 and corrected for Galactic absorption.  A description of the procedure can be found in Coffey et al. (in prep.) |
| **XRAY_DET_ML** | float64 | 		 | The source
  detection likelihood from the RASS Bright Source and Faint Source Catalogues
<tr><td>BAYES_POSTERIOR_PROB</td><td>float32</td><td> </td><td>The
  posterior probability that the optical source is the counterpart to
  the RASS detection</td></tr> |
| **BAYES_POSTERIOR_PROB** | float32 | 		 | The
  posterior probability that the optical source is the counterpart to
  the RASS detection |



