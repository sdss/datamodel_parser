
# Datamodel: cannonField



#### General Description
cannonField files summarize the <em>Cannon</em> results for all stars in a given field.


#### Naming Convention
<code>cannonField-LOCATION_ID-xh-censor.fits</code>
<dt>Approximate Size</dt>
<dd id="filesize">24 MB</dd>
<dt>File Type</dt>
<dd id="filetype">FITS</dd>
<dt>Read by Products</dt>
<dd>idlwrap </dd>
<dt>Written by Products</dt>
<dd>idlwrap </dd>
<dt>Sections</dt>
<dd><p>This should contain internal links to parts of the file (if any).</p>
<ul>
<li><a href="#hdu0">HDU0</a>: Primary Header</li>
<li><a href="#hdu1">HDU1</a>: Table with <em>Cannon</em>-derived parameters, spectra, errors, and spectra model reconstruction for all stars in the field</li>
</ul>
</dd>


#### Approximate Size
24 MB


#### File Type
FITS


#### Read by Products
idlwrap


#### Written by Products
idlwrap


## Page Contents
* [HDU0: THE PRIMARY HEADER](#hdu0-the-primary-header)
* [HDU1: CANNON-BASED DATA](#hdu1-cannon-based-data)

## HDU0: THE PRIMARY HEADER
This HDU has no non-standard required keywords.




## HDU1: CANNON-BASED DATA


### HDU Type
IMAGE




		Required Data Table Columns


| **Name** | **Type** | **Unit** | **Description** |
| :--- | :----- | :---- | :------- |
| **FILENAME** | char[53] | 		 | cannonStar .pkl files containing spectra and Cannon spectra models |
| **APOGEE_ID** | char[18] | 		 | TMASS-STYLE object names |
| **LOCATION_ID** | int64 | 		 | Field Location ID |
| **FIELD** | char[5] | 		 | Field name |
| **TEFF** | float64 | K | Teff from Cannon analysis of combined spectra |
| **LOGG** | float64 | dex | log g from Cannon analysis of combined spectra |
| **M_H** | float64 | dex | [Z/H] from Cannon analysis of combined spectra |
| **ALPHA_M** | float64 | dex | [alpha/M] from Cannon analysis of combined spectra |
| **FE_H** | float64 | dex | [Fe/H] from Cannon analysis of combined spectra |
| **C_H** | float64 | dex | [C/H] from Cannon analysis of combined spectra |
| **CI_H** | float64 | dex | [CI/H] from Cannon analysis of combined spectra |
| **N_H** | float64 | dex | [N/H] from Cannon analysis of combined spectra |
| **O_H** | float64 | dex | [O/H] from Cannon analysis of combined spectra |
| **NA_H** | float64 | dex | [Na/H] from Cannon analysis of combined spectra |
| **MG_H** | float64 | dex | [Mg/H] from Cannon analysis of combined spectra |
| **AL_H** | float64 | dex | [Al/H] from Cannon analysis of combined spectra |
| **SI_H** | float64 | dex | [Si/H] from Cannon analysis of combined spectra |
| **P_H** | float64 | dex | [P/H] from Cannon analysis of combined spectra |
| **S_H** | float64 | dex | [S/H] from Cannon analysis of combined spectra |
| **K_H** | float64 | dex | [K/H] from Cannon analysis of combined spectra |
| **CA_H** | float64 | dex | [Ca/H] from Cannon analysis of combined spectra |
| **TI_H** | float64 | dex | [Ti/H] from Cannon analysis of combined spectra |
| **TIII_H** | float64 | dex | [TiII/H] from Cannon analysis of combined spectra |
| **V_H** | float64 | dex | [V/H] from Cannon analysis of combined spectra |
| **CR_H** | float64 | dex | [Cr/H] from Cannon analysis of combined spectra |
| **MN_H** | float64 | dex | [Mn/H] from Cannon analysis of combined spectra |
| **CO_H** | float64 | dex | [Co/H] from Cannon analysis of combined spectra |
| **NI_H** | float64 | dex | [Ni/H] from Cannon analysis of combined spectra |
| **TEFF_RAWERR** | float64 | K | uncertainty in Teff from Cannon analysis of combined spectra |
| **LOGG_RAWERR** | float64 | dex | uncertainty in log g from Cannon analysis of combined spectra |
| **M_H_RAWERR** | float64 | dex | uncertainty in [Z/H] from Cannon analysis of combined spectra |
| **ALPHA_M_RAWERR** | float64 | dex | uncertainty in [alpha/M] from Cannon analysis of combined spectra |
| **FE_H_RAWERR** | float64 | dex | uncertainty in [Fe/H] from Cannon analysis of combined spectra |
| **C_H_RAWERR** | float64 | dex | uncertainty in [C/H] from Cannon analysis of combined spectra |
| **CI_H_RAWERR** | float64 | dex | uncertainty in [CI/H] from Cannon analysis of combined spectra |
| **N_H_RAWERR** | float64 | dex | uncertainty in [N/H] from Cannon analysis of combined spectra |
| **O_H_RAWERR** | float64 | dex | uncertainty in [O/H] from Cannon analysis of combined spectra |
| **NA_H_RAWERR** | float64 | dex | uncertainty in [Na/H] from Cannon analysis of combined spectra |
| **MG_H_RAWERR** | float64 | dex | uncertainty in [Mg/H] from Cannon analysis of combined spectra |
| **AL_H_RAWERR** | float64 | dex | uncertainty in [Al/H] from Cannon analysis of combined spectra |
| **SI_H_RAWERR** | float64 | dex | uncertainty in [Si/H] from Cannon analysis of combined spectra |
| **P_H_RAWERR** | float64 | dex | uncertainty in [P/H] from Cannon analysis of combined spectra |
| **S_H_RAWERR** | float64 | dex | uncertainty in [S/H] from Cannon analysis of combined spectra |
| **K_H_RAWERR** | float64 | dex | uncertainty in [K/H] from Cannon analysis of combined spectra |
| **CA_H_RAWERR** | float64 | dex | uncertainty in [Ca/H] from Cannon analysis of combined spectra |
| **TI_H_RAWERR** | float64 | dex | uncertainty in [Ti/H] from Cannon analysis of combined spectra |
| **TIII_H_RAWERR** | float64 | dex | uncertainty in [TiII/H] from Cannon analysis of combined spectra |
| **V_H_RAWERR** | float64 | dex | uncertainty in [V/H] from Cannon analysis of combined spectra |
| **CR_H_RAWERR** | float64 | dex | uncertainty in [Cr/H] from Cannon analysis of combined spectra |
| **MN_H_RAWERR** | float64 | dex | uncertainty in [Mn/H] from Cannon analysis of combined spectra |
| **CO_H_RAWERR** | float64 | dex | uncertainty in [Co/H] from Cannon analysis of combined spectra |
| **NI_H_RAWERR** | float64 | dex | uncertainty in [Ni/H] from Cannon analysis of combined spectra |
| **TEFF_ERR** | float64 | K | the larger of: TEFF_RAWERR above and the scatter between the input and recovered labels from the training set |
| **LOGG_ERR** | float64 | dex | the larger of: LOGG_RAWERR above and the scatter between the input and recovered labels from the training set |
| **M_H_ERR** | float64 | dex | the larger of: M_H_RAWERR above and the scatter between the input and recovered labels from the training set |
| **ALPHA_M_ERR** | float64 | dex | the larger of: ALPHA_M_RAWERR above and the scatter between the input and recovered labels from the training set |
| **FE_H_ERR** | float64 | dex | the larger of: FE_H_RAWERR above and the scatter between the input and recovered labels from the training set |
| **C_H_ERR** | float64 | dex | the larger of: C_H_RAWERR above and the scatter between the input and recovered labels from the training set |
| **CI_H_ERR** | float64 | dex | the larger of: CI_H_RAWERR above and the scatter between the input and recovered labels from the training set |
| **N_H_ERR** | float64 | dex | the larger of: N_H_RAWERR above and the scatter between the input and recovered labels from the training set |
| **O_H_ERR** | float64 | dex | the larger of: O_H_RAWERR above and the scatter between the input and recovered labels from the training set |
| **NA_H_ERR** | float64 | dex | the larger of: NA_H_RAWERR above and the scatter between the input and recovered labels from the training set |
| **MG_H_ERR** | float64 | dex | the larger of: MG_H_RAWERR above and the scatter between the input and recovered labels from the training set |
| **AL_H_ERR** | float64 | dex | the larger of: AL_H_RAWERR above and the scatter between the input and recovered labels from the training set |
| **SI_H_ERR** | float64 | dex | the larger of: SI_H_RAWERR above and the scatter between the input and recovered labels from the training set |
| **P_H_ERR** | float64 | dex | the larger of: P_H_RAWERR above and the scatter between the input and recovered labels from the training set |
| **S_H_ERR** | float64 | dex | the larger of: S_H_RAWERR above and the scatter between the input and recovered labels from the training set |
| **K_H_ERR** | float64 | dex | the larger of: K_H_RAWERR above and the scatter between the input and recovered labels from the training set |
| **CA_H_ERR** | float64 | dex | the larger of: CA_H_RAWERR above and the scatter between the input and recovered labels from the training set |
| **TI_H_ERR** | float64 | dex | the larger of: TI_H_RAWERR above and the scatter between the input and recovered labels from the training set |
| **TIII_H_ERR** | float64 | dex | the larger of: TIII_H_RAWERR above and the scatter between the input and recovered labels from the training set |
| **V_H_ERR** | float64 | dex | the larger of: V_H_RAWERR above and the scatter between the input and recovered labels from the training set |
| **CR_H_ERR** | float64 | dex | the larger of: CR_H_RAWERR above and the scatter between the input and recovered labels from the training set |
| **MN_H_ERR** | float64 | dex | the larger of: MN_H_RAWERR above and the scatter between the input and recovered labels from the training set |
| **CO_H_ERR** | float64 | dex | the larger of: CO_H_RAWERR above and the scatter between the input and recovered labels from the training set |
| **NI_H_ERR** | float64 | dex | the larger of: NI_H_RAWERR above and the scatter between the input and recovered labels from the training set |
| **chi_sq** | float64 | 		 | chi^2 between normalized spectra and Cannon reconstructions |
| **r_chi_sq** | float64 | 		 | reduced chi^2 of above |
| **model_flux** | float64[8575] | 		 | Cannon model fluxes.  Note that the wavelength information can be found in the <code>aspcapField</code> or <code>aspcapStar</code> files. |
| **flux** | float32[8575] | 		 | normalized observed fluxes |
| **ivar** | float32[8575] | 		 | flux inverse variances |



