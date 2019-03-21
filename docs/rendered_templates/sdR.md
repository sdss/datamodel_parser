
# Data model sdR



# Data model: sdR



### General description
This file contains raw spectro data from the BOSS spectro CCDs.
Simultaneous frames in different chips all have the same frame number.
Which frames are what type of observation is indicated by the FLAVOR keyword in each header.
HDU 0 contains the raw counts as integers (4352x4224).


### Naming convention
sdR-[br][12]-[FRAME].fit, indicating which blue or red spectrograph (1 or 2), and the frame number.


### Approximate size
36771840 bytes.


### File type
FITS


### Read by products
<code>idlspec2d, sdssproc.pro</code>


### Written by products
???


### Format notes
The overscan regions for each amplifier are currently hardcoded in <code>sdssproc</code> .  They are (in IDL slice notation): <li>Red spectrograph MJD 55067 and later:<br/>
<table>
<tr><td>data[ 119:2175,   48:2111]</td><td>bias[  10:100,    48:2111]</td></tr>
<tr><td>data[2176:4232,   48:2111]</td><td>bias[4250:4340,   48:2111]</td></tr>
<tr><td>data[ 119:2175, 2112:4175]</td><td>bias[  10:100,  2112:4175]</td></tr>
<tr><td>data[2176:4232, 2112:4175]</td><td>bias[4250:4340, 2112:4175]</td></tr>
</table>
</li> <li>Blue spectrograph:<br/>
<table>
<tr><td>data[ 128:2175,   56:2111]</td><td>bias[  10:67,     56:2111]</td></tr>
<tr><td>data[2176:4223,   56:2111]</td><td>bias[4284:4340,   56:2111]</td></tr>
<tr><td>data[ 128:2175, 2112:4167]</td><td>bias[  10:67,   2112:4167]</td></tr>
<tr><td>data[2176:4223, 2112:4167]</td><td>bias[4284:4340, 2112:4167]</td></tr>
</table>
</li> 
Fiber 1 is on the left with wavelengths running up.
MJD<55113 have images rotated 180 degrees.



