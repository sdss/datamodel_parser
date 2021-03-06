---CREATE DATABASE datamodel OWNER sdss ENCODING 'UTF8' LC_COLLATE='en_US.UTF-8' LC_CTYPE='en_US.UTF-8' TEMPLATE template0;
---CREATE SCHEMA sdss AUTHORIZATION sdss;

DROP TABLE IF EXISTS sdss.column;
DROP TABLE IF EXISTS sdss.data;
DROP TABLE IF EXISTS sdss.keyword;
DROP TABLE IF EXISTS sdss.header;
DROP TABLE IF EXISTS sdss.hdu;
DROP TABLE IF EXISTS sdss.section;
DROP TABLE IF EXISTS sdss.filespec;
DROP TABLE IF EXISTS sdss.intro;
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

CREATE TABLE sdss.env (
    id SERIAL NOT NULL PRIMARY KEY,
    tree_id INT4 REFERENCES sdss.tree(id) NOT NULL,
    variable VARCHAR(32) NOT NULL,
    created TIMESTAMP WITH TIME ZONE DEFAULT NULL,
    modified TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE sdss.location (
    id SERIAL NOT NULL PRIMARY KEY,
    env_id INT4 REFERENCES sdss.env(id) NOT NULL,
    path VARCHAR(128),
    created TIMESTAMP WITH TIME ZONE DEFAULT NULL,
    modified TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE sdss.directory (
    id SERIAL NOT NULL PRIMARY KEY,
    location_id INT4 REFERENCES sdss.location(id) NOT NULL,
    name VARCHAR(64) NOT NULL,
    depth INT2 NOT NULL,
    created TIMESTAMP WITH TIME ZONE DEFAULT NULL,
    modified TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE sdss.file (
    id SERIAL NOT NULL PRIMARY KEY,
    location_id INT4 REFERENCES sdss.location(id) NOT NULL,
    name VARCHAR(64) NOT NULL,
    status VARCHAR(16),
    intro_type INT2,
    file_type INT2,
    created TIMESTAMP WITH TIME ZONE DEFAULT NULL,
    modified TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE sdss.intro (
    id SERIAL NOT NULL PRIMARY KEY,
    file_id INT4 REFERENCES sdss.file(id) NOT NULL,
    position INT2 NOT NULL,
    heading_level INT2,
    heading_title VARCHAR(128),
    description VARCHAR(4096),
    created TIMESTAMP WITH TIME ZONE DEFAULT NULL,
    modified TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE sdss.filespec (
    id SERIAL NOT NULL PRIMARY KEY,
    tree_id INT4 REFERENCES sdss.tree(id) NOT NULL,
    file_id INT4 REFERENCES sdss.file(id) NOT NULL,
    env_label VARCHAR(32),
    location VARCHAR(512),
    name VARCHAR(128),
    ext VARCHAR(16),
    path_example VARCHAR(512),
    note VARCHAR(512),
    created TIMESTAMP WITH TIME ZONE DEFAULT NULL,
    modified TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE sdss.section (
    id SERIAL NOT NULL PRIMARY KEY,
    file_id INT4 REFERENCES sdss.file(id) NOT NULL,
    hdu_number INT2,
    hdu_title VARCHAR(32),
    created TIMESTAMP WITH TIME ZONE DEFAULT NULL,
    modified TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE sdss.hdu (
    id SERIAL NOT NULL PRIMARY KEY,
    file_id INT4 REFERENCES sdss.file(id) NOT NULL,
    is_image BOOLEAN,
    number INT2,
    title VARCHAR(128),
    size VARCHAR(64),
    description VARCHAR(4096),
    hdu_type INT2,
    created TIMESTAMP WITH TIME ZONE DEFAULT NULL,
    modified TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE sdss.header (
    id SERIAL NOT NULL PRIMARY KEY,
    hdu_id INT4 REFERENCES sdss.hdu(id) NOT NULL,
    hdu_number INT2 NOT NULL,
    table_caption VARCHAR(1024),
    created TIMESTAMP WITH TIME ZONE DEFAULT NULL,
    modified TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE sdss.keyword (
    id SERIAL NOT NULL PRIMARY KEY,
    header_id INT4 REFERENCES sdss.header(id) NOT NULL,
    position INT2 NOT NULL,
    keyword VARCHAR(64),
    value VARCHAR(256),
    datatype VARCHAR(80),
    comment VARCHAR(16384),
    created TIMESTAMP WITH TIME ZONE DEFAULT NULL,
    modified TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE sdss.data (
    id SERIAL NOT NULL PRIMARY KEY,
    hdu_id INT4 REFERENCES sdss.hdu(id) NOT NULL,
    hdu_number INT2 NOT NULL,
    table_caption VARCHAR(1024),
    created TIMESTAMP WITH TIME ZONE DEFAULT NULL,
    modified TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE sdss.column (
    id SERIAL NOT NULL PRIMARY KEY,
    data_id INT4 REFERENCES sdss.data(id) NOT NULL,
    position INT2 NOT NULL,
    name VARCHAR(128),
    datatype VARCHAR(128),
    units VARCHAR(128),
    description VARCHAR(2048),
    created TIMESTAMP WITH TIME ZONE DEFAULT NULL,
    modified TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
