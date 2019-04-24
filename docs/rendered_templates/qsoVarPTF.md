
# Datamodel: qsoVarPTF



#### General Description
This "QSO variability" VAC provides additionnal photometric variability data for the DR13 QSO targets as well for the Stripe82. It extends to a larger number of objects the variability informations that were already provided within the DR12Q catalog.

The file spec "qsoVarPTF" contains variability informations for most DR13 QSO targets (EBOSS_TARGET1=0,9,10,11,12), derived from the combination of SDSS and PTF photometries, on a large fraction of the eBOSS footprint. Due to the inhomogeneity of the PTF sky survey, the sensitivity of these variability measurements is highly variable as a function of sky coordinates.


#### Naming Convention
<code>qsoVarPTF.fits</code>


#### Approximate Size
46 MB


#### File Type
FITS


#### Read by Products
None


#### Written by Products
build_qsovar_dr13vac.py


## Page Contents
* [HDU1: QSOVARPTF CATALOG](#hdu1-qsovarptf-catalog)

## HDU1: QSOVARPTF CATALOG
This HDU has no non-standard required keywords.

### HDU Type
IMAGE




		Data Table Columns


| **Name** | **Type** | **Unit** | **Description** |
| :--- | :----- | :---- | :------- |
| **VAR_OBJID** | int64 | - | ObjId |
| **THING_ID_TARGETING** | int32 | - | ThingID, as in the DR13 target list |
| **RA** | float64 | deg | RA (DR12 astrometry) |
| **DEC** | float64 | deg | DEC (DR12 astrometry) |
| **VAR_MATCHED** | int16 | - | Number of epoqs used for the lightcurve construction. For SDSS, one epoq = a single observation. For PTF, one epoq = a set of (coadded) observations, typically from a few months to a year. There are at least two PTF and one SDSS epoq for each object. |
| **VAR_CHI2** | float64 | - | Reduced chi2 when the combined light curve is adjusted to a constant |
| **VAR_A** | float64 | - | Structure function parameter A as defined in Palanque-Delabrouille et al. (2011) |
| **VAR_GAMMA** | float64 | - | Structure function parameter gamma as defined in Palanque-Delabrouille et al. (2011) |



