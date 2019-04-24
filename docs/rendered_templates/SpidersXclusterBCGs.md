
# Datamodel: SpidersXclusterBCGs



#### General Description
The SpidersXclusterBCGs file contains the catalogue of the brightest
Cluster Galaxies properties of <a href="http://www.sdss.org/vac/spiders-x-ray-galaxy-cluster-catalogue-for-dr14/">SPIDERS X-ray galaxy clusters</a>.
This file lists the BCGs identified as part of this process, along with stellar mass, star formation
and morphlogical properties of them.

 BCGs are identified based on the available spectroscopic data from SPIDERS and photometric data from SDSS (Erfanianfar et al. in preparation).
 Only those SPIDERS clusters which have one componant in <a href="http://www.sdss.org/vac/spiders-x-ray-galaxy-cluster-catalogue-for-dr14/">SPIDERS X-ray galaxy clusters</a> are considered in this analysis.
 Stellar masses and SFRs of the BCGs are computed by combining SDSS, WISE and GALEX photometry and using state-of-art SED fitting. When the SFR from MPA-JHU value-added catalog is available, we substitute it for SED fitting SFR. The morphology properties (effective radius, Sersic index, axis ratio, integrated magnitude and reduces chi2 for the frame) for all BCGs are provided by Sersic profile fitting using SIGMA (Kelvin et al., 2012) in different optical bands (g/r/i). Three models are provided, in 3 bands: Free Sersic (n=1-20, S), Free Sersic + Exponential (n=1-20 + n=1, SX) and De Vaucouleurs (n=4, V) (Furnell et al. in preparation).


#### Naming Convention
SpidersXclusterBCGs-v2.0


#### Approximate Size
1 MB


#### File Type
FITS


