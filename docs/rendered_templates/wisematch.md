
# Data model: wisematch



#### General Description
Contains cross-matches between the SDSS photoObj objects and the WISE
All-Sky Release catalog.  Please refer to
the <a href="http://wise2.ipac.caltech.edu/docs/release/allsky/expsup/sec2_2a.html">WISE
catalog explanatory supplement</a> for full details on the WISE
catalog columns.  These files only include a subset of the columns.
<br/>

The astrometric matching was done as follows.  First, the "gal" and
"star" datasweep files were loaded and combined.  Then, a
nearest-neighbor astrometric matching was performed to each of the
WISE "slices" (Dec ranges).  This matching records only the nearest
SDSS object for each WISE object, to a maximum distance of 4
arcseconds.  Once all these matches were finished, the results were
combined by inserting the single-slice matches into a table that is
parallel to the "star" and "gal" datasweep files.  For this reason,
there may be some slight oddities near the WISE "slice" boundaries.
But to first order, each WISE object appears at most once.
<br/>

These files are "parallel" to the datasweep files; row 0 of the
"wisematch" file contains the WISE object matching row 0 of the
"calibObj" datasweep file.  The row will contain null values if there
is no such match; you could check the "sweep_index" column to identify
valid matches: value "-1" indicates no match.


#### Naming Convention
<code>wisematch-calibObj-[0-9]{6}-[1-6]-{star,gal}.fits</code>; <code>wisematch-calibObj-RRRRRR-C-{star,gal}.fits</code>
for run RRRRRR and camcol C.

<dt>Approximate Size</dt>
<dd id="filesize">16 MB average</dd>
<dt>File Type</dt>
<dd id="filetype">FITS</dd>
<dt>Read by Products</dt>
<dd>sas</dd>
<dt>Written by Products</dt>
<dd>http://trac.astrometry.net/browser/trunk/projects/wise-sdss</dd>
<dt>Sections</dt>
<dd><p>Parts of files:</p>
<ul>
<li><a href="#hdu0">HDU0</a>: Trivial Primary Header</li>
<li><a href="#hdu1">HDU1</a>: WISE Matches Table</li>
</ul>
</dd>


#### Approximate Size
16 MB average


#### File Type
FITS


#### Read by Products
sas


#### Written by Products
http://trac.astrometry.net/browser/trunk/projects/wise-sdss


## Page Contents
* [HDU0: THE PRIMARY HEADER](#hdu0-the-primary-header)
* [HDU1: WISE CATALOG MATCHES](#hdu1-wise-catalog-matches)

## HDU0: THE PRIMARY HEADER
This HDU has no non-standard required keywords.




## HDU1: WISE CATALOG MATCHES
FITS binary table (BINTABLE) containing WISE catalog data for matched objects.
The <a href="http://wise2.ipac.caltech.edu/docs/release/allsky/expsup/sec2_2a.html">WISE catalog explanatory supplement</a> contains full documentation on the WISE catalog data.
This HDU has no non-standard required keywords.

### HDU Type
IMAGE




		Required Data Table Columns


| **Name** | **Type** | **Unit** | **Description** |
| :--- | :----- | :---- | :------- |
| **cntr** | int64 | 		 | WISE primary key |
| **designation** | char[20] | 		 | WISE object designation, eg "J220625.92+265848.1" |
| **ra** | float64 | deg | WISE RA (right ascension) |
| **dec** | float64 | deg | WISE Dec (declination) |
| **sigra** | float32 | arcsec | WISE error on RA |
| **sigdec** | float32 | arcsec | WISE error on Dec |
| **cc_flags** | char[4] | 		 | WISE contamination and confusion flags |
| **ext_flg** | int32 | 		 | WISE extended source flags |
| **var_flg** | char[4] | 		 | WISE variability flags |
| **moon_lev** | char[4] | 		 | WISE moon level flags |
| **ph_qual** | char[4] | 		 | WISE photometric quality flags |
| **w1mpro** | float32 | mag | WISE W1 profile-fitting mag |
| **w1sigmpro** | float32 | mag | WISE error on w1mpro |
| **w1sat** | float32 | 		 | WISE fraction of pixels saturated |
| **w1nm** | uint8 | 		 | WISE number of individual frames with W1 S/N>3 |
| **w1m** | uint8 | 		 | WISE total number of individual frames |
| **w1snr** | float32 | 		 | WISE W1 signal-to-noise |
| **w1cov** | float32 | 		 | WISE pixel coverage |
| **w1mag** | float32 | mag | WISE W1 aperture mag |
| **w1sigm** | float32 | mag | WISE error on w1mag |
| **w1flg** | uint8 | 		 | WISE W1 flags |
| **w2mpro** | float32 | mag | WISE W2 profile-fitting mag |
| **w2sigmpro** | float32 | mag | WISE error on w2mpro |
| **w2sat** | float32 | 		 | WISE fraction of pixels saturated |
| **w2nm** | uint8 | 		 | WISE number of individual frames with W2 S/N>3 |
| **w2m** | uint8 | 		 | WISE total number of individual frames |
| **w2snr** | float32 | 		 | WISE W2 signal-to-noise |
| **w2cov** | float32 | 		 | WISE pixel coverage |
| **w2mag** | float32 | mag | WISE W2 aperture mag |
| **w2sigm** | float32 | mag | WISE error on w2mag |
| **w2flg** | uint8 | 		 | WISE W2 flags |
| **w3mpro** | float32 | mag | WISE W3 profile-fitting mag |
| **w3sigmpro** | float32 | mag | WISE error on w3mpro |
| **w3sat** | float32 | 		 | WISE fraction of pixels saturated |
| **w3nm** | uint8 | 		 | WISE number of individual frames with W3 S/N>3 |
| **w3m** | uint8 | 		 | WISE total number of individual frames |
| **w3snr** | float32 | 		 | WISE W3 signal-to-noise |
| **w3cov** | float32 | 		 | WISE pixel coverage |
| **w3mag** | float32 | mag | WISE W3 aperture mag |
| **w3sigm** | float32 | mag | WISE error on w3mag |
| **w3flg** | uint8 | 		 | WISE W3 flags |
| **w4mpro** | float32 | mag | WISE W4 profile-fitting mag |
| **w4sigmpro** | float32 | mag | WISE error on w4mpro |
| **w4sat** | float32 | 		 | WISE fraction of pixels saturated |
| **w4nm** | uint8 | 		 | WISE number of individual frames with W4 S/N>3 |
| **w4m** | uint8 | 		 | WISE total number of individual frames |
| **w4snr** | float32 | 		 | WISE W4 signal-to-noise |
| **w4cov** | float32 | 		 | WISE pixel coverage |
| **w4mag** | float32 | mag | WISE W4 aperture mag |
| **w4sigm** | float32 | mag | WISE error on w4mag |
| **w4flg** | uint8 | 		 | WISE W4 flags |
| **sweep_index** | int64 | 		 | Index in the "calibObj" file of this object; equals row index for matches, or -1 for non-matches. |
| **nmatches** | uint8 | 		 | Number of SDSS objects within the 4 arcsecond search radius for the matched WISE object. |
| **match_dist** | float32 | arcsec | Astrometric match distance between SDSS and WISE objects |
| **wise_slice** | int64 | 		 | WISE catalog Dec slice ("part") number (1 to 50); the Dec ranges are listed <a href="http://irsadist.ipac.caltech.edu/wise-allsky/wise-allsky-cat-dec-ranges.txt">here</a>. |
| **wise_index** | int64 | 		 | WISE catalog index within slice ("part") |



