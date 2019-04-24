
# Datamodel: BOSSLyaDR9_cat



#### General Description
<p>This catalog lists objects in the <a href="https://www.sdss.org/dr9/algorithms/lyaf_sample.php">DR9 Lyman-alpha Forest Sample</a>,
that are suitable for Lyman-alpha forest analysis. This is a greatly simplified sub-sample of the
<a href="https://www.sdss.org/dr9/algorithms/qso_catalog.php">DR9 Quasar Catalog</a>, with the fields
SNR, SNR_LYAF, CHISQ_CONT, CONT_FLAG, CONT_TEMPLATE, Z_DLA, and Z_DLA added.
Each object in the catalog has a corresponding <a href="speclya.html">speclya</a> file.</p>
<p>
This documentation describes the FITS format file
<a href="/sas/dr9/env/BOSS_LYA/cat/BOSSLyaDR9_cat.fits">BOSSLyaDR9_cat.fits</a>;
there is also an ASCII version
<a href="/sas/dr9/env/BOSS_LYA/cat/BOSSLyaDR9_cat.txt">BOSSLyaDR9_cat.txt</a>
with the same columns in the same order as described below.
</p>


#### Naming Convention
<code>BOSSLyaDR9_cat\.(fits|txt)</code>


#### Approximate Size
4 MB


#### File Type
FITS or ASCII


## Page Contents
* [HDU0: NULL EXTENSION](#hdu0-null-extension)
* [HDU1: BOSSLYADR9_CAT CATALOG](#hdu1-bosslyadr9-cat-catalog)

## HDU0: NULL EXTENSION
This is a null header created by IDL MWRFITS.




## HDU1: BOSSLYADR9_CAT CATALOG
EXTNAME="BOSSLyaDR9_cat" with a binary FITS table containing the following columns:

### HDU Type
IMAGE




		Required Data Table Columns


| **Name** | **Type** | **Unit** | **Description** |
| :--- | :----- | :---- | :------- |
| **SDSS_NAME** | char[18] | - | SDSS-DR9 designation |
| **RA** | float32 | deg | RA (J2000) |
| **DEC** | float32 | deg | DEC (J2000) |
| **THING_ID** | int32 | - | Unique identifier |
| **PLATE** | int32 | - | Plate number |
| **MJD** | int32 | - | Spectroscopic MJD |
| **FIBERID** | int32 | - | Fiber number |
| **Z_VI** | float32 | - | Visual inspection redshift from DR9Q |
| **Z_PIPE** | float32 | - | BOSS pipeline redshift |
| **SNR** | float32 | - | Median signal-to-noise ratio (1268-1380A rest) |
| **SNR_LYAF** | float32 | - | Median signal-to-noise ratio (1041-1185A rest) |
| **CHISQ_CONT** | float32 | - | Reduced chi-squared of continuum fit |
| **CONT_FLAG** | int32 | - | Continuum visual inspection flag |
| **CONT_TEMPLATE** | char[8] | - | Quasar template used |
| **Z_DLA** | float32 | - | DLA absorption redshift. Set to -1 in objects without DLAs. |
| **LOG_NHI** | float32 | - | DLA HI column density, log10(N_HI [cm^-2]). Set to -1 in objects without DLAs. |