## Page Contents
* [HDU1: SPIDERS XCLUSTER BCGS](#hdu1-spiders-xcluster-bcgs)

## HDU1: SPIDERS XCLUSTER BCGS
This HDU contains the list of BCGs of the SPIDER Xray galaxy clusters and their properties.

### HDU Type
IMAGE




		Required Data Table Columns


| **Name** | **Type** | **Unit** | **Description** |
| :--- | :----- | :---- | :------- |
| **CLUS_ID** | char | 		 | The SPIDERS/CODEX
  identification number {i}_{nnnnn} (from <a href="/datamodel/files/SPIDERS_TARGET/spiderstargetClusters.html">spiderstargetClusters</a>) |
| **CLUZSPEC** | float | 		 | Galaxy cluster redshift |
| **RA_BCG** | double | deg | BCG right ascension (J2000) |
| **DEC_BCG** | double | deg | BCG declination (J2000) |
| **Mass_MEDIAN** | double | Msun | log(Stellar Mass) |
| **SFR_MEDIAN** | double | Msun/yr | log(SFR) |
| **flag_SFR_MPA_JHU** | double | 		 | =1 if from MPA_JHU VAC |
| **GAL_sdss_g_modS_CHI2NU** | double | 		 | Reduced chi^2 for single-Sersic fit in the g_band |
| **GAL_sdss_g_modS_C1_MAG** | float | 		 | Primary object magnitude for single-Sersic fit in the g_band |
| **GAL_sdss_g_modS_C1_RE** | double | arcsec | Primary object effective radius for single-Sersic fit in the g_band |
| **GAL_sdss_g_modS_C1_N** | float | 		 | Primary object sersic index for single-Sersic fit in the g_band |
| **GAL_sdss_g_modS_C1_AR** | float | 		 | Primary object axis ratio for single-Sersic fit in the g_band |
| **GAL_sdss_g_modS_C1_PA** | double | 		 | Primary object position angle for single-Sersic fit in the g_band |
| **GAL_sdss_g_modS_C1_MAG_ERR** | float | 		 | Error on magnitude for single-Sersic fit in the g_band |
| **GAL_sdss_g_modS_C1_RE_ERR** | double | arcsec | Error on effective radius of primary object for single-Sersic fit in the g_band |
| **GAL_sdss_g_modS_C1_N_ERR** | float | 		 | Error on Sersic index of primary object for single-Sersic fit in the g_band |
| **GAL_sdss_g_modS_C1_AR_ERR** | float | 		 | Error on axis ratio of primary object for single-Sersic fit in the g_band |
| **GAL_sdss_g_modS_C1_PA_ERR** | float | 		 | Error on position angle of primary object for single-Sersic fit in the g_band |
| **GAL_sdss_r_modS_CHI2NU** | double | 		 | Reduced chi^2 for single-Sersic fit in the r_band |
| **GAL_sdss_r_modS_C1_MAG** | float | 		 | Primary object magnitude for single-Sersic fit in the r_band |
| **GAL_sdss_r_modS_C1_RE** | double | arcsec | Primary object effective radius for single-Sersic fit in the r_band |
| **GAL_sdss_r_modS_C1_N** | float | 		 | Primary object sersic index for single-Sersic fit in the r_band |
| **GAL_sdss_r_modS_C1_AR** | float | 		 | Primary object axis ratio for single-Sersic fit in the r_band |
| **GAL_sdss_r_modS_C1_PA** | double | 		 | Primary object position angle for single-Sersic fit in the r_band |
| **GAL_sdss_r_modS_C1_MAG_ERR** | float | 		 | Error on magnitude for single-Sersic fit in the r_band |
| **GAL_sdss_r_modS_C1_RE_ERR** | double | arcsec | Error on effective radius of primary object for single-Sersic fit in the r_band |
| **GAL_sdss_r_modS_C1_N_ERR** | float | 		 | Error on Sersic index of primary object for single-Sersic fit in the r_band |
| **GAL_sdss_r_modS_C1_AR_ERR** | float | 		 | Error on axis ratio of primary object for single-Sersic fit in the r_band |
| **GAL_sdss_r_modS_C1_PA_ERR** | float | 		 | Error on position angle of primary object for single-Sersic fit in the r_band |
| **GAL_sdss_i_modS_CHI2NU** | double | 		 | Reduced chi^2 for single-Sersic fit in the i_band |
| **GAL_sdss_i_modS_C1_MAG** | float | 		 | Primary object magnitude for single-Sersic fit in the i_band |
| **GAL_sdss_i_modS_C1_RE** | double | arcsec | Primary object effective radius for single-Sersic fit in the i_band |
| **GAL_sdss_i_modS_C1_N** | float | 		 | Primary object sersic index for single-Sersic fit in the i_band |
| **GAL_sdss_i_modS_C1_AR** | float | 		 | Primary object axis ratio for single-Sersic fit in the i_band |
| **GAL_sdss_i_modS_C1_PA** | double | 		 | Primary object position angle for single-Sersic fit in the i_band |
| **GAL_sdss_i_modS_C1_MAG_ERR** | float | 		 | Error on magnitude for single-Sersic fit in the i_band |
| **GAL_sdss_i_modS_C1_RE_ERR** | double | arcsec | Error on effective radius of primary object for single-Sersic fit in the i_band |
| **GAL_sdss_i_modS_C1_N_ERR** | float | 		 | Error on Sersic index of primary object for single-Sersic fit in the i_band |
| **GAL_sdss_i_modS_C1_AR_ERR** | float | 		 | Error on axis ratio of primary object for single-Sersic fit in the i_band |
| **GAL_sdss_i_modS_C1_PA_ERR** | float | 		 | Error on position angle of primary object for single-Sersic fit in the i_band |
| **GAL_sdss_g_modV_CHI2NU** | double | 		 | Reduced chi^2 for De Vaucouleurs fit in the g_band |
| **GAL_sdss_g_modV_C1_MAG** | float | 		 | Primary object magnitude for De Vaucouleurs fit in the g_band |
| **GAL_sdss_g_modV_C1_RE** | double | arcsec | Primary object effective radius for De Vaucouleurs fit in the g_band |
| **GAL_sdss_g_modV_C1_N** | short | 		 | Primary object sersic index for De Vaucouleurs fit in the g_band |
| **GAL_sdss_g_modV_C1_AR** | float | 		 | Primary object axis ratio for De Vaucouleurs fit in the g_band |
| **GAL_sdss_g_modV_C1_PA** | double | 		 | Primary object position angle for De Vaucouleurs fit in the g_band |
| **GAL_sdss_g_modV_C1_MAG_ERR** | float | 		 | Error on magnitude for De Vaucouleurs fit in the g_band |
| **GAL_sdss_g_modV_C1_RE_ERR** | double | arcsec | Error on effective radius of primary object for De Vaucouleurs fit in the g_band |
| **GAL_sdss_g_modV_C1_N_ERR** | short | 		 | Error on Sersic index of primary object for De Vaucouleurs fit in the g_band |
| **GAL_sdss_g_modV_C1_AR_ERR** | float | 		 | Error on axis ratio of primary object for De Vaucouleurs fit in the g_band |
| **GAL_sdss_g_modV_C1_PA_ERR** | float | 		 | Error on position angle of primary object for De Vaucouleurs fit in the g_band |
| **GAL_sdss_r_modV_CHI2NU** | double | 		 | Reduced chi^2 for De Vaucouleurs fit in the r_band |
| **GAL_sdss_r_modV_C1_MAG** | float | 		 | Primary object magnitude for De Vaucouleurs fit in the r_band |
| **GAL_sdss_r_modV_C1_RE** | double | arcsec | Primary object effective radius for De Vaucouleurs fit in the r_band |
| **GAL_sdss_r_modV_C1_N** | short | 		 | Primary object sersic index for De Vaucouleurs fit in the r_band |
| **GAL_sdss_r_modV_C1_AR** | float | 		 | Primary object axis ratio for De Vaucouleurs fit in the r_band |
| **GAL_sdss_r_modV_C1_PA** | double | 		 | Primary object position angle for De Vaucouleurs fit in the r_band |
| **GAL_sdss_r_modV_C1_MAG_ERR** | float | 		 | Error on magnitude for De Vaucouleurs fit in the r_band |
| **GAL_sdss_r_modV_C1_RE_ERR** | double | arcsec | Error on effective radius of primary object for De Vaucouleurs fit in the r_band |
| **GAL_sdss_r_modV_C1_N_ERR** | short | 		 | Error on Sersic index of primary object for De Vaucouleurs fit in the r_band |
| **GAL_sdss_r_modV_C1_AR_ERR** | float | 		 | Error on axis ratio of primary object for De Vaucouleurs fit in the r_band |
| **GAL_sdss_r_modV_C1_PA_ERR** | float | 		 | Error on position angle of primary object for De Vaucouleurs fit in the r_band |
| **GAL_sdss_i_modV_CHI2NU** | double | 		 | Reduced chi^2 for De Vaucouleurs fit in the i_band |
| **GAL_sdss_i_modV_C1_MAG** | float | 		 | Primary object magnitude for De Vaucouleurs fit in the i_band |
| **GAL_sdss_i_modV_C1_RE** | double | arcsec | Primary object effective radius for De Vaucouleurs fit in the i_band |
| **GAL_sdss_i_modV_C1_N** | short | 		 | Primary object sersic index for De Vaucouleurs fit in the i_band |
| **GAL_sdss_i_modV_C1_AR** | float | 		 | Primary object axis ratio for De Vaucouleurs fit in the i_band |
| **GAL_sdss_i_modV_C1_PA** | double | 		 | Primary object position angle for De Vaucouleurs fit in the i_band |
| **GAL_sdss_i_modV_C1_MAG_ERR** | float | 		 | Error on magnitude for De Vaucouleurs fit in the i_band |
| **GAL_sdss_i_modV_C1_RE_ERR** | double | arcsec | Error on effective radius of primary object for De Vaucouleurs fit in the i_band |
| **GAL_sdss_i_modV_C1_N_ERR** | short | 		 | Error on Sersic index of primary object for De Vaucouleurs fit in the i_band |
| **GAL_sdss_i_modV_C1_AR_ERR** | float | 		 | Error on axis ratio of primary object for De Vaucouleurs fit in the i_band |
| **GAL_sdss_i_modV_C1_PA_ERR** | float | 		 | Error on position angle of primary object for De Vaucouleurs fit in the i_band |
| **GAL_sdss_g_modSX_CHI2NU** | double | 		 | Reduced chi^2 of Sersic+exponential fit in the g_band |
| **GAL_sdss_g_modSX_C1_MAG** | float | 		 | Magnitude of component 1 (single-Sersic) of Sersic+exponential fit in the g_band |
| **GAL_sdss_g_modSX_C1_RE** | double | arcsec | Effective radius of component 1 (single-Sersic) of Sersic+exponential fit in the g_band |
| **GAL_sdss_g_modSX_C1_N** | float | 		 | Sersic index of component 1 (single-Sersic) of Sersic+exponential fit in the g_band |
| **GAL_sdss_g_modSX_C1_AR** | float | 		 | Axis ratio of component 1 (single-Sersic) of Sersic+exponential fit in the g_band |
| **GAL_sdss_g_modSX_C1_PA** | double | 		 | Position angle of component 1 (single-Sersic) of Sersic+exponential fit in the g_band |
| **GAL_sdss_g_modSX_C1_MAG_ERR** | float | 		 | Error on magnitude of component 1 (single-Sersic) of Sersic+exponential fit in the g_band |
| **GAL_sdss_g_modSX_C1_RE_ERR** | double | arcsec | Error on effective radius of component 1 (single-Sersic) of Sersic+exponential fit in the g_band |
| **GAL_sdss_g_modSX_C1_N_ERR** | double | 		 | Error on Sersic index of component 1 (single-Sersic) of Sersic+exponential fit in the g_band |
| **GAL_sdss_g_modSX_C1_AR_ERR** | float | 		 | Error on axis ratio of component 1 (single-Sersic) of Sersic+exponential fit in the g_band |
| **GAL_sdss_g_modSX_C1_PA_ERR** | float | 		 | Error on position angle of component 1 (single-Sersic) of Sersic+exponential fit in the g_band |
| **GAL_sdss_g_modSX_C2_MAG** | float | 		 | Magnitude of component 2 (exponential) of Sersic+exponential fit in the g_band |
| **GAL_sdss_g_modSX_C2_RE** | double | arcsec | Effective radius of component 2 (exponential) of Sersic+exponential fit in the g_band |
| **GAL_sdss_g_modSX_C2_N** | short | 		 | Sersic index of component 2 (exponential) of Sersic+exponential fit in the g_band |
| **GAL_sdss_g_modSX_C2_AR** | double | 		 | Axis ratio of component 2 (exponential) of Sersic+exponential fit in the g_band |
| **GAL_sdss_g_modSX_C2_PA** | double | 		 | Position angle of component 2 (exponential) of Sersic+exponential fit in the g_band |
| **GAL_sdss_g_modSX_C2_MAG_ERR** | float | 		 | Error on magnitude of component 2 (exponential) of Sersic+exponential fit in the g_band |
| **GAL_sdss_g_modSX_C2_RE_ERR** | double | arcsec | Error on effective radius of component 2 (exponential) of Sersic+exponential fit in the g_band |
| **GAL_sdss_g_modSX_C2_N_ERR** | short | 		 | Error on Sersic index of component 2 (exponential) of Sersic+exponential fit in the g_band |
| **GAL_sdss_g_modSX_C2_AR_ERR** | float | 		 | Error on axis ratio of component 2 (exponential) of Sersic+exponential fit in the g_band |
| **GAL_sdss_g_modSX_C2_PA_ERR** | float | 		 | Error on position angle of component 2 (exponential) of Sersic+exponential fit in the g_band |
| **GAL_sdss_r_modSX_CHI2NU** | double | 		 | Reduced chi^2 of Sersic+exponential fit in the r_band |
| **GAL_sdss_r_modSX_C1_MAG** | float | 		 | Magnitude of component 1 (single-Sersic) of Sersic+exponential fit in the r_band |
| **GAL_sdss_r_modSX_C1_RE** | double | arcsec | Effective radius of component 1 (single-Sersic) of Sersic+exponential fit in the r_band |
| **GAL_sdss_r_modSX_C1_N** | float | 		 | Sersic index of component 1 (single-Sersic) of Sersic+exponential fit in the r_band |
| **GAL_sdss_r_modSX_C1_AR** | float | 		 | Axis ratio of component 1 (single-Sersic) of Sersic+exponential fit in the r_band |
| **GAL_sdss_r_modSX_C1_PA** | double | 		 | Position angle of component 1 (single-Sersic) of Sersic+exponential fit in the r_band |
| **GAL_sdss_r_modSX_C1_MAG_ERR** | float | 		 | Error on magnitude of component 1 (single-Sersic) of Sersic+exponential fit in the r_band |
| **GAL_sdss_r_modSX_C1_RE_ERR** | double | arcsec | Error on effective radius of component 1 (single-Sersic) of Sersic+exponential fit in the r_band |
| **GAL_sdss_r_modSX_C1_N_ERR** | float | 		 | Error on Sersic index of component 1 (single-Sersic) of Sersic+exponential fit in the r_band |
| **GAL_sdss_r_modSX_C1_AR_ERR** | float | 		 | Error on axis ratio of component 1 (single-Sersic) of Sersic+exponential fit in the r_band |
| **GAL_sdss_r_modSX_C1_PA_ERR** | float | 		 | Error on position angle of component 1 (single-Sersic) of Sersic+exponential fit in the r_band |
| **GAL_sdss_r_modSX_C2_MAG** | float | 		 | Magnitude of component 2 (exponential) of Sersic+exponential fit in the r_band |
| **GAL_sdss_r_modSX_C2_RE** | double | arcsec | Effective radius of component 2 (exponential) of Sersic+exponential fit in the r_band |
| **GAL_sdss_r_modSX_C2_N** | short | 		 | Sersic index of component 2 (exponential) of Sersic+exponential fit in the r_band |
| **GAL_sdss_r_modSX_C2_AR** | float | 		 | Axis ratio of component 2 (exponential) of Sersic+exponential fit in the r_band |
| **GAL_sdss_r_modSX_C2_PA** | double | 		 | Position angle of component 2 (exponential) of Sersic+exponential fit in the r_band |
| **GAL_sdss_r_modSX_C2_MAG_ERR** | float | 		 | Error on magnitude of component 2 (exponential) of Sersic+exponential fit in the r_band |
| **GAL_sdss_r_modSX_C2_RE_ERR** | double | arcsec | Error on effective radius of component 2 (exponential) of Sersic+exponential fit in the r_band |
| **GAL_sdss_r_modSX_C2_N_ERR** | short | 		 | Error on Sersic index of component 2 (exponential) of Sersic+exponential fit in the r_band |
| **GAL_sdss_r_modSX_C2_AR_ERR** | float | 		 | Error on axis ratio of component 2 (exponential) of Sersic+exponential fit in the r_band |
| **GAL_sdss_r_modSX_C2_PA_ERR** | float | 		 | Error on position angle of component 2 (exponential) of Sersic+exponential fit in the r_band |
| **GAL_sdss_i_modSX_CHI2NU** | double | 		 | Reduced chi^2 of Sersic+exponential fit in the i_band |
| **GAL_sdss_i_modSX_C1_MAG** | float | 		 | Magnitude of component 1 (single-Sersic) of Sersic+exponential fit in the i_band |
| **GAL_sdss_i_modSX_C1_RE** | double | arcsec | Effective radius of component 1 (single-Sersic) of Sersic+exponential fit in the i_band |
| **GAL_sdss_i_modSX_C1_N** | float | 		 | Sersic index of component 1 (single-Sersic) of Sersic+exponential fit in the i_band |
| **GAL_sdss_i_modSX_C1_AR** | float | 		 | Axis ratio of component 1 (single-Sersic) of Sersic+exponential fit in the i_band |
| **GAL_sdss_i_modSX_C1_PA** | double | 		 | Position angle of component 1 (single-Sersic) of Sersic+exponential fit in the i_band |
| **GAL_sdss_i_modSX_C1_MAG_ERR** | float | 		 | Error on magnitude of component 1 (single-Sersic) of Sersic+exponential fit in the i_band |
| **GAL_sdss_i_modSX_C1_RE_ERR** | double | arcsec | Error on effective radius of component 1 (single-Sersic) of Sersic+exponential fit in the i_band |
| **GAL_sdss_i_modSX_C1_N_ERR** | float | 		 | Error on Sersic index of component 1 (single-Sersic) of Sersic+exponential fit in the i_band |
| **GAL_sdss_i_modSX_C1_AR_ERR** | float | 		 | Error on axis ratio of component 1 (single-Sersic) of Sersic+exponential fit in the i_band |
| **GAL_sdss_i_modSX_C1_PA_ERR** | float | 		 | Error on position angle of component 1 (single-Sersic) of Sersic+exponential fit in the i_band |
| **GAL_sdss_i_modSX_C2_MAG** | float | 		 | Magnitude of component 2 (exponential) of Sersic+exponential fit in the i_band |
| **GAL_sdss_i_modSX_C2_RE** | double | arcsec | Effective radius of component 2 (exponential) of Sersic+exponential fit in the i_band |
| **GAL_sdss_i_modSX_C2_N** | short | 		 | Sersic index of component 2 (exponential) of Sersic+exponential fit in the i_band |
| **GAL_sdss_i_modSX_C2_AR** | float | 		 | Axis ratio of component 2 (exponential) of Sersic+exponential fit in the i_band |
| **GAL_sdss_i_modSX_C2_PA** | double | 		 | Position angleof component 2 (exponential) of Sersic+exponential fit in the i_band |
| **GAL_sdss_i_modSX_C2_MAG_ERR** | float | 		 | Error on magnitude of component 2 (exponential) of Sersic+exponential fit in the i_band |
| **GAL_sdss_i_modSX_C2_RE_ERR** | double | arcsec | Error on effective radius of component 2 (exponential) of Sersic+exponential fit in the i_band |
| **GAL_sdss_i_modSX_C2_N_ERR** | short | 		 | Error on Sersic index of component 2 (exponential) of Sersic+exponential fit in the i_band |
| **GAL_sdss_i_modSX_C2_AR_ERR** | float | 		 | Error on axis ratio of component 2 (exponential) of Sersic+exponential fit in the i_band |
| **GAL_sdss_i_modSX_C2_PA_ERR** | float | 		 | Error on position angle of component 2 (exponential) of Sersic+exponential fit in the i_band |



