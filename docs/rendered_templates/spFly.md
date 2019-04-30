
# Datamodel: spFly



#### General Description
This page documents the lowest level outputs of the run of the <a href="https://svn.sdss.org/repo/sdss/firefly/tags/v1_0_4/">firefly galaxy product</a> on the DR14 SDSS single spectra files. 
For DR14, the version of firefly used is FIREFLY_VER=v1_0_4

This file contains the model spectra obtained when fitting the stellar population parameters with the firefly software. 
For the data release 14 exist one such file per spectra classified as a galaxy with a definite positive redshift by the pipeline. 
This file contains the complete outputs of firefly.

This <a href="http://www.sdss.org/dr14/spectro/eboss-firefly-value-added-catalog/">page</a> describes the Firefly galaxy product.


#### Naming Convention
<code>FIREFLY_VER/RUN2D/stellarpop/PLATE/spFly-PLATE-MJD-FIBERID.fits</code> where RUN2D=[v5_10_0,26] for eBOSS and SDSS in dr14


#### Approximate Size
Less than 1 MB


#### File Type
FITS


#### Read by Products
sas, firefly


#### Written by Products
sas, firefly



## Page Contents
* [HDU0: THE PRIMARY HEADER](#hdu0-the-primary-header)
* [HDU1: STELLAR POPULATION MODEL RESULTS](#hdu1-stellar-population-model-results)

## HDU0: THE PRIMARY HEADER
The primary header contains global information about the run.

### HDU Type
IMAGE



		Required Header Keywords


| **Key** | **Value** | **Type** | **Comment** |
| :--- | :----- | :---- | :------- |
| **FILE** | file name | str | 'spFly-2313-53726-0140.fits' | 
| **PLATE** | plate number | int | 2313 | 
| **MJD** | modified julian date of the observation | int | 53726 | 
| **FIBERID** | fiber identifier | int | 0140 | 
| **MODELS** | Models used, here Maraston et al. 2011 | str | 'Maraston_2011' | 
| **FITTER** | Name of the fitter | str | 'FIREFLY' | 
| **AGEMIN** | Minimum log10(stellar age / yr) | float | 		 | 
| **AGEMAX** | Maximum log10(stellar age / yr) | float | 		 | 
| **ZMIN** | Minimum log10(stellar metallicity / solar metallicity) | float | 		 | 
| **ZMAX** | Maximum log10(stellar metallicity / solar metallicity) | float | 		 | 
| **redshift** | Redshift used for the fitting | float | 		 | 
| **age_universe** | Age of the Universe at this redshift [Gyr] | float | 		 | 



## HDU1: STELLAR POPULATION MODEL RESULTS
Each hdu contains the best model spectrum (wavelength and model flux in the .data extension) and the corresponding parameters (given in the in .header). In each hdu were assumed different stellar libraries and initial mass function (IMF). The default value for an empty cell is -9999.<li>HDU1: MILES library and Chabrier IMF</li>
<li>HDU2: MILES library and Salpeter IMF</li>
<li>HDU3: MILES library and Kroupa IMF</li>
<li>HDU4: ELODIE library and Chabrier IMF</li>
<li>HDU5: ELODIE library and Salpeter IMF</li>
<li>HDU6: ELODIE library and Kroupa IMF</li>
<li>HDU7: STELIB library and Chabrier IMF</li>
<li>HDU8: STELIB library and Salpeter IMF</li>
<li>HDU9: STELIB library and Kroupa IMF</li>



		<h3>Data: model spectrum of the stellar population model</h3>


| **Key** | **Value** | **Type** | **Comment** |
| :--- | :----- | :---- | :------- |
| **IMF** | Name of the IMFi: 'Chabrier', 'Kroupa' or 'Salpeter' | str | 		 | 
| **library** | Name of the stellar library used: 'MILES', 'ELODIE' or 'STELIB' | str | 		 | 
| **converged** | Did the fit converge ? | boolean | 		 | 
| **age_lightW** | log10( light weighted age / yr ) - 9 | float64 | 		 | 
| **age_lightW_up** | log10( light weighted age upper value / yr ) - 9 | float64 | 		 | 
| **age_lightW_low** | log10( light weighted age lower value / yr ) - 9 | float64 | 		 | 
| **metallicity_lightW** | log10( light weighted stellar metallicity / solar metallicity ) | float64 | 		 | 
| **metallicity_lightW_up** | log10( light weighted stellar metallicity upper value / solar metallicity ) | float64 | 		 | 
| **metallicity_lightW_low** | log10( light weighted stellar metallicity lower value / solar metallicity ) | float64 | 		 | 
| **age_massW** | log10( mass weighted age / yr ) - 9 | float64 | 		 | 
| **age_massW_up** | log10( mass weighted age upper value / yr ) - 9 | float64 | 		 | 
| **age_massW_low** | log10( mass weighted age lower value / yr ) - 9 | float64 | 		 | 
| **metallicity_massW** | log10( mass weighted stellar metallicity / solar metallicity ) | float64 | 		 | 
| **metallicity_massW_up** | log10( mass weighted stellar metallicity upper value / solar metallicity ) | float64 | 		 | 
| **metallicity_massW_low** | log10( mass weighted stellar metallicity lower value / solar metallicity ) | float64 | 		 | 
| **stellar_mass** | log10( stellar mass / solar mass ) | float64 | 		 | 
| **stellar_mass_up** | log10( stellar mass upper value / solar mass ) | float64 | 		 | 
| **stellar_mass_low** | log10( stellar mass lower value / solar mass ) | float64 | 		 | 
| **EBV** | reddenning fitted, E(B-V) | float64 | 		 | 
| **ssp_number** | number of single stellar population components, up to 8 SSPs are written | int | 		 | 
| **stellar_mass_ssp_$i** | log10( Stellar mass of the SSP / solar mass ) | float | 		 | 
| **age_ssp_$i** | log10( Age of the SSP / yr ) - 9 | float | 		 | 
| **metal_ssp_$i** | log10( Metallicity of the SSP / solar metallicity ) | float | 		 | 
| **SFR_ssp_$i** | Star formation rate of the SSP [solar mass per year] | float | 		 | 
| **weightMass_ssp_$i** | mass weight of the SSP in the overall solution | float | 		 | 
| **weightLight_ssp_$i** | light weight of the SSP in the overall solution | float | 		 | 




