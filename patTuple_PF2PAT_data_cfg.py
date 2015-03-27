from FWCore.ParameterSet.VarParsing import VarParsing
options = VarParsing()

options.register ('globalTag', '', VarParsing.multiplicity.singleton, VarParsing.varType.string, "The globaltag to be used")

options.parseArguments()
if len(options.globalTag) == 0:
  raise Exception("You _must_ pass a globalTag options to this script. Use --help for more informations")

from patTuple_PF2PAT_common_cfg import createPATProcess
process = createPATProcess(False, options.globalTag)
# process = createPATProcess(False, "FT53_V21A_AN6")

process.source.fileNames = [ 
    #'file:input_data.root'
    # '/store/data/Run2012C/SingleMu/AOD/TOPMuPlusJets-24Aug2012-v1/00000/C8186FFC-2BEF-E111-80FB-001EC9D8D993.root'
    # '/store/data/Run2012B/SingleMu/AOD/TOPMuPlusJets-22Jan2013-v1/20000/FA21ADAF-AE71-E211-83D4-90E6BA19A243.root'
    ## SingleMu/Run2012B-22Jan2013-v1/AOD
    #'/store/data/Run2012B/SingleMu/AOD/22Jan2013-v1/110000/0412B176-AEE3-E211-A700-20CF3019DF03.root',
    #'/store/data/Run2012B/SingleMu/AOD/22Jan2013-v1/110000/0A2FCA76-AEE3-E211-A8A2-E0CB4E19F9A6.root',
    #'/store/data/Run2012B/SingleMu/AOD/22Jan2013-v1/110000/0C3C6077-AEE3-E211-A4CA-20CF305B059C.root',
    #'/store/data/Run2012B/SingleMu/AOD/22Jan2013-v1/110000/0C57EA77-AEE3-E211-8DCA-00259073E4D4.root',
    #'/store/data/Run2012B/SingleMu/AOD/22Jan2013-v1/110000/0E653900-AEE3-E211-8E25-90E6BA19A266.root',
    #'/store/data/Run2012B/SingleMu/AOD/22Jan2013-v1/110000/100D9A77-AEE3-E211-BDA9-20CF305B058E.root',
    #'/store/data/Run2012B/SingleMu/AOD/22Jan2013-v1/110000/1637B176-AEE3-E211-AAA0-90E6BA0D09AF.root',
    #'/store/data/Run2012B/SingleMu/AOD/22Jan2013-v1/110000/1821BA77-AEE3-E211-A284-002590747DDC.root',
    #'/store/data/Run2012B/SingleMu/AOD/22Jan2013-v1/110000/189322F2-AEE3-E211-86EF-E0CB4E5536A8.root',
    #'/store/data/Run2012B/SingleMu/AOD/22Jan2013-v1/110000/1C111592-AEE3-E211-99F8-90E6BA442F33.root'
    ## /SingleElectron/Run2012B-22Jan2013-v1/AOD
    '/store/data/Run2012B/SingleElectron/AOD/22Jan2013-v1/20000/001C4345-867D-E211-93E8-001E6739762F.root',
    '/store/data/Run2012B/SingleElectron/AOD/22Jan2013-v1/20000/00445686-0E7E-E211-B896-002590489DE0.root',
    '/store/data/Run2012B/SingleElectron/AOD/22Jan2013-v1/20000/005847D4-067E-E211-84D9-003048F1C81C.root',
    '/store/data/Run2012B/SingleElectron/AOD/22Jan2013-v1/20000/009061B0-BF7D-E211-9360-002590489DF0.root',
    '/store/data/Run2012B/SingleElectron/AOD/22Jan2013-v1/20000/00C3D12C-467D-E211-BF20-0025901E3E64.root',
    '/store/data/Run2012B/SingleElectron/AOD/22Jan2013-v1/20000/00F189F4-237E-E211-B0F5-003048FEACA4.root',
    '/store/data/Run2012B/SingleElectron/AOD/22Jan2013-v1/20000/00FC534F-0D7E-E211-8C8D-003048F02C60.root',
    '/store/data/Run2012B/SingleElectron/AOD/22Jan2013-v1/20000/0216C79D-3F7D-E211-A333-003048CF9E56.root',
    '/store/data/Run2012B/SingleElectron/AOD/22Jan2013-v1/20000/02545274-C77D-E211-9AFE-0025902CB678.root',
    '/store/data/Run2012B/SingleElectron/AOD/22Jan2013-v1/20000/0256E4A7-647D-E211-B06F-0025901DD2B2.root',
    ]

process.maxEvents.input = 5000
process.options.wantSummary = False
process.MessageLogger.cerr.FwkReport.reportEvery = 100
