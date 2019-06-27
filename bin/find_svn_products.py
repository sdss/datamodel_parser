#!/usr/bin/env python3
from os import walk
from os.path import join, exists
from datamodel_parser.application import Argument
from datamodel_parser.application import Store

from json import dumps

print('Finding SVN Products')
arg = Argument('find_svn_products')
options = arg.options if arg else None
store = Store(options=options) if options else None
logger = store.logger if store else None
ready = options and store and logger
ready = ready and store.ready
if not ready:
    print('Fail! ready: {}'.format(ready))
    exit(1)
else:
    store.svn_products = list()
    root_dir = 'https://trac.sdss.org/browser/repo/'
    store.set_svn_products(root_dir=root_dir)
    print('store.svn_products: \n' + dumps(store.svn_products,indent=1))
    store.exit()

'''
https://trac.sdss.org/browser/repo/apogee/apogeedb
https://trac.sdss.org/browser/repo/apogee/apogeelinelist
https://trac.sdss.org/browser/repo/apogee/apogeereduce
https://trac.sdss.org/browser/repo/apogee/apogeesim
https://trac.sdss.org/browser/repo/apogee/apogeetarget
https://trac.sdss.org/browser/repo/apogee/aporbit
https://trac.sdss.org/browser/repo/apogee/aprwebapp
https://trac.sdss.org/browser/repo/apogee/arthur
https://trac.sdss.org/browser/repo/apogee/idlwrap
https://trac.sdss.org/browser/repo/apogee/mri2012
https://trac.sdss.org/browser/repo/apogee/optimize_lst
https://trac.sdss.org/browser/repo/apogee/plate_images
https://trac.sdss.org/browser/repo/apogee/slarti
https://trac.sdss.org/browser/repo/apogee/speclib
https://trac.sdss.org/browser/repo/apogee/tselect
https://trac.sdss.org/browser/repo/apogee/tselectdb
https://trac.sdss.org/browser/repo/eboss/DECamprop
https://trac.sdss.org/browser/repo/eboss/DR14QSOBAO
https://trac.sdss.org/browser/repo/eboss/MyCat
https://trac.sdss.org/browser/repo/eboss/OriginalProposal
https://trac.sdss.org/browser/repo/eboss/ViSpec
https://trac.sdss.org/browser/repo/eboss/doe_proposal
https://trac.sdss.org/browser/repo/eboss/ebosstarget
https://trac.sdss.org/browser/repo/eboss/ebosstile
https://trac.sdss.org/browser/repo/eboss/ebosstilelist
https://trac.sdss.org/browser/repo/eboss/eddie
https://trac.sdss.org/browser/repo/eboss/elg_clf
https://trac.sdss.org/browser/repo/eboss/elg_fisher
https://trac.sdss.org/browser/repo/eboss/elg_technical
https://trac.sdss.org/browser/repo/eboss/elgredshiftflag
https://trac.sdss.org/browser/repo/eboss/final_cosmology
https://trac.sdss.org/browser/repo/eboss/findDLA
https://trac.sdss.org/browser/repo/eboss/forecast_technical
https://trac.sdss.org/browser/repo/eboss/galaxy
https://trac.sdss.org/browser/repo/eboss/idlspec2d
https://trac.sdss.org/browser/repo/eboss/kpnos3prop
https://trac.sdss.org/browser/repo/eboss/legacysurveyts
https://trac.sdss.org/browser/repo/eboss/lrg_technical
https://trac.sdss.org/browser/repo/eboss/lss/mkAllsamples
https://trac.sdss.org/browser/repo/eboss/lss/mkEsample
https://trac.sdss.org/browser/repo/eboss/ops_proposal
https://trac.sdss.org/browser/repo/eboss/pep_doc
https://trac.sdss.org/browser/repo/eboss/qso_technical
https://trac.sdss.org/browser/repo/eboss/qso_var_technical
https://trac.sdss.org/browser/repo/eboss/sequels_prop
https://trac.sdss.org/browser/repo/eboss/srd_doc
https://trac.sdss.org/browser/repo/eboss/stellarpop
https://trac.sdss.org/browser/repo/eboss/stripe82x
https://trac.sdss.org/browser/repo/eboss/survey_technical
https://trac.sdss.org/browser/repo/eboss/variability/qso_catalogs
https://trac.sdss.org/browser/repo/manga/Totoro
https://trac.sdss.org/browser/repo/manga/flowcharts
https://trac.sdss.org/browser/repo/manga/mangaPlateWebApp
https://trac.sdss.org/browser/repo/manga/mangacore
https://trac.sdss.org/browser/repo/manga/mangadap
https://trac.sdss.org/browser/repo/manga/mangadesign
https://trac.sdss.org/browser/repo/manga/mangadrp
https://trac.sdss.org/browser/repo/manga/mangalss
https://trac.sdss.org/browser/repo/manga/mangapca
https://trac.sdss.org/browser/repo/manga/mangatarget
https://trac.sdss.org/browser/repo/manga/mangatile
https://trac.sdss.org/browser/repo/manga/marvin
https://trac.sdss.org/browser/repo/manga/marvin_brain
https://trac.sdss.org/browser/repo/manga/mastar/mastarproc
https://trac.sdss.org/browser/repo/manga/mastar/mastartargets
https://trac.sdss.org/browser/repo/manga/utils
https://trac.sdss.org/browser/repo/operations/apo/Scripts
https://trac.sdss.org/browser/repo/operations/apo/bossforth
https://trac.sdss.org/browser/repo/operations/apo/interlocks
https://trac.sdss.org/browser/repo/operations/apo/mcp
https://trac.sdss.org/browser/repo/operations/apo/mcp_fiducials
https://trac.sdss.org/browser/repo/operations/apo/mcpop
https://trac.sdss.org/browser/repo/operations/apo/ntpvx
https://trac.sdss.org/browser/repo/operations/apo/observersBin
https://trac.sdss.org/browser/repo/operations/apo/plc
https://trac.sdss.org/browser/repo/operations/apo/sdssProcedures
https://trac.sdss.org/browser/repo/operations/apo/specMech
https://trac.sdss.org/browser/repo/operations/apo/swig
https://trac.sdss.org/browser/repo/operations/apo/thermo
https://trac.sdss.org/browser/repo/operations/apo/vx_tools
https://trac.sdss.org/browser/repo/operations/apo/xyplex
https://trac.sdss.org/browser/repo/operations/autoscheduler
https://trac.sdss.org/browser/repo/operations/general/actorcore
https://trac.sdss.org/browser/repo/operations/general/actorkeys
https://trac.sdss.org/browser/repo/operations/general/actors/alertsActor
https://trac.sdss.org/browser/repo/operations/general/actors/apoActor
https://trac.sdss.org/browser/repo/operations/general/actors/apogeeql
https://trac.sdss.org/browser/repo/operations/general/actors/apogeetest
https://trac.sdss.org/browser/repo/operations/general/actors/gcameraActor
https://trac.sdss.org/browser/repo/operations/general/actors/guiderActor
https://trac.sdss.org/browser/repo/operations/general/actors/hartmannActor
https://trac.sdss.org/browser/repo/operations/general/actors/platedbActor
https://trac.sdss.org/browser/repo/operations/general/actors/sopActor
https://trac.sdss.org/browser/repo/operations/general/actors/sosActor
https://trac.sdss.org/browser/repo/operations/general/actors/toyActor
https://trac.sdss.org/browser/repo/operations/general/apqlwebapp
https://trac.sdss.org/browser/repo/operations/general/documentation
https://trac.sdss.org/browser/repo/operations/general/external
https://trac.sdss.org/browser/repo/operations/general/iccs/bossICC
https://trac.sdss.org/browser/repo/operations/general/iccs/gcameraICC
https://trac.sdss.org/browser/repo/operations/general/idlmapper
https://trac.sdss.org/browser/repo/operations/general/opscore
https://trac.sdss.org/browser/repo/operations/general/sdssdb_sync
https://trac.sdss.org/browser/repo/operations/general/telemetry
https://trac.sdss.org/browser/repo/operations/general/tron
https://trac.sdss.org/browser/repo/operations/petunia
https://trac.sdss.org/browser/repo/papers/cpws
https://trac.sdss.org/browser/repo/papers/eboss/acacia_temp
https://trac.sdss.org/browser/repo/papers/sdss-general/DataReview
https://trac.sdss.org/browser/repo/papers/sdss-general/drpapers
https://trac.sdss.org/browser/repo/papers/sdss-general/sdss4-overview
https://trac.sdss.org/browser/repo/papers/tdss/SES_Technical_Paper
https://trac.sdss.org/browser/repo/proposals/sdss4-general/bigdata
https://trac.sdss.org/browser/repo/proposals/sdss4-general/pire
https://trac.sdss.org/browser/repo/proposals/sdss4-general/sdss4-msip
https://trac.sdss.org/browser/repo/proposals/sdss4-general/sloan
https://trac.sdss.org/browser/repo/sdss/datamodel
https://trac.sdss.org/browser/repo/sdss/ferre
https://trac.sdss.org/browser/repo/sdss/firefly
https://trac.sdss.org/browser/repo/sdss/flask_webapp_template
https://trac.sdss.org/browser/repo/sdss/idlsql
https://trac.sdss.org/browser/repo/sdss/idlutils
https://trac.sdss.org/browser/repo/sdss/ix
https://trac.sdss.org/browser/repo/sdss/master_schedule
https://trac.sdss.org/browser/repo/sdss/photoop
https://trac.sdss.org/browser/repo/sdss/plate
https://trac.sdss.org/browser/repo/sdss/platedesign
https://trac.sdss.org/browser/repo/sdss/platedesign_webapp
https://trac.sdss.org/browser/repo/sdss/platemeas/adjustFancucFiles
https://trac.sdss.org/browser/repo/sdss/platemeas/cmmPrograms
https://trac.sdss.org/browser/repo/sdss/platemeas/fitPlugPlateMeas
https://trac.sdss.org/browser/repo/sdss/platemeas/generateCMMData
https://trac.sdss.org/browser/repo/sdss/sas
https://trac.sdss.org/browser/repo/sdss/sdss4tools
https://trac.sdss.org/browser/repo/sdss/sdss_access
https://trac.sdss.org/browser/repo/sdss/sdss_maskbits
https://trac.sdss.org/browser/repo/sdss/sdss_python_module
https://trac.sdss.org/browser/repo/sdss/template
https://trac.sdss.org/browser/repo/sdss/trac
https://trac.sdss.org/browser/repo/sdss/transfer
https://trac.sdss.org/browser/repo/sdss/tree
https://trac.sdss.org/browser/repo/sdss/webapps/inspection
https://trac.sdss.org/browser/repo/sdss/webapps/pipe3d_php
https://trac.sdss.org/browser/repo/sdss/webapps/saw
'''
