
# Data model: plates



#### General Description
This file contains the list of plates for a given data release, with
associated meta-data gathered from the design files and the reductions.
There is both a FITS and a Yanny version of this file, for convenience;
however, the Yanny version has some of the columns removed.


#### Naming Convention
<code>plates-dr[0-9]+\.(fits|par)</code>, where
<code>[0-9]+</code> is the release number.


#### Approximate Size
5 Mbytes


#### File Type
FITS, Yanny


#### Read by Products
sas


#### Written by Products
sas



## Page Contents
* [HDU0: THE PRIMARY HEADER](#hdu0-the-primary-header)
* [HDU1: THE PLATES DATA](#hdu1-the-plates-data)

## HDU0: THE PRIMARY HEADER


### HDU Type
IMAGE



		Required Header Keywords


| **Key** | **Value** | **Type** | **Comment** |
| :--- | :----- | :---- | :------- |
| **NAXIS** | 0 | int | Empty Header | 
| **SAS_VERS** | 		 | str | Version of sas product | 
| **TREE_VER** | 		 | str | Version of tree product | 



## HDU1: THE PLATES DATA




		Required Header Keywords


| **Key** | **Value** | **Type** | **Comment** |
| :--- | :----- | :---- | :------- |
| **PLATEID** | 		 | char[19] | unique ID, composite of plate number and MJD | 
| **XTENSION** | BINTABLE | str | Table Extension | 
| **FIRSTRELEASE** | 		 | char[4] | Name of release that this plate/mjd/rerun was first distributed in | 
| **TFIELDS** | 131 | int | Number of columns in table | 
| **RUN2D** | 		 | char[6] | reduction name for 2d extraction of plate | 
| **RUN1D** | 		 | char[6] | reduction name for 1d extraction of plate | 
| **RUNSSPP** | 		 | char[3] | reduction name for SSPP ("none" if not run) | 
| **PLATE** | 		 | int32 | plate number | 
| **TILE** | 		 | int32 | tile number for SDSS-I, -II plates (-1 for SDSS-III) [from platelist product] | 
| **DESIGNID** | 		 | int32 | design ID number for SDSS-III plates (-1 for SDSS-I, -II) [from platelist product] | 
| **LOCATIONID** | 		 | int32 | location ID number for SDSS-III plates (-1 for SDSS-I, -II) [from platelist product] | 
| **MJD** | 		 | int32 | MJD of observation (last)  (days) | 
| **MJDLIST** | 		 | char[53] | List of contributing MJDs [from spPlate header] | 
| **racen** | 		 | float64 | RA, J2000 of plate center [from spPlate header]  (deg) | 
| **deccen** | 		 | float64 | Dec, J2000 of plate center [from spPlate header]   (deg) | 
| **iopVersion** | 		 | string | IOP Version [from spPlate header] | 
| **camVersion** | 		 | string | Camera code version  [from spPlate header] | 
| **taiHMS** | 		 | string | Time in string format [from spPlate header] | 
| **dateObs** | 		 | string | Date of 1st row [from spPlate header] | 
| **timeSys** | 		 | string | Time System [from spPlate header] | 
| **cx** | 		 | float64 | x of Normal unit vector in J2000 | 
| **cy** | 		 | float64 | y of Normal unit vector in J2000 | 
| **cz** | 		 | float64 | z of Normal unit vector in J2000 | 
| **cartid** | 		 | int16 | ID of cartridge used for the observation [from spPlate header] | 
| **tai** | 		 | float64 | Mean time (TAI) [from spPlate header]  (sec) | 
| **tai_beg** | 		 | float64 | Beginning time (TAI) [from spPlate header] --/U sec  (sec) | 
| **tai_end** | 		 | float64 | Ending time (TAI) [from spPlate header] --/U sec  (sec) | 
| **airmass** | 		 | float32 | Airmass at central TAI time [from spPlate header] | 
| **mapMjd** | 		 | int32 | hash of map MJD and map number [from spPlate header]  (days) | 
| **mapName** | 		 | string | ID of mapping file [from spPlate header] | 
| **plugFile** | 		 | string | full name of mapping file [from spPlate header] | 
| **expTime** | 		 | float32 | Total Exposure time [from spPlate header]  (sec) | 
| **expt_b1** | 		 | float32 | exposure time in B1 spectrograph [from spPlate header] --/U sec  (sec) | 
| **expt_b2** | 		 | float32 | exposure time in B2 spectrograph [from spPlate header] --/U sec  (sec) | 
| **expt_r1** | 		 | float32 | exposure time in R1 spectrograph [from spPlate header] --/U sec  (sec) | 
| **expt_r2** | 		 | float32 | exposure time in R2 spectrograph [from spPlate header] --/U sec  (sec) | 
| **vers2d** | 		 | string | idlspec2d version used during 2d reduction [from spPlate header] | 
| **verscomb** | 		 | string | idlspec2d version used during combination of multiple exposures [from spPlate header] | 
| **vers1d** | 		 | string | idlspec2d version used during redshift fitting [from spPlate header] | 
| **survey** | 		 | string | Name of survey [from platelist product] | 
| **chunk** | 		 | string | Name of tiling chunk  [from platelist product] | 
| **programname** | 		 | string | Name of program to which plate belongs (see the target selection section of the <a href="http://www.sdss.org/dr13/algorithms">algorithms page</a> for details) [from platelist product] | 
| **platerun** | 		 | string | Drilling run for plate [from platelist product] | 
| **design_comments** | 		 | string | Comments on the plate design from plate plans [from platelist product] | 
| **platequality** | 		 | string | Characterization of <a href="http://www.sdss.org/dr13/help/glossary/#platequality">plate quality</a> | 
| **platesn2** | 		 | float32 | Overall signal to noise measure for plate | 
| **nExp** | 		 | int16 | Number of exposures total [from spPlate header] | 
| **nExp_B1** | 		 | int32 | Number of exposures in B1 spectrograph  [from spPlate header] | 
| **nExp_B2** | 		 | int32 | Number of exposures in B2 spectrograph  [from spPlate header] | 
| **nExp_R1** | 		 | int32 | Number of exposures in R1 spectrograph  [from spPlate header] | 
| **nExp_R2** | 		 | int32 | Number of exposures in R2 spectrograph  [from spPlate header] | 
| **sn2_g1** | 		 | float32 | signal-to-noise ratio squared in spectrograph #1 in g-band [from spPlate header] | 
| **sn2_r1** | 		 | float32 | signal-to-noise ratio squared in spectrograph #1 in r-band [from spPlate header] | 
| **sn2_i1** | 		 | float32 | signal-to-noise ratio squared in spectrograph #1 in i-band [from spPlate header] | 
| **sn2_g2** | 		 | float32 | signal-to-noise ratio squared in spectrograph #2 in g-band [from spPlate header] | 
| **sn2_r2** | 		 | float32 | signal-to-noise ratio squared in spectrograph #2 in r-band [from spPlate header] | 
| **sn2_i2** | 		 | float32 | signal-to-noise ratio squared in spectrograph #2 in i-band [from spPlate header] | 
| **snturnoff** | 		 | float32 | for SEGUE plates, signal-to-noise of turnoff stars at g=18 (-9999 if no turnoff stars available) | 
| **nturnoff** | 		 | float32 | for SEGUE plates, number of turnoff stars available | 
| **helio_RV** | 		 | float32 | Heliocentric velocity correction [from spPlate header]  (km) | 
| **gOffStd** | 		 | float32 | Mean g-band mag difference (spectro - photo) for standards [from spPlate header]  (mag) | 
| **gRMSStd** | 		 | float32 | Stddev of g-band mag difference (spectro - photo) for standards [from spPlate header]  (mag) | 
| **rOffStd** | 		 | float32 | Mean r-band mag difference (spectro - photo) for standards [from spPlate header]  (mag) | 
| **rRMSStd** | 		 | float32 | Stddev of r-band mag difference (spectro - photo) for standards [from spPlate header]  (mag) | 
| **iOffStd** | 		 | float32 | Mean i-band mag difference (spectro - photo) for standards [from spPlate header]  (mag) | 
| **iRMSStd** | 		 | float32 | Stddev of i-band mag difference (spectro - photo) for standards [from spPlate header]  (mag) | 
| **grOffStd** | 		 | float32 | Mean g-band mag difference (spectro - photo) for standards [from spPlate header]  (mag) | 
| **grRMSStd** | 		 | float32 | Stddev of g-band mag difference (spectro - photo) for standards [from spPlate header]  (mag) | 
| **riOffStd** | 		 | float32 | Mean r-band mag difference (spectro - photo) for standards [from spPlate header]  (mag) | 
| **riRMSStd** | 		 | float32 | Stddev of r-band mag difference (spectro - photo) for standards [from spPlate header]  (mag) | 
| **gOffGal** | 		 | float32 | Mean g-band mag difference (spectro - photo) for galaxies [from spPlate header]  (mag) | 
| **gRMSGal** | 		 | float32 | Stddev of g-band mag difference (spectro - photo) for galaxies [from spPlate header]  (mag) | 
| **rOffGal** | 		 | float32 | Mean r-band mag difference (spectro - photo) for galaxies [from spPlate header]  (mag) | 
| **rRMSGal** | 		 | float32 | Stddev of r-band mag difference (spectro - photo) for galaxies [from spPlate header]  (mag) | 
| **iOffGal** | 		 | float32 | Mean i-band mag difference (spectro - photo) for galaxies [from spPlate header]  (mag) | 
| **iRMSGal** | 		 | float32 | Stddev of i-band mag difference (spectro - photo) for galaxies [from spPlate header]  (mag) | 
| **grOffGal** | 		 | float32 | Mean g-band mag difference (spectro - photo) for galaxies [from spPlate header]  (mag) | 
| **grRMSGal** | 		 | float32 | Stddev of g-band mag difference (spectro - photo) for galaxies [from spPlate header]  (mag) | 
| **riOffGal** | 		 | float32 | Mean r-band mag difference (spectro - photo) for galaxies [from spPlate header]  (mag) | 
| **riRMSGal** | 		 | float32 | Stddev of r-band mag difference (spectro - photo) for galaxies [from spPlate header]  (mag) | 
| **nGuide** | 		 | int32 | Number of guider camera frames taken during the exposure [from spPlate header] | 
| **seeing20** | 		 | float32 | 20th-percentile of seeing during exposure (arcsec) [from spPlate header] | 
| **seeing50** | 		 | float32 | 50th-percentile of seeing during exposure (arcsec) [from spPlate header] | 
| **seeing80** | 		 | float32 | 80th-percentile of seeing during exposure (arcsec) [from spPlate header] | 
| **rmsoff20** | 		 | float32 | 20th-percentile of RMS offset of guide fibers (arcsec) [from spPlate header] | 
| **rmsoff50** | 		 | float32 | 50th-percentile of RMS offset of guide fibers (arcsec) [from spPlate header] | 
| **rmsoff80** | 		 | float32 | 80th-percentile of RMS offset of guide fibers (arcsec) [from spPlate header] | 
| **airtemp** | 		 | float32 | Air temperature in the dome [from spPlate header] (deg) | 
| **sfd_used** | 		 | int8 | Were the SFD dust maps applied to the output spectrum? (0 = no, 1 = yes) | 
| **xSigma** | 		 | float32 | sigma of gaussian fit to spatial profile [from spPlate header] | 
| **xSigMin** | 		 | float32 | minimum of xSigma for all exposures [from spPlate header] | 
| **xSigMax** | 		 | float32 | maximum of xSigma for all exposures [from spPlate header] | 
| **wSigma** | 		 | float32 | sigma of gaussian fit to arc-line profiles in wavelength direction [from spPlate header] | 
| **wSigMin** | 		 | float32 | minimum of wSigma for all exposures [from spPlate header] | 
| **wSigMax** | 		 | float32 | minimum of wSigma for all exposures [from spPlate header] | 
| **xChi2** | 		 | float32 | [from spPlate header] | 
| **xChi2Min** | 		 | float32 | [from spPlate header] | 
| **xChi2Max** | 		 | float32 | [from spPlate header] | 
| **skyChi2** | 		 | float32 | average chi-squared from sky subtraction from all exposures [from spPlate header] | 
| **schi2min** | 		 | float32 | minimum and maximum skyChi2 over all exposures [from spPlate header] | 
| **schi2max** | 		 | float32 | minimum and maximum skyChi2 over all exposures [from spPlate header] | 
| **fBadPix** | 		 | float32 | Fraction of pixels that are bad (total), meaning masked or with BADSKYCHI or REDMONSTER flags set [from spPlate header] | 
| **fBadPix1** | 		 | float32 | Fraction of pixels that are bad (spectrograph #1) [from spPlate header] | 
| **fBadPix2** | 		 | float32 | Fraction of pixels that are bad (spectrograph #2) [from spPlate header] | 
| **status2d** | 		 | string | Status of 2D extraction | 
| **statuscombine** | 		 | string | Status of combination of multiple MJDs | 
| **status1d** | 		 | string | Status of 1D reductions | 
| **n_galaxy** | 		 | float32 | Number of objects classified as galaxy [calculated from spZbest file] | 
| **n_qso** | 		 | float32 | Number of objects classified as QSO [calculated from spZbest file] | 
| **n_star** | 		 | float32 | Number of objects classified as Star [calculated from spZbest file] | 
| **n_sky** | 		 | float32 | Number of sky objects  [calculated from spZbest file] | 
| **n_unknown** | 		 | float32 | Number of objects with zWarning set non-zero (such objects still classified as star, galaxy or QSO) [calculated from spZbest file] | 
| **is_tile** | 		 | int8 | is this plate the best representative of this tile? only set for "legacy" program plates (see <a href="http://www.sdss.org/dr13/help/glossary/#IS_TILE"> glossary</a>) | 
| **is_primary** | 		 | int8 | is this MJD a primary observation a plate (best and not bad quality; see <a href="http://www.sdss.org/dr13/help/glossary/#IS_PRIMARY">glossary</a>) | 
| **is_best** | 		 | int8 | is this MJD the best observation of the plate (see <a href="http://www.sdss.org/dr13/help/glossary/#IS_BEST">glossary</a>) | 
| **haMin** | 		 | float32 | min hour angle design [from plPlugMapM file] --/U deg  (deg) | 
| **haMax** | 		 | float32 | max hour angle design [from plPlugMapM file] --/U deg  (deg) | 
| **mjdDesign** | 		 | int32 | MJD designed for [from plPlugMapM file] | 
| **theta** | 		 | float32 | cartridge position angle [from plPlugMapM file] | 
| **fscan_version** | 		 | string | version of fiber scanning software [from plPlugMapM file] | 
| **fmap_version** | 		 | string | version of fiber mapping software [from plPlugMapM file] | 
| **fscan_mode** | 		 | string | 'slow', 'fast', or 'extreme' [from plPlugMapM file] | 
| **fscan_speed** | 		 | int32 | speed of scan [from plPlugMapM file] | 



		Required Columns


| **Name** | **Type** | **Unit** | **Description** |
| :--- | :----- | :---- | :------- |
| **PLATEID** | 		 | char[19] | unique ID, composite of plate number and MJD |
| **FIRSTRELEASE** | 		 | char[4] | Name of release that this plate/mjd/rerun was first distributed in |
| **RUN2D** | 		 | char[6] | reduction name for 2d extraction of plate |
| **RUN1D** | 		 | char[6] | reduction name for 1d extraction of plate |
| **RUNSSPP** | 		 | char[3] | reduction name for SSPP ("none" if not run) |
| **PLATE** | 		 | int32 | plate number |
| **TILE** | 		 | int32 | tile number for SDSS-I, -II plates (-1 for SDSS-III) [from platelist product] |
| **DESIGNID** | 		 | int32 | design ID number for SDSS-III plates (-1 for SDSS-I, -II) [from platelist product] |
| **LOCATIONID** | 		 | int32 | location ID number for SDSS-III plates (-1 for SDSS-I, -II) [from platelist product] |
| **MJD** | 		 | int32 | MJD of observation (last)  (days) |
| **MJDLIST** | 		 | char[53] | List of contributing MJDs [from spPlate header] |
| **racen** | 		 | float64 | RA, J2000 of plate center [from spPlate header]  (deg) |
| **deccen** | 		 | float64 | Dec, J2000 of plate center [from spPlate header]   (deg) |
| **iopVersion** | 		 | string | IOP Version [from spPlate header] |
| **camVersion** | 		 | string | Camera code version  [from spPlate header] |
| **taiHMS** | 		 | string | Time in string format [from spPlate header] |
| **dateObs** | 		 | string | Date of 1st row [from spPlate header] |
| **timeSys** | 		 | string | Time System [from spPlate header] |
| **cx** | 		 | float64 | x of Normal unit vector in J2000 |
| **cy** | 		 | float64 | y of Normal unit vector in J2000 |
| **cz** | 		 | float64 | z of Normal unit vector in J2000 |
| **cartid** | 		 | int16 | ID of cartridge used for the observation [from spPlate header] |
| **tai** | 		 | float64 | Mean time (TAI) [from spPlate header]  (sec) |
| **tai_beg** | 		 | float64 | Beginning time (TAI) [from spPlate header] --/U sec  (sec) |
| **tai_end** | 		 | float64 | Ending time (TAI) [from spPlate header] --/U sec  (sec) |
| **airmass** | 		 | float32 | Airmass at central TAI time [from spPlate header] |
| **mapMjd** | 		 | int32 | hash of map MJD and map number [from spPlate header]  (days) |
| **mapName** | 		 | string | ID of mapping file [from spPlate header] |
| **plugFile** | 		 | string | full name of mapping file [from spPlate header] |
| **expTime** | 		 | float32 | Total Exposure time [from spPlate header]  (sec) |
| **expt_b1** | 		 | float32 | exposure time in B1 spectrograph [from spPlate header] --/U sec  (sec) |
| **expt_b2** | 		 | float32 | exposure time in B2 spectrograph [from spPlate header] --/U sec  (sec) |
| **expt_r1** | 		 | float32 | exposure time in R1 spectrograph [from spPlate header] --/U sec  (sec) |
| **expt_r2** | 		 | float32 | exposure time in R2 spectrograph [from spPlate header] --/U sec  (sec) |
| **vers2d** | 		 | string | idlspec2d version used during 2d reduction [from spPlate header] |
| **verscomb** | 		 | string | idlspec2d version used during combination of multiple exposures [from spPlate header] |
| **vers1d** | 		 | string | idlspec2d version used during redshift fitting [from spPlate header] |
| **survey** | 		 | string | Name of survey [from platelist product] |
| **chunk** | 		 | string | Name of tiling chunk  [from platelist product] |
| **programname** | 		 | string | Name of program to which plate belongs (see the target selection section of the <a href="http://www.sdss.org/dr13/algorithms">algorithms page</a> for details) [from platelist product] |
| **platerun** | 		 | string | Drilling run for plate [from platelist product] |
| **design_comments** | 		 | string | Comments on the plate design from plate plans [from platelist product] |
| **platequality** | 		 | string | Characterization of <a href="http://www.sdss.org/dr13/help/glossary/#platequality">plate quality</a> |
| **platesn2** | 		 | float32 | Overall signal to noise measure for plate |
| **nExp** | 		 | int16 | Number of exposures total [from spPlate header] |
| **nExp_B1** | 		 | int32 | Number of exposures in B1 spectrograph  [from spPlate header] |
| **nExp_B2** | 		 | int32 | Number of exposures in B2 spectrograph  [from spPlate header] |
| **nExp_R1** | 		 | int32 | Number of exposures in R1 spectrograph  [from spPlate header] |
| **nExp_R2** | 		 | int32 | Number of exposures in R2 spectrograph  [from spPlate header] |
| **sn2_g1** | 		 | float32 | signal-to-noise ratio squared in spectrograph #1 in g-band [from spPlate header] |
| **sn2_r1** | 		 | float32 | signal-to-noise ratio squared in spectrograph #1 in r-band [from spPlate header] |
| **sn2_i1** | 		 | float32 | signal-to-noise ratio squared in spectrograph #1 in i-band [from spPlate header] |
| **sn2_g2** | 		 | float32 | signal-to-noise ratio squared in spectrograph #2 in g-band [from spPlate header] |
| **sn2_r2** | 		 | float32 | signal-to-noise ratio squared in spectrograph #2 in r-band [from spPlate header] |
| **sn2_i2** | 		 | float32 | signal-to-noise ratio squared in spectrograph #2 in i-band [from spPlate header] |
| **snturnoff** | 		 | float32 | for SEGUE plates, signal-to-noise of turnoff stars at g=18 (-9999 if no turnoff stars available) |
| **nturnoff** | 		 | float32 | for SEGUE plates, number of turnoff stars available |
| **helio_RV** | 		 | float32 | Heliocentric velocity correction [from spPlate header]  (km) |
| **gOffStd** | 		 | float32 | Mean g-band mag difference (spectro - photo) for standards [from spPlate header]  (mag) |
| **gRMSStd** | 		 | float32 | Stddev of g-band mag difference (spectro - photo) for standards [from spPlate header]  (mag) |
| **rOffStd** | 		 | float32 | Mean r-band mag difference (spectro - photo) for standards [from spPlate header]  (mag) |
| **rRMSStd** | 		 | float32 | Stddev of r-band mag difference (spectro - photo) for standards [from spPlate header]  (mag) |
| **iOffStd** | 		 | float32 | Mean i-band mag difference (spectro - photo) for standards [from spPlate header]  (mag) |
| **iRMSStd** | 		 | float32 | Stddev of i-band mag difference (spectro - photo) for standards [from spPlate header]  (mag) |
| **grOffStd** | 		 | float32 | Mean g-band mag difference (spectro - photo) for standards [from spPlate header]  (mag) |
| **grRMSStd** | 		 | float32 | Stddev of g-band mag difference (spectro - photo) for standards [from spPlate header]  (mag) |
| **riOffStd** | 		 | float32 | Mean r-band mag difference (spectro - photo) for standards [from spPlate header]  (mag) |
| **riRMSStd** | 		 | float32 | Stddev of r-band mag difference (spectro - photo) for standards [from spPlate header]  (mag) |
| **gOffGal** | 		 | float32 | Mean g-band mag difference (spectro - photo) for galaxies [from spPlate header]  (mag) |
| **gRMSGal** | 		 | float32 | Stddev of g-band mag difference (spectro - photo) for galaxies [from spPlate header]  (mag) |
| **rOffGal** | 		 | float32 | Mean r-band mag difference (spectro - photo) for galaxies [from spPlate header]  (mag) |
| **rRMSGal** | 		 | float32 | Stddev of r-band mag difference (spectro - photo) for galaxies [from spPlate header]  (mag) |
| **iOffGal** | 		 | float32 | Mean i-band mag difference (spectro - photo) for galaxies [from spPlate header]  (mag) |
| **iRMSGal** | 		 | float32 | Stddev of i-band mag difference (spectro - photo) for galaxies [from spPlate header]  (mag) |
| **grOffGal** | 		 | float32 | Mean g-band mag difference (spectro - photo) for galaxies [from spPlate header]  (mag) |
| **grRMSGal** | 		 | float32 | Stddev of g-band mag difference (spectro - photo) for galaxies [from spPlate header]  (mag) |
| **riOffGal** | 		 | float32 | Mean r-band mag difference (spectro - photo) for galaxies [from spPlate header]  (mag) |
| **riRMSGal** | 		 | float32 | Stddev of r-band mag difference (spectro - photo) for galaxies [from spPlate header]  (mag) |
| **nGuide** | 		 | int32 | Number of guider camera frames taken during the exposure [from spPlate header] |
| **seeing20** | 		 | float32 | 20th-percentile of seeing during exposure (arcsec) [from spPlate header] |
| **seeing50** | 		 | float32 | 50th-percentile of seeing during exposure (arcsec) [from spPlate header] |
| **seeing80** | 		 | float32 | 80th-percentile of seeing during exposure (arcsec) [from spPlate header] |
| **rmsoff20** | 		 | float32 | 20th-percentile of RMS offset of guide fibers (arcsec) [from spPlate header] |
| **rmsoff50** | 		 | float32 | 50th-percentile of RMS offset of guide fibers (arcsec) [from spPlate header] |
| **rmsoff80** | 		 | float32 | 80th-percentile of RMS offset of guide fibers (arcsec) [from spPlate header] |
| **airtemp** | 		 | float32 | Air temperature in the dome [from spPlate header] (deg) |
| **sfd_used** | 		 | int8 | Were the SFD dust maps applied to the output spectrum? (0 = no, 1 = yes) |
| **xSigma** | 		 | float32 | sigma of gaussian fit to spatial profile [from spPlate header] |
| **xSigMin** | 		 | float32 | minimum of xSigma for all exposures [from spPlate header] |
| **xSigMax** | 		 | float32 | maximum of xSigma for all exposures [from spPlate header] |
| **wSigma** | 		 | float32 | sigma of gaussian fit to arc-line profiles in wavelength direction [from spPlate header] |
| **wSigMin** | 		 | float32 | minimum of wSigma for all exposures [from spPlate header] |
| **wSigMax** | 		 | float32 | minimum of wSigma for all exposures [from spPlate header] |
| **xChi2** | 		 | float32 | [from spPlate header] |
| **xChi2Min** | 		 | float32 | [from spPlate header] |
| **xChi2Max** | 		 | float32 | [from spPlate header] |
| **skyChi2** | 		 | float32 | average chi-squared from sky subtraction from all exposures [from spPlate header] |
| **schi2min** | 		 | float32 | minimum and maximum skyChi2 over all exposures [from spPlate header] |
| **schi2max** | 		 | float32 | minimum and maximum skyChi2 over all exposures [from spPlate header] |
| **fBadPix** | 		 | float32 | Fraction of pixels that are bad (total), meaning masked or with BADSKYCHI or REDMONSTER flags set [from spPlate header] |
| **fBadPix1** | 		 | float32 | Fraction of pixels that are bad (spectrograph #1) [from spPlate header] |
| **fBadPix2** | 		 | float32 | Fraction of pixels that are bad (spectrograph #2) [from spPlate header] |
| **status2d** | 		 | string | Status of 2D extraction |
| **statuscombine** | 		 | string | Status of combination of multiple MJDs |
| **status1d** | 		 | string | Status of 1D reductions |
| **n_galaxy** | 		 | float32 | Number of objects classified as galaxy [calculated from spZbest file] |
| **n_qso** | 		 | float32 | Number of objects classified as QSO [calculated from spZbest file] |
| **n_star** | 		 | float32 | Number of objects classified as Star [calculated from spZbest file] |
| **n_sky** | 		 | float32 | Number of sky objects  [calculated from spZbest file] |
| **n_unknown** | 		 | float32 | Number of objects with zWarning set non-zero (such objects still classified as star, galaxy or QSO) [calculated from spZbest file] |
| **is_tile** | 		 | int8 | is this plate the best representative of this tile? only set for "legacy" program plates (see <a href="http://www.sdss.org/dr13/help/glossary/#IS_TILE"> glossary</a>) |
| **is_primary** | 		 | int8 | is this MJD a primary observation a plate (best and not bad quality; see <a href="http://www.sdss.org/dr13/help/glossary/#IS_PRIMARY">glossary</a>) |
| **is_best** | 		 | int8 | is this MJD the best observation of the plate (see <a href="http://www.sdss.org/dr13/help/glossary/#IS_BEST">glossary</a>) |
| **haMin** | 		 | float32 | min hour angle design [from plPlugMapM file] --/U deg  (deg) |
| **haMax** | 		 | float32 | max hour angle design [from plPlugMapM file] --/U deg  (deg) |
| **mjdDesign** | 		 | int32 | MJD designed for [from plPlugMapM file] |
| **theta** | 		 | float32 | cartridge position angle [from plPlugMapM file] |
| **fscan_version** | 		 | string | version of fiber scanning software [from plPlugMapM file] |
| **fmap_version** | 		 | string | version of fiber mapping software [from plPlugMapM file] |
| **fscan_mode** | 		 | string | 'slow', 'fast', or 'extreme' [from plPlugMapM file] |
| **fscan_speed** | 		 | int32 | speed of scan [from plPlugMapM file] |



