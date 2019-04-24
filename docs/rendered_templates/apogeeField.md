
# Data model: apogeeField



#### General Description
This file contains the parameters of all APOGEE fields in a given data release.


#### Naming Convention
<code>apogeeField_DR[N].fits</code>


#### Approximate Size
14 KB


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
| **RA** | 		 | float64 | Right ascension of field center (J2000.0, deg) | 
| **DEC** | 		 | float64 | Declination of field center (J2000.0, deg) | 
| **LOCATION_ID** | 		 | int32 | Field location ID | 
| **FIELD_NAME** | 		 | string | Field name | 
| **EXPECTED_NO_OF_VISITS** | 		 | int32 | Number of visits anticipated for field (may differ from actual number of visits achieved) | 




