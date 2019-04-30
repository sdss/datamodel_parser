
# Data model: knownMissing



#### General Description
This file contains a list of files that are known to be missing from SDSS
spectro reductions.  Only <a href="/sas/dr9/sdss/spectro/redux/26">reduction 26</a>
has these files.  There is only one 'good' plate-mjd
(in the <a href="http://www.sdss.org/dr13/help/glossary/#platequality">platequality</a>
sense) in all SDSS reductions that has known missing files: 1836-54567.  A
handful of 'marginal' plates have missing files.  We have carefully audited
all 'good' and 'marginal' plates and are confident that the knownMissing.txt files
reflect reality in these cases.  We have not attempted to audit 'bad' plates.
We have also corrected cases where a knownMissing.txt file listed files that
are actually present.


#### Naming Convention
<code>knownMissing\.txt</code>


#### Approximate Size
100 bytes


#### File Type
ASCII


