---CREATE DATABASE datamodel OWNER sdss ENCODING 'UTF8' LC_COLLATE='en_US.UTF-8' LC_CTYPE='en_US.UTF-8' TEMPLATE template0;
---CREATE SCHEMA sdss AUTHORIZATION sdss;

DROP TABLE IF EXISTS sdss.column;
DROP TABLE IF EXISTS sdss.data;
DROP TABLE IF EXISTS sdss.keyword;
DROP TABLE IF EXISTS sdss.header;
DROP TABLE IF EXISTS sdss.extension;
DROP TABLE IF EXISTS sdss.description;
DROP TABLE IF EXISTS sdss.file;
DROP TABLE IF EXISTS sdss.directory;
DROP TABLE IF EXISTS sdss.location;
DROP TABLE IF EXISTS sdss.env;
DROP TABLE IF EXISTS sdss.tree;


CREATE TABLE sdss.tree (
    id SERIAL NOT NULL PRIMARY KEY,
    edition VARCHAR(32) NOT NULL UNIQUE,
    created TIMESTAMP WITH TIME ZONE DEFAULT NULL,
    modified TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
INSERT INTO sdss.tree (edition,created) VALUES ('dr15',NOW());

CREATE TABLE sdss.env (
    id SERIAL NOT NULL PRIMARY KEY,
    tree_id INT4 REFERENCES sdss.tree(id) NOT NULL,
    variable VARCHAR(16) NOT NULL UNIQUE,
    created TIMESTAMP WITH TIME ZONE DEFAULT NULL,
    modified TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
INSERT INTO sdss.env (tree_id,variable,created)
VALUES (1,'APOGEE_REDUX',NOW());

CREATE TABLE sdss.location (
    id SERIAL NOT NULL PRIMARY KEY,
    env_id INT4 REFERENCES sdss.env(id) NOT NULL,
    path VARCHAR(64) NOT NULL UNIQUE,
    created TIMESTAMP WITH TIME ZONE DEFAULT NULL,
    modified TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
INSERT INTO sdss.location (env_id,path,created)
VALUES (1,'APRED_VERS/red/MJD5',NOW());

CREATE TABLE sdss.directory (
    id SERIAL NOT NULL PRIMARY KEY,
    location_id INT4 REFERENCES sdss.location(id) NOT NULL,
    name VARCHAR(64) NOT NULL UNIQUE,
    depth INT2,
    created TIMESTAMP WITH TIME ZONE DEFAULT NULL,
    modified TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
INSERT INTO sdss.directory (location_id,name,depth,created)
VALUES (1,'APRED_VERS',0,NOW());
INSERT INTO sdss.directory (location_id,name,depth,created)
VALUES (1,'red',1,NOW());
INSERT INTO sdss.directory (location_id,name,depth,created)
VALUES (1,'MJD5',2,NOW());

CREATE TABLE sdss.file (
    id SERIAL NOT NULL PRIMARY KEY,
    location_id INT4 REFERENCES sdss.location(id) NOT NULL,
    name VARCHAR(64) NOT NULL UNIQUE,
    extension_count INT2,
    created TIMESTAMP WITH TIME ZONE DEFAULT NULL,
    modified TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
INSERT INTO sdss.file (location_id,name,extension_count,created)
VALUES (1,'ap1D.html',6,NOW());

CREATE TABLE sdss.description (
    id SERIAL NOT NULL PRIMARY KEY,
    file_id INT4 REFERENCES sdss.file(id) NOT NULL,
    sas_path VARCHAR(128) NOT NULL UNIQUE,
    general_description VARCHAR(256) NOT NULL UNIQUE,
    naming_convention VARCHAR(128) NOT NULL UNIQUE,
    approximate_size VARCHAR(32) NOT NULL UNIQUE,
    file_type VARCHAR(32) NOT NULL UNIQUE,
    created TIMESTAMP WITH TIME ZONE DEFAULT NULL,
    modified TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
INSERT INTO sdss.description (file_id,
                              sas_path,
                              general_description,
                              naming_convention,
                              approximate_size,
                              file_type,
                              created)
VALUES (1,
        'https://data.sdss.org/sas/dr15/apogee/spectro/redux',
        'ap1D contain the raw extractions from the 2D spectra. A wavelength calibration is attached, but no sky subtraction, or telluric correction is applied.',
        'ap1D-[abc]-[0-9]{8}\.fits',
        '2048x2048x3x4 bytes',
        'FITS',
        NOW());

CREATE TABLE sdss.extension (
    id SERIAL NOT NULL PRIMARY KEY,
    file_id INT4 REFERENCES sdss.file(id) NOT NULL,
    hdu_number INT2,
    created TIMESTAMP WITH TIME ZONE DEFAULT NULL,
    modified TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
INSERT INTO sdss.extension (file_id,hdu_number,created) VALUES (1,0,NOW());
INSERT INTO sdss.extension (file_id,hdu_number,created) VALUES (1,1,NOW());
INSERT INTO sdss.extension (file_id,hdu_number,created) VALUES (1,2,NOW());
INSERT INTO sdss.extension (file_id,hdu_number,created) VALUES (1,3,NOW());
INSERT INTO sdss.extension (file_id,hdu_number,created) VALUES (1,4,NOW());
INSERT INTO sdss.extension (file_id,hdu_number,created) VALUES (1,5,NOW());

CREATE TABLE sdss.header (
    id SERIAL NOT NULL PRIMARY KEY,
    extension_id INT4 REFERENCES sdss.extension(id) NOT NULL,
    title VARCHAR(32) NOT NULL UNIQUE,
    created TIMESTAMP WITH TIME ZONE DEFAULT NULL,
    modified TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
INSERT INTO sdss.header (extension_id,title,created)
VALUES (1,'Master',NOW());
INSERT INTO sdss.header (extension_id,title,created)
VALUES (2,'Spectra',NOW());
INSERT INTO sdss.header (extension_id,title,created)
VALUES (3,'Errors',NOW());
INSERT INTO sdss.header (extension_id,title,created)
VALUES (4,'Mask',NOW());
INSERT INTO sdss.header (extension_id,title,created)
VALUES (5,'Wavelength array',NOW());
INSERT INTO sdss.header (extension_id,title,created)
VALUES (6,'Wavelength coefficients',NOW());

CREATE TABLE sdss.keyword (
    id SERIAL NOT NULL PRIMARY KEY,
    header_id INT4 REFERENCES sdss.header(id) NOT NULL,
    keyword VARCHAR(32) NOT NULL,
    value VARCHAR(80) NOT NULL,
    comment VARCHAR(80) NOT NULL,
    created TIMESTAMP WITH TIME ZONE DEFAULT NULL,
    modified TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
INSERT INTO sdss.keyword (header_id,keyword,value,comment,created)
VALUES (1,'SIMPLE','T','image conforms to FITS standard',NOW());
INSERT INTO sdss.keyword (header_id,keyword,value,comment,created)
VALUES (1,'BITPIX','16','bits per data value',NOW());
INSERT INTO sdss.keyword (header_id,keyword,value,comment,created)
VALUES (1,'NAXIS','0','number of axes',NOW());
INSERT INTO sdss.keyword (header_id,keyword,value,comment,created)
VALUES (1,'EXTEND','T','file may contain extensions',NOW());

INSERT INTO sdss.keyword (header_id,keyword,value,comment,created)
VALUES (2,'XTENSION','IMAGE   ','IMAGE extension',NOW());
INSERT INTO sdss.keyword (header_id,keyword,value,comment,created)
VALUES (2,'BITPIX','-32','Number of bits per data pixel',NOW());
INSERT INTO sdss.keyword (header_id,keyword,value,comment,created)
VALUES (2,'NAXIS','2','Number of data axes',NOW());
INSERT INTO sdss.keyword (header_id,keyword,value,comment,created)
VALUES (2,'NAXIS1','2048','',NOW());

INSERT INTO sdss.keyword (header_id,keyword,value,comment,created)
VALUES (3,'XTENSION','IMAGE   ','IMAGE extension',NOW());
INSERT INTO sdss.keyword (header_id,keyword,value,comment,created)
VALUES (3,'BITPIX','-32','Number of bits per data pixel',NOW());
INSERT INTO sdss.keyword (header_id,keyword,value,comment,created)
VALUES (3,'NAXIS','2','Number of data axes',NOW());
INSERT INTO sdss.keyword (header_id,keyword,value,comment,created)
VALUES (3,'NAXIS1','2048','',NOW());

INSERT INTO sdss.keyword (header_id,keyword,value,comment,created)
VALUES (4,'XTENSION','IMAGE   ','IMAGE extension',NOW());
INSERT INTO sdss.keyword (header_id,keyword,value,comment,created)
VALUES (4,'BITPIX','16','Number of bits per data pixel',NOW());
INSERT INTO sdss.keyword (header_id,keyword,value,comment,created)
VALUES (4,'NAXIS','2','Number of data axes',NOW());
INSERT INTO sdss.keyword (header_id,keyword,value,comment,created)
VALUES (4,'NAXIS1','2048','',NOW());

INSERT INTO sdss.keyword (header_id,keyword,value,comment,created)
VALUES (5,'XTENSION','IMAGE   ','IMAGE extension',NOW());
INSERT INTO sdss.keyword (header_id,keyword,value,comment,created)
VALUES (5,'BITPIX','-64','Number of bits per data pixel',NOW());
INSERT INTO sdss.keyword (header_id,keyword,value,comment,created)
VALUES (5,'NAXIS','2','Number of data axes',NOW());
INSERT INTO sdss.keyword (header_id,keyword,value,comment,created)
VALUES (5,'NAXIS1','2048','',NOW());

INSERT INTO sdss.keyword (header_id,keyword,value,comment,created)
VALUES (6,'XTENSION','IMAGE   ','IMAGE extension',NOW());
INSERT INTO sdss.keyword (header_id,keyword,value,comment,created)
VALUES (6,'BITPIX','-64','Number of bits per data pixel',NOW());
INSERT INTO sdss.keyword (header_id,keyword,value,comment,created)
VALUES (6,'NAXIS','2','Number of data axes',NOW());
INSERT INTO sdss.keyword (header_id,keyword,value,comment,created)
VALUES (6,'NAXIS1','300','',NOW());

CREATE TABLE sdss.data (
    id SERIAL NOT NULL PRIMARY KEY,
    extension_id INT4 REFERENCES sdss.extension(id) NOT NULL,
    is_image BOOLEAN NOT NULL DEFAULT FALSE,
    created TIMESTAMP WITH TIME ZONE DEFAULT NULL,
    modified TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
INSERT INTO sdss.data (extension_id,is_image,created)
VALUES (1,FALSE,NOW());
INSERT INTO sdss.data (extension_id,is_image,created)
VALUES (2,TRUE,NOW());
INSERT INTO sdss.data (extension_id,is_image,created)
VALUES (3,TRUE,NOW());
INSERT INTO sdss.data (extension_id,is_image,created)
VALUES (4,TRUE,NOW());
INSERT INTO sdss.data (extension_id,is_image,created)
VALUES (5,TRUE,NOW());
INSERT INTO sdss.data (extension_id,is_image,created)
VALUES (6,TRUE,NOW());

CREATE TABLE sdss.column (
    id SERIAL NOT NULL PRIMARY KEY,
    data_id INT4 REFERENCES sdss.data(id) NOT NULL,
    name VARCHAR(32) NOT NULL,
    value VARCHAR(64) NOT NULL,
    length int2 NOT NULL,
    description VARCHAR(80),
    created TIMESTAMP WITH TIME ZONE DEFAULT NULL,
    modified TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
INSERT INTO sdss.column (data_id,name,value,length,description,created)
VALUES (1,'SIMPLE','T',1,'image conforms to FITS standard',NOW());
INSERT INTO sdss.column (data_id,name,value,length,description,created)
VALUES (1,'BITPIX','16',1,'bits per data value',NOW());
INSERT INTO sdss.column (data_id,name,value,length,description,created)
VALUES (1,'NAXIS','0',1,'number of axes',NOW());
INSERT INTO sdss.column (data_id,name,value,length,description,created)
VALUES (1,'EXTEND','T',1,'file may contain extensions',NOW());
