from FWCore.ParameterSet.VarParsing import VarParsing
# options = VarParsing()

# options.register ('globalTag', '', VarParsing.multiplicity.singleton, VarParsing.varType.string, "The globaltag to be used")

# options.parseArguments()
# if len(options.globalTag) == 0:
#   raise Exception("You _must_ pass a globalTag options to this script. Use --help for more informations")

from patTuple_PF2PAT_common_cfg import createPATProcess
# process = createPATProcess(False, options.globalTag)
process = createPATProcess(True, "START53_V27")

process.source.fileNames = cms.untracked.vstring(
   # from /TTbar173_16Feb13-v1/verdier-pv-fullsim535-step2-TTbar173-c9b345a6407f828c1cc6a52f8007a229/USER
   #'/store/user/verdier/TTbar173_16Feb13-v1/pv-fullsim535-step2-TTbar173/c9b345a6407f828c1cc6a52f8007a229/STEP2_RAW2DIGI_L1Reco_RECO_PU_10_1_ogJ.root',
   #'/store/user/verdier/TTbar173_16Feb13-v1/pv-fullsim535-step2-TTbar173/c9b345a6407f828c1cc6a52f8007a229/STEP2_RAW2DIGI_L1Reco_RECO_PU_11_1_1Ax.root'
   # from /TTJets_FullLeptMGDecays_8TeV-madgraph/Summer12_DR53X-PU_S10_START53_V7A-v2/AODSIM
   #'/store/mc/Summer12_DR53X/TTJets_FullLeptMGDecays_8TeV-madgraph/AODSIM/PU_S10_START53_V7A-v2/00000/000C5D15-AB1A-E211-8BDE-00215E22053A.root'
   # from /TTJets_SemiLeptMGDecays_8TeV-madgraph/Summer12_DR53X-PU_RD1_START53_V7N-v1/AODSIM
   '/store/mc/Summer12_DR53X/TTJets_SemiLeptMGDecays_8TeV-madgraph/AODSIM/PU_RD1_START53_V7N-v1/10000/00008678-63D7-E211-AB07-001E67398110.root',
   '/store/mc/Summer12_DR53X/TTJets_SemiLeptMGDecays_8TeV-madgraph/AODSIM/PU_RD1_START53_V7N-v1/10000/00089C1F-44D2-E211-B4BA-003048D45FF4.root',
    )
process.maxEvents.input = cms.untracked.int32(100)
