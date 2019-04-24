
# Datamodel: ssppOut



#### General Description
This file consolidates the
<a href="RERUN/PLATE4/output/param/ssppOut.html">ssppOut</a>
results from the SSPP pipeline for all plates associated
with a given data release.  The format is similar to the individual ssppOut files,
but some additional columns are added. For
the SEGUE-2 targets associated with each star, see the associated
<a href="ssppTargets.html">ssppTargets</a> file.


#### Naming Convention
<code>ssppOut-dr[0-9]+\.fits</code>, where <code>[0-9]+</code> is the data release number.


#### Approximate Size
2 Gbytes


#### File Type
FITS


#### Read by Products
sas


#### Written by Products
sas


## Page Contents
* [HDU0: EMPTY HEADER](#hdu0-empty-header)
* [HDU1: SSPPOUT TABLE](#hdu1-ssppout-table)

## HDU0: EMPTY HEADER
This HDU is empty.
This HDU has no non-standard required keywords.




## HDU1: SSPPOUT TABLE




		Required Header Keywords


| **Key** | **Value** | **Type** | **Comment** |
| :--- | :----- | :---- | :------- |
| **XTENSION** | BINTABLE | str | Table Extension | 
| **TFIELDS** | 239 | int | Number of columns in table | 



		Required Data Table Columns


| **Name** | **Type** | **Unit** | **Description** |
| :--- | :----- | :---- | :------- |
| **SPECOBJID** | char[22] | 		 | <a href="/datamodel/files/SPECTRO_REDUX/specObj.html">See description in specObj file</a> |
| **PLATEID** | char[19] | 		 | <a href="/datamodel/files/SPECTRO_REDUX/specObj.html">See description in specObj file</a> |
| **BESTOBJID** | char[19] | 		 | <a href="/datamodel/files/SPECTRO_REDUX/specObj.html">See description in specObj file</a> |
| **FLUXOBJID** | char[19] | 		 | <a href="/datamodel/files/SPECTRO_REDUX/specObj.html">See description in specObj file</a> |
| **TARGETOBJID** | char[22] | 		 | <a href="/datamodel/files/SPECTRO_REDUX/specObj.html">See description in specObj file</a> |
| **SPECPRIMARY** | int32 | 		 | <a href="/datamodel/files/SPECTRO_REDUX/specObj.html">See description in specObj file</a> |
| **SPECLEGACY** | int32 | 		 | <a href="/datamodel/files/SPECTRO_REDUX/specObj.html">See description in specObj file</a> |
| **SPECSEGUE** | int32 | 		 | <a href="/datamodel/files/SPECTRO_REDUX/specObj.html">See description in specObj file</a> |
| **SPECSEGUE1** | int32 | 		 | <a href="/datamodel/files/SPECTRO_REDUX/specObj.html">See description in specObj file</a> |
| **SPECSEGUE2** | int32 | 		 | <a href="/datamodel/files/SPECTRO_REDUX/specObj.html">See description in specObj file</a> |
| **PLUG_RA** | float64 | 		 | <a href="/datamodel/files/SPECTRO_REDUX/specObj.html">See description in specObj file</a> |
| **PLUG_DEC** | float64 | 		 | <a href="/datamodel/files/SPECTRO_REDUX/specObj.html">See description in specObj file</a> |
| **LEGACY_TARGET1** | int32 | 		 | <a href="/datamodel/files/SPECTRO_REDUX/specObj.html">See description in specObj file</a> |
| **LEGACY_TARGET2** | int32 | 		 | <a href="/datamodel/files/SPECTRO_REDUX/specObj.html">See description in specObj file</a> |
| **SPECIAL_TARGET1** | int64 | 		 | <a href="/datamodel/files/SPECTRO_REDUX/specObj.html">See description in specObj file</a> |
| **SPECIAL_TARGET2** | int64 | 		 | <a href="/datamodel/files/SPECTRO_REDUX/specObj.html">See description in specObj file</a> |
| **FIRSTRELEASE** | char[3] | 		 | <a href="/datamodel/files/SPECTRO_REDUX/specObj.html">See description in specObj file</a> |
| **PROGRAMNAME** | char[23] | 		 | <a href="/datamodel/files/SPECTRO_REDUX/specObj.html">See description in specObj file</a> |
| **CHUNK** | char[16] | 		 | <a href="/datamodel/files/SPECTRO_REDUX/specObj.html">See description in specObj file</a> |
| **PLATERUN** | char[16] | 		 | <a href="/datamodel/files/SPECTRO_REDUX/specObj.html">See description in specObj file</a> |
| **RUNSSPP** | char[3] | 		 | <a href="/datamodel/files/SPECTRO_REDUX/specObj.html">See description in specObj file</a> |
| **RUN1D** | char[1] | 		 | <a href="/datamodel/files/SPECTRO_REDUX/specObj.html">See description in specObj file</a> |
| **RUN2D** | char[3] | 		 | <a href="/datamodel/files/SPECTRO_REDUX/specObj.html">See description in specObj file</a> |
| **MJD** | int32 | 		 | <a href="RERUN/PLATE4/output/param/ssppOut.html">See the individual ssppOut files.</a> |
| **PLATE** | int16 | 		 | <a href="RERUN/PLATE4/output/param/ssppOut.html">See the individual ssppOut files.</a> |
| **FIBER** | int16 | 		 | <a href="RERUN/PLATE4/output/param/ssppOut.html">See the individual ssppOut files.</a> |
| **PRIM_TARGET** | char[13] | 		 | <a href="RERUN/PLATE4/output/param/ssppOut.html">See the individual ssppOut files.</a> |
| **SPECTYPE_HAMMER** | char[4] | 		 | <a href="RERUN/PLATE4/output/param/ssppOut.html">See the individual ssppOut files.</a> |
| **SPECTYPE_SUBCLASS** | char[20] | 		 | <a href="RERUN/PLATE4/output/param/ssppOut.html">See the individual ssppOut files.</a> |
| **FLAG** | char[5] | 		 | <a href="RERUN/PLATE4/output/param/ssppOut.html">See the individual ssppOut files.</a> |
| **TEFF_ADOP** | float32 | 		 | <a href="RERUN/PLATE4/output/param/ssppOut.html">See the individual ssppOut files.</a> |
| **TEFF_ADOP_N** | int16 | 		 | <a href="RERUN/PLATE4/output/param/ssppOut.html">See the individual ssppOut files.</a> |
| **TEFF_ADOP_UNC** | float32 | 		 | <a href="RERUN/PLATE4/output/param/ssppOut.html">See the individual ssppOut files.</a> |
| **TEFF_HA24** | float32 | 		 | <a href="RERUN/PLATE4/output/param/ssppOut.html">See the individual ssppOut files.</a> |
| **TEFF_HD24** | float32 | 		 | <a href="RERUN/PLATE4/output/param/ssppOut.html">See the individual ssppOut files.</a> |
| **TEFF_TK** | float32 | 		 | <a href="RERUN/PLATE4/output/param/ssppOut.html">See the individual ssppOut files.</a> |
| **TEFF_TG** | float32 | 		 | <a href="RERUN/PLATE4/output/param/ssppOut.html">See the individual ssppOut files.</a> |
| **TEFF_TI** | float32 | 		 | <a href="RERUN/PLATE4/output/param/ssppOut.html">See the individual ssppOut files.</a> |
| **TEFF_NGS1** | float32 | 		 | <a href="RERUN/PLATE4/output/param/ssppOut.html">See the individual ssppOut files.</a> |
| **TEFF_ANNSR** | float32 | 		 | <a href="RERUN/PLATE4/output/param/ssppOut.html">See the individual ssppOut files.</a> |
| **TEFF_ANNRR** | float32 | 		 | <a href="RERUN/PLATE4/output/param/ssppOut.html">See the individual ssppOut files.</a> |
| **TEFF_WBG** | float32 | 		 | <a href="RERUN/PLATE4/output/param/ssppOut.html">See the individual ssppOut files.</a> |
| **TEFF_K24** | float32 | 		 | <a href="RERUN/PLATE4/output/param/ssppOut.html">See the individual ssppOut files.</a> |
| **TEFF_KI13** | float32 | 		 | <a href="RERUN/PLATE4/output/param/ssppOut.html">See the individual ssppOut files.</a> |
| **TEFF_HA24_IND** | int16 | 		 | <a href="RERUN/PLATE4/output/param/ssppOut.html">See the individual ssppOut files.</a> |
| **TEFF_HD24_IND** | int16 | 		 | <a href="RERUN/PLATE4/output/param/ssppOut.html">See the individual ssppOut files.</a> |
| **TEFF_TK_IND** | int16 | 		 | <a href="RERUN/PLATE4/output/param/ssppOut.html">See the individual ssppOut files.</a> |
| **TEFF_TG_IND** | int16 | 		 | <a href="RERUN/PLATE4/output/param/ssppOut.html">See the individual ssppOut files.</a> |
| **TEFF_TI_IND** | int16 | 		 | <a href="RERUN/PLATE4/output/param/ssppOut.html">See the individual ssppOut files.</a> |
| **TEFF_NGS1_IND** | int16 | 		 | <a href="RERUN/PLATE4/output/param/ssppOut.html">See the individual ssppOut files.</a> |
| **TEFF_ANNSR_IND** | int16 | 		 | <a href="RERUN/PLATE4/output/param/ssppOut.html">See the individual ssppOut files.</a> |
| **TEFF_ANNRR_IND** | int16 | 		 | <a href="RERUN/PLATE4/output/param/ssppOut.html">See the individual ssppOut files.</a> |
| **TEFF_WBG_IND** | int16 | 		 | <a href="RERUN/PLATE4/output/param/ssppOut.html">See the individual ssppOut files.</a> |
| **TEFF_K24_IND** | int16 | 		 | <a href="RERUN/PLATE4/output/param/ssppOut.html">See the individual ssppOut files.</a> |
| **TEFF_KI13_IND** | int16 | 		 | <a href="RERUN/PLATE4/output/param/ssppOut.html">See the individual ssppOut files.</a> |
| **TEFF_HA24_UNC** | float32 | 		 | <a href="RERUN/PLATE4/output/param/ssppOut.html">See the individual ssppOut files.</a> |
| **TEFF_HD24_UNC** | float32 | 		 | <a href="RERUN/PLATE4/output/param/ssppOut.html">See the individual ssppOut files.</a> |
| **TEFF_TK_UNC** | float32 | 		 | <a href="RERUN/PLATE4/output/param/ssppOut.html">See the individual ssppOut files.</a> |
| **TEFF_TG_UNC** | float32 | 		 | <a href="RERUN/PLATE4/output/param/ssppOut.html">See the individual ssppOut files.</a> |
| **TEFF_TI_UNC** | float32 | 		 | <a href="RERUN/PLATE4/output/param/ssppOut.html">See the individual ssppOut files.</a> |
| **TEFF_NGS1_UNC** | float32 | 		 | <a href="RERUN/PLATE4/output/param/ssppOut.html">See the individual ssppOut files.</a> |
| **TEFF_ANNSR_UNC** | float32 | 		 | <a href="RERUN/PLATE4/output/param/ssppOut.html">See the individual ssppOut files.</a> |
| **TEFF_ANNRR_UNC** | float32 | 		 | <a href="RERUN/PLATE4/output/param/ssppOut.html">See the individual ssppOut files.</a> |
| **TEFF_WBG_UNC** | float32 | 		 | <a href="RERUN/PLATE4/output/param/ssppOut.html">See the individual ssppOut files.</a> |
| **TEFF_K24_UNC** | float32 | 		 | <a href="RERUN/PLATE4/output/param/ssppOut.html">See the individual ssppOut files.</a> |
| **TEFF_KI13_UNC** | float32 | 		 | <a href="RERUN/PLATE4/output/param/ssppOut.html">See the individual ssppOut files.</a> |
| **LOGG_ADOP** | float32 | 		 | <a href="RERUN/PLATE4/output/param/ssppOut.html">See the individual ssppOut files.</a> |
| **LOGG_ADOP_N** | int16 | 		 | <a href="RERUN/PLATE4/output/param/ssppOut.html">See the individual ssppOut files.</a> |
| **LOGG_ADOP_UNC** | float32 | 		 | <a href="RERUN/PLATE4/output/param/ssppOut.html">See the individual ssppOut files.</a> |
| **LOGG_NGS2** | float32 | 		 | <a href="RERUN/PLATE4/output/param/ssppOut.html">See the individual ssppOut files.</a> |
| **LOGG_NGS1** | float32 | 		 | <a href="RERUN/PLATE4/output/param/ssppOut.html">See the individual ssppOut files.</a> |
| **LOGG_ANNSR** | float32 | 		 | <a href="RERUN/PLATE4/output/param/ssppOut.html">See the individual ssppOut files.</a> |
| **LOGG_ANNRR** | float32 | 		 | <a href="RERUN/PLATE4/output/param/ssppOut.html">See the individual ssppOut files.</a> |
| **LOGG_CAI1** | float32 | 		 | <a href="RERUN/PLATE4/output/param/ssppOut.html">See the individual ssppOut files.</a> |
| **LOGG_CAI2** | float32 | 		 | <a href="RERUN/PLATE4/output/param/ssppOut.html">See the individual ssppOut files.</a> |
| **LOGG_MGH** | float32 | 		 | <a href="RERUN/PLATE4/output/param/ssppOut.html">See the individual ssppOut files.</a> |
| **LOGG_WBG** | float32 | 		 | <a href="RERUN/PLATE4/output/param/ssppOut.html">See the individual ssppOut files.</a> |
| **LOGG_K24** | float32 | 		 | <a href="RERUN/PLATE4/output/param/ssppOut.html">See the individual ssppOut files.</a> |
| **LOGG_KI13** | float32 | 		 | <a href="RERUN/PLATE4/output/param/ssppOut.html">See the individual ssppOut files.</a> |
| **LOGG_NGS2_IND** | int16 | 		 | <a href="RERUN/PLATE4/output/param/ssppOut.html">See the individual ssppOut files.</a> |
| **LOGG_NGS1_IND** | int16 | 		 | <a href="RERUN/PLATE4/output/param/ssppOut.html">See the individual ssppOut files.</a> |
| **LOGG_ANNSR_IND** | int16 | 		 | <a href="RERUN/PLATE4/output/param/ssppOut.html">See the individual ssppOut files.</a> |
| **LOGG_ANNRR_IND** | int16 | 		 | <a href="RERUN/PLATE4/output/param/ssppOut.html">See the individual ssppOut files.</a> |
| **LOGG_CAI1_IND** | int16 | 		 | <a href="RERUN/PLATE4/output/param/ssppOut.html">See the individual ssppOut files.</a> |
| **LOGG_CAI2_IND** | int16 | 		 | <a href="RERUN/PLATE4/output/param/ssppOut.html">See the individual ssppOut files.</a> |
| **LOGG_MGH_IND** | int16 | 		 | <a href="RERUN/PLATE4/output/param/ssppOut.html">See the individual ssppOut files.</a> |
| **LOGG_WBG_IND** | int16 | 		 | <a href="RERUN/PLATE4/output/param/ssppOut.html">See the individual ssppOut files.</a> |
| **LOGG_K24_IND** | int16 | 		 | <a href="RERUN/PLATE4/output/param/ssppOut.html">See the individual ssppOut files.</a> |
| **LOGG_KI13_IND** | int16 | 		 | <a href="RERUN/PLATE4/output/param/ssppOut.html">See the individual ssppOut files.</a> |
| **LOGG_NGS2_UNC** | float32 | 		 | <a href="RERUN/PLATE4/output/param/ssppOut.html">See the individual ssppOut files.</a> |
| **LOGG_NGS1_UNC** | float32 | 		 | <a href="RERUN/PLATE4/output/param/ssppOut.html">See the individual ssppOut files.</a> |
| **LOGG_ANNSR_UNC** | float32 | 		 | <a href="RERUN/PLATE4/output/param/ssppOut.html">See the individual ssppOut files.</a> |
| **LOGG_ANNRR_UNC** | float32 | 		 | <a href="RERUN/PLATE4/output/param/ssppOut.html">See the individual ssppOut files.</a> |
| **LOGG_CAI1_UNC** | float32 | 		 | <a href="RERUN/PLATE4/output/param/ssppOut.html">See the individual ssppOut files.</a> |
| **LOGG_CAI2_UNC** | float32 | 		 | <a href="RERUN/PLATE4/output/param/ssppOut.html">See the individual ssppOut files.</a> |
| **LOGG_MGH_UNC** | float32 | 		 | <a href="RERUN/PLATE4/output/param/ssppOut.html">See the individual ssppOut files.</a> |
| **LOGG_WBG_UNC** | float32 | 		 | <a href="RERUN/PLATE4/output/param/ssppOut.html">See the individual ssppOut files.</a> |
| **LOGG_K24_UNC** | float32 | 		 | <a href="RERUN/PLATE4/output/param/ssppOut.html">See the individual ssppOut files.</a> |
| **LOGG_KI13_UNC** | float32 | 		 | <a href="RERUN/PLATE4/output/param/ssppOut.html">See the individual ssppOut files.</a> |
| **FEH_ADOP** | float32 | 		 | <a href="RERUN/PLATE4/output/param/ssppOut.html">See the individual ssppOut files.</a> |
| **FEH_ADOP_N** | int16 | 		 | <a href="RERUN/PLATE4/output/param/ssppOut.html">See the individual ssppOut files.</a> |
| **FEH_ADOP_UNC** | float32 | 		 | <a href="RERUN/PLATE4/output/param/ssppOut.html">See the individual ssppOut files.</a> |
| **FEH_NGS2** | float32 | 		 | <a href="RERUN/PLATE4/output/param/ssppOut.html">See the individual ssppOut files.</a> |
| **FEH_NGS1** | float32 | 		 | <a href="RERUN/PLATE4/output/param/ssppOut.html">See the individual ssppOut files.</a> |
| **FEH_ANNSR** | float32 | 		 | <a href="RERUN/PLATE4/output/param/ssppOut.html">See the individual ssppOut files.</a> |
| **FEH_ANNRR** | float32 | 		 | <a href="RERUN/PLATE4/output/param/ssppOut.html">See the individual ssppOut files.</a> |
| **FEH_CAIIK1** | float32 | 		 | <a href="RERUN/PLATE4/output/param/ssppOut.html">See the individual ssppOut files.</a> |
| **FEH_CAIIK2** | float32 | 		 | <a href="RERUN/PLATE4/output/param/ssppOut.html">See the individual ssppOut files.</a> |
| **FEH_CAIIK3** | float32 | 		 | <a href="RERUN/PLATE4/output/param/ssppOut.html">See the individual ssppOut files.</a> |
| **FEH_ACF** | float32 | 		 | <a href="RERUN/PLATE4/output/param/ssppOut.html">See the individual ssppOut files.</a> |
| **FEH_CAIIT** | float32 | 		 | <a href="RERUN/PLATE4/output/param/ssppOut.html">See the individual ssppOut files.</a> |
| **FEH_WBG** | float32 | 		 | <a href="RERUN/PLATE4/output/param/ssppOut.html">See the individual ssppOut files.</a> |
| **FEH_K24** | float32 | 		 | <a href="RERUN/PLATE4/output/param/ssppOut.html">See the individual ssppOut files.</a> |
| **FEH_KI13** | float32 | 		 | <a href="RERUN/PLATE4/output/param/ssppOut.html">See the individual ssppOut files.</a> |
| **FEH_NGS2_IND** | int16 | 		 | <a href="RERUN/PLATE4/output/param/ssppOut.html">See the individual ssppOut files.</a> |
| **FEH_NGS1_IND** | int16 | 		 | <a href="RERUN/PLATE4/output/param/ssppOut.html">See the individual ssppOut files.</a> |
| **FEH_ANNSR_IND** | int16 | 		 | <a href="RERUN/PLATE4/output/param/ssppOut.html">See the individual ssppOut files.</a> |
| **FEH_ANNRR_IND** | int16 | 		 | <a href="RERUN/PLATE4/output/param/ssppOut.html">See the individual ssppOut files.</a> |
| **FEH_CAIIK1_IND** | int16 | 		 | <a href="RERUN/PLATE4/output/param/ssppOut.html">See the individual ssppOut files.</a> |
| **FEH_CAIIK2_IND** | int16 | 		 | <a href="RERUN/PLATE4/output/param/ssppOut.html">See the individual ssppOut files.</a> |
| **FEH_CAIIK3_IND** | int16 | 		 | <a href="RERUN/PLATE4/output/param/ssppOut.html">See the individual ssppOut files.</a> |
| **FEH_ACF_IND** | int16 | 		 | <a href="RERUN/PLATE4/output/param/ssppOut.html">See the individual ssppOut files.</a> |
| **FEH_CAIIT_IND** | int16 | 		 | <a href="RERUN/PLATE4/output/param/ssppOut.html">See the individual ssppOut files.</a> |
| **FEH_WBG_IND** | int16 | 		 | <a href="RERUN/PLATE4/output/param/ssppOut.html">See the individual ssppOut files.</a> |
| **FEH_K24_IND** | int16 | 		 | <a href="RERUN/PLATE4/output/param/ssppOut.html">See the individual ssppOut files.</a> |
| **FEH_KI13_IND** | int16 | 		 | <a href="RERUN/PLATE4/output/param/ssppOut.html">See the individual ssppOut files.</a> |
| **FEH_NGS2_UNC** | float32 | 		 | <a href="RERUN/PLATE4/output/param/ssppOut.html">See the individual ssppOut files.</a> |
| **FEH_NGS1_UNC** | float32 | 		 | <a href="RERUN/PLATE4/output/param/ssppOut.html">See the individual ssppOut files.</a> |
| **FEH_ANNSR_UNC** | float32 | 		 | <a href="RERUN/PLATE4/output/param/ssppOut.html">See the individual ssppOut files.</a> |
| **FEH_ANNRR_UNC** | float32 | 		 | <a href="RERUN/PLATE4/output/param/ssppOut.html">See the individual ssppOut files.</a> |
| **FEH_CAIIK1_UNC** | float32 | 		 | <a href="RERUN/PLATE4/output/param/ssppOut.html">See the individual ssppOut files.</a> |
| **FEH_CAIIK2_UNC** | float32 | 		 | <a href="RERUN/PLATE4/output/param/ssppOut.html">See the individual ssppOut files.</a> |
| **FEH_CAIIK3_UNC** | float32 | 		 | <a href="RERUN/PLATE4/output/param/ssppOut.html">See the individual ssppOut files.</a> |
| **FEH_ACF_UNC** | float32 | 		 | <a href="RERUN/PLATE4/output/param/ssppOut.html">See the individual ssppOut files.</a> |
| **FEH_CAIIT_UNC** | float32 | 		 | <a href="RERUN/PLATE4/output/param/ssppOut.html">See the individual ssppOut files.</a> |
| **FEH_WBG_UNC** | float32 | 		 | <a href="RERUN/PLATE4/output/param/ssppOut.html">See the individual ssppOut files.</a> |
| **FEH_K24_UNC** | float32 | 		 | <a href="RERUN/PLATE4/output/param/ssppOut.html">See the individual ssppOut files.</a> |
| **FEH_KI13_UNC** | float32 | 		 | <a href="RERUN/PLATE4/output/param/ssppOut.html">See the individual ssppOut files.</a> |
| **AFE** | float32 | 		 | <a href="RERUN/PLATE4/output/param/ssppOut.html">See the individual ssppOut files.</a> |
| **AFE_IND** | int16 | 		 | <a href="RERUN/PLATE4/output/param/ssppOut.html">See the individual ssppOut files.</a> |
| **AFE_UNC** | float32 | 		 | <a href="RERUN/PLATE4/output/param/ssppOut.html">See the individual ssppOut files.</a> |
| **DIST_DWARF** | float32 | 		 | <a href="RERUN/PLATE4/output/param/ssppOut.html">See the individual ssppOut files.</a> |
| **DIST_TO** | float32 | 		 | <a href="RERUN/PLATE4/output/param/ssppOut.html">See the individual ssppOut files.</a> |
| **DIST_GIANT** | float32 | 		 | <a href="RERUN/PLATE4/output/param/ssppOut.html">See the individual ssppOut files.</a> |
| **DIST_AGB** | float32 | 		 | <a href="RERUN/PLATE4/output/param/ssppOut.html">See the individual ssppOut files.</a> |
| **DIST_FHB** | float32 | 		 | <a href="RERUN/PLATE4/output/param/ssppOut.html">See the individual ssppOut files.</a> |
| **DIST_AP** | float32 | 		 | <a href="RERUN/PLATE4/output/param/ssppOut.html">See the individual ssppOut files.</a> |
| **DIST_Z** | float32 | 		 | <a href="RERUN/PLATE4/output/param/ssppOut.html">See the individual ssppOut files.</a> |
| **RV_FLAG** | char[4] | 		 | <a href="RERUN/PLATE4/output/param/ssppOut.html">See the individual ssppOut files.</a> |
| **RV_ADOP** | float32 | 		 | <a href="RERUN/PLATE4/output/param/ssppOut.html">See the individual ssppOut files.</a> |
| **RV_ADOP_UNC** | float32 | 		 | <a href="RERUN/PLATE4/output/param/ssppOut.html">See the individual ssppOut files.</a> |
| **RV_CAL** | float32 | 		 | <a href="RERUN/PLATE4/output/param/ssppOut.html">See the individual ssppOut files.</a> |
| **RV_CAL_UNC** | float32 | 		 | <a href="RERUN/PLATE4/output/param/ssppOut.html">See the individual ssppOut files.</a> |
| **RV_BS** | float32 | 		 | <a href="RERUN/PLATE4/output/param/ssppOut.html">See the individual ssppOut files.</a> |
| **RV_BS_UNC** | float32 | 		 | <a href="RERUN/PLATE4/output/param/ssppOut.html">See the individual ssppOut files.</a> |
| **RV_ELODIE** | float32 | 		 | <a href="RERUN/PLATE4/output/param/ssppOut.html">See the individual ssppOut files.</a> |
| **RV_ELODIE_UNC** | float32 | 		 | <a href="RERUN/PLATE4/output/param/ssppOut.html">See the individual ssppOut files.</a> |
| **RV_GSR** | float32 | 		 | <a href="RERUN/PLATE4/output/param/ssppOut.html">See the individual ssppOut files.</a> |
| **RV_GSR_UNC** | float32 | 		 | <a href="RERUN/PLATE4/output/param/ssppOut.html">See the individual ssppOut files.</a> |
| **V_MAG** | float32 | 		 | <a href="RERUN/PLATE4/output/param/ssppOut.html">See the individual ssppOut files.</a> |
| **BV** | float32 | 		 | <a href="RERUN/PLATE4/output/param/ssppOut.html">See the individual ssppOut files.</a> |
| **BV_BALMER** | float32 | 		 | <a href="RERUN/PLATE4/output/param/ssppOut.html">See the individual ssppOut files.</a> |
| **GR_PREDICT** | float32 | 		 | <a href="RERUN/PLATE4/output/param/ssppOut.html">See the individual ssppOut files.</a> |
| **GR_HA24** | float32 | 		 | <a href="RERUN/PLATE4/output/param/ssppOut.html">See the individual ssppOut files.</a> |
| **GR_HD24** | float32 | 		 | <a href="RERUN/PLATE4/output/param/ssppOut.html">See the individual ssppOut files.</a> |
| **GR_HP** | float32 | 		 | <a href="RERUN/PLATE4/output/param/ssppOut.html">See the individual ssppOut files.</a> |
| **G_MAG** | float32 | 		 | <a href="RERUN/PLATE4/output/param/ssppOut.html">See the individual ssppOut files.</a> |
| **UG** | float32 | 		 | <a href="RERUN/PLATE4/output/param/ssppOut.html">See the individual ssppOut files.</a> |
| **GR** | float32 | 		 | <a href="RERUN/PLATE4/output/param/ssppOut.html">See the individual ssppOut files.</a> |
| **RI** | float32 | 		 | <a href="RERUN/PLATE4/output/param/ssppOut.html">See the individual ssppOut files.</a> |
| **IZ** | float32 | 		 | <a href="RERUN/PLATE4/output/param/ssppOut.html">See the individual ssppOut files.</a> |
| **U_MAG_UNC** | float32 | 		 | <a href="RERUN/PLATE4/output/param/ssppOut.html">See the individual ssppOut files.</a> |
| **G_MAG_UNC** | float32 | 		 | <a href="RERUN/PLATE4/output/param/ssppOut.html">See the individual ssppOut files.</a> |
| **R_MAG_UNC** | float32 | 		 | <a href="RERUN/PLATE4/output/param/ssppOut.html">See the individual ssppOut files.</a> |
| **I_MAG_UNC** | float32 | 		 | <a href="RERUN/PLATE4/output/param/ssppOut.html">See the individual ssppOut files.</a> |
| **Z_MAG_UNC** | float32 | 		 | <a href="RERUN/PLATE4/output/param/ssppOut.html">See the individual ssppOut files.</a> |
| **EBV** | float32 | 		 | <a href="RERUN/PLATE4/output/param/ssppOut.html">See the individual ssppOut files.</a> |
| **SNR** | float32 | 		 | <a href="RERUN/PLATE4/output/param/ssppOut.html">See the individual ssppOut files.</a> |
| **QA** | int16 | 		 | <a href="RERUN/PLATE4/output/param/ssppOut.html">See the individual ssppOut files.</a> |
| **CC_CAHK** | float32 | 		 | <a href="RERUN/PLATE4/output/param/ssppOut.html">See the individual ssppOut files.</a> |
| **CC_MGH** | float32 | 		 | <a href="RERUN/PLATE4/output/param/ssppOut.html">See the individual ssppOut files.</a> |
| **RA** | float64 | 		 | <a href="RERUN/PLATE4/output/param/ssppOut.html">See the individual ssppOut files.</a> |
| **DEC** | float64 | 		 | <a href="RERUN/PLATE4/output/param/ssppOut.html">See the individual ssppOut files.</a> |
| **L** | float64 | 		 | <a href="RERUN/PLATE4/output/param/ssppOut.html">See the individual ssppOut files.</a> |
| **B** | float64 | 		 | <a href="RERUN/PLATE4/output/param/ssppOut.html">See the individual ssppOut files.</a> |
| **TEFF_SPEC** | float32 | 		 | <a href="RERUN/PLATE4/output/param/ssppOut.html">See the individual ssppOut files.</a> |
| **TEFF_SPEC_N** | int16 | 		 | <a href="RERUN/PLATE4/output/param/ssppOut.html">See the individual ssppOut files.</a> |
| **TEFF_SPEC_UNC** | float32 | 		 | <a href="RERUN/PLATE4/output/param/ssppOut.html">See the individual ssppOut files.</a> |
| **LOGG_SPEC** | float32 | 		 | <a href="RERUN/PLATE4/output/param/ssppOut.html">See the individual ssppOut files.</a> |
| **LOGG_SPEC_N** | int16 | 		 | <a href="RERUN/PLATE4/output/param/ssppOut.html">See the individual ssppOut files.</a> |
| **LOGG_SPEC_UNC** | float32 | 		 | <a href="RERUN/PLATE4/output/param/ssppOut.html">See the individual ssppOut files.</a> |
| **FEH_SPEC** | float32 | 		 | <a href="RERUN/PLATE4/output/param/ssppOut.html">See the individual ssppOut files.</a> |
| **FEH_SPEC_N** | int16 | 		 | <a href="RERUN/PLATE4/output/param/ssppOut.html">See the individual ssppOut files.</a> |
| **FEH_SPEC_UNC** | float32 | 		 | <a href="RERUN/PLATE4/output/param/ssppOut.html">See the individual ssppOut files.</a> |
| **TEFF_COL** | float32 | 		 | <a href="RERUN/PLATE4/output/param/ssppOut.html">See the individual ssppOut files.</a> |
| **TEFF_COL_UNC** | float32 | 		 | <a href="RERUN/PLATE4/output/param/ssppOut.html">See the individual ssppOut files.</a> |
| **FEH_TFIX_NGS2** | float32 | 		 | <a href="RERUN/PLATE4/output/param/ssppOut.html">See the individual ssppOut files.</a> |
| **FEH_TFIX_NGS1** | float32 | 		 | <a href="RERUN/PLATE4/output/param/ssppOut.html">See the individual ssppOut files.</a> |
| **LOGG_TFIX_NGS2** | float32 | 		 | <a href="RERUN/PLATE4/output/param/ssppOut.html">See the individual ssppOut files.</a> |
| **LOGG_TFIX_NGS1** | float32 | 		 | <a href="RERUN/PLATE4/output/param/ssppOut.html">See the individual ssppOut files.</a> |
| **FEH_TFIX_NGS2_UNC** | float32 | 		 | <a href="RERUN/PLATE4/output/param/ssppOut.html">See the individual ssppOut files.</a> |
| **FEH_TFIX_NGS1_UNC** | float32 | 		 | <a href="RERUN/PLATE4/output/param/ssppOut.html">See the individual ssppOut files.</a> |
| **LOGG_TFIX_NGS2_UNC** | float32 | 		 | <a href="RERUN/PLATE4/output/param/ssppOut.html">See the individual ssppOut files.</a> |
| **LOGG_TFIX_NGS1_UNC** | float32 | 		 | <a href="RERUN/PLATE4/output/param/ssppOut.html">See the individual ssppOut files.</a> |
| **FEH_TFIX_CAIIK1** | float32 | 		 | <a href="RERUN/PLATE4/output/param/ssppOut.html">See the individual ssppOut files.</a> |
| **FEH_TFIX_CAIIK1_UNC** | float32 | 		 | <a href="RERUN/PLATE4/output/param/ssppOut.html">See the individual ssppOut files.</a> |
| **ACF1** | float32 | 		 | <a href="RERUN/PLATE4/output/param/ssppOut.html">See the individual ssppOut files.</a> |
| **ACF1_SNR** | float32 | 		 | <a href="RERUN/PLATE4/output/param/ssppOut.html">See the individual ssppOut files.</a> |
| **ACF2** | float32 | 		 | <a href="RERUN/PLATE4/output/param/ssppOut.html">See the individual ssppOut files.</a> |
| **ACF2_SNR** | float32 | 		 | <a href="RERUN/PLATE4/output/param/ssppOut.html">See the individual ssppOut files.</a> |
| **INSPECT** | char[6] | 		 | <a href="RERUN/PLATE4/output/param/ssppOut.html">See the individual ssppOut files.</a> |
| **ELODIERVFINAL** | float32 | 		 | <a href="RERUN/PLATE4/output/param/ssppOut.html">See the individual ssppOut files.</a> |
| **ELODIERVFINALERR** | float32 | 		 | <a href="RERUN/PLATE4/output/param/ssppOut.html">See the individual ssppOut files.</a> |
| **ZWARNING** | int32 | 		 | <a href="RERUN/PLATE4/output/param/ssppOut.html">See the individual ssppOut files.</a> |
| **SURVEY** | char[6] | 		 | <a href="RERUN/PLATE4/output/param/ssppOut.html">See the individual ssppOut files.</a> |
| **PRIMTARGET** | int32 | 		 | <a href="RERUN/PLATE4/output/param/ssppOut.html">See the individual ssppOut files.</a> |
| **SECTARGET** | int32 | 		 | <a href="RERUN/PLATE4/output/param/ssppOut.html">See the individual ssppOut files.</a> |
| **SEGUE1_TARGET1** | int32 | 		 | <a href="RERUN/PLATE4/output/param/ssppOut.html">See the individual ssppOut files.</a> |
| **SEGUE1_TARGET2** | int32 | 		 | <a href="RERUN/PLATE4/output/param/ssppOut.html">See the individual ssppOut files.</a> |
| **SEGUE2_TARGET1** | int32 | 		 | <a href="RERUN/PLATE4/output/param/ssppOut.html">See the individual ssppOut files.</a> |
| **SEGUE2_TARGET2** | int32 | 		 | <a href="RERUN/PLATE4/output/param/ssppOut.html">See the individual ssppOut files.</a> |
| **L_CLASS** | char[4] | 		 | <a href="RERUN/PLATE4/output/param/ssppOut.html">See the individual ssppOut files.</a> |
| **DIST_ADOP** | float32 | 		 | <a href="RERUN/PLATE4/output/param/ssppOut.html">See the individual ssppOut files.</a> |
| **MP_FLAG** | char[2] | 		 | <a href="RERUN/PLATE4/output/param/ssppOut.html">See the individual ssppOut files.</a> |
| **TEFF_IRFM** | float32 | 		 | <a href="RERUN/PLATE4/output/param/ssppOut.html">See the individual ssppOut files.</a> |
| **TEFF_IRFM_IND** | int16 | 		 | <a href="RERUN/PLATE4/output/param/ssppOut.html">See the individual ssppOut files.</a> |
| **TEFF_IRFM_UNC** | float32 | 		 | <a href="RERUN/PLATE4/output/param/ssppOut.html">See the individual ssppOut files.</a> |
| **LOGG_NGS1_IRFM** | float32 | 		 | <a href="RERUN/PLATE4/output/param/ssppOut.html">See the individual ssppOut files.</a> |
| **LOGG_NGS1_IRFM_IND** | int16 | 		 | <a href="RERUN/PLATE4/output/param/ssppOut.html">See the individual ssppOut files.</a> |
| **LOGG_NGS1_IRFM_UNC** | float32 | 		 | <a href="RERUN/PLATE4/output/param/ssppOut.html">See the individual ssppOut files.</a> |
| **FEH_NGS1_IRFM** | float32 | 		 | <a href="RERUN/PLATE4/output/param/ssppOut.html">See the individual ssppOut files.</a> |
| **FEH_NGS1_IRFM_IND** | int16 | 		 | <a href="RERUN/PLATE4/output/param/ssppOut.html">See the individual ssppOut files.</a> |
| **FEH_NGS1_IRFM_UNC** | float32 | 		 | <a href="RERUN/PLATE4/output/param/ssppOut.html">See the individual ssppOut files.</a> |
| **LOGG_CAI1_IRFM** | float32 | 		 | <a href="RERUN/PLATE4/output/param/ssppOut.html">See the individual ssppOut files.</a> |
| **LOGG_CAI1_IRFM_IND** | int16 | 		 | <a href="RERUN/PLATE4/output/param/ssppOut.html">See the individual ssppOut files.</a> |
| **LOGG_CAI1_IRFM_UNC** | float32 | 		 | <a href="RERUN/PLATE4/output/param/ssppOut.html">See the individual ssppOut files.</a> |
| **FEH_CAIIK1_IRFM** | float32 | 		 | <a href="RERUN/PLATE4/output/param/ssppOut.html">See the individual ssppOut files.</a> |
| **FEH_CAIIK1_IRFM_IND** | int16 | 		 | <a href="RERUN/PLATE4/output/param/ssppOut.html">See the individual ssppOut files.</a> |
| **FEH_CAIIK1_IRFM_UNC** | float32 | 		 | <a href="RERUN/PLATE4/output/param/ssppOut.html">See the individual ssppOut files.</a> |



