
# Data model: ap2D



#### General Description
ap2D files contain 2D data derived from the up-the-ramp data cubes. Cosmic
rays are flagged and CR repair is attempted. Saturated pixels are flagged.
Dark current is subtracted, and the final 2D image is flat-fielded.


#### Naming Convention
<dd id="filename"><code>ap2D-[abc]-[0-9]{8}\.fits</code></dd>


#### Approximate Size
2048x2048x3x4 bytes


#### File Type
FITS




## Sections
* [HDU0: master header](#hdu0-master header)
* [HDU1: image (ADU) [FLOAT]](#hdu1-image (ADU) [FLOAT])
* [HDU2: error (ADU) [FLOAT]](#hdu2-error (ADU) [FLOAT])
* [HDU3: flag mask [INT*2]](#hdu3-flag mask [INT*2])

## HDU0: MASTER




| **Key** | **Value** | **Type** | **Comment** |
| :--- | :----- | :---- | :------- |
| **SIMPLE** |                     T  | 		 | image conforms to FITS standard | 
| **BITPIX** |                    16  | 		 | bits per data value | 
| **NAXIS** |                     0  | 		 | number of axes | 
| **EXTEND** |                     T  | 		 | file may contain extensions | 
| **INTDELAY** |                   0.1  | 		 | Integration Delay(S) | 
| **DATE-OBS** |  '2011-09-09T03:52:24.384'  | 		 | Date at start of integration | 
| **TIMESYS** |  'UTC     '            | 		 | Time Zone of Date | 
| **NFRAMES** |                    47  | 		 | Num of SUTR | 
| **INTOFF** |                 10647  | 		 | Single read duration in mSec | 
| **EXPTIME** |               500.509  | 		 | Actual Integration Time | 
| **FILENAME** |  ' | 		 | data-ql | 
| **IMAGETYP** |  'Object  '            | 		 | Object type for EXP | 
| **FULLX** |                  8192  | 		 | Camera Full Frame X DIM | 
| **FULLY** |                  2048  | 		 | Camera Full Frame X DIM | 
| **BEGX** |                     1  | 		 | IRAF 1-indexed Value | 
| **BEGY** |                     1  | 		 | IRAF 1-indexed Value | 
| **BINX** |                     1  | 		 | in pixels | 
| **BINY** |                     1  | 		 | in pixels | 
| **ACAMREV** |  'UVA-Astrocam v1.2r55'  | 		 | Camera Software revision | 
| **OBSCMNT** |  'C. 6, 5214, NGC6819_1'  | 		 | Observer comment | 
| **LKSHPWR** |                   0.0  | 		 | LS-PWR1-% | 
| **TDETTOP** |                74.845  | 		 | T_DETPOLE_TOP in Degrees K | 
| **TDETBASE** |                 74.44  | 		 | T_DETPOLE_BASE in Degrees K | 
| **COLPITCH** |                 5.817  | 		 | Collimator Pitch(pix) | 
| **TTENTTOP** |                82.702  | 		 | T_TENT_TOP in Degrees K | 
| **COLLM3** |              2377.976  | 		 | Collimator M3(um) | 
| **TCLDPMID** |                78.058  | 		 | T_CP_MIDDLE in Degrees K | 
| **COLLM2** |              2354.858  | 		 | Collimator M2(um) | 
| **COLLM1** |              2494.161  | 		 | Collimator M1(um) | 
| **TGETTER** |                77.001  | 		 | T_GETTER in Degrees K | 
| **TTLMBRD** |               301.363  | 		 | T_TempBrd in Degrees K | 
| **TLSOUTH** |                76.644  | 		 | T_L_SOUTH in Degrees K | 
| **TLNORTH** |                76.833  | 		 | T_L_NORTH in Degrees K | 
| **TLSCAM2** |                  78.9  | 		 | T_LS-Camera2 in Degrees K | 
| **TLSCAM1** |                78.891  | 		 | T_LS-Camera1 in Degrees K | 
| **TLSDETC** |                74.835  | 		 | T_LS-DetectorC in Degrees K | 
| **TLSDETB** |                73.869  | 		 | T_LS-DetectorB in Degrees K | 
| **TPGVAC** |               6.59E-7  | 		 | Pfeiffer-Vacuum in Torr | 
| **LN2CNTRL** |                   0.0  | 		 | LN2(%) | 
| **TCAMAFT** |                77.632  | 		 | T_CAM_AFT in Degrees K | 
| **TCAMMID** |                78.593  | 		 | T_CAM_MIDDLE in Degrees K | 
| **COLLYAW** |                17.413  | 		 | Collimator Yaw(pix) | 
| **TCAMFWD** |                78.579  | 		 | T_CAM_FWD in Degrees K | 
| **TEMPVPH** |                78.268  | 		 | T_VPH in Degrees K | 
| **TRADSHLD** |                87.204  | 		 | T_RADSHIELD_E in Degrees K | 
| **TCOLLIM** |                78.875  | 		 | T_COLLIMATOR in Degrees K | 
| **TCPCORN** |                79.757  | 		 | T_CP_CORNER in Degrees K | 
| **TCLDPHNG** |                79.768  | 		 | T_CP_HANGERS in Degrees K | 
| **COLLPIST** |              2401.243  | 		 | Collimator Piston(um) | 
| **DITHPIX** |                12.994  | 		 | Dither Position(pix) | 
| **RELHUM** |                21.165  | 		 | RH_T(%) | 
| **LN2LEVEL** |                91.394  | 		 | LN2_T(%) | 
| **MKSVAC** |              6.896E-7  | 		 | MKS-Vacuum in Torr | 
| **OBJECT** |  'ObjName '            | 		 | 		 | 
| **FILTER1** |  'FILTER  '            | 		 | 		 | 
| **ICSREV** |  'APOGEE ICS2.0r032'   | 		 | 		 | 
| **DSPFILE** |  'UNKNOWN '            | 		 | 		 | 
| **TELESCOP** |  'SDSS 2-5m' | 		 | 		 | 
| **EXPTYPE** |  'OBJECT  ' | 		 | 		 | 
| **LAMPQRTZ** |                     0  | 		 | CalBox Quartz Lamp Status | 
| **LAMPUNE** |                     0  | 		 | CalBox UNe Lamp Status | 
| **LAMPTHAR** |                     0  | 		 | CalBox ThArNe Lamp Status | 
| **LAMPSHTR** |                     0  | 		 | CalBox Shutter Lamp Status | 
| **LAMPCNTL** |                     1  | 		 | CalBox Controller Status | 
| **SEEING** |               1.78419  | 		 | RMS seeing from guide fibers | 
| **FF** |  '0 0 0 0 '            | 		 | FF lamps 1:on 0:0ff | 
| **NE** |  '0 0 0 0 '            | 		 | NE lamps 1:on 0:0ff | 
| **HGCD** |  '0 0 0 0 '            | 		 | HGCD lamps 1:on 0:0ff | 
| **FFS** |  '0 0 0 0 0 0 0 0'     | 		 | Flatfield Screen 1:closed 0:open | 
| **OBJSYS** |  'ICRS    '            | 		 | The TCC objSys | 
| **RA** |            294.845058  | 		 | RA of telescope boresight (deg) | 
| **DEC** |             39.300427  | 		 | Dec of telescope boresight (deg) | 
| **RADEG** |              294.8546  | 		 | RA of telescope pointing(deg) | 
| **DECDEG** |                  39.3  | 		 | Dec of telescope pointing (deg) | 
| **ROTTYPE** |  'Obj     '            | 		 | Rotator request type | 
| **ROTPOS** |                   0.0  | 		 | Rotator request position (deg) | 
| **BOREOFFX** |                   0.0  | 		 | TCC Boresight offset, deg | 
| **BOREOFFY** |                   0.0  | 		 | TCC Boresight offset, deg | 
| **ARCOFFX** |             -0.007391  | 		 | TCC ObjArcOff, deg | 
| **ARCOFFY** |              0.000425  | 		 | TCC ObjArcOff, deg | 
| **OBJOFFX** |                   0.0  | 		 | TCC ObjOff, deg | 
| **OBJOFFY** |                   0.0  | 		 | TCC ObjOff, deg | 
| **CALOFFX** |               0.00079  | 		 | TCC CalibOff, deg | 
| **CALOFFY** |              0.000357  | 		 | TCC CalibOff, deg | 
| **CALOFFR** |                   0.0  | 		 | TCC CalibOff, deg | 
| **GUIDOFFX** |                   0.0  | 		 | TCC GuideOff, deg | 
| **GUIDOFFY** |                   0.0  | 		 | TCC GuideOff, deg | 
| **GUIDOFFR** |             -0.040153  | 		 | TCC GuideOff, deg | 
| **AZ** |               210.519  | 		 | Azimuth axis pos. (approx, deg) | 
| **ALT** |                82.283  | 		 | Altitude axis pos. (approx, deg) | 
| **IPA** |                33.433  | 		 | Rotator axis pos. (approx, deg) | 
| **SPA** |    -145.6139673163376  | 		 | TCC SpiderInstAng | 
| **FOCUS** |                466.38  | 		 | User-specified focus offset (um) | 
| **M2PISTON** |                356.88  | 		 | TCC SecOrient | 
| **M2XTILT** |                 12.94  | 		 | TCC SecOrient | 
| **M2YTILT** |     8.029999999999999  | 		 | TCC SecOrient | 
| **M2XTRAN** |                 -60.0  | 		 | TCC SecOrient | 
| **M2YTRAN** |               -171.54  | 		 | TCC SecOrient | 
| **M1PISTON** |              -1481.27  | 		 | TCC PrimOrient | 
| **M1XTILT** |                -24.31  | 		 | TCC PrimOrient | 
| **M1YTILT** |                  11.4  | 		 | TCC PrimOrient | 
| **M1XTRAN** |                612.27  | 		 | TCC PrimOrient | 
| **M1YTRAN** |               1325.79  | 		 | TCC PrimOrient | 
| **SCALE** |               1.00015  | 		 | User-specified scale factor | 
| **NAME** |  '5214-55811-01'       | 		 | The name of the currently loaded plate | 
| **PLATEID** |                  5214  | 		 | The currently loaded plate | 
| **CARTID** |                     6  | 		 | The currently loaded cartridge | 
| **MAPID** |                     1  | 		 | The mapping version of the loaded plate | 
| **POINTING** |  'A       '            | 		 | The currently specified pointing | 
| **CHIP** |  'a       '            | 		 | 		 | 
| **NREAD** |                    47  | 		 | 		 | 
| **CHECKSUM** |  'gEdci9ZbgCdbg9Zb'    | 		 | HDU checksum updated 2012-11-15T13:03:37 | 
| **HISTORY** |  AP3D: Thu Nov 15 03:01:03 2012 | 		 | 		 | 
| **HISTORY** |  AP3D: holtz on milkyway.nmsu.edu | 		 | 		 | 
| **HISTORY** |  AP3D: IDL 8.0.1 linux x86_64 | 		 | 		 | 
| **HISTORY** |  AP3D:  APOGEE Reduction Pipeline Version: trunk | 		 | 		 | 
| **HISTORY** |  AP3D: Output File: | 		 | 		 | 
| **HISTORY** |  AP3D:  HDU1 - image (ADU) | 		 | 		 | 
| **HISTORY** |  AP3D:  HDU2 - error (ADU) | 		 | 		 | 
| **HISTORY** |  AP3D:  HDU3 - flag mask | 		 | 		 | 
| **HISTORY** |  AP3D:         1 - bad pixels | 		 | 		 | 
| **HISTORY** |  AP3D:         2 - cosmic ray | 		 | 		 | 
| **HISTORY** |  AP3D:         4 - saturated | 		 | 		 | 
| **HISTORY** |  AP3D:         8 - unfixable | 		 | 		 | 
| **HISTORY** |  AP3D: Global fractional variability = 0.272 | 		 | 		 | 
| **HISTORY** |  AP3D: BAD PIXEL MASK file=" | 		 | net | 
| **HISTORY** |  AP3D: fits" | 		 | 		 | 
| **HISTORY** |  AP3D: DETECTOR file=" | 		 | net | 
| **HISTORY** |  AP3D: .fits" | 		 | 		 | 
| **HISTORY** |  AP3D: Dark Current Correction file=" | 		 | net | 
| **HISTORY** |  AP3D: ark-a-05560001.fits" | 		 | 		 | 
| **HISTORY** |  AP3D: Flat Field Correction file=" | 		 | net | 
| **HISTORY** |  AP3D: t-a-04750009.fits" | 		 | 		 | 
| **HISTORY** |  AP3D: Persistence mask file=" | 		 | net | 
| **HISTORY** |  AP3D: -04680019.fits" | 		 | 		 | 
| **HISTORY** |  AP3D: 42498 pixels are bad | 		 | 		 | 
| **HISTORY** |  AP3D: 455 pixels have cosmic rays | 		 | 		 | 
| **HISTORY** |  AP3D: Cosmic Rays FIXED | 		 | 		 | 
| **HISTORY** |  AP3D: 32 pixels are saturated | 		 | 		 | 
| **HISTORY** |  AP3D: 32 saturated pixels FIXED | 		 | 		 | 
| **HISTORY** |  AP3D: 0 pixels are unfixable | 		 | 		 | 
| **HISTORY** |  AP3D: UP-THE-RAMP Sampling | 		 | 		 | 
| **UT-MID** |  '2011-09-09T03:56:34.6'  | 		 | Date at midpoint of exposure | 
| **JD-MID** |         2455813.66429  | 		 | JD at midpoint of exposure | 
| **DATASUM** |  '         0'          | 		 | data unit checksum updated 2012-11-15T13:03:37 | 
| **END** | 		 | 		 | 		 | 

## HDU1: DATA




| **Key** | **Value** | **Type** | **Comment** |
| :--- | :----- | :---- | :------- |
| **XTENSION** |  'IMAGE   '            | 		 | IMAGE extension | 
| **BITPIX** |                   -32  | 		 | Number of bits per data pixel | 
| **NAXIS** |                     2  | 		 | Number of data axes | 
| **NAXIS1** |                  2048  | 		 | 		 | 
| **NAXIS2** |                  2048  | 		 | 		 | 
| **PCOUNT** |                     0  | 		 | No Group Parameters | 
| **GCOUNT** |                     1  | 		 | One Data Group | 
| **CTYPE1** |  'Pixel   '            | 		 | 		 | 
| **CTYPE2** |  'Pixel   '            | 		 | 		 | 
| **BUNIT** |  'Flux (ADU)'          | 		 | 		 | 
| **HISTORY** |  Image was compressed by CFITSIO using scaled integer quantization: | 		 | 		 | 
| **HISTORY** |    q = 4.000000  | 		 | quantized level scaling parameter | 
| **HISTORY** |  'SUBTRACTIVE_DITHER_1'  | 		 | Pixel Quantization Algorithm | 
| **CHECKSUM** |  'XenSXclPXclPXclP'    | 		 | HDU checksum updated 2012-11-15T21:35:29 | 
| **DATASUM** |  '3618308333'          | 		 | data unit checksum updated 2012-11-15T21:35:29 | 
| **END** | 		 | 		 | 		 | 

## HDU2: ERROR




| **Key** | **Value** | **Type** | **Comment** |
| :--- | :----- | :---- | :------- |
| **XTENSION** |  'IMAGE   '            | 		 | IMAGE extension | 
| **BITPIX** |                   -32  | 		 | Number of bits per data pixel | 
| **NAXIS** |                     2  | 		 | Number of data axes | 
| **NAXIS1** |                  2048  | 		 | 		 | 
| **NAXIS2** |                  2048  | 		 | 		 | 
| **PCOUNT** |                     0  | 		 | No Group Parameters | 
| **GCOUNT** |                     1  | 		 | One Data Group | 
| **CTYPE1** |  'Pixel   '            | 		 | 		 | 
| **CTYPE2** |  'Pixel   '            | 		 | 		 | 
| **BUNIT** |  'Error (ADU)'         | 		 | 		 | 
| **HISTORY** |  Image was compressed by CFITSIO using scaled integer quantization: | 		 | 		 | 
| **HISTORY** |    q = 4.000000  | 		 | quantized level scaling parameter | 
| **HISTORY** |  'SUBTRACTIVE_DITHER_1'  | 		 | Pixel Quantization Algorithm | 
| **CHECKSUM** |  '9GTHGFR99FREGFR9'    | 		 | HDU checksum updated 2012-11-15T21:35:57 | 
| **DATASUM** |  '908871677'           | 		 | data unit checksum updated 2012-11-15T21:35:57 | 
| **END** | 		 | 		 | 		 | 

## HDU3: MASK




| **Key** | **Value** | **Type** | **Comment** |
| :--- | :----- | :---- | :------- |
| **XTENSION** |  'IMAGE   '            | 		 | IMAGE extension | 
| **BITPIX** |                    16  | 		 | Number of bits per data pixel | 
| **NAXIS** |                     2  | 		 | Number of data axes | 
| **NAXIS1** |                  2048  | 		 | 		 | 
| **NAXIS2** |                  2048  | 		 | 		 | 
| **PCOUNT** |                     0  | 		 | No Group Parameters | 
| **GCOUNT** |                     1  | 		 | One Data Group | 
| **CTYPE1** |  'Pixel   '            | 		 | 		 | 
| **CTYPE2** |  'Pixel   '            | 		 | 		 | 
| **BUNIT** |  'Flag Mask (bitwise)'  | 		 | 		 | 
| **HISTORY** |  Explanation of BITWISE flag mask | 		 | 		 | 
| **HISTORY** |   1 - bad pixels | 		 | 		 | 
| **HISTORY** |   2 - cosmic ray | 		 | 		 | 
| **HISTORY** |   4 - saturated | 		 | 		 | 
| **HISTORY** |   8 - unfixable | 		 | 		 | 
| **CHECKSUM** |  '1Gjd4Fgb1Fgb1Fgb'    | 		 | HDU checksum updated 2012-11-15T21:36:14 | 
| **DATASUM** |  '1362512632'          | 		 | data unit checksum updated 2012-11-15T21:36:14 | 
| **END** | 		 | 		 | 		 | 


