
# Datamodel: VAC_spiders_XMMSL



#### General Description
X-ray and multi-wavelength properties of the <a href="https://heasarc.gsfc.nasa.gov/W3Browse/all/xmmslewcln.html">XMM Slew Survey (version 1.6)</a> sources within the unique, complete "DR14" area, defined as the intersection of the footprints completely covered by spectroscopic observations with SDSS-III/SEQUELS and SDSS-IV/eBOSS DR14. For each XMMSL object, we provide: X-ray properties (separately for each detection band: B0=0.2-12 keV; B4=2-12 keV; B5=0.2-2 keV) ; <a href="http://wise2.ipac.caltech.edu/docs/release/allwise/">AllWISE</a> counterparts, identified via a Bayesian cross-matching algorithm (Dwelly et al. 2017, in press; Salvato et al., in prep.) and WISE photometry; SDSS optical counterparts, and optical photometry; SDSS spectroscopic redshift and flags, as obtained from SDSS-I-II-III and SDSS-IV/SPIDERS observations (up until DR14), and the results of visual inspection (VI) of the spectra, including VI flags; <a href="http://sundog.stsci.edu/">FIRST</a> radio counterparts and radio fluxes; <a href="https://www.cosmos.esa.int/web/gaia/dr1">Gaia DR1</a> optical counterparts, with proper motion (when available) and photometry.


#### Approximate Size
590 KB


#### File Type
FITS


