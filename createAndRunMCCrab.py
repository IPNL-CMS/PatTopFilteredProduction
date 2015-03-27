#! /usr/bin/env python

import os, copy, datetime, pwd, re

from optparse import OptionParser
parser = OptionParser()
parser.add_option("", "--run", action="store_true", dest="run", default=False, help="run crab")
(options, args) = parser.parse_args()


datasets = {}
for file in args:
    with open(file) as f:
        datasets.update(json.load(f))
    
# Get username address
#user_name = "\'/store/user/%s\'" % (pwd.getpwuid(os.getuid()).pw_name)
user_name = "\'/store/user/ebouvier\'" 

d = datetime.datetime.now().strftime("%y%b%d")

version = 1

datasets = [
    # Standard ttbar
    ["/TTJets_FullLeptMGDecays_8TeV-madgraph/Summer12_DR53X-PU_S10_START53_V7A-v2/AODSIM", "TTJets_FullLeptMGDecays", "START53_V27"],
    ["/TTJets_SemiLeptMGDecays_8TeV-madgraph/Summer12_DR53X-PU_S10_START53_V7A_ext-v1/AODSIM", "TTJets_SemiLeptMGDecays", "START53_V27"],
    ["/TTJets_HadronicMGDecays_8TeV-madgraph/Summer12_DR53X-PU_S10_START53_V7A_ext-v1/AODSIM", "TTJets_HadronicMGDecays", "START53_V27"],
    # W + jets
    #["/WJetsToLNu_TuneZ2Star_8TeV-madgraph-tarball/Summer12_DR53X-PU_S10_START53_V7A-v2/AODSIM", "WJetsToLNu", "START53_V27"],
    ["/W1JetsToLNu_TuneZ2Star_8TeV-madgraph/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM", "W1JetsToLNu", "START53_V27"],
    ["/W2JetsToLNu_TuneZ2Star_8TeV-madgraph/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM", "W2JetsToLNu", "START53_V27"],
    ["/W3JetsToLNu_TuneZ2Star_8TeV-madgraph/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM", "W3JetsToLNu", "START53_V27"],
    ["/W4JetsToLNu_TuneZ2Star_8TeV-madgraph/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM", "W4JetsToLNu", "START53_V27"],
    # Z + jets
    #["/DYJetsToLL_M-10To50filter_8TeV-madgraph/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM", "DYJetsToLL_M-10To50", "START53_V27"],
    #["/DYJetsToLL_M-50_TuneZ2Star_8TeV-madgraph-tarball/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM", "DYJetsToLL_M-50", "START53_V27"],
    ["/DY1JetsToLL_M-50_TuneZ2Star_8TeV-madgraph/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM", "DY1JetsToLL_M-50", "START53_V27"],
    ["/DY2JetsToLL_M-50_TuneZ2Star_8TeV-madgraph/Summer12_DR53X-PU_S10_START53_V7C-v1/AODSIM", "DY2JetsToLL_M-50", "START53_V27"],
    ["/DY3JetsToLL_M-50_TuneZ2Star_8TeV-madgraph/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM", "DY3JetsToLL_M-50", "START53_V27"],
    ["/DY4JetsToLL_M-50_TuneZ2Star_8TeV-madgraph/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM", "DY4JetsToLL_M-50", "START53_V27"],
    # diboson
    ["/WW_TuneZ2star_8TeV_pythia6_tauola/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM", "WW-incl", "START53_V27"],
    ["/WZ_TuneZ2star_8TeV_pythia6_tauola/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM", "WZ-incl", "START53_V27"],
    ["/ZZ_TuneZ2star_8TeV_pythia6_tauola/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM", "ZZ-incl", "START53_V27"],
    # ttbar other
    ["/TTWJets_8TeV-madgraph/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM", "TTWJets", "START53_V27"],
    ["/TTWWJets_8TeV-madgraph/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM", "TTWWJets", "START53_V27"],
    ["/TTZJets_8TeV-madgraph_v2/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM", "TTZJets", "START53_V27"],
    # single top 
    ## central
    ["/T_s-channel_TuneZ2star_8TeV-powheg-tauola/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM", "T_s-channel", "START53_V27"],
    ["/T_t-channel_TuneZ2star_8TeV-powheg-tauola/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM", "T_t-channel", "START53_V27"],
    ["/T_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM", "T_tW-channel", "START53_V27"],
    ["/Tbar_s-channel_TuneZ2star_8TeV-powheg-tauola/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM", "Tbar_s-channel", "START53_V27"],
    ["/Tbar_t-channel_TuneZ2star_8TeV-powheg-tauola/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM", "Tbar_t-channel", "START53_V27"],
    ## single top t-chanel, top mass variations
    ["/TToLeptons_t-channel_mass166_5_8TeV-powheg-tauola/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM", "TToLeptons_t-channel_mass166_5", "START53_V27"],
    ["/TToLeptons_t-channel_mass169_5_8TeV-powheg-tauola/Summer12_DR53X-PU_S10_START53_V19-v1/AODSIM", "TToLeptons_t-channel_mass169_5", "START53_V27"],
    ["/TToLeptons_t-channel_mass171_5_8TeV-powheg-tauola/Summer12_DR53X-PU_S10_START53_V19-v1/AODSIM", "TToLeptons_t-channel_mass171_5", "START53_V27"],
    ["/TToLeptons_t-channel_mass173_5_8TeV-powheg-tauola/Summer12_DR53X-PU_S10_START53_V19-v1/AODSIM", "TToLeptons_t-channel_mass173_5", "START53_V27"],
    ["/TToLeptons_t-channel_mass175_5_8TeV-powheg-tauola/Summer12_DR53X-PU_S10_START53_V19-v1/AODSIM", "TToLeptons_t-channel_mass175_5", "START53_V27"],
    ["/TToLeptons_t-channel_mass178_5_8TeV-powheg-tauola/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM", "TToLeptons_t-channel_mass178_5", "START53_V27"],
    ["/TBarToLeptons_t-channel_mass166_5_8TeV-powheg-tauola/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM", "TBarToLeptons_t-channel_mass166_5", "START53_V27"],
    ["/TBarToLeptons_t-channel_mass169_5_8TeV-powheg-tauola/Summer12_DR53X-PU_S10_START53_V19-v1/AODSIM", "TBarToLeptons_t-channel_mass169_5", "START53_V27"],
    ["/TBarToLeptons_t-channel_mass171_5_8TeV-powheg-tauola/Summer12_DR53X-PU_S10_START53_V19-v1/AODSIM", "TBarToLeptons_t-channel_mass171_5", "START53_V27"],
    ["/TBarToLeptons_t-channel_mass173_5_8TeV-powheg-tauola/Summer12_DR53X-PU_S10_START53_V19-v1/AODSIM", "TBarToLeptons_t-channel_mass173_5", "START53_V27"],
    ["/TBarToLeptons_t-channel_mass175_5_8TeV-powheg-tauola/Summer12_DR53X-PU_S10_START53_V19-v1/AODSIM", "TBarToLeptons_t-channel_mass175_5", "START53_V27"],
    ["/TBarToLeptons_t-channel_mass178_5_8TeV-powheg-tauola/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM", "TBarToLeptons_t-channel_mass178_5", "START53_V27"],
    ## 166.5
    ["/TBarToLeptons_s-channel_mass166_5_8TeV-powheg-tauola/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM", "TBarToLeptons_s-channel_mass166_5", "START53_V27"],
    ["/TBarToLeptons_t-channel_mass166_5_8TeV-powheg-tauola/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM", "TBarToLeptons_t-channel_mass166_5", "START53_V27"],
    ["/TBarToTlepWhad_tW-channel-DR_mass166_5_8TeV-powheg-tauola/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM", "TBarToTlepWhad_tW-channel-DR_mass166_5", "START53_V27"],
    ["/TBarToThadWlep_tW-channel-DR_mass166_5_8TeV-powheg-tauola/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM", "TBarToThadWlep_tW-channel-DR_mass166_5", "START53_V27"],
    ["/TBarToDilepton_tW-channel-DR_mass166_5_8TeV-powheg-tauola/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM", "TBarToDilepton_tW-channel-DR_mass166_5", "START53_V27"],
    ["/TToLeptons_s-channel_mass166_5_8TeV-powheg-tauola/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM", "TToLeptons_s-channel_mass166_5", "START53_V27"],
    ["/TToLeptons_t-channel_mass166_5_8TeV-powheg-tauola/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM", "TToLeptons_t-channel_mass166_5", "START53_V27"],
    ["/TToTlepWhad_tW-channel-DR_mass166_5_8TeV-powheg-tauola/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM", "TToTlepWhad_tW-channel-DR_mass166_5", "START53_V27"],
    ["/TToThadWlep_tW-channel-DR_mass166_5_8TeV-powheg-tauola/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM", "TToThadWlep_tW-channel-DR_mass166_5", "START53_V27"],
    ["/TToDilepton_tW-channel-DR_mass166_5_8TeV-powheg-tauola/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM", "TToDilepton_tW-channel-DR_mass166_5", "START53_V27"],
    ## 178.5
    ["/TBarToLeptons_s-channel_mass178_5_8TeV-powheg-tauola/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM", "TBarToLeptons_s-channel_mass178_5", "START53_V27"],
    ["/TBarToLeptons_t-channel_mass178_5_8TeV-powheg-tauola/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM", "TBarToLeptons_t-channel_mass178_5", "START53_V27"],
    ["/TBarToTlepWhad_tW-channel-DR_mass178_5_8TeV-powheg-tauola/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM", "TBarToTlepWhad_tW-channel-DR_mass178_5", "START53_V27"],
    ["/TBarToThadWlep_tW-channel-DR_mass178_5_8TeV-powheg-tauola/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM", "TBarToThadWlep_tW-channel-DR_mass178_5", "START53_V27"],
    ["/TBarToDilepton_tW-channel-DR_mass178_5_8TeV-powheg-tauola/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM", "TBarToDilepton_tW-channel-DR_mass178_5", "START53_V27"],
    ["/TToLeptons_s-channel_mass178_5_8TeV-powheg-tauola/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM", "TToLeptons_s-channel_mass178_5", "START53_V27"],
    ["/TToLeptons_t-channel_mass178_5_8TeV-powheg-tauola/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM", "TToLeptons_t-channel_mass178_5", "START53_V27"],
    ["/TToTlepWhad_tW-channel-DR_mass178_5_8TeV-powheg-tauola/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM", "TToTlepWhad_tW-channel-DR_mass178_5", "START53_V27"],
    ["/TToThadWlep_tW-channel-DR_mass178_5_8TeV-powheg-tauola/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM", "TToThadWlep_tW-channel-DR_mass178_5", "START53_V27"],
    ["/TToDilepton_tW-channel-DR_mass178_5_8TeV-powheg-tauola/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM", "TToDilepton_tW-channel-DR_mass178_5", "START53_V27"],
    ]