## Page Contents
* [HDU0: EXAMPLE HEADER (HDU 0)](#hdu0-example header (hdu 0))

## HDU0: EXAMPLE HEADER (HDU 0)



| **Key** | **Value** | **Type** | **Comment** |
| :--- | :----- | :---- | :------- |
| **SIMPLE** |                     T  | 		 | conforms to FITS standard | 
| **BITPIX** |                    16  | 		 | array data type | 
| **NAXIS** |                     2  | 		 | number of array dimensions | 
| **NAXIS1** |                  4352                                                   | 		 | 		 | 
| **NAXIS2** |                  4224                                                   | 		 | 		 | 
| **BSCALE** |                     1                                                   | 		 | 		 | 
| **BZERO** |                 32768                                                   | 		 | 		 | 
| **EXTEND** |                     T                                                   | 		 | 		 | 
| **TELESCOP** |  'SDSS 2-5m'                                                            | 		 | 		 | 
| **FILENAME** |  'sdR-b1-00160726.fit'                                                  | 		 | 		 | 
| **CAMERAS** |  'b1      '                                                             | 		 | 		 | 
| **EXPOSURE** |                160726                                                   | 		 | 		 | 
| **V_BOSS** |  'v3_6    '            | 		 | Active version of the BOSS ICC | 
| **DAQVER** |  '1.3.2   '                                                             | 		 | 		 | 
| **CAMDAQ** |  '1.5.0:37'                                                             | 		 | 		 | 
| **SUBFRAME** |  ''  | 		 | the subframe readout command | 
| **ERRCNT** |  'NONE    '                                                             | 		 | 		 | 
| **SYNCERR** |  'NONE    '                                                             | 		 | 		 | 
| **SLINES** |  'NONE    '                                                             | 		 | 		 | 
| **PIXERR** |  'NONE    '                                                             | 		 | 		 | 
| **PLINES** |  'NONE    '                                                             | 		 | 		 | 
| **PFERR** |  'NONE    '                                                             | 		 | 		 | 
| **DIDFLUSH** |                     T  | 		 | CCD was flushed before integration | 
| **FLAVOR** |  'bias    '            | 		 | exposure type, SDSS spectro style | 
| **BOSSVER** |  '2       '            | 		 | ICC version | 
| **MJD** |                 56408  | 		 | APO fMJD day at start of exposure | 
| **TAI-BEG** |          4873650659.0  | 		 | MJD(TAI) seconds at start of integration | 
| **DATE-OBS** |  '2013-04-25T23:50:59'  | 		 | TAI date at start of integration | 
| **NAME** |  '6846-56407-01'       | 		 | The name of the currently loaded plate | 
| **PLATEID** |                  6846  | 		 | The currently loaded plate | 
| **CARTID** |                     7  | 		 | The currently loaded cartridge | 
| **MAPID** |                     1  | 		 | The mapping version of the loaded plate | 
| **POINTING** |  'A       '            | 		 | The currently specified pointing | 
| **OBJSYS** |  'Mount   '            | 		 | The TCC objSys | 
| **RA** |  'NaN     '            | 		 | Telescope is not tracking the sky | 
| **DEC** |  'NaN     '            | 		 | Telescope is not tracking the sky | 
| **RADEG** |  'NaN     '            | 		 | Telescope is not tracking the sky | 
| **DECDEG** |  'NaN     '            | 		 | Telescope is not tracking the sky | 
| **SPA** |  'NaN     '            | 		 | Telescope is not tracking the sky | 
| **ROTTYPE** |  'Mount   '            | 		 | Rotator request type | 
| **ROTPOS** |                   0.0  | 		 | Rotator request position (deg) | 
| **BOREOFFX** |                   0.0  | 		 | TCC Boresight offset, deg | 
| **BOREOFFY** |                   0.0  | 		 | TCC Boresight offset, deg | 
| **ARCOFFX** |                   0.0  | 		 | TCC ObjArcOff, deg | 
| **ARCOFFY** |                   0.0  | 		 | TCC ObjArcOff, deg | 
| **OBJOFFX** |                   0.0  | 		 | TCC ObjOff, deg | 
| **OBJOFFY** |                   0.0  | 		 | TCC ObjOff, deg | 
| **CALOFFX** |                -0.002  | 		 | TCC CalibOff, deg | 
| **CALOFFY** |                -0.002  | 		 | TCC CalibOff, deg | 
| **CALOFFR** |                   0.0  | 		 | TCC CalibOff, deg | 
| **GUIDOFFX** |                   0.0  | 		 | TCC GuideOff, deg | 
| **GUIDOFFY** |                   0.0  | 		 | TCC GuideOff, deg | 
| **GUIDOFFR** |                   0.0  | 		 | TCC GuideOff, deg | 
| **AZ** |                 121.0  | 		 | Azimuth axis pos. (approx, deg) | 
| **ALT** |                  30.0  | 		 | Altitude axis pos. (approx, deg) | 
| **IPA** |                   0.0  | 		 | Rotator axis pos. (approx, deg) | 
| **FOCUS** |                299.16  | 		 | User-specified focus offset (um) | 
| **M2PISTON** |    -658.6900000000001  | 		 | TCC SecOrient | 
| **M2XTILT** |                  2.83  | 		 | TCC SecOrient | 
| **M2YTILT** |                  5.56  | 		 | TCC SecOrient | 
| **M2XTRAN** |                  0.35  | 		 | TCC SecOrient | 
| **M2YTRAN** |                115.54  | 		 | TCC SecOrient | 
| **M1PISTON** |              -2675.84  | 		 | TCC PrimOrient | 
| **M1XTILT** |                   0.0  | 		 | TCC PrimOrient | 
| **M1YTILT** |                   0.0  | 		 | TCC PrimOrient | 
| **M1XTRAN** |                612.28  | 		 | TCC PrimOrient | 
| **M1YTRAN** |               1500.38  | 		 | TCC PrimOrient | 
| **SCALE** |              1.000271  | 		 | User-specified scale factor | 
| **PRESSURE** |                21.448  | 		 | pressure | 
| **WINDD** |                 203.3  | 		 | windd | 
| **WINDS** |                  23.8  | 		 | winds | 
| **GUSTD** |                 211.0  | 		 | gustd | 
| **GUSTS** |                  37.1  | 		 | gusts | 
| **AIRTEMP** |                  15.7  | 		 | airTempPT | 
| **DEWPOINT** |                  -0.9  | 		 | dpTempPT | 
| **HUMIDITY** |                  30.0  | 		 | humidity | 
| **DUSTA** |               51275.0  | 		 | dusta | 
| **DUSTB** |                2826.0  | 		 | dustb | 
| **WINDD25M** |                 272.5  | 		 | windd25m | 
| **WINDS25M** |                   3.6  | 		 | winds25m | 
| **FF** |  '0 0 0 0 '            | 		 | FF lamps 1:on 0:0ff | 
| **NE** |  '0 0 0 0 '            | 		 | NE lamps 1:on 0:0ff | 
| **HGCD** |  '0 0 0 0 '            | 		 | HGCD lamps 1:on 0:0ff | 
| **FFS** |  '1 1 1 1 1 1 1 1'     | 		 | Flatfield Screen 1:closed 0:open | 
| **GUIDER1** |  'proc-gimg-0780.fits'  | 		 | The first guider image | 
| **SLITID1** |                     7  | 		 | Normalized slithead ID. sp1&2 should match. | 
| **SLITID2** |                     7  | 		 | Normalized slithead ID. sp1&2 should match. | 
| **GUIDERN** |  'proc-gimg-0780.fits'  | 		 | The last guider image | 
| **COLLA** |                   541  | 		 | The position of the A collimator motor | 
| **COLLB** |                   508  | 		 | The position of the B collimator motor | 
| **COLLC** |                   599  | 		 | The position of the C collimator motor | 
| **HARTMANN** |  'Closed, Closed'      | 		 | Hartmanns: Left,Right,Out | 
| **MC1HUMHT** |                  18.7  | 		 | sp1 mech Hartmann humidity, % | 
| **MC1HUMCO** |     8.699999999999999  | 		 | sp1 mech Central optics humidity, % | 
| **MC1TEMDN** |                  12.2  | 		 | sp1 mech Median temp, C | 
| **MC1THT** |                  13.3  | 		 | sp1 mech Hartmann Top Temp, C | 
| **MC1TRCB** |                  12.1  | 		 | sp1 mech Red Cam Bottom Temp, C | 
| **MC1TRCT** |                  12.2  | 		 | sp1 mech Red Cam Top Temp, C | 
| **MC1TBCB** |                  12.3  | 		 | sp1 mech Blue Cam Bottom Temp, C | 
| **MC1TBCT** |                  11.9  | 		 | sp1 mech Blue Cam Top Temp, C | 
| **REQTIME** |                     0  | 		 | requested exposure time | 
| **EXPTIME** |                     0  | 		 | requested exposure time | 
| **DARKTIME** |     8.800732851028442  | 		 | time between flush end and readout start | 
| **LN2TEMP** |     91.01600000000001                                                   | 		 | 		 | 
| **CCDTEMP** |    -99.60899999999999                                                   | 		 | 		 | 
| **IONPUMP** |                 -6.59                                                   | 		 | 		 | 
| **CHECKSUM** |  '9o9D9m7A9m7A9m7A'    | 		 | HDU checksum updated 2013-04-25T23:52:20 | 
| **DATASUM** |  '413425119'           | 		 | data unit checksum updated 2013-04-25T23:52:20 | 
| **END** | 		 | 		 | 		 | 
| **SUBFROW1** |                   850  | 		 | first row of subframe readout | 
| **SUBFROWN** |                  1400  | 		 | last row of subframe readout | 
| **V_BOSS** |  'v3_6    '            | 		 | Active version of the BOSS ICC | 
| **V_GUIDER** |  'v3_1    '            | 		 | version of the current guiderActor | 
| **V_SOP** |  'trunk+svn161790'     | 		 | version of the current sopActor | 
| **V_APO** |  'trunk+svn158476'     | 		 | version of the current apoActor | 


