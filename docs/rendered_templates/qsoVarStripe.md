
# Datamodel: qsoVarStripe



#### General Description
This "QSO variability" VAC provides additionnal photometric variability data for the DR13 QSO targets as well for the Stripe82. It extends to a larger number of objects the variability informations that were already provided within the DR12Q catalog.

The file spec "qsoVarStripe" contains additional informations derived from essentially all multi-epoq SDSS photometry carried out in the Stripe 82 region.


#### Naming Convention
<code>qsoVarStripe.fits</code>


#### Approximate Size
10 MB


#### File Type
FITS


#### Read by Products
None


#### Written by Products
build_qsovar_dr13vac.py


## Page Contents
* [HDU1: QSOVARSTRIPE CATALOG](#hdu1-qsovarstripe-catalog)

## HDU1: QSOVARSTRIPE CATALOG
This HDU has no non-standard required keywords.

### HDU Type
IMAGE




		Required Data Table Columns


| **Name** | **Type** | **Unit** | **Description** |
| :--- | :----- | :---- | :------- |
| **VAR_OBJID** | int64 | - | ObjId |
| **RA** | float64 | deg | RA (DR12 astrometry) |
| **DEC** | float64 | deg | DEC (DR12 astrometry) |
| **VAR_CHI2** | float64 | - | Reduced chi2 when the light curve is adjusted to a constant |
| **VAR_A** | float64 | - | Structure function parameter A as defined in Palanque-Delabrouille et al. (2011) |
| **VAR_GAMMA** | float64 | - | Structure function parameter gamma as defined in Palanque-Delabrouille et al. (2011) |
| **NEPOQS** | int32 | - | Number of epoqs (SDSS observations) used in lightcurve |
| **CHI2_U** | float64 | - | Reduced chi2 in u band |
| **CHI2_G** | float64 | - | Reduced chi2 in g band |
| **CHI2_R** | float64 | - | Reduced chi2 in r band |
| **CHI2_I** | float64 | - | Reduced chi2 in i band |
| **CHI2_Z** | float64 | - | Reduced chi2 in z band |
| **VAR_NN** | float64 | - | Variability neural network output to discriminate stars against QSO |
| **MJD_FIRST** | float64 | - | MJD for the first observation |
| **MJD_LAST** | float64 | - | MJD for the last observation |



