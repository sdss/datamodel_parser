
# Data model: manga-RSS



#### General Description
The MaNGA DRP provides summary row-stacked spectra (RSS; with both logarithmic and linear wavelength solutions) for each galaxy that combine individual fiber spectra of that galaxy across multiple exposures into a single row-stacked format.
The RSS files are a two-dimensional array with horizontal size N_spec and vertical size N = \sum N_fiber(i) where N_fiber(i) is the number of fibers in the IFU targeting this galaxy for the i'th exposure and the sum runs over all exposures.


#### Naming Convention
<code>manga-[plate]-[ifudesign]-[type]RSS.fits.gz</code>, where <code>[plate]</code> is the plate number, <code>[ifudesign]</code> is the design IFU size and number, and <code>[type]</code> is either LOG or LIN indicating whether the file uses a logarithmic or linear based wavelength solution.  The combined <code>[plate]-[ifudesign]</code> is also known as the 'plate-ifu' designation of a given galaxy.


#### Approximate Size
8 MB - 200+ MB (depending on IFU size, wavelength format, and number of exposures)


#### File Type
gzipped multi-extension FITS


#### Generated by Product
<a href="https://svn.sdss.org/public/repo/manga/mangadrp/tags/v2_4_3/pro/spec3d/mdrp_reduceoneifu.pro">mangadrp: mdrp_reduceoneifu.pro</a>



