import FWCore.ParameterSet.Config as cms

process = cms.Process("Test")

process.load("FWCore.MessageService.MessageLogger_cfi")

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )

process.source = cms.Source("PoolSource",
    # replace 'myfile.root' with the source file you want to use
    fileNames = cms.untracked.vstring(
        'file:../../patTuple.root'
    )
)

process.TFileService = cms.Service("TFileService",
  fileName = cms.string('branchesTested.root')
)

process.test = cms.EDAnalyzer('TestBranches',
        muSrc         = cms.string("selectedPatMuonsPFlow"),
        elSrc         = cms.string("selectedPatElectronsPFlow"),
        jetSrc        = cms.string("selectedPatJetsPFlow"),
        nonIsoMuMinPt = cms.double(1.),
        muJpsiMinPt   = cms.double(1.),
        jpsiMassMin   = cms.double(2.8),
        jpsiMassMax   = cms.double(3.4),
        nTrD0Max      = cms.uint32(5),
        trD0MinPt     = cms.double(0.15),
        d0MassMin     = cms.double(1.5),
        d0MassMax     = cms.double(2.2)        
)


process.p = cms.Path(process.test)
