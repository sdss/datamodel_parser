
# Data model: specObj



#### General Description
This file contains the list of all spectra for a given data release, with
associated parameters from the 2D and 1D pipelines for each.


#### Naming Convention
<code>specObj-dr[0-9]+\.fits</code>, where <code>[0-9]+</code>
is the release number (8, 9, 10, ...).


#### Approximate Size
2 Gbytes


#### File Type
FITS


#### Read by Products
sas


#### Written by Products
sas


## Page Contents
* [HDU0: HEADER HDU FOR TABLE](#hdu0-header-hdu-for-table)
* [HDU1: TABLE WITH CATALOG](#hdu1-table-with-catalog)

## HDU0: HEADER HDU FOR TABLE


### HDU Type
IMAGE



		Required Header Keywords


| **Key** | **Value** | **Type** | **Comment** |
| :--- | :----- | :---- | :------- |
| **SIMPLE** | T | bool | Conforms to FITS standard | 
| **BITPIX** | 16 | int | 16 bit floating point (dummy value) | 
| **NAXIS** | 0 | int | 0 (no data in this HDU) | 
| **EXTEND** | T | bool | Extensions may be present | 
| **SAS_VERS** | 		 | str | Version of sas used to create file | 
| **TREE_VER** | 		 | str | Version of tree used to create file | 



## HDU1: TABLE WITH CATALOG




		Required Columns


| **Key** | **Value** | **Type** | **Comment** |
| :--- | :----- | :---- | :------- |
| **XTENSION** | BINTABLE | str | Table Extension | 
| **SURVEY** | 		 | str | Survey that this object is part of | 
| **TFIELDS** | 127 | int | Number of columns in table | 
| **INSTRUMENT** | 		 | str | Instrument that this spectrum was observed with (SDSS or BOSS) | 
| **CHUNK** | 		 | str | Name of tiling chunk that this spectrum was tiled in (boss1, boss2, etc), important for tracking large-scale structure samples | 
| **PROGRAMNAME** | 		 | str | Program within each survey that the plate was part of | 
| **PLATERUN** | 		 | str | Drilling run that this plate was drilled in | 
| **PLATEQUALITY** | 		 | str | Final quality of plate this spectrum came from ("good", "marginal" or "bad") | 
| **PLATESN2** | 		 | float32 | Overall signal-to-noise-squared measure for plate (only for SDSS spectrograph plates) | 
| **DEREDSN2** | 		 | float32 | Dereddened overall signal-to-noise-squared measure for plate (only for BOSS spectrograph plates) | 
| **LAMBDA_EFF** | 		 | float32 | Effective wavelength drilling position was optimized for (Angstroms) | 
| **BLUE_FIBER** | 		 | int32 | Set to 1 if this was requested to be a "blue fiber" target, 0 if it was a "red fiber" (in BOSS high redshift LRGs are requested to be on red fibers) | 
| **ZOFFSET** | 		 | float32 | Washer thickness used (for backstopping BOSS quasar targets, so they are closer to 4000 Angstrom focal plan (microns) | 
| **SNTURNOFF** | 		 | float32 | Signal to noise measure for MS turnoff stars on plate (-9999 if not appropriate) | 
| **NTURNOFF** | 		 | int32 | Number of stars used for SNTURNOFF determination | 
| **SPECPRIMARY** | 		 | int1 | Set to 1 for primary observation of object, 0 otherwise | 
| **SPECSDSS** | 		 | int1 | Set to 1 for primary SDSS spectrograph observation of object, 0 otherwise | 
| **SPECLEGACY** | 		 | int1 | Set to 1 for primary SDSS Legacy program observation of object, 0 otherwise | 
| **SPECSEGUE** | 		 | int1 | Set to 1 for primary SDSS SEGUE program observation of object (including SEGUE-1 and SEGUE-2), 0 otherwise | 
| **SPECSEGUE1** | 		 | int1 | Set to 1 for primary SDSS SEGUE-1 program observation of object, 0 otherwise | 
| **SPECSEGUE2** | 		 | int1 | Set to 1 for primary SDSS SEGUE-2 program observation of object, 0 otherwise | 
| **SPECBOSS** | 		 | int1 | Set to 1 for primary BOSS spectrograph observation of object, 0 otherwise | 
| **BOSS_SPECOBJ_ID** | 		 | int32 | Identification number internal to BOSS for SPECBOSS=1 objects | 
| **SPECOBJID** | 		 | str | Unique database ID based on PLATE, MJD, FIBERID, RUN2D (same as SkyServer version) | 
| **FLUXOBJID** | 		 | str | Unique database ID of flux-based photometric match based on RUN, RERUN, CAMCOl, FIELD, ID (same as SkyServer version) | 
| **BESTOBJID** | 		 | str | Unique database ID of (recommended) position-based photometric match based on RUN, RERUN, CAMCOl, FIELD, ID (same as SkyServer version) | 
| **TARGETOBJID** | 		 | str | Unique database ID of targeting object based on RUN, RERUN, CAMCOl, FIELD, ID (same as SkyServer version) | 
| **PLATEID** | 		 | str | Unique database ID of plate based on PLATE, MJD, RUN2D (same as SkyServer version) | 
| **NSPECOBS** | 		 | int16 | Number of spectroscopic observations of this source | 
| **FIRSTRELEASE** | 		 | str | Name of first release this PLATE, MJD, FIBERID, RUN2D was associated with | 
| **RUN2D** | 		 | str | Spectroscopic 2D reduction (extraction of spectra) name | 
| **RUN1D** | 		 | str | Spectroscopic 1D reduction (redshift and classification) name | 
| **DESIGNID** | 		 | int32 | Design identification number for plate | 
| **CX** | 		 | float64 | Position of object on J2000 unit sphere | 
| **CY** | 		 | float64 | Position of object on J2000 unit sphere | 
| **CZ** | 		 | float64 | Position of object on J2000 unit sphere | 
| **XFOCAL** | 		 | float32 | Hole position on plate (+X = +RA) in mm | 
| **YFOCAL** | 		 | float32 | Hole position on plate (+Y = +DEC) in mm | 
| **SOURCETYPE** | 		 | str | String expressing type of source (similar to OBJTYPE in DR8 and earlier) | 
| **TARGETTYPE** | 		 | str | General type of target ("SCIENCE", "STANDARD" or "SKY") | 
| **PRIMTARGET** | 		 | int32 | Deprecated version of primary (science) target flags (meanings highly overloaded) | 
| **SECTARGET** | 		 | int32 | Deprecated version of secondary (calibration) target flags (meanings highly overloaded) | 
| **LEGACY_TARGET1** | 		 | int32 | <a href="http://www.sdss.org/dr13/algorithms/bitmasks/#LEGACY_TARGET1">Primary (science) target flags for SDSS-I and SDSS-II Legacy survey</a> | 
| **LEGACY_TARGET2** | 		 | int32 | <a href="http://www.sdss.org/dr13/algorithms/bitmasks/#LEGACY_TARGET2">Secondary (calibration) target flags for SDSS-I and SDSS-II Legacy survey</a> | 
| **SPECIAL_TARGET1** | 		 | int32 | <a href="http://www.sdss.org/dr13/algorithms/bitmasks/#SPECIAL_TARGET1">Primary (science) target flags for SDSS-I and SDSS-II special program targets</a> | 
| **SPECIAL_TARGET2** | 		 | int32 | <a href="http://www.sdss.org/dr13/algorithms/bitmasks/#SPECIAL_TARGET2">Secondary (calibration) target flags for SDSS-I and SDSS-II special program targets</a> | 
| **SEGUE1_TARGET1** | 		 | int32 | <a href="http://www.sdss.org/dr13/algorithms/bitmasks/#SEGUE1_TARGET">Primary (science) target flags for SEGUE-1 targets</a> | 
| **SEGUE2_TARGET1** | 		 | int32 | <a href="http://www.sdss.org/dr13/algorithms/bitmasks/#SEGUE2_TARGET1">Primary (science) target flags for SEGUE-2 targets</a> | 
| **SEGUE2_TARGET2** | 		 | int32 | <a href="http://www.sdss.org/dr13/algorithms/bitmasks/#SEGUE2_TARGET2">Secondary (calibration) target flags for SEGUE-2 targets</a> | 
| **MARVELS_TARGET1** | 		 | int32 | Primary (science) target flags for MARVELS targets | 
| **MARVELS_TARGET2** | 		 | int32 | Secondary (calibration) target flags for MARVELS targets | 
| **BOSS_TARGET1** | 		 | int64 | <a href="http://www.sdss.org/dr13/algorithms/bitmasks/#BOSS_TARGET1">Primary (science) target flags for BOSS targets</a> | 
| **BOSS_TARGET2** | 		 | int64 | Always set to zero (placeholder for BOSS target flags never used) | 
| **EBOSS_TARGET0** | 		 | int64 | <a href="http://www.sdss.org/dr13/algorithms/bitmasks/#EBOSS_TARGET0">SEQUELS, TDSS and SPIDERS target selection flags</a> | 
| **ANCILLARY_TARGET1** | 		 | int64 | <a href="http://www.sdss.org/dr13/algorithms/bitmasks/#ANCILLARY_TARGET1">Target flags for BOSS ancillary targets</a> | 
| **ANCILLARY_TARGET2** | 		 | int64 | <a href="http://www.sdss.org/dr13/algorithms/bitmasks/#ANCILLARY_TARGET2">More target flags for BOSS ancillary targets</a> | 
| **SPECTROGRAPHID** | 		 | int16 | Which spectrograph (1 or 2) | 
| **PLATE** | 		 | int32 | Plate number (each plate corresponds to an actual plug plate) | 
| **TILE** | 		 | int32 | Tile number (each tile can have several plates drilled for it) | 
| **MJD** | 		 | int32 | Modified Julian Day of observation | 
| **FIBERID** | 		 | int32 | Fiber number | 
| **OBJID** | 		 | int32[5] | SDSS photometric object identification numbers (RUN, RERUN, CAMCOL, FIELD, ID) | 
| **PLUG_RA** | 		 | float64 | Right ascension of hole (J2000 deg) | 
| **PLUG_DEC** | 		 | float64 | Declination of hole  (J2000 deg) | 
| **CLASS** | 		 | str | Best spectroscopic classification ("STAR", "GALAXY" or "QSO") | 
| **SUBCLASS** | 		 | str | Best spectroscopic subclassification | 
| **Z** | 		 | float32 | Best redshift | 
| **Z_ERR** | 		 | float32 | Error in best redshift | 
| **RCHI2** | 		 | float32 | Reduced chi-squared of best fit | 
| **DOF** | 		 | int32 | Number of degrees of freedom in best fit | 
| **RCHI2DIFF** | 		 | float32 | Difference in reduced chi-squared between best and second best fit | 
| **TFILE** | 		 | str | File that best fit template comes from in idlspec2d product | 
| **TCOLUMN** | 		 | float32[10] | Columns of template files that correspond to each template | 
| **NPOLY** | 		 | int32 | Number of polynomial terms in fit | 
| **THETA** | 		 | float32[10] | Template coefficients of best fit | 
| **VDISP** | 		 | float32 | Velocity dispersion (km/s) | 
| **VDISP_ERR** | 		 | float32 | Error in velocity dispersion (km/s) | 
| **VDISPZ** | 		 | float32 | Redshift associated with best-fit velocity dispersion | 
| **VDISPZ_ERR** | 		 | float32 | Error in redshift associated with best-fit velocity dispersion | 
| **VDISP_DOF** | 		 | int32 | Number of degrees of freedom in velocity dispersion fit | 
| **VDISPCHI2** | 		 | float32 | Chi-squared for best-fit velocity dispersion | 
| **VDISPNPIX** | 		 | int32 | Number of pixels overlapping the templates used in the velocity dispersion fit | 
| **WAVEMIN** | 		 | float32 | Minimum observed (vacuum) wavelength  (Angstroms) | 
| **WAVEMAX** | 		 | float32 | Maximum observed (vacuum) wavelength  (Angstroms) | 
| **WCOVERAGE** | 		 | float32 | Coverage in wavelength, in units of log10 wavelength | 
| **ZWARNING** | 		 | int32 | <a href="http://www.sdss.org/dr13/algorithms/bitmasks/#ZWARNING">Bitmask of spectroscopic warning values</a>; 0 means everything is OK | 
| **SN_MEDIAN_ALL** | 		 | float32 | Median signal-to-noise per pixel across full spectrum | 
| **SN_MEDIAN** | 		 | float32[5] | Median signal-to-noise per pixel within each of the <i>ugriz</i> bandpasses | 
| **CHI68P** | 		 | float32 | 68-th percentile value of abs(chi) of the best-fit synthetic spectrum to the actual spectrum (around 1.0 for a good fit) | 
| **FRACNSIGMA** | 		 | float32[10] | Fraction of pixels deviant by more than N sigma relative to best-fit (for 1,2,..,10 sigma) | 
| **FRACNSIGHI** | 		 | float32 | Fraction of pixels high by more than N sigma relative to best-fit (for 1,2,..,10 sigma) | 
| **FRACNSIGLO** | 		 | float32 | Fraction of pixels low by more than N sigma relative to best-fit (for 1,2,..,10 sigma) | 
| **SPECTROFLUX** | 		 | float32[5] | Spectrum projected onto <i>ugriz</i> filters (nanomaggies) | 
| **SPECTROFLUX_IVAR** | 		 | float32[5] | Inverse variance of spectrum projected onto <i>ugriz</i> filters (nanomaggies) | 
| **SPECTROSYNFLUX** | 		 | float32[5] | Best-fit template spectrum projected onto <i>ugriz</i> filters (nanomaggies) | 
| **SPECTROSYNFLUX_IVAR** | 		 | float32[5] | Inverse variance of best-fit template spectrum projected onto <i>ugriz</i> filters (nanomaggies) | 
| **SPECTROSKYFLUX** | 		 | float32[5] | Sky flux in each of the <i>ugriz</i> imaging filters (nanomaggies) | 
| **ANYANDMASK** | 		 | int32 | For each bit, records whether any pixel in the spectrum has that bit set in its ANDMASK | 
| **ANYORMASK** | 		 | int32 | For each bit, records whether any pixel in the spectrum has that bit set in its ORMASK | 
| **SPEC1_G** | 		 | float32 | Signal-to-noise squared for spectrograph #1, at g=20.20 for SDSS spectrograph spectra, g=21.20 for BOSS spectrograph spectra | 
| **SPEC1_R** | 		 | float32 | Signal-to-noise squared for spectrograph #1, at r=20.25 for SDSS spectrograph spectra, r=20.20 for BOSS spectrograph spectra | 
| **SPEC1_I** | 		 | float32 | Signal-to-noise squared for spectrograph #1, at i=19.90 for SDSS spectrograph spectra, i=20.20 for BOSS spectrograph spectra | 
| **SPEC2_G** | 		 | float32 | Signal-to-noise squared for spectrograph #2, at g=20.20 for SDSS spectrograph spectra, g=21.20 for BOSS spectrograph spectra | 
| **SPEC2_R** | 		 | float32 | Signal-to-noise squared for spectrograph #2, at r=20.25 for SDSS spectrograph spectra, r=20.20 for BOSS spectrograph spectra | 
| **SPEC2_I** | 		 | float32 | Signal-to-noise squared for spectrograph #2, at i=19.90 for SDSS spectrograph spectra, i=20.20 for BOSS spectrograph spectra | 
| **ELODIE_FILENAME** | 		 | str | File name for best-fit ELODIE star | 
| **ELODIE_OBJECT** | 		 | str | Star name for ELODIE star | 
| **ELODIE_SPTYPE** | 		 | str | ELODIE star spectral type | 
| **ELODIE_BV** | 		 | float32 | (B-V) color index for ELODIE star (mag) | 
| **ELODIE_TEFF** | 		 | float32 | Effective temperature of ELODIE star (Kelvin) | 
| **ELODIE_LOGG** | 		 | float32 | log10(gravity) of ELODIE star | 
| **ELODIE_FEH** | 		 | float32 | Metallicity [Fe/H] of ELODIE star | 
| **ELODIE_Z** | 		 | float32 | Redshift fit to ELODIE star | 
| **ELODIE_Z_ERR** | 		 | float32 | Error in redshift fit to ELODIE star | 
| **ELODIE_Z_MODELERR** | 		 | float32 | Standard deviation in redshift among the 12 best-fit ELODIE stars | 
| **ELODIE_RCHI2** | 		 | float32 | Reduced chi-squared of fit to best ELODIE star | 
| **ELODIE_DOF** | 		 | int32 | Degrees of freedom in fit to best ELODIE star | 
| **Z_NOQSO** | 		 | float32 | Best redshift when ignoring QSO fits, recommended for BOSS CMASS and LOWZ targets; calculated only for survey='boss' spectra, not for any SDSS spectrograph data | 
| **Z_ERR_NOQSO** | 		 | float32 | Error in Z_NOQSO redshift | 
| **ZWARNING_NOQSO** | 		 | int32 | For Z_NOQSO redshift, the
<a href="http://www.sdss.org/dr13/algorithms/bitmasks/#ZWARNING">bitmask of spectroscopic warning values</a>; 0 means everything is OK | 
| **CLASS_NOQSO** | 		 | str | Spectroscopic classification for Z_NOQSO redshift | 
| **SUBCLASS_NOQSO** | 		 | str | Spectroscopic subclassification for Z_NOQSO redshift | 
| **RCHI2DIFF_NOQSO** | 		 | float32 | Difference in reduced chi-squared between best and second best fit for Z_NOQSO redshift | 
| **Z_PERSON** | 		 | float32 | Visual-inspection redshift | 
| **CLASS_PERSON** | 		 | int32 | Visual-inspection classification (0=not inspected or unknown, 1=star, 2=narrow emission-line galaxy, 3=QSO, 4=galaxy) | 
| **Z_CONF_PERSON** | 		 | int32 | Visual-inspection confidence (0=not inspected or no confidence, 1,2=low confidence, 3,4=high confidence) | 
| **COMMENTS_PERSON** | 		 | str | Visual-inspection comments | 
| **CALIBFLUX** | 		 | float32[5] | <i>ugriz</i> fluxes used for calibrations (nanomaggies) | 
| **CALIBFLUX_IVAR** | 		 | float32[5] | Inverse variances of <i>ugriz</i> fluxes used for calibrations (nanomaggies) | 