print("Creating configs for crab. Today is %s, you are %s and it's version %d" % (d, user_name, version))
print("")

if not os.path.exists(d):
    os.mkdir(d)

pset_name = "\'patTuple_PF2PAT_MC_cfg.py\'"

for dataset in datasets:

    dataset_path = "\'"+dataset[0]+"\'"
    dataset_name = dataset[1]
    dataset_globaltag = "\'"+dataset[2]+"\'"

    task_name = ("\'MC_PF2PAT_%s\'") % (dataset_name)
    publish_name = "\'%s_%s-v%d\'" % (dataset_name, d, version)
    output_file = "%s/crab_MC_PF2PAT_%s.py" % (d, dataset_name)
    output_dir = ("\'crab_tasks/%s\'") % (d)

    print("\tCreating config file for %s" % (dataset_path))
    print("\t\tName: \'%s\'" % dataset_name)
    print("\t\tGlobal tag: %s" % dataset_globaltag)
    print("\t\tPublishing name: %s" % publish_name)
    print("")

    os.system("sed -e \"s#@datasetname@#%s#\" -e \"s#@taskname@#%s#g\" -e \"s#@outputdir@#%s#g\" -e \"s#@username@#%s#g\" -e \"s#@psetname@#%s#g\" -e \"s#@globaltag@#%s#g\" -e \"s#@publishname@#%s#g\" crab_MC.cfg.template.ipnl > %s" % (dataset_path, task_name, output_dir, user_name, pset_name, dataset_globaltag, publish_name, output_file))
    
    cmd = "crab submit %s" % (output_file)
    if options.run:
        os.system(cmd)

