
# Data model: apogeeDesign



#### General Description
This file contains the parameters of all APOGEE designs in a given data release.


#### Naming Convention
<code>apogeeDesign_DR[N].fits</code>


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
| **RA** | 		 | float64 | Right ascension of design center | 
| **DEC** | 		 | float64 | Declination of design center | 
| **LOCATION_ID** | 		 | int32 | Field location ID | 
| **RADIUS** | 		 | float32 | Field radius from which targets could be drawn (deg) | 
| **SHARED** | 		 | int32 | Boolean flag indicating whether this design included MARVELS targets (SHARED=1) or not (SHARED=0) | 
| **COMMENTS** | 		 | string | Additional comments on design | 
| **SHORT_COHORT_VERSION** | 		 | int32 | Which of this field's short cohorts is in this design | 
| **MEDIUM_COHORT_VERSION** | 		 | int32 | Which of this field's medium cohorts is in this design | 
| **LONG_COHORT_VERSION** | 		 | int32 | Which of this field's long cohorts is in this design | 
| **NUMBER_OF_SHORT_FIBERS** | 		 | int32 | Number of fibers alloted to short cohort targets (OR ACTUAL DRILLED NUMBER OF SHORT COHORT TARGETS?) | 
| **NUMBER_OF_MEDIUM_FIBERS** | 		 | int32 | Number of fibers alloted to medium cohort targets (OR ACTUAL DRILLED NUMBER OF MEDIUM COHORT TARGETS?) | 
| **NUMBER_OF_LONG FIBERS** | 		 | int32 | Number of fibers alloted to long cohort targets (OR ACTUAL DRILLED NUMBER OF LONG COHORT TARGETS?) | 
| **SHORT_COHORT_MIN_H** | 		 | float32 | Minimum H mag of short cohort | 
| **SHORT_COHORT_MAX_H** | 		 | float32 | Maximum H mag of short cohort | 
| **MEDIUM_COHORT_MIN_H** | 		 | float32 | Minimum H mag of medium cohort | 
| **MEDIUM_COHORT_MAX_H** | 		 | float32 | Maximum H mag of medium cohort | 
| **LONG_COHORT_MIN_H** | 		 | float32 | Minimum H mag of long cohort | 
| **LONG_COHORT_MAX_H** | 		 | float32 | Maximum H mag of long cohort | 
| **DEREDDENED_MIN_J_KS_COLOR** | 		 | float32 | Minimum (J-Ks)o for this design; -1 if no color cut applied | 
| **NUMBER_OF_VISITS** | 		 | int32 | Total number of visits intended for this design | 
| **NUMBER_OF_TELLURICS** | 		 | int32 | Number of hot star tellurics on this design (tellurics/science targets may overlap) | 
| **NUMBER_OF_SKY** | 		 | int32 | Number of blank sky positions on this design (sky/science targets may overlap) | 
| **NUMBER_OF_SCIENCE** | 		 | int32 | Number of science targets on this design (tellurics/sky/science targets may overlap) | 




