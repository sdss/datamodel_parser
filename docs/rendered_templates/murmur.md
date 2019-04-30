
# Data model: murmur



#### General Description
Low level log messages produced by SDSS telescope hardware.  The file
is simply a text file with timestamped messages.  This log system has
been replaced by the <a href="/datamodel/files/APOLOGS_DIR/">actor log system</a>.


#### Naming Convention
<code>murmur\.[0-9]{2}:[0-9]{2}:[0-9]{2}[A-Z][a-z][a-z][0-9]{6}\.log\.gz</code>,
where the complicated regular expression is a timestamp of the form HH:MM:SSMmmDDYYYY.


#### Approximate Size
3 MB (compressed)


#### File Type
TEXT


