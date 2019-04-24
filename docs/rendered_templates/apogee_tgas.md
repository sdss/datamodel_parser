
# Datamodel: apogee_tgas



#### General Description
apogee_tgas-VERS.fits contains combined APOGEE-TGAS information for all stars in common between the two surveys, where VERS is the latest data release (currently DR14).


#### Naming Convention
<code>apogee_tgas-VERS.fits</code>


#### Approximate Size
143 MB


#### File Type
FITS


## Page Contents
* [HDU0: PRIMARY HEADER](#hdu0-primary-header)
* [HDU1: APOGEE-TGAS CATALOGUE](#hdu1-apogee-tgas-catalogue)

## HDU0: PRIMARY HEADER


### HDU Type
IMAGE



		Required Header Keywords


| **Key** | **Value** | **Type** | **Comment** |
| :--- | :----- | :---- | :------- |
| **Name** | apogee_tgas-DR14.fits | str | Table name | 
| **Column Count** | 206 | int | Number of columns | 
| **Row Count** | 46033 | int | Number of rows | 
| **DATE** | 2017-04-24 | str | Creation UTC (YYYY-MM-DD) date of FITS header | 



## HDU1: APOGEE-TGAS CATALOGUE
Contains an entry for every APOGEE object in the data release in common with TGAS, giving information about each star and its derived quantities, in particular, RV and stellar parameters derived from <a href="https://data.sdss.org/datamodel/files/APOGEE_REDUX/APRED_VERS/APSTAR_VERS/ASPCAP_VERS/RESULTS_VERS/allStar.html"> ASPCAP analysis</a>, <a href="https://gaia.esac.esa.int/documentation/GDR1/datamodel/Ch1/tgas_source.html"> TGAS astrometry</a>, <a href="http://www2.mpia-hd.mpg.de/homes/calj/"> astrometric distances</a> from <a href="http://adsabs.harvard.edu/abs/2016ApJ...833..119A"> Astraatmadja and Bailer-Jones (2016)</a>, improved astro-spectro-photometric distances from the BPG StarHorse code (<a href="http://adsabs.harvard.edu/abs/2016A%26A...585A..42S">Santiago et al. 2016</a>, Queiroz et al. 2017, in prep.), and precise Galactic orbital parameters from <a href="https://fernandez-trincado.github.io/GravPot16/index.html"> GravPot16</a> (Fernandez-Trincado 2017, in prep.).

To compute the distances and Galactic kinematics, we use a solar position of R<sub>sun</sub> = 8.3 kpc, Z<sub>sun</sub> = 11 pc, local kinematic parameters of V<sub>LSR</sub> = 238 km/s and [U,V,W]<sub>sun</sub> = [10, 11, 7] km/s, a bar pattern speed of 43 km/s/kpc, a bar angle of 30 deg, and a bar mass of 1.0*10<sup>10</sup> M<sub>sun</sub>, in line with <a href="http://adsabs.harvard.edu/abs/2016ARA%26A..54..529B"> Bland-Hawthorn and Gerhard (2016)</a>.

### HDU Type
IMAGE




		Required Data Table Columns


| **Name** | **Type** | **Unit** | **Description** |
| :--- | :----- | :---- | :------- |
| **ASPCAP_ID** | char[46] | 		 | Unique ASPCAP identifier: apogee.[ns].[sc].RESULTS_VERS.LOC.STAR |
| **APOGEE_ID** | char[18] | 		 | TMASS-STYLE object name |
| **TELESCOPE** | char[8] | 		 | String representation of of telescope used for observation (currently APO 1m or 2.5m) |
| **LOCATION_ID** | int16 | 		 | Field Location ID |
| **FIELD** | char[16] | 		 | Field name |
| **J** | float32 | mag | 2MASS J mag [bad=99] |
| **J_ERR** | float32 | mag | uncertainty in 2MASS J mag |
| **H** | float32 | mag | 2MASS H mag [bad=99] |
| **H_ERR** | float32 | mag | uncertainty in 2MASS H mag |
| **K** | float32 | mag | 2MASS Ks mag  [bad=99] |
| **K_ERR** | float32 | mag | uncertainty in 2MASS Ks mag |
| **RA** | float64 | deg | Right ascension (J2000) |
| **DEC** | float64 | deg | Declination (J2000) |
| **GLON** | float64 | deg | Galactic longitude |
| **GLAT** | float64 | deg | Galactic latitude |
| **TARGFLAGS** | char[140] | 		 | target flags in English |
| **NVISITS** | int32 | 		 | Number of visits into combined spectrum |
| **STARFLAGS** | char[165] | 		 | STARFLAG in English |
| **VHELIO_AVG** | float32 | km/s | average radial velocity, weighted by S/N, using RVs determined from cross-correlation of individual spectra with combined spectrum |
| **VSCATTER** | float32 | km/s | scatter of individual visit RVs around average |
| **VERR** | float32 | km/s | Uncertainty in VHELIO_AVG from the S/N-weighted individual RVs |
| **SNREV** | float32 | 		 | Revised S/N estimate (avoiding persistence issues) |
| **PARAM** | float32[9] | 		 | Empirically calibrated parameter array, using ASPCAP stellar parameters fit + calibrations, in order given in PARAM_SYMBOL array in HDU3: Teff, logg, vmicro, [M/H], [C/M], [N/M], [alpha/M], vsini/vmacro |
| **FPARAM** | float32[9] | 		 | Output parameter array from ASPCAP stellar parameters fit, in order given in PARAM_SYMBOL array in HDU3: Teff, logg, vmicro, [M/H], [C/M], [N/M], [alpha/M], vsini/vmacro |
| **PARAM_COV** | float32[81] | 		 | Covariance of calibrated parameters, but with only diagonal elements from "external" uncertainty estimation |
| **FPARAM_COV** | float32[81] | 		 | Covariance of fitted parameters from FERRE |
| **TEFF** | float32 | K | Teff from ASPCAP analysis of combined spectrum (from PARAM) |
| **TEFF_ERR** | float32 | K | Teff uncertainty (from PARAM_COV) |
| **LOGG** | float32 | log (cgs) | log g from ASPCAP analysis of combined spectrum (from PARAM) |
| **LOGG_ERR** | float32 | log (cgs) | log g uncertainty (from PARAM_COV) |
| **VMICRO** | float32 | (cgs) | microturbulent velocity (fit for dwarfs, f(log g) for giants) |
| **VMACRO** | float32 | (cgs) | macroturbulent velocity (f(log Teff, [M/H]) for giants) |
| **VSINI** | float32 | (cgs) | rotational+macroturbulent velocity (fit for dwarfs) |
| **M_H** | float32 | dex | [Z/H] from ASPCAP analysis of combined spectrum (from PARAM) |
| **M_H_ERR** | float32 | dex | [Z/H] uncertainty (from PARAM_COV) |
| **ALPHA_M** | float32 | dex | [alpha/M] from ASPCAP analysis of combined spectrum (from PARAM) |
| **ALPHA_M_ERR** | float32 | dex | [alpha/M] uncertainty (from PARAM_COV) |
| **ASPCAP_CHI2** | float32 | 		 | Chi^2 from ASPCAP fit |
| **ASPCAPFLAGS** | char[114] | 		 | ASPCAPFLAG in English |
| **PARAMFLAG** | int32[7] | 		 | Individual parameter flag for ASPCAP analysis, see <a href="http://www.sdss.org/dr13/algorithms/bitmasks/#APOGEE_PARAMFLAG"> bitmask definitions</a> |
| **FELEM** | float32[26] | 		 | Output individual element array from ASPCAP stellar abundances fit, in order given in ELEM_SYMBOL array in HDU3 |
| **FELEM_ERR** | float32[26] | 		 | Uncertainty from FERRE in individual element abundances |
| **X_H** | float32[26] | 		 | Empirically calibrated individual element array, using ASPCAP stellar abundances fit + calibrations, all expressed in logarithmic abundance relative to H ([X/H]), in order given in ELEM_SYMBOL array in HDU3 |
| **X_H_ERR** | float32[26] | 		 | Empirical uncertainties in [X/H], derived from scatter within clusters |
| **X_M** | float32[26] | 		 | Empirically calibrated individual element array, using ASPCAP stellar abundances fit + calibrations, all expressed in logarithmic abundance relative to M ([X/M]) in order given in ELEM_SYMBOL array in HDU3 |
| **X_M_ERR** | float32[26] | 		 | Empirical uncertainties in [X/M], derived from scatter within clusters |
| **C_FE** | float32 | dex | [C/Fe] from ASPCAP analysis  of combined spectrum (from PARAM) |
| **CI_FE** | float32 | dex | [CI/Fe] from ASPCAP analysis  of combined spectrum (from PARAM) |
| **N_FE** | float32 | dex | [N/Fe] from ASPCAP analysis  of combined spectrum (from PARAM) |
| **O_FE** | float32 | dex | [O/Fe] from ASPCAP analysis  of combined spectrum (from PARAM) |
| **NA_FE** | float32 | dex | [Na/Fe] from ASPCAP analysis  of combined spectrum (from PARAM) |
| **MG_FE** | float32 | dex | [Mg/Fe] from ASPCAP analysis  of combined spectrum (from PARAM) |
| **AL_FE** | float32 | dex | [Al/Fe] from ASPCAP analysis  of combined spectrum (from PARAM) |
| **SI_FE** | float32 | dex | [Si/Fe] from ASPCAP analysis  of combined spectrum (from PARAM) |
| **P_FE** | float32 | dex | [P/Fe] from ASPCAP analysis  of combined spectrum (from PARAM) |
| **S_FE** | float32 | dex | [S/Fe] from ASPCAP analysis  of combined spectrum (from PARAM) |
| **K_FE** | float32 | dex | [K/Fe] from ASPCAP analysis  of combined spectrum (from PARAM) |
| **CA_FE** | float32 | dex | [Ca/Fe] from ASPCAP analysis  of combined spectrum (from PARAM) |
| **TI_FE** | float32 | dex | [Ti/Fe] from ASPCAP analysis  of combined spectrum (from PARAM) |
| **TIII_FE** | float32 | dex | [TiII/Fe] from ASPCAP analysis  of combined spectrum (from PARAM) |
| **V_FE** | float32 | dex | [V/Fe] from ASPCAP analysis  of combined spectrum (from PARAM) |
| **CR_FE** | float32 | dex | [Cr/Fe] from ASPCAP analysis  of combined spectrum (from PARAM) |
| **MN_FE** | float32 | dex | [Mn/Fe] from ASPCAP analysis  of combined spectrum (from PARAM) |
| **FE_H** | float32 | dex | [Fe/H] from ASPCAP analysis  of combined spectrum (from PARAM) |
| **CO_FE** | float32 | dex | [Co/Fe] from ASPCAP analysis  of combined spectrum (from PARAM) |
| **NI_FE** | float32 | dex | [Ni/Fe] from ASPCAP analysis  of combined spectrum (from PARAM) |
| **CU_FE** | float32 | dex | [Cu/Fe] from ASPCAP analysis  of combined spectrum (from PARAM) |
| **GE_FE** | float32 | dex | [Ge/Fe] from ASPCAP analysis  of combined spectrum (from PARAM) |
| **RB_FE** | float32 | dex | [Rb/Fe] from ASPCAP analysis  of combined spectrum (from PARAM) |
| **Y_FE** | float32 | dex | [Y/Fe] from ASPCAP analysis  of combined spectrum (from PARAM) |
| **ND_FE** | float32 | dex | [Nd/Fe] from ASPCAP analysis  of combined spectrum (from PARAM) |
| **C_FE_ERR** | float32 | dex | [C/Fe] uncertainty from ASPCAP analysis  of combined spectrum (from PARAM) |
| **CI_FE_ERR** | float32 | dex | [CI/Fe] uncertainty from ASPCAP analysis  of combined spectrum (from PARAM) |
| **N_FE_ERR** | float32 | dex | [N/Fe] uncertainty from ASPCAP analysis  of combined spectrum (from PARAM) |
| **O_FE_ERR** | float32 | dex | [O/Fe] uncertainty from ASPCAP analysis  of combined spectrum (from PARAM) |
| **NA_FE_ERR** | float32 | dex | [Na/Fe] uncertainty from ASPCAP analysis  of combined spectrum (from PARAM) |
| **MG_FE_ERR** | float32 | dex | [Mg/Fe] uncertainty from ASPCAP analysis  of combined spectrum (from PARAM) |
| **AL_FE_ERR** | float32 | dex | [Al/Fe] uncertainty from ASPCAP analysis  of combined spectrum (from PARAM) |
| **SI_FE_ERR** | float32 | dex | [Si/Fe] uncertainty from ASPCAP analysis  of combined spectrum (from PARAM) |
| **P_FE_ERR** | float32 | dex | [P/Fe] uncertainty from ASPCAP analysis  of combined spectrum (from PARAM) |
| **S_FE_ERR** | float32 | dex | [S/Fe] uncertainty from ASPCAP analysis  of combined spectrum (from PARAM) |
| **K_FE_ERR** | float32 | dex | [K/Fe] uncertainty from ASPCAP analysis  of combined spectrum (from PARAM) |
| **CA_FE_ERR** | float32 | dex | [Ca/Fe] uncertainty from ASPCAP analysis  of combined spectrum (from PARAM) |
| **TI_FE_ERR** | float32 | dex | [Ti/Fe] uncertainty from ASPCAP analysis  of combined spectrum (from PARAM) |
| **TIII_FE_ERR** | float32 | dex | [TiII/Fe] uncertainty from ASPCAP analysis  of combined spectrum (from PARAM) |
| **V_FE_ERR** | float32 | dex | [V/Fe] uncertainty from ASPCAP analysis  of combined spectrum (from PARAM) |
| **CR_FE_ERR** | float32 | dex | [Cr/Fe] uncertainty from ASPCAP analysis  of combined spectrum (from PARAM) |
| **MN_FE_ERR** | float32 | dex | [Mn/Fe] uncertainty from ASPCAP analysis  of combined spectrum (from PARAM) |
| **FE_H_ERR** | float32 | dex | [Fe/H] uncertainty from ASPCAP analysis  of combined spectrum (from PARAM) |
| **CO_FE_ERR** | float32 | dex | [Co/Fe] uncertainty from ASPCAP analysis  of combined spectrum (from PARAM) |
| **NI_FE_ERR** | float32 | dex | [Ni/Fe] uncertainty from ASPCAP analysis  of combined spectrum (from PARAM) |
| **CU_FE_ERR** | float32 | dex | [Cu/Fe] uncertainty from ASPCAP analysis  of combined spectrum (from PARAM) |
| **GE_FE_ERR** | float32 | dex | [Ge/Fe] uncertainty from ASPCAP analysis  of combined spectrum (from PARAM) |
| **RB_FE_ERR** | float32 | dex | [Rb/Fe] uncertainty from ASPCAP analysis  of combined spectrum (from PARAM) |
| **Y_FE_ERR** | float32 | dex | [Y/Fe] uncertainty from ASPCAP analysis  of combined spectrum (from PARAM) |
| **ND_FE_ERR** | float32 | dex | [Nd/Fe] uncertainty from ASPCAP analysis  of combined spectrum (from PARAM) |
| **C_FE_FLAG** | int32 | 		 | [C/Fe] flag |
| **CI_FE_FLAG** | int32 | 		 | [CI/Fe] flag |
| **N_FE_FLAG** | int32 | 		 | [N/Fe] flag |
| **O_FE_FLAG** | int32 | 		 | [O/Fe] flag |
| **NA_FE_FLAG** | int32 | 		 | [Na/Fe] flag |
| **MG_FE_FLAG** | int32 | 		 | [Mg/Fe] flag |
| **AL_FE_FLAG** | int32 | 		 | [Al/Fe] flag |
| **SI_FE_FLAG** | int32 | 		 | [Si/Fe] flag |
| **P_FE_FLAG** | int32 | 		 | [P/Fe] flag |
| **S_FE_FLAG** | int32 | 		 | [S/Fe] flag |
| **K_FE_FLAG** | int32 | 		 | [K/Fe] flag |
| **CA_FE_FLAG** | int32 | 		 | [Ca/Fe] flag |
| **TI_FE_FLAG** | int32 | 		 | [Ti/Fe] flag |
| **TIII_FE_FLAG** | int32 | 		 | [TiII/Fe] flag |
| **V_FE_FLAG** | int32 | 		 | [V/Fe] flag |
| **CR_FE_FLAG** | int32 | 		 | [Cr/Fe] flag |
| **MN_FE_FLAG** | int32 | 		 | [Mn/Fe] flag |
| **FE_H_FLAG** | int32 | 		 | [Fe/H] flag |
| **CO_FE_FLAG** | int32 | 		 | [Co/Fe] flag |
| **NI_FE_FLAG** | int32 | 		 | [Ni/Fe] flag |
| **CU_FE_FLAG** | int32 | 		 | [Cu/Fe] flag |
| **GE_FE_FLAG** | int32 | 		 | [Ge/Fe] flag |
| **RB_FE_FLAG** | int32 | 		 | [Rb/Fe] flag |
| **Y_FE_FLAG** | int32 | 		 | [Y/Fe] flag |
| **ND_FE_FLAG** | int32 | 		 | [Nd/Fe] flag |
| **ELEM_CHI2** | float32[26] | 		 | Chi^2 from ASPCAP fit of individual abundances |
| **ELEMFLAG** | int32[26] | 		 | Flags for analysis of individual abundances, see <a href="http://www.sdss.org/dr13/algorithms/bitmasks/#APOGEE_STARFLAG"> bitmask definitions</a> |
| **AK_TARG** | float32 | mag | Ks-band extinction adopted for targetting |
| **AK_TARG_METHOD** | char[17] | 		 | Method used to get targetting extinction |
| **AK_WISE** | float32 | mag | WISE all-sky Ks-band extinction |
| **SFD_EBV** | float32 | mag | SFD reddening |
| **gaia_source_id** | int64 | 		 | Gaia Source ID |
| **tycho2_id** | char[12] | 		 | Tycho-2 ID |
| **hip** | int32 | 		 | Hipparcos ID |
| **ra_gaia** | float64 | mas | TGAS Right Ascension (J2015.0) |
| **dec_gaia** | float64 | mas | TGAS Right Ascension uncertainty |
| **ra_error** | float64 | mas | TGAS Declination (J2015.0) |
| **dec_error** | float64 | mas | TGAS Declination uncertainty |
| **parallax** | float64 | mas | TGAS parallax |
| **parallax_error** | float64 | mas | Formal TGAS parallax uncertainty |
| **pmra** | float64 | mas/yr | TGAS proper motion |
| **pmra_error** | float64 | mas/yr | TGAS proper motion uncertainty |
| **pmdec** | float64 | mas/yr | TGAS proper motion |
| **pmdec_error** | float64 | mas/yr | TGAS proper motion uncertainty |
| **ra_dec_corr** | float64 | 		 | Correlation between right ascension and declination |
| **ra_parallax_corr** | float64 | 		 | Correlation between right ascension and parallax |
| **ra_pmra_corr** | float64 | 		 | Correlation between right ascension and proper motion in right ascension |
| **ra_pmdec_corr** | float64 | 		 | Correlation between right ascension and proper motion in declination |
| **dec_parallax_corr** | float64 | 		 | Correlation between declination and parallax |
| **dec_pmra_corr** | float64 | 		 | Correlation between declination and proper motion in right ascension |
| **dec_pmdec_corr** | float64 | 		 | Correlation between declination and proper motion in declination |
| **parallax_pmra_corr** | float64 | 		 | Correlation between parallax and proper motion in right ascension |
| **parallax_pmdec_corr** | float64 | 		 | Correlation between parallax and proper motion in declination |
| **pmra_pmdec_corr** | float64 | 		 | Correlation between proper motion in right ascension and proper motion in declination |
| **duplicated_source** | int16 | 		 | Source with duplicate sources; may indicate observational, cross-matching or processing problems, or stellar multiplicity |
| **phot_g_mean_mag** | float64 | mag | Gaia G magnitude |
| **angDist_Gaia** | float64 | arcsec | Angular distance to APOGEE counterpart |
| **rMoMW_ABJ16** | float64 | kpc | Mode distance from Astraatmadja + Bailer-Jones (2016) using parallax (including syst. uncertainty) and MW prior |
| **r5MW_ABJ16** | float64 | kpc | 5th percentile distance from Astraatmadja + Bailer-Jones (2016) using parallax (including syst. uncertainty) and MW prior |
| **r50MW_ABJ16** | float64 | kpc | Median distance from Astraatmadja + Bailer-Jones (2016) using parallax (including syst. uncertainty) and MW prior |
| **r95MW_ABJ16** | float64 | kpc | 95th percentile distance from Astraatmadja + Bailer-Jones (2016) using parallax (including syst. uncertainty) and MW prior |
| **sigmaRMW_ABJ16** | float64 | kpc | Distance standard deviation from Astraatmadja + Bailer-Jones (2016) using parallax (including syst. uncertainty) and MW prior |
| **Vmag** | float32 | mag | APASS DR9 V magnitude |
| **e_Vmag** | float32 | mag | APASS DR9 V magnitude uncertainty |
| **Bmag** | float32 | mag | APASS DR9 B magnitude |
| **e_Bmag** | float32 | mag | APASS DR9 B magnitude uncertainty |
| **gpmag** | float32 | mag | APASS DR9 g magnitude |
| **e_gpmag** | float32 | mag | APASS DR9 g magnitude uncertainty |
| **rpmag** | float32 | mag | APASS DR9 r magnitude |
| **e_rpmag** | float32 | mag | APASS DR9 r magnitude uncertainty |
| **ipmag** | float32 | mag | APASS DR9 i magnitude |
| **e_ipmag** | float32 | mag | APASS DR9 i magnitude uncertainty |
| **angDist_APASS** | float64 | arcsec | Angular distance to APOGEE counterpart |
| **dist05** | float32 | kpc | BPG StarHorse 5th astro-spectro-photometric distance percentile (Queiroz et al. 2017) |
| **dist16** | float32 | kpc | BPG StarHorse 16th astro-spectro-photometric distance percentile (Queiroz et al. 2017) |
| **dist50** | float32 | kpc | BPG StarHorse median astro-spectro-photometric distance (Queiroz et al. 2017) |
| **dist84** | float32 | kpc | BPG StarHorse 84th astro-spectro-photometric distance percentile (Queiroz et al. 2017) |
| **dist95** | float32 | kpc | BPG StarHorse 95th astro-spectro-photometric distance percentile (Queiroz et al. 2017) |
| **meandist** | float32 | kpc | BPG StarHorse mean astro-spectro-photometric distance (Queiroz et al. 2017) |
| **diststd** | float32 | kpc | BPG StarHorse astro-spectro-photometric distance standard deviation (Queiroz et al. 2017) |
| **AV05** | float32 | mag | BPG StarHorse 5th posterior A(V) percentile (Queiroz et al. 2017) |
| **AV16** | float32 | mag | BPG StarHorse 16th posterior A(V) percentile (Queiroz et al. 2017) |
| **AV50** | float32 | mag | BPG StarHorse median posterior A(V) (Queiroz et al. 2017) |
| **AV84** | float32 | mag | BPG StarHorse 84th posterior A(V) percentile (Queiroz et al. 2017) |
| **AV95** | float32 | mag | BPG StarHorse 95th posterior A(V) percentile (Queiroz et al. 2017) |
| **meanAV** | float32 | mag | BPG StarHorse mean posterior A(V) (Queiroz et al. 2017) |
| **AVstd** | float32 | mag | BPG StarHorse posterior A(V) standard deviation (Queiroz et al. 2017) |
| **StarHorse_INPUTFLAGS** | char[80] | 		 | StarHorse Input flags (Queiroz et al. 2017) |
| **StarHorse_OUTPUTFLAGS** | char[50] | 		 | StarHorse Output flags (Queiroz et al. 2017) |
| **Xg** | float64 | kpc | Galactocentric X coordinate |
| **Xg_sig** | float64 | kpc | Galactocentric X coordinate uncertainty |
| **Yg** | float64 | kpc | Galactocentric Y coordinate |
| **Yg_sig** | float64 | kpc | Galactocentric Y coordinate uncertainty |
| **Zg** | float64 | kpc | Galactocentric Z coordinate |
| **Zg_sig** | float64 | kpc | Galactocentric Z coordinate uncertainty |
| **Rg** | float64 | kpc | Galactocentric distance (cylindrical frame) |
| **Rg_sig** | float64 | kpc | Galactocentric distance uncertainty |
| **rmin_med** | float64 | kpc | Minimum Galactocentric distance from GravPot16 (Fernandez-Trincado 2017), median value |
| **rmin_upp** | float64 | kpc | Minimum Galactocentric distance from GravPot16 (Fernandez-Trincado 2017), 84th percentile |
| **rmin_low** | float64 | kpc | Minimum Galactocentric distance from GravPot16 (Fernandez-Trincado 2017), 16th percentile |
| **rmax_med** | float64 | kpc | Maximum Galactocentric distance from GravPot16 (Fernandez-Trincado 2017), median value |
| **rmax_upp** | float64 | kpc | Maximum Galactocentric distance from GravPot16 (Fernandez-Trincado 2017), 84th percentile |
| **rmax_low** | float64 | kpc | Maximum Galactocentric distance from GravPot16 (Fernandez-Trincado 2017), 16th percentile |
| **rmean_med** | float64 | kpc | Mean Galactocentric distance from GravPot16 (Fernandez-Trincado 2017), median value |
| **rmean_upp** | float64 | kpc | Mean Galactocentric distance from GravPot16 (Fernandez-Trincado 2017), 84th percentile |
| **rmean_low** | float64 | kpc | Mean Galactocentric distance from GravPot16 (Fernandez-Trincado 2017), 16th percentile |
| **ecc_med** | float64 | 		 | Orbital eccentricity from GravPot16 (Fernandez-Trincado 2017), median value |
| **ecc_upp** | float64 | 		 | Orbital eccentricity from GravPot16 (Fernandez-Trincado 2017), 84th percentile |
| **ecc_low** | float64 | 		 | Orbital eccentricity from GravPot16 (Fernandez-Trincado 2017), 16th percentile |
| **zmax_med** | float64 | kpc | Maximum distance to the Galactic plane from GravPot16 (Fernandez-Trincado 2017), median value |
| **zmax_upp** | float64 | kpc | Maximum distance to the Galactic plane from GravPot16 (Fernandez-Trincado 2017), 84th percentile |
| **zmax_low** | float64 | kpc | Maximum distance to the Galactic plane from GravPot16 (Fernandez-Trincado 2017), 16th percentile |



