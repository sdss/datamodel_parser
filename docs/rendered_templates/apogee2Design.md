
# Data model: apogee2Design



#### General Description
This file contains the parameters of all APOGEE-2 designs in a given data release.


#### Naming Convention
<code>apogee2Design.fits</code>


#### Approximate Size
50 KB


#### File Type
FITS


#### Read by Products
none


#### Written by Products
none


## Page Contents
* [HDU1: TABLE WITH CATALOG OF DESIGN PARAMETERS](#hdu1-table-with-catalog-of-design-parameters)

## HDU1: TABLE WITH CATALOG OF DESIGN PARAMETERS




		Required Columns


| **Key** | **Value** | **Type** | **Comment** |
| :--- | :----- | :---- | :------- |
| **TBD** | 		 | 		 | 		 | 
| **DESIGN_ID** | 		 | int32 | Design ID | 
| **LOCATION_ID** | 		 | int32 | Field location ID | 
| **RA** | 		 | float64 | Right ascension of design center | 
| **DEC** | 		 | float64 | Declination of design center | 
| **FIELD_NAME** | 		 | float64 | Name of design field | 
| **DESIGN_TYPE** | 		 | int32 | Galactic component or location that determines the rest of the design parameters | 
| **DESIGN_DRIVER** | 		 | int32 | One of "core", "goal", or other | 
| **RADIUS** | 		 | float32 | Field radius from which targets could be drawn (deg) | 
| **SHARED** | 		 | int32 | Boolean flag indicating whether this design included MARVELS targets (SHARED=1) or not (SHARED=0) | 
| **COMMENTS** | 		 | string | Additional comments on design | 
| **NUMBER_OF_VISITS** | 		 | int32 | Total number of visits intended for this design | 
| **NUMBER_OF_TELLURICS** | 		 | int32 | Number of hot star tellurics on this design (tellurics/science targets may overlap) | 
| **NUMBER_OF_SKY** | 		 | int32 | Number of blank sky positions on this design (sky/science targets may overlap) | 
| **NUMBER_OF_SCIENCE** | 		 | int32 | Number of science targets on this design (tellurics/sky/science targets may overlap) | 
| **COHORT_SHORT_VERSION** | 		 | int32 | Which of this field's short cohorts is in this design | 
| **COHORT_MEDIUM_VERSION** | 		 | int32 | Which of this field's medium cohorts is in this design | 
| **COHORT_LONG_VERSION** | 		 | int32 | Which of this field's long cohorts is in this design | 
| **COHORT_FRACTION** | 		 | int32[3] | Fraction of this design's targets in each cohort | 
| **COHORT_MIN_H** | 		 | float32[3] | Minimum H mag of the cohorts | 
| **COHORT_MAX_H** | 		 | float32[3] | Minimum H mag of the cohorts | 
| **COHORT_NUMBER_OF_VISITS** | 		 | float32[3] | Number of visits planned for the cohorts | 
| **NUMBER_OF_SELECTION_BINS** | 		 | int32 | Number of selection bins used within a cohort | 
| **BIN_FRACTION** | 		 | int32[5] | Fraction of fibers in each selection bin | 
| **BIN_PRIORITY** | 		 | int32[5] | Which selection bins were used | 
| **BIN_USE_WD_FLAG** | 		 | int32[5] | Which bins had W+D photometry used | 
| **BIN_DEREDDENED_MIN_JK_COLOR** | 		 | int32[5] | Minimum (J-Ks)o for each selection bin | 
| **BIN_DEREDDENED_MAX_JK_COLOR** | 		 | int32[5] | Maximum (J-Ks)o for each selection bin | 




