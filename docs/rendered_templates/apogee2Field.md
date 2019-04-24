
# Data model: apogee2Field



#### General Description
This file contains the parameters of all APOGEE-2 fields in a given data release.


#### Naming Convention
<code>apogee2Field.fits</code>


#### Approximate Size
50 KB


#### File Type
FITS


#### Read by Products
none


#### Written by Products
none


## Page Contents
* [HDU1: TABLE WITH CATALOG OF APOGEE FIELDS](#hdu1-table-with-catalog-of-apogee-fields)

## HDU1: TABLE WITH CATALOG OF APOGEE FIELDS


### HDU Type
IMAGE



		Required Columns


| **Key** | **Value** | **Type** | **Comment** |
| :--- | :----- | :---- | :------- |
| **FIELD_NAME** | 		 | string | Field name | 
| **RA** | 		 | float64 | Right ascension of field center (deg) | 
| **DEC** | 		 | float64 | Declination of field center (deg) | 
| **GLON** | 		 | float64 | Galactic Longitude of field center (deg) | 
| **GLAT** | 		 | float64 | Galactic Latitude of field center (deg) | 
| **LOCATION_ID** | 		 | int32 | Field location ID | 
| **EXPECTED_NO_OF_DESIGNS** | 		 | int32 | Number of designs anticipated for field (may differ from actual number of designs made) | 
| **NO_OF_DESIGNS_COMPLETED** | 		 | int32 | Number of designs made for field by the DR cutoff date | 
| **EXPECTED_NO_OF_VISITS** | 		 | int32 | Number of visits anticipated for field (may differ from actual number of visits achieved) | 