## Page Contents
* [HDU0: PRIMARY](#hdu0-primary)
* [HDU1: FLUX](#hdu1-flux)
* [HDU2: IVAR](#hdu2-ivar)
* [HDU3: MASK](#hdu3-mask)
* [HDU4: DISP](#hdu4-disp)
* [HDU5: PREDISP](#hdu5-predisp)
* [HDU6: WAVE](#hdu6-wave)
* [HDU7: SPECRES](#hdu7-specres)
* [HDU8: SPECRESD](#hdu8-specresd)
* [HDU9: PRESPECRES](#hdu9-prespecres)
* [HDU10: PRESPECRESD](#hdu10-prespecresd)
* [HDU11: OBSINFO](#hdu11-obsinfo)
* [HDU12: XPOS](#hdu12-xpos)
* [HDU13: YPOS](#hdu13-ypos)

## HDU0: PRIMARY
Empty except for global header

### HDU Type
IMAGE


### HDU Size
0 bytes


		Header Table Caption for HDU0


| **Key** | **Value** | **Type** | **Comment** |
| :--- | :----- | :---- | :------- |
| **SIMPLE** | True | 		 | 		 | 
| **BITPIX** | 8 | 		 | 		 | 
| **NAXIS** | 0 | 		 | 		 | 
| **EXTEND** | True | 		 | 		 | 
| **AUTHOR** | Brian Cherinka & David Law <bcherin1@jhu.edu, dlaw@stsci.edu=""></bcherin1@jhu.edu,> | 		 | 		 | 
| **VERSDRP2** | v2_4_3 | 		 | MaNGA DRP version (2d processing) | 
| **VERSDRP3** | v2_4_3 | 		 | MaNGA DRP Version (3d processing) | 
| **VERSPLDS** | v2_52 | 		 | Platedesign Version | 
| **VERSFLAT** | v1_31 | 		 | Specflat Version | 
| **VERSCORE** | v1_6_2 | 		 | MaNGAcore Version | 
| **VERSPRIM** | v2_5 | 		 | MaNGA Preimaging Version | 
| **VERSUTIL** | v5_5_32 | 		 | Version of idlutils | 
| **VERSIDL** | x86_64 linux unix linux 7.1.1 Aug 21 2009 64 64 | 		 | Version of IDL | 
| **BSCALE** | 1.0 | 		 | Intensity unit scaling | 
| **BZERO** | 0.0 | 		 | Intensity zeropoint | 
| **BUNIT** | 1E-17 erg/s/cm^2/Ang/fiber | 		 | Specific intensity (per fiber-area) | 
| **MASKNAME** | MANGA_DRP2PIXMASK | 		 | Bits in sdssMaskbits.par used by mask extension | 
| **TELESCOP** | SDSS 2.5-M | 		 | Sloan Digital Sky Survey | 
| **INSTRUME** | MaNGA | 		 | SDSS-IV MaNGA IFU | 
| **SRVYMODE** | MaNGA dither | 		 | Survey leading this observation and its mode | 
| **PLATETYP** | APOGEE-2&MaNGA | 		 | Type of plate (e.g. MANGA, APOGEE-2&MANGA) | 
| **OBJSYS** | ICRS | 		 | The TCC objSys | 
| **EQUINOX** | 2000.0 | 		 | 		 | 
| **RADESYS** | FK5 | 		 | 		 | 
| **LAMPLIST** | lamphgcdne.dat | 		 | 		 | 
| **TPLDATA** | BOSZ_3000-11000A.fits | 		 | 		 | 
| **NEXP** | 9 | 		 | Total number of exposures | 
| **EXPTIME** | 8100.87 | 		 | Total exposure time (seconds) | 
| **BLUESN2** | 19.9834 | 		 | Total SN2 in blue channel | 
| **REDSN2** | 42.7417 | 		 | Total SN2 in red channel | 
| **AIRMSMIN** | 1.03987 | 		 | Minimum airmass | 
| **AIRMSMED** | 1.04708 | 		 | Median airmass | 
| **AIRMSMAX** | 1.08221 | 		 | Maximum airmass | 
| **SEEMIN** | 1.1779 | 		 | Best guider seeing | 
| **SEEMED** | 1.30425 | 		 | Median guider seeing | 
| **SEEMAX** | 1.42179 | 		 | Worst guider seeing | 
| **TRANSMIN** | 0.802254 | 		 | Worst guider transparency | 
| **TRANSMED** | 0.831209 | 		 | Median guider transparency | 
| **TRANSMAX** | 0.839501 | 		 | Best guider transparency | 
| **MJDMIN** | 57132 | 		 | MJD of first exposure | 
| **MJDMED** | 57132 | 		 | MJD of median exposure | 
| **MJDMAX** | 57132 | 		 | MJD of last exposure | 
| **DATE-OBS** | 2015-04-20 | 		 | Date of median exposure | 
| **MJDRED** | 58198 | 		 | MJD of the reduction | 
| **DATERED** | 2018-03-21 | 		 | Date of the reduction | 
| **MNGTARG1** | 2336 | 		 | manga_target1 maskbit | 
| **MNGTARG2** | 0 | 		 | manga_target2 maskbit | 
| **MNGTARG3** | 0 | 		 | manga_target3 maskbit | 
| **IFURA** | 232.5447 | 		 | IFU R.A. (J2000 deg.) | 
| **IFUDEC** | 48.690201 | 		 | IFU Dec. (J2000 deg.) | 
| **OBJRA** | 232.544703894 | 		 | Object R.A. (J2000 deg.) | 
| **OBJDEC** | 48.6902009334 | 		 | Object Dec. (J2000 deg.) | 
| **CENRA** | 234.06426 | 		 | Plate center R.A. (J2000 deg.) | 
| **CENDEC** | 48.589874 | 		 | Plate center Dec. (J2000 deg.) | 
| **PLATEID** | 8485 | 		 | Current plate | 
| **DESIGNID** | 8980 | 		 | Current design | 
| **IFUDSGN** | 1901 | 		 | ifuDesign | 
| **FRLPLUG** | 29 | 		 | Plugged ferrule | 
| **PLATEIFU** | 8485-1901 | 		 | PLATEID-ifuDesign | 
| **CARTID** | 3 | 		 | Cart(s) used | 
| **HARNAME** | ma060 | 		 | Harness name(s) | 
| **METFILE** | ma060-56887-1.par | 		 | IFU metrology file(s) | 
| **MANGAID** | 1-209232 | 		 | MaNGA ID number | 
| **CATIDNUM** | 1 | 		 | Primary target input catalog | 
| **PLTTARG** | plateTargets-1.par | 		 | plateTarget reference file | 
| **DRP3QUAL** | 0 | 		 | DRP-3d quality bitmask | 
| **IFUGLON** | 78.9550411299 | 		 | IFU Galactic longitude (deg) | 
| **IFUGLAT** | 52.6212190954 | 		 | IFU Galactic latitude (deg) | 
| **EBVGAL** | 0.0144335 | 		 | Galactic reddening E(B-V) | 
| **DATASUM** | 0 | 		 | data unit checksum updated 2018-03-21T06:08:46 | 
| **CHECKSUM** | YG5FZ949YE4EY949 | 		 | HDU checksum updated 2018-03-21T06:08:46 | 



## HDU1: FLUX
Row-stacked spectra in units of 10^{-17} erg/s/cm2/Angstrom/fiber

### HDU Type
IMAGE


### HDU Size
2 MB


		Header Table Caption for HDU1


| **Key** | **Value** | **Type** | **Comment** |
| :--- | :----- | :---- | :------- |
| **XTENSION** | IMAGE | 		 | IMAGE extension | 
| **BITPIX** | -32 | 		 | Number of bits per data pixel | 
| **NAXIS** | 2 | 		 | Number of data axes | 
| **NAXIS1** | 4563 | 		 | 		 | 
| **NAXIS2** | 171 | 		 | 		 | 
| **PCOUNT** | 0 | 		 | No Group Parameters | 
| **GCOUNT** | 1 | 		 | One Data Group | 
| **AUTHOR** | Brian Cherinka & David Law <bcherin1@jhu.edu, dlaw@stsci.edu=""></bcherin1@jhu.edu,> | 		 | 		 | 
| **VERSDRP2** | v2_4_3 | 		 | MaNGA DRP version (2d processing) | 
| **VERSDRP3** | v2_4_3 | 		 | MaNGA DRP Version (3d processing) | 
| **VERSPLDS** | v2_52 | 		 | Platedesign Version | 
| **VERSFLAT** | v1_31 | 		 | Specflat Version | 
| **VERSCORE** | v1_6_2 | 		 | MaNGAcore Version | 
| **VERSPRIM** | v2_5 | 		 | MaNGA Preimaging Version | 
| **VERSUTIL** | v5_5_32 | 		 | Version of idlutils | 
| **VERSIDL** | x86_64 linux unix linux 7.1.1 Aug 21 2009 64 64 | 		 | Version of IDL | 
| **BSCALE** | 1.0 | 		 | Intensity unit scaling | 
| **BZERO** | 0.0 | 		 | Intensity zeropoint | 
| **BUNIT** | 1E-17 erg/s/cm^2/Ang/fiber | 		 | Specific intensity (per fiber-area) | 
| **MASKNAME** | MANGA_DRP2PIXMASK | 		 | Bits in sdssMaskbits.par used by mask extension | 
| **TELESCOP** | SDSS 2.5-M | 		 | Sloan Digital Sky Survey | 
| **INSTRUME** | MaNGA | 		 | SDSS-IV MaNGA IFU | 
| **SRVYMODE** | MaNGA dither | 		 | Survey leading this observation and its mode | 
| **PLATETYP** | APOGEE-2&MaNGA | 		 | Type of plate (e.g. MANGA, APOGEE-2&MANGA) | 
| **OBJSYS** | ICRS | 		 | The TCC objSys | 
| **EQUINOX** | 2000.0 | 		 | 		 | 
| **RADESYS** | FK5 | 		 | 		 | 
| **LAMPLIST** | lamphgcdne.dat | 		 | 		 | 
| **TPLDATA** | BOSZ_3000-11000A.fits | 		 | 		 | 
| **NEXP** | 9 | 		 | Total number of exposures | 
| **EXPTIME** | 8100.87 | 		 | Total exposure time (seconds) | 
| **BLUESN2** | 19.9834 | 		 | Total SN2 in blue channel | 
| **REDSN2** | 42.7417 | 		 | Total SN2 in red channel | 
| **AIRMSMIN** | 1.03987 | 		 | Minimum airmass | 
| **AIRMSMED** | 1.04708 | 		 | Median airmass | 
| **AIRMSMAX** | 1.08221 | 		 | Maximum airmass | 
| **SEEMIN** | 1.1779 | 		 | Best guider seeing | 
| **SEEMED** | 1.30425 | 		 | Median guider seeing | 
| **SEEMAX** | 1.42179 | 		 | Worst guider seeing | 
| **TRANSMIN** | 0.802254 | 		 | Worst guider transparency | 
| **TRANSMED** | 0.831209 | 		 | Median guider transparency | 
| **TRANSMAX** | 0.839501 | 		 | Best guider transparency | 
| **MJDMIN** | 57132 | 		 | MJD of first exposure | 
| **MJDMED** | 57132 | 		 | MJD of median exposure | 
| **MJDMAX** | 57132 | 		 | MJD of last exposure | 
| **DATE-OBS** | 2015-04-20 | 		 | Date of median exposure | 
| **MJDRED** | 58198 | 		 | MJD of the reduction | 
| **DATERED** | 2018-03-21 | 		 | Date of the reduction | 
| **MNGTARG1** | 2336 | 		 | manga_target1 maskbit | 
| **MNGTARG2** | 0 | 		 | manga_target2 maskbit | 
| **MNGTARG3** | 0 | 		 | manga_target3 maskbit | 
| **IFURA** | 232.5447 | 		 | IFU R.A. (J2000 deg.) | 
| **IFUDEC** | 48.690201 | 		 | IFU Dec. (J2000 deg.) | 
| **OBJRA** | 232.544703894 | 		 | Object R.A. (J2000 deg.) | 
| **OBJDEC** | 48.6902009334 | 		 | Object Dec. (J2000 deg.) | 
| **CENRA** | 234.06426 | 		 | Plate center R.A. (J2000 deg.) | 
| **CENDEC** | 48.589874 | 		 | Plate center Dec. (J2000 deg.) | 
| **PLATEID** | 8485 | 		 | Current plate | 
| **DESIGNID** | 8980 | 		 | Current design | 
| **IFUDSGN** | 1901 | 		 | ifuDesign | 
| **FRLPLUG** | 29 | 		 | Plugged ferrule | 
| **PLATEIFU** | 8485-1901 | 		 | PLATEID-ifuDesign | 
| **CARTID** | 3 | 		 | Cart(s) used | 
| **HARNAME** | ma060 | 		 | Harness name(s) | 
| **METFILE** | ma060-56887-1.par | 		 | IFU metrology file(s) | 
| **MANGAID** | 1-209232 | 		 | MaNGA ID number | 
| **CATIDNUM** | 1 | 		 | Primary target input catalog | 
| **PLTTARG** | plateTargets-1.par | 		 | plateTarget reference file | 
| **DRP3QUAL** | 0 | 		 | DRP-3d quality bitmask | 
| **IFUGLON** | 78.9550411299 | 		 | IFU Galactic longitude (deg) | 
| **IFUGLAT** | 52.6212190954 | 		 | IFU Galactic latitude (deg) | 
| **EBVGAL** | 0.0144335 | 		 | Galactic reddening E(B-V) | 
| **CTYPE1** | WAVE-LOG | 		 | 		 | 
| **CRPIX1** | 1 | 		 | Starting pixel (1-indexed) | 
| **CRVAL1** | 3621.59598486 | 		 | Central wavelength of first pixel | 
| **CD1_1** | 0.833903304339 | 		 | Initial dispersion per pixel | 
| **CUNIT1** | Angstrom | 		 | 		 | 
| **HDUCLASS** | SDSS | 		 | SDSS format class | 
| **HDUCLAS1** | IMAGE | 		 | 		 | 
| **HDUCLAS2** | DATA | 		 | 		 | 
| **ERRDATA** | IVAR | 		 | Error extension name | 
| **QUALDATA** | MASK | 		 | Mask extension name | 
| **EXTNAME** | FLUX | 		 | 		 | 
| **DATASUM** | 404143304 | 		 | data unit checksum updated 2018-03-21T06:08:46 | 
| **CHECKSUM** | MZISMYFQMYFQMYFQ | 		 | HDU checksum updated 2018-03-21T06:08:46 | 



## HDU2: IVAR
Inverse variance of row-stacked spectra

### HDU Type
IMAGE


### HDU Size
2 MB


		Header Table Caption for HDU2


| **Key** | **Value** | **Type** | **Comment** |
| :--- | :----- | :---- | :------- |
| **XTENSION** | IMAGE | 		 | IMAGE extension | 
| **BITPIX** | -32 | 		 | Number of bits per data pixel | 
| **NAXIS** | 2 | 		 | Number of data axes | 
| **NAXIS1** | 4563 | 		 | 		 | 
| **NAXIS2** | 171 | 		 | 		 | 
| **PCOUNT** | 0 | 		 | No Group Parameters | 
| **GCOUNT** | 1 | 		 | One Data Group | 
| **HDUCLASS** | SDSS | 		 | SDSS format class | 
| **HDUCLAS1** | IMAGE | 		 | 		 | 
| **HDUCLAS2** | ERROR | 		 | 		 | 
| **HDUCLAS3** | INVMSE | 		 | Inverse variance | 
| **SCIDATA** | FLUX | 		 | Science extension name | 
| **QUALDATA** | MASK | 		 | Mask extension name | 
| **EXTNAME** | IVAR | 		 | 		 | 
| **DATASUM** | 1140307641 | 		 | data unit checksum updated 2018-03-21T06:08:46 | 
| **CHECKSUM** | 6K5C9K396K3C6K39 | 		 | HDU checksum updated 2018-03-21T06:08:46 | 



## HDU3: MASK
Pixel mask (MANGA_DRP2PIXMASK)

### HDU Type
IMAGE


### HDU Size
2 MB


		Header Table Caption for HDU3


| **Key** | **Value** | **Type** | **Comment** |
| :--- | :----- | :---- | :------- |
| **XTENSION** | IMAGE | 		 | IMAGE extension | 
| **BITPIX** | 32 | 		 | Number of bits per data pixel | 
| **NAXIS** | 2 | 		 | Number of data axes | 
| **NAXIS1** | 4563 | 		 | 		 | 
| **NAXIS2** | 171 | 		 | 		 | 
| **PCOUNT** | 0 | 		 | No Group Parameters | 
| **GCOUNT** | 1 | 		 | One Data Group | 
| **HDUCLASS** | SDSS | 		 | SDSS format class | 
| **HDUCLAS1** | IMAGE | 		 | 		 | 
| **HDUCLAS2** | QUALITY | 		 | 		 | 
| **HDUCLAS3** | FLAG64BIT | 		 | 		 | 
| **SCIDATA** | FLUX | 		 | Science extension name | 
| **ERRDATA** | IVAR | 		 | Error extension name | 
| **EXTNAME** | MASK | 		 | 		 | 
| **DATASUM** | 2359936278 | 		 | data unit checksum updated 2018-03-21T06:08:46 | 
| **CHECKSUM** | cbdRdabOcabOcabO | 		 | HDU checksum updated 2018-03-21T06:08:46 | 



## HDU4: DISP
Spectral LSF  (1-sigma) in units of Angstroms

### HDU Type
IMAGE


### HDU Size
2 MB


		Header Table Caption for HDU4


| **Key** | **Value** | **Type** | **Comment** |
| :--- | :----- | :---- | :------- |
| **XTENSION** | IMAGE | 		 | IMAGE extension | 
| **BITPIX** | -32 | 		 | Number of bits per data pixel | 
| **NAXIS** | 2 | 		 | Number of data axes | 
| **NAXIS1** | 4563 | 		 | 		 | 
| **NAXIS2** | 171 | 		 | 		 | 
| **PCOUNT** | 0 | 		 | No Group Parameters | 
| **GCOUNT** | 1 | 		 | One Data Group | 
| **EXTNAME** | DISP | 		 | 		 | 
| **DATASUM** | 2453379726 | 		 | data unit checksum updated 2018-03-21T06:08:46 | 
| **CHECKSUM** | RAH2S3G2R9G2R9G2 | 		 | HDU checksum updated 2018-03-21T06:08:46 | 



## HDU5: PREDISP
Broadened pre-pixel dispersion solution (1sigma LSF in Angstroms)

### HDU Type
IMAGE


### HDU Size
2 MB


		Header Table Caption for HDU5


| **Key** | **Value** | **Type** | **Comment** |
| :--- | :----- | :---- | :------- |
| **XTENSION** | IMAGE | 		 | IMAGE extension | 
| **BITPIX** | -32 | 		 | Number of bits per data pixel | 
| **NAXIS** | 2 | 		 | Number of data axes | 
| **NAXIS1** | 4563 | 		 | 		 | 
| **NAXIS2** | 171 | 		 | 		 | 
| **PCOUNT** | 0 | 		 | No Group Parameters | 
| **GCOUNT** | 1 | 		 | One Data Group | 
| **EXTNAME** | PREDISP | 		 | 		 | 
| **DATASUM** | 1425839999 | 		 | data unit checksum updated 2018-03-21T06:08:46 | 
| **CHECKSUM** | FAP7F3O4FAO4F3O4 | 		 | HDU checksum updated 2018-03-21T06:08:46 | 



## HDU6: WAVE
Wavelength vector in units of Angstroms (vacuum heliocentric)

### HDU Type
IMAGE


### HDU Size
35 KB


		Header Table Caption for HDU6


| **Key** | **Value** | **Type** | **Comment** |
| :--- | :----- | :---- | :------- |
| **XTENSION** | IMAGE | 		 | IMAGE extension | 
| **BITPIX** | -64 | 		 | Number of bits per data pixel | 
| **NAXIS** | 1 | 		 | Number of data axes | 
| **NAXIS1** | 4563 | 		 | 		 | 
| **PCOUNT** | 0 | 		 | No Group Parameters | 
| **GCOUNT** | 1 | 		 | One Data Group | 
| **EXTNAME** | WAVE | 		 | 		 | 
| **DATASUM** | 3938867060 | 		 | data unit checksum updated 2018-03-21T06:08:46 | 
| **CHECKSUM** | cL7TfJ5TcJ5TcJ5T | 		 | HDU checksum updated 2018-03-21T06:08:46 | 



## HDU7: SPECRES
Median spectral resolution vs wavelength

### HDU Type
IMAGE


### HDU Size
35 KB


		Header Table Caption for HDU7


| **Key** | **Value** | **Type** | **Comment** |
| :--- | :----- | :---- | :------- |
| **XTENSION** | IMAGE | 		 | IMAGE extension | 
| **BITPIX** | -64 | 		 | Number of bits per data pixel | 
| **NAXIS** | 1 | 		 | Number of data axes | 
| **NAXIS1** | 4563 | 		 | 		 | 
| **PCOUNT** | 0 | 		 | No Group Parameters | 
| **GCOUNT** | 1 | 		 | One Data Group | 
| **EXTNAME** | SPECRES | 		 | 		 | 
| **DATASUM** | 1547448224 | 		 | data unit checksum updated 2018-03-21T06:08:46 | 
| **CHECKSUM** | OcOcRaOZOaObOaOZ | 		 | HDU checksum updated 2018-03-21T06:08:46 | 



## HDU8: SPECRESD
Standard deviation (1-sigma) of spectral resolution vs wavelength

### HDU Type
IMAGE


### HDU Size
35 KB


		Header Table Caption for HDU8


| **Key** | **Value** | **Type** | **Comment** |
| :--- | :----- | :---- | :------- |
| **XTENSION** | IMAGE | 		 | IMAGE extension | 
| **BITPIX** | -64 | 		 | Number of bits per data pixel | 
| **NAXIS** | 1 | 		 | Number of data axes | 
| **NAXIS1** | 4563 | 		 | 		 | 
| **PCOUNT** | 0 | 		 | No Group Parameters | 
| **GCOUNT** | 1 | 		 | One Data Group | 
| **EXTNAME** | SPECRESD | 		 | 		 | 
| **DATASUM** | 706612906 | 		 | data unit checksum updated 2018-03-21T06:08:46 | 
| **CHECKSUM** | K3YcN3WZK3WbK3WZ | 		 | HDU checksum updated 2018-03-21T06:08:46 | 



## HDU9: PRESPECRES
Median pre-pixel spectral resolution vs wavelength

### HDU Type
IMAGE


### HDU Size
35 KB


		Header Table Caption for HDU9


| **Key** | **Value** | **Type** | **Comment** |
| :--- | :----- | :---- | :------- |
| **XTENSION** | IMAGE | 		 | IMAGE extension | 
| **BITPIX** | -64 | 		 | Number of bits per data pixel | 
| **NAXIS** | 1 | 		 | Number of data axes | 
| **NAXIS1** | 4563 | 		 | 		 | 
| **PCOUNT** | 0 | 		 | No Group Parameters | 
| **GCOUNT** | 1 | 		 | One Data Group | 
| **EXTNAME** | PRESPECRES | 		 | 		 | 
| **DATASUM** | 2694726452 | 		 | data unit checksum updated 2018-03-21T06:08:46 | 
| **CHECKSUM** | bD8IeD8IbD8IbD8I | 		 | HDU checksum updated 2018-03-21T06:08:46 | 



## HDU10: PRESPECRESD
Standard deviation of pre-pixel spectral resolution vs wavelength

### HDU Type
IMAGE


### HDU Size
35 KB


		Header Table Caption for HDU10


| **Key** | **Value** | **Type** | **Comment** |
| :--- | :----- | :---- | :------- |
| **XTENSION** | IMAGE | 		 | IMAGE extension | 
| **BITPIX** | -64 | 		 | Number of bits per data pixel | 
| **NAXIS** | 1 | 		 | Number of data axes | 
| **NAXIS1** | 4563 | 		 | 		 | 
| **PCOUNT** | 0 | 		 | No Group Parameters | 
| **GCOUNT** | 1 | 		 | One Data Group | 
| **EXTNAME** | PRESPECRESD | 		 | 		 | 
| **DATASUM** | 2908884265 | 		 | data unit checksum updated 2018-03-21T06:08:46 | 
| **CHECKSUM** | eDDUe9BTeABTe9BT | 		 | HDU checksum updated 2018-03-21T06:08:46 | 



## HDU11: OBSINFO
Table detailing exposures combined to create this file


### HDU Size
2 KB


		Header Table Caption for HDU11


| **Key** | **Value** | **Type** | **Comment** |
| :--- | :----- | :---- | :------- |
| **XTENSION** | BINTABLE | 		 | Written by IDL:  Wed Mar 21 00:08:46 2018 | 
| **BITPIX** | 8 | 		 | 		 | 
| **NAXIS** | 2 | 		 | Binary table | 
| **NAXIS1** | 332 | 		 | Number of bytes per row | 
| **NAXIS2** | 9 | 		 | Number of rows | 
| **PCOUNT** | 0 | 		 | Random parameter count | 
| **GCOUNT** | 1 | 		 | Group count | 
| **TFIELDS** | 65 | 		 | Number of columns | 
| **COMMENT** | 		 | 		 | 		 | 
| **COMMENT** | *** End of mandatory fields *** | 		 | 		 | 
| **COMMENT** | 		 | 		 | 		 | 
| **EXTNAME** | OBSINFO | 		 | 		 | 
| **COMMENT** | 		 | 		 | 		 | 
| **COMMENT** | *** Column names *** | 		 | 		 | 
| **COMMENT** | 		 | 		 | 		 | 
| **COMMENT** | 		 | 		 | 		 | 
| **COMMENT** | *** Column formats *** | 		 | 		 | 
| **COMMENT** | 		 | 		 | 		 | 



		Binary Table Caption for HDU11


| **Name** | **Type** | **Unit** | **Description** |
| :--- | :----- | :---- | :------- |
| **SLITFILE** | char[25] | 		 | Name of the slitmap |
| **METFILE** | char[17] | 		 | Name of the metrology file |
| **HARNAME** | char[5] | 		 | Harness name |
| **IFUDESIGN** | int32 | 		 | ifudesign (e.g., 12701) |
| **FRLPLUG** | int16 | 		 | The physical ferrule matching this part of the slit |
| **MANGAID** | char[8] | 		 | MaNGA identification number |
| **AIRTEMP** | float32 | 		 | Temperature in Celsius |
| **HUMIDITY** | float32 | 		 | Relative humidity in percent |
| **PRESSURE** | float32 | 		 | Pressure in inHg |
| **SEEING** | float32 | 		 | Best guider seeing in Arcsec |
| **PSFFAC** | float32 | 		 | Best-fit PSF size relative to guider measurement |
| **TRANSPAR** | float32 | 		 | Guider transparency |
| **PLATEID** | int32 | 		 | Plate id number |
| **DESIGNID** | int32 | 		 | Design id number |
| **CARTID** | int16 | 		 | Cart id number |
| **MJD** | int32 | 		 | MJD of observation |
| **EXPTIME** | float32 | 		 | Exposure time (seconds) |
| **EXPNUM** | char[12] | 		 | Exposure number |
| **SET** | int32 | 		 | Which set this exposure belongs to |
| **MGDPOS** | char[8] | 		 | MaNGA dither position (NSEC) |
| **MGDRA** | float32 | 		 | MaNGA dither offset in RA (arcsec) |
| **MGDDEC** | float32 | 		 | MaNGA dither offset in DEC (arcsec) |
| **OMEGASET_U** | float32 | 		 | Omega value of this set in u-band (3622 Angstrom) |
| **OMEGASET_G** | float32 | 		 | Omega value of this set in g-band (4703 Angstrom) |
| **OMEGASET_R** | float32 | 		 | Omega value of this set in r-band (6177 Angstrom) |
| **OMEGASET_I** | float32 | 		 | Omega value of this set in i-band (7496 Angstrom) |
| **OMEGASET_Z** | float32 | 		 | Omega value of this set in z-band (10354 Angstrom) |
| **EAMFIT_RA** | float32 | 		 | DeltaRA (arcsec) from extended astrometry module |
| **EAMFIT_DEC** | float32 | 		 | DeltaDEC (arcsec) from extended astrometry module |
| **EAMFIT_THETA** | float32 | 		 | Final DeltaTHETA (degrees) from extended astrometry module |
| **EAMFIT_THETA0** | float32 | 		 | Original DeltaTHETA from the EAM (free for all exposures) |
| **EAMFIT_A** | float32 | 		 | A (flux scaling) from extended astrometry module |
| **EAMFIT_B** | float32 | 		 | B (flux zeropoint) from extended astrometry module |
| **EAMFIT_RAERR** | float32 | 		 | 1-sigma uncertainty in DeltaRA (arcsec) |
| **EAMFIT_DECERR** | float32 | 		 | 1-sigma uncertainty in DeltaDEC (arcsec) |
| **EAMFIT_THETAERR** | float32 | 		 | 1-sigma uncertainty in DeltaTHETA (degrees) |
| **EAMFIT_THETA0ERR** | float32 | 		 | 1-sigma uncertainty in DeltaTHETA0 (degrees) |
| **EAMFIT_AERR** | float32 | 		 | 1-sigma uncertainty in A |
| **EAMFIT_BERR** | float32 | 		 | 1-sigma uncertainty in B |
| **TAIBEG** | char[13] | 		 | TAI at the start of the exposure |
| **HADRILL** | float32 | 		 | Hour angle plate was drilled for |
| **LSTMID** | float32 | 		 | Local sidereal time at midpoint of exposure |
| **HAMID** | float32 | 		 | Hour angle at midpoint of exposure for this IFU |
| **AIRMASS** | float32 | 		 | Airmass at midpoint of exposure for this IFU |
| **IFURA** | float64 | 		 | IFU right ascension (J2000) |
| **IFUDEC** | float64 | 		 | IFU declination (J2000) |
| **CENRA** | float64 | 		 | Plate center right ascension (J2000) |
| **CENDEC** | float64 | 		 | Plate center declination (J2000) |
| **XFOCAL** | float32 | 		 | Hole location in xfocal coordinates (mm) |
| **YFOCAL** | float32 | 		 | Hole location in yfocal coordinates (mm) |
| **MNGTARG1** | int32 | 		 | manga_target1 maskbit for galaxy target catalog |
| **MNGTARG2** | int32 | 		 | manga_target2 maskbit for non-galaxy target catalog |
| **MNGTARG3** | int32 | 		 | manga_target3 maskbit for ancillary target catalog |
| **BLUESN2** | float32 | 		 | SN2 in blue for this exposure |
| **REDSN2** | float32 | 		 | SN2 in red for this exposure |
| **BLUETHRUPT** | float32 | 		 | Throughput in blue for this exposure |
| **REDTHRUPT** | float32 | 		 | Throughput in red for this exposure |
| **BLUEPSTAT** | float32 | 		 | Poisson statistic in blue for this exposure |
| **REDPSTAT** | float32 | 		 | Poisson statistic in red for this exposure |
| **DRP2QUAL** | int32 | 		 | DRP-2d quality bitmask |
| **THISBADIFU** | int32 | 		 | 0 if good, 1 if this IFU was bad in this frame |
| **PF_FWHM_G** | float32 | 		 | FWHM (arcsec) of a single-gaussian fit to the point source response function Prior to Fiber convolution in g band |
| **PF_FWHM_R** | float32 | 		 | FWHM (arcsec) of a single-gaussian fit to the point source response function Prior to Fiber convolution in r band |
| **PF_FWHM_I** | float32 | 		 | FWHM (arcsec) of a single-gaussian fit to the point source response function Prior to Fiber convolution in i band |
| **PF_FWHM_Z** | float32 | 		 | FWHM (arcsec) of a single-gaussian fit to the point source response function Prior to Fiber convolution in z band |


## HDU12: XPOS
Array of fiber X-positions (units of arcsec) relative to the IFU center.  Because of chromatic DAR, each wavelength for a given fiber has a slightly different position, and therefore the positional arrays have the same dimensionality as the corresponding flux array.

### HDU Type
IMAGE


### HDU Size
2 MB


		Header Table Caption for HDU12


| **Key** | **Value** | **Type** | **Comment** |
| :--- | :----- | :---- | :------- |
| **XTENSION** | IMAGE | 		 | IMAGE extension | 
| **BITPIX** | -32 | 		 | Number of bits per data pixel | 
| **NAXIS** | 2 | 		 | Number of data axes | 
| **NAXIS1** | 4563 | 		 | 		 | 
| **NAXIS2** | 171 | 		 | 		 | 
| **PCOUNT** | 0 | 		 | No Group Parameters | 
| **GCOUNT** | 1 | 		 | One Data Group | 
| **EXTNAME** | XPOS | 		 | 		 | 
| **DATASUM** | 3023661791 | 		 | data unit checksum updated 2018-03-21T06:08:46 | 
| **CHECKSUM** | 64MB71K961KA61K9 | 		 | HDU checksum updated 2018-03-21T06:08:46 | 



## HDU13: YPOS
Array of fiber Y-positions (units of arcsec) relative to the IFU center.  Because of chromatic DAR, each wavelength for a given fiber has a slightly different position, and therefore the positional arrays have the same dimensionality as the corresponding flux array.

### HDU Type
IMAGE


### HDU Size
2 MB


		Header Table Caption for HDU13


| **Key** | **Value** | **Type** | **Comment** |
| :--- | :----- | :---- | :------- |
| **XTENSION** | IMAGE | 		 | IMAGE extension | 
| **BITPIX** | -32 | 		 | Number of bits per data pixel | 
| **NAXIS** | 2 | 		 | Number of data axes | 
| **NAXIS1** | 4563 | 		 | 		 | 
| **NAXIS2** | 171 | 		 | 		 | 
| **PCOUNT** | 0 | 		 | No Group Parameters | 
| **GCOUNT** | 1 | 		 | One Data Group | 
| **EXTNAME** | YPOS | 		 | 		 | 
| **DATASUM** | 2342972923 | 		 | data unit checksum updated 2018-03-21T06:08:46 | 
| **CHECKSUM** | 0Apa14oX0Aoa03oW | 		 | HDU checksum updated 2018-03-21T06:08:46 | 




