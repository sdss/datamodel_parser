
# Datamodel: spiderstargetSequelsClus



#### General Description
The spiderstargetSequelsClus file contains information about SPIDERS Cluster
  targets in SEQUELS. It contains information on the X-ray origin of the targets
  as well as on parent clusters to which they are likely to belong.


#### Naming Convention
spiderstargetSequelsClus-{TARGET_TYPE}-{version}


#### Approximate Size
680 KB


#### File Type
FITS


## Page Contents
* [HDU1: TARGETING METADATA](#hdu1-targeting-metadata)
* [HDU2: TARGET INFORMATION](#hdu2-target-information)

## HDU1: TARGETING METADATA
This HDU contains a few information relative to the targeting process.

### HDU Type
IMAGE




		Required Data Table Columns


| **Name** | **Type** | **Unit** | **Description** |
| :--- | :----- | :---- | :------- |
| **TARGET_TYPE** | string | 		 | The target type |
| **TARGET_RUN** | string | 		 | The date of the targeting |
| **X_RAY** | string | 		 | Type of X-ray data |
| **SAMPLES** | string | 		 | Original samples |
| **NOBJ** | int32 | 		 | Number of objects in the file |


## HDU2: TARGET INFORMATION
This HDU contains the actual information on the targets

### HDU Type
IMAGE




		Required Data Table Columns


| **Name** | **Type** | **Unit** | **Description** |
| :--- | :----- | :---- | :------- |
| **RA** | float64 | deg | RA (from the SDSS DR9 imaging catalogue) |
| **DEC** | float64 | deg | DEC (from the SDSS DR9 imaging catalogue) |
| **FIBER2MAG** | float32[5] | 		 | fiber2
  magnitudes (u,g,r,i,z) (from the SDSS DR9 imaging catalogue) |
| **RUN** | int32 | 		 | (from the SDSS DR9 imaging catalogue) |
| **RERUN** | string | 		 | (from the SDSS DR9 imaging catalogue) |
| **CAMCOL** | int32 | 		 | (from the SDSS DR9 imaging catalogue) |
| **FIELD** | int32 | 		 | (from the SDSS DR9 imaging catalogue) |
| **ID** | int32 | 		 | (from the SDSS DR9 imaging catalogue) |
| **PRIORITY** | int32 | 		 | Internal SPIDERS
  targeting priority (highest=0 ... 50=lowest) |
| **TARGETSELECTED** | int32 | 		 | Rank of the
  target in its own parent cluster red-sequence |
| **Z_LAMBDA** | float64 | 		 | redMaPPer parent cluster
  photometric redshift |
| **Z_LAMBDA_ERR** | float64 | 		 | redMaPPer
  uncertainty on parent cluster photometric redshift |
| **LAMBDA_OPT** | float64 | 		 | redMaPPer parent cluster
richness |
| **SAMPLE** | string | 		 | Original sample |
| **CLUS_ID** | string | 		 | Unique parent cluster
name |