## Page Contents
* [HDU1: [PROPERTIES OF XMM SLEW SURVEY SOURCES]](#hdu1-[properties-of-xmm-slew-survey-sources])

## HDU1: [PROPERTIES OF XMM SLEW SURVEY SOURCES]
Multi-wavelegth properties of ROSAT X-ray sources in DR14 unique footprint.
This HDU has no non-standard required keywords.

### HDU Type
IMAGE




		Required Data Table Columns


| **Name** | **Type** | **Unit** | **Description** |
| :--- | :----- | :---- | :------- |
| **XMMSL_IAU_NAME** | char[40] | 		 | XMMSL source name |
| **XMMSL_RA** | float64 | degrees | XMMSL source Right Ascension |
| **XMMSL_DEC** | float64 | degrees | XMMSL source Declination |
| **XMMSL_RADEC_ERR** | float64 | arcsec | XMMSL source positional error |
| **XMMSL_DET_ML_B0** | float32 | 		 | XMMSL detection likelihood band B0 |
| **XMMSL_DET_ML_B4** | float32 | 		 | XMMSL detection likelihood band B4 |
| **XMMSL_DET_ML_B5** | float32 | 		 | XMMSL detection likelihood band B5 |
| **XMMSL_SCTS_B0** | float32 | counts | XMMSL number of X-ray counts band B0 |
| **XMMSL_SCTS_B0_ERR** | float32 | counts | Error on number of X-ray counts band B0 |
| **XMMSL_SCTS_B4** | float32 | counts | XMMSL number of X-ray counts band B4 |
| **XMMSL_SCTS_B4_ERR** | float32 | counts | Error on number of X-ray counts band B4 |
| **XMMSL_SCTS_B5** | float32 | counts | XMMSL number of X-ray counts band B5 |
| **XMMSL_SCTS_B5_ERR** | float32 | counts | Error on number of X-ray counts band B5 |
| **XMMSL_EXT_B0** | float32 | pixels | XMMSL source extent in pixels band B0 |
| **XMMSL_EXT_B0_ERR** | float32 | pixels | Error on source extent band B0 |
| **XMMSL_EXT_B4** | float32 | pixels | XMMSL source extent in pixels band B4 |
| **XMMSL_EXT_B4_ERR** | float32 | pixels | Error on source extent band B4 |
| **XMMSL_EXT_B5** | float32 | pixels | XMMSL source extent in pixels band B5 |
| **XMMSL_EXT_B5_ERR** | float32 | pixels | Error on source extent band B5 |
| **XMMSL_EXT_ML_B0** | float32 | 		 | XMMSL likelihood of source being extended band B0 |
| **XMMSL_EXT_ML_B4** | float32 | 		 | XMMSL likelihood of source being extended band B4 |
| **XMMSL_EXT_ML_B5** | float32 | 		 | XMMSL likelihood of source being extended band B5 |
| **XMMSL_EXP_MAP_B0** | float32 | seconds | XMMSL Exposure band B0 |
| **XMMSL_EXP_MAP_B4** | float32 | seconds | XMMSL Exposure band B4 |
| **XMMSL_EXP_MAP_B5** | float32 | seconds | XMMSL Exposure band B5 |
| **XMMSL_FLUX_B0** | float32 | (10E-12)ergs/s/cm2 | XMMSL Flux band B0 |
| **XMMSL_FLUX_B0_ERR** | float32 | (10E-12)ergs/s/cm2 | XMMSL Flux Error band B0 |
| **XMMSL_FLUX_B4** | float32 | (10E-12)ergs/s/cm2 | XMMSL Flux band B4 |
| **XMMSL_FLUX_B4_ERR** | float32 | (10E-12)ergs/s/cm2 | XMMSL Flux Error band B4 |
| **XMMSL_FLUX_B5** | float32 | (10E-12)ergs/s/cm2 | XMMSL Flux band B5 |
| **XMMSL_FLUX_B5_ERR** | float32 | (10E-12)ergs/s/cm2 | XMMSL Flux Error band B5 |
| **XMMSL_RATE_B0** | float32 | c/s | XMMSL count rate band B0 |
| **XMMSL_RATE_B0_ERR** | float32 | c/s | XMMSL count rate error band B0 |
| **XMMSL_RATE_B4** | float32 | c/s | XMMSL count rate band B4 |
| **XMMSL_RATE_B4_ERR** | float32 | c/s | XMMSL count rate error band B4 |
| **XMMSL_RATE_B5** | float32 | c/s | XMMSL count rate band B5 |
| **XMMSL_RATE_B5_ERR** | float32 | c/s | XMMSL count rate error band B5 |
| **XMMSL_LOGGALNH** | float32 | log10(cm^-2) | Log of mean Galactic equivalent hydrogen column in the direction of the source |
| **DIST_XRAY_ALLW** | float32 | arcsec | Distance between X-ray source and best AllWISE counterpart |
| **NWAY_bias** | float32 | 		 | bias parameter for the NWAY association (see Salvato et al. 2017) |
| **NWAY_p_any** | float32 | 		 | NWAY probability 2RXS source has an AllWISE counterpart (see Salvato et al. 2017) |
| **NWAY_p_i** | float32 | 		 | NWAY probability AllWISE source is the best counterpart (see Salvato et al. 2017) |
| **ALLW_designation** | char[20] | 		 | AllWISE catalog designation |
| **ALLW_ra** | float64 | deg | AllWISE counterpart Right Ascension |
| **ALLW_dec** | float64 | deg | AllWISE counterpart Declination |
| **ALLW_sigra** | float32 | arcsec | AllWISE error on Right Ascension |
| **ALLW_sigdec** | float32 | arcsec | AllWISE error on Declination |
| **ALLW_RADECERR** | float32 | arcsec | AllWISE positional error |
| **ALLW_w1mpro** | float32 | mag,Vega | W1 magnitude |
| **ALLW_w1sigmpro** | float32 | mag,Vega | Error on W1 magnitude |
| **ALLW_w1snr** | float32 | 		 | W1 SNR |
| **ALLW_w2mpro** | float32 | mag,Vega | W2 magnitude |
| **ALLW_w2sigmpro** | float32 | mag,Vega | Error on W2 magnitude |
| **ALLW_w2snr** | float32 | 		 | W2 SNR |
| **ALLW_w3mpro** | float32 | mag,Vega | W3 magnitude |
| **ALLW_w3sigmpro** | float32 | mag,Vega | Error on W3 magnitude |
| **ALLW_w3snr** | float32 | 		 | W3 SNR |
| **ALLW_w4mpro** | float32 | mag,Vega | W4 magnitude |
| **ALLW_w4sigmpro** | float32 | mag,Vega | Error on W4 magnitude |
| **ALLW_w4snr** | float32 | 		 | W4 SNR |
| **ALLW_cc_flags** | char[4] | 		 | AllWISE CC Flags |
| **ALLW_ext_flg** | int32 | 		 | AllWISE Extent Flag |
| **ALLW_var_flg** | char[4] | 		 | AllWISE Variability Flag |
| **ALLW_r_2mass** | float32 | arcsec | Distance of AllWISE counterpart to 2MASS counterpart |
| **ALLW_n_2mass** | int16 | 		 | Number of near 2MASS counterparts |
| **ALLW_j_m_2mass** | float32 | mag,Vega | 2MASS J magnitude |
| **ALLW_j_msig_2mass** | float32 | mag,Vega | Error on 2MASS J magnitude |
| **ALLW_h_m_2mass** | float32 | mag,Vega | 2MASS H magnitude |
| **ALLW_h_msig_2mass** | float32 | mag,Vega | Error on 2MASS H magnitude |
| **ALLW_k_m_2mass** | float32 | mag,Vega | 2MASS K magnitude |
| **ALLW_k_msig_2mass** | float32 | mag,Vega | Error on 2MASS K magnitude |
| **SDSS_RUN** | int16 | 		 | SDSS counterpart Imaging run number (from photoObj) |
| **SDSS_RERUN** | char[3] | 		 | SDSS counterpart Procession rerun number (from photoObj) |
| **SDSS_CAMCOL** | bool | 		 | SDSS counterpart Column in the imaging camera (from photoObj) |
| **SDSS_FIELD** | int16 | 		 | SDSS counterpart Field sequence number (from photoObj) |
| **SDSS_ID** | int16 | 		 | SDSS counterpart ID |
| **SDSS_RA** | float64 | 		 | SDSS counterpart Right Ascension |
| **SDSS_DEC** | float64 | 		 | SDSS counterpart Declination |
| **SDSS_MODELMAG_u** | float32 | 		 | SDSS counterpart u band MODELMAG |
| **SDSS_MODELMAG_g** | float32 | 		 | SDSS counterpart g band MODELMAG |
| **SDSS_MODELMAG_r** | float32 | 		 | SDSS counterpart r band MODELMAG |
| **SDSS_MODELMAG_i** | float32 | 		 | SDSS counterpart i band MODELMAG |
| **SDSS_MODELMAG_z** | float32 | 		 | SDSS counterpart z band MODELMAG |
| **SDSS_FIBER2MAG_u** | float32 | 		 | SDSS counterpart u band FIBER2MAG |
| **SDSS_FIBER2MAG_g** | float32 | 		 | SDSS counterpart g band FIBER2MAG |
| **SDSS_FIBER2MAG_r** | float32 | 		 | SDSS counterpart r band FIBER2MAG |
| **SDSS_FIBER2MAG_i** | float32 | 		 | SDSS counterpart i band FIBER2MAG |
| **SDSS_FIBER2MAG_z** | float32 | 		 | SDSS counterpart z band FIBER2MAG |
| **DIST_ALLW_SDSS** | float64 | arcsec | Distance between AllWISE and SDSD objects |
| **RANK_DIST_ALLW_SDSS** | int16 | 		 | Rank order of SDSS counterpart in distance |
| **NUM_SDSS** | int16 | 		 | Number of SDSS potential counterparts within 3 arcsec |
| **BESTSDSSDR** | char[4] | 		 | Spectroscopic Data Release used |
| **BESTSDSSDR_PLATE** | int32 | 		 | SDSS Spectroscopic Plate Number (from SpecObj) |
| **BESTSDSSDR_MJD** | int32 | 		 | SDSS Spectroscopic MJD (from SpecObj) |
| **BESTSDSSDR_FIBERID** | int32 | 		 | SDSS Spectroscopic FiberID (from SpecObj) |
| **BESTSDSSDR_Z** | float32 | 		 | SDSS pipeline Redshift |
| **BESTSDSSDR_Z_ERR** | float32 | 		 | SDSS pipeline Redshift Error |
| **BESTSDSSDR_CLASS** | char[6] | 		 | SDSS pipeline Class |
| **BESTSDSSDR_SUBCLASS** | char[21] | 		 | SDSS pipeline Subclass |
| **BESTSDSSDR_ZWARNING** | int32 | 		 | SDSS pipeline ZWARNING |
| **BESTSDSSDR_SN_MEDIAN_ALL** | float32 | 		 | SDSS pipeline median SN |
| **DR7Q_MEMBER** | bool | 		 | Spectroscopic redshift information in DR7 QSO Catalog |
| **DR12Q_MEMBER** | bool | 		 | Spectroscopic redshift information in DR12 QSO Catalog |
| **DR14Q_MEMBER** | bool | 		 | Spectroscopic redshift information in DR14 QSO Catalog |
| **A07_MEMBER** | bool | 		 | Spectroscopic redshift information in Anderson et al. (2007) |
| **P10_MEMBER** | bool | 		 | FIRST Radio Counterpart Right Ascension |
| **VI_MEMBER** | bool | 		 | Flag: Redshift has been visually inspected |
| **VI_ORIGIN** | char[7] | 		 | Origin of Visually inspected Redshift |
| **VI_Z** | float32 | 		 | Visually Inspected Redshift |
| **VI_Z_VS_VI_PIPE** | float32 | 		 | Difference between pipeline and Visually Inspected redshift |
| **VI_CLASS** | char[8] | 		 | Spectral classification after Visual Inspection: (QSO/BLAGN: broad-line quasar; BAL_QSO/QSO_BAL: broad absorption line quasar; NALGN: narrow line AGN; BLAZAR/BLLAC: blazar; GALAXY: galaxy; STAR: star; NONE/UNDET.: unknown) |
| **VI_CONF** | int16 | 		 | Visual Inspection confidence class: (3: secure redshift; 2: uncertain redshift; 1: poor quality redshift; 0: poor quality data; -1: no redshift information) |
| **FIRST_RA** | float64 | deg | FIRST Radio Counterpart Right Ascension |
| **FIRST_DEC** | float64 | deg | FIRST Radio Counterpart Declination |
| **FIRST_FPEAK** | float32 | mJy | FIRST Peak Radio Flux |
| **FIRST_FINT** | float32 | mJy | FIRST Integrated Radio Flux |
| **FIRST_RMS** | float32 | mJy | FIRST Radio flux rms |
| **DIST_ALLW_FIRST** | float64 | arcsec | Distance between AllWISE and FIRST counterparts |
| **FIRST_NCTP** | int16 | 		 | Number of potential FIRST counterparts |
| **GAIA_DR1_ra** | float64 | deg | Gaia DR1 Right Ascension |
| **GAIA_DR1_dec** | float64 | deg | Gaia DR1 Declination |
| **GAIA_DR1_source_id** | int64 | 		 | Gaia DR1 source ID |
| **GAIA_DR1_ref_epoch** | float32 | yr | Gaia DR1 Epoch |
| **GAIA_DR1_ra_error** | float64 | mas | GAIA DR1 Right Ascension Error |
| **GAIA_DR1_dec_error** | float64 | mas | GAIA DR1 Declination Error |
| **GAIA_DR1_parallax** | float64 | mas | GAIA DR1 Parallax |
| **GAIA_DR1_parallax_error** | float64 | mas | GAIA DR1 Parallax Error |
| **GAIA_DR1_pmra** | float64 | mas/yr | GAIA DR1 Right Ascension Proper Motion |
| **GAIA_DR1_pmra_error** | float64 | mas/yr | GAIA DR1 Right Ascension Proper Motion Error |
| **GAIA_DR1_pmdec** | float64 | mas/yr | GAIA DR1 Declination Proper Motion |
| **GAIA_DR1_pmdec_error** | float64 | mas/yr | GAIA DR1 Declination Proper Motion Error |
| **GAIA_DR1_phot_g_mean_flux** | float64 | e-/s | GAIA DR1 g Flux |
| **GAIA_DR1_phot_g_mean_flux_error** | float64 | e-/s | GAIA DR1 g Flux Error |
| **GAIA_ALLW_angDist** | float64 | arcsec | Distance between AllWISE source and GAIA counterparts |



