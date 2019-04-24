
# Datamodel: spiderstargetAGN-SPIDERS_XMMSL_AGN



#### General Description
The spiderstargetAGN file contains information about SPIDERS AGN
  targets selected in XMM Slew survey data: the <a href="http://www.cosmos.esa.int/web/xmm-newton/xmmsl1d-ug">XMMSL1 catalogue</a> (Saxton
  et al. 2008). It contains information on the X-ray origin of the targets
  as well as on the WISE photometry involved in the bayesian
  association process.


#### Naming Convention
spiderstargetAGN-{TARGET_TYPE}-{version}


#### Approximate Size
1 MB


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
| **TARGET_VERSION** | string | 		 | The version
  of the targeting |
| **X_RAY** | string | 		 | Type of X-ray data |
| **PHOTO_SWEEP** | string | 		 | Basename of the
  sweep files |
| **NOBJ** | int32 | 		 | Number of objects in the
file |


## HDU2: TARGET INFORMATION
This HDU contains the actual information on the targets
Note: XRAY_OBSID: For the SPIDERS_XMMSL_AGN targets this column gives the Observation Identifier (OBSID) for the XMM-Newton observation in which the target was detected.

### HDU Type
IMAGE




		Required Data Table Columns


| **Name** | **Type** | **Unit** | **Description** |
| :--- | :----- | :---- | :------- |
| **RA** | float64 | deg | RA (from the SDSS DR13 imaging catalogue) |
| **DEC** | float64 | deg | DEC (from the SDSS DR13 imaging catalogue) |
| **FIBER2MAG** | float32[5] | 		 | fiber2
  magnitudes (u,g,r,i,z) (from the SDSS DR13 imaging catalogue) |
| **RUN** | int32 | 		 | (from the SDSS DR13 imaging catalogue) |
| **RERUN** | string | 		 | (from the SDSS DR13 imaging catalogue) |
| **CAMCOL** | int32 | 		 | (from the SDSS DR13 imaging catalogue) |
| **FIELD** | int32 | 		 | (from the SDSS DR13 imaging catalogue) |
| **ID** | int32 | 		 | (from the SDSS DR13 imaging catalogue) |
| **PRIORITY** | int32 | 		 | Internal SPIDERS
  targeting priority (highest=0 ... 80=lowest) |
| **XRAY_SRC_NAME** | string | 		 | Name of the
  original X-ray source (XRAY origin: see HDU1) |
| **XRAY_RA** | float64 | deg | RA (J2000) of the original
  X-ray source (XRAY origin: see HDU1) |
| **XRAY_DEC** | float64 | deg | DEC (J2000) of
  the original X-ray source (XRAY origin: see HDU1) |
| **XRAY_RADEC_ERR** | float32 | arcsec | The
  positional uncertainty of the X-ray source (XRAY origin: see HDU1) |
| **XRAY_FLUX** | float64[3] | ergs/s/cm^2 | The
  estimated total-, hard- and soft-band
  fluxes extracted from the XMMSL1 catalogue (XRAY origin: see
  HDU1) |
| **XRAY_DET_ML** | float64[3] | 		 | The total-,
  hard- and soft-band source detection likelihoods from the XMMSL1 catalogue
  (XRAY origin: see HDU1)
<tr><td>BAYES_POSTERIOR_PROB</td><td>float32</td><td> </td><td>The
  posterior probability that the AllWise source is the mid-IR
  counterpart to the X-ray detection (XRAY origin: see HDU1)</td></tr>
<tr><td>XRAY_OBSID</td><td>string</td><td> </td><td>X-ray
  Observation identifier (XRAY origin: see HDU1)</td></tr>
<tr><td>ALLWISE_DESIGNATION</td><td>string</td><td> </td><td>Source name of the AllWISE counterpart corresponding to the 'designation' column of the ALLWISE catalogue, in the form: hhmmss.ss+ddmmss.s.</td></tr>
<tr><td>ALLWISE_RA</td><td>float64</td><td>deg</td><td>RA (J2000)
  given in the AllWISE catalogue</td></tr>
<tr><td>ALLWISE_DEC</td><td>float64</td><td>deg</td><td>DEC (J2000)
  given in the AllWISE catalogue</td></tr>
<tr><td>ALLWISE_RADEC_ERR</td><td>float32</td><td>arcsec</td><td>The
  source position uncertainty used for cross-matching, derived from
  the value given in the AllWISE catalogue</td></tr>
<tr><td>ALLWISE_W2MPRO</td><td>float32</td><td>mag</td><td>4.6um Vega
  magnitude given in the AllWISE catalogue</td></tr>
<tr><td>ALLWISE_W1_W2</td><td>float32</td><td>mag</td><td>[3.4um-4.6um]
colour (Vega) derived from the w1mpro and w2mpro given in the AllWISE catalogue</td></tr> |
| **BAYES_POSTERIOR_PROB** | float32 | 		 | The
  posterior probability that the AllWise source is the mid-IR
  counterpart to the X-ray detection (XRAY origin: see HDU1) |
| **XRAY_OBSID** | string | 		 | X-ray
  Observation identifier (XRAY origin: see HDU1) |
| **ALLWISE_DESIGNATION** | string | 		 | Source name of the AllWISE counterpart corresponding to the 'designation' column of the ALLWISE catalogue, in the form: hhmmss.ss+ddmmss.s. |
| **ALLWISE_RA** | float64 | deg | RA (J2000)
  given in the AllWISE catalogue |
| **ALLWISE_DEC** | float64 | deg | DEC (J2000)
  given in the AllWISE catalogue |
| **ALLWISE_RADEC_ERR** | float32 | arcsec | The
  source position uncertainty used for cross-matching, derived from
  the value given in the AllWISE catalogue |
| **ALLWISE_W2MPRO** | float32 | mag | 4.6um Vega
  magnitude given in the AllWISE catalogue |
| **ALLWISE_W1_W2** | float32 | mag | [3.4um-4.6um]
colour (Vega) derived from the w1mpro and w2mpro given in the AllWISE catalogue |



