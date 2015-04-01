import FWCore.ParameterSet.Config as cms

from patTuple_PF2PAT_common_cfg import createPATProcess

process = createPATProcess(False, "FT53_V21A_AN6")

process.source.fileNames = cms.untracked.vstring( 
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
    )

process.maxEvents.input = cms.untracked.int32(100)
process.options.wantSummary = cms.untracked.bool(False)
process.MessageLogger.cerr.FwkReport.reportEvery = cms.untracked.int32(100)
