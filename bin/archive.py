#!/usr/bin/env python3
from sdssdb.sqlalchemy.archive.sas import *
import time

#---select * from env where label='MANGA_SPECTRO_ANALYSIS' and tree_id=15; ---276
#---select id,location from directory where env_id=276 order by location asc limit 10;---1207150
#select * from file where directory_id=1207150 and location ilike '%dapall%';

session = database.Session()
tree_id = 15
env_label = 'MANGA_SPECTRO_ANALYSIS'
location = 'manga/spectro/analysis/v2_4_3/2.2.1'
t = time.time()
env = (session.query(Env)
              .filter(Env.tree_id == tree_id)
              .filter(Env.label == env_label)
              .one())
directory = (session.query(Directory)
                    .filter(Directory.env_id == env.id)
                    .filter(Directory.location == location)
                    .one())
file = (session.query(File)
               .filter(File.directory_id == directory.id)
               .filter(File.location.like('%dapall%'))
               .one())

print(f'env: {env}')
print(f'directory: {directory}')
print(f'file: {file}')
print(f'file.path given location: {file.path}')
print(f'time elapsed: {time.time() - t}')

#t = time.time()
#file_start = 'dapall-'
#directories = (session.query(Directory)
#                      .filter(Directory.env_id == env.id)
#                      .all())
#file_list = list()
#for directory in directories:
#    files = (session.query(File)
#                    .filter(File.directory_id == directory.id)
#                    .filter(File.location.like('%' + file_start + '%'))
#                    .all())
#    if files:
#        print('files: %r' % files)
#        file_list.extend(files)
#for file in file_list:
#    print(f'file.path not given location: {file.path}')
#print(f'time elapsed: {time.time() - t}')

split = file.location.split('/')
location = '/'.join(split[:-2]) if split else None
name = split[-1] if split else None
split = name.split('.')
ext = split[-1] if split and len(split) == 2 else None
filespec = session.add(Filespec)(tree_id = tree_id,
                    file_id = file.id,
                    env_label = env_label,
                    location = location,
                    name = name,
                    ext = ext,
                    path_example = file.location,
                    note = None,
                  )
if filespec:
    filespec.add()
    filespec.commit()
print(filespec)
