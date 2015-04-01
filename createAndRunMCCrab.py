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
    ["/TTJets_FullLeptMGDecays_8TeV-madgraph-tauola/Summer12_DR53X-PU_S10_START53_V7C-v2/AODSIM", "TTJets_FullLeptMGDecays", "4"],
    ["/TTJets_SemiLeptMGDecays_8TeV-madgraph-tauola/Summer12_DR53X-PU_S10_START53_V19_ext1-v1/AODSIM", "TTJets_SemiLeptMGDecays", "4"],
    ["/TTJets_HadronicMGDecays_8TeV-madgraph/Summer12_DR53X-PU_S10_START53_V7A_ext-v1/AODSIM", "TTJets_HadronicMGDecays", "25"],
    # W + jets
    #["/WJetsToLNu_TuneZ2Star_8TeV-madgraph-tarball/Summer12_DR53X-PU_S10_START53_V7A-v2/AODSIM", "WJetsToLNu", "FIXME"],
    ["/W1JetsToLNu_TuneZ2Star_8TeV-madgraph/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM", "W1JetsToLNu", "10"],
    ["/W2JetsToLNu_TuneZ2Star_8TeV-madgraph/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM", "W2JetsToLNu", "10"],
    ["/W3JetsToLNu_TuneZ2Star_8TeV-madgraph/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM", "W3JetsToLNu", "10"],
    ["/W4JetsToLNu_TuneZ2Star_8TeV-madgraph/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM", "W4JetsToLNu", "10"],
    # Z + jets
    #["/DYJetsToLL_M-10To50filter_8TeV-madgraph/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM", "DYJetsToLL_M-10To50", "FIXME"],
    #["/DYJetsToLL_M-50_TuneZ2Star_8TeV-madgraph-tarball/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM", "DYJetsToLL_M-50", "FIXME"],
    ["/DY1JetsToLL_M-50_TuneZ2Star_8TeV-madgraph/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM", "DY1JetsToLL_M-50", "7"],
    ["/DY2JetsToLL_M-50_TuneZ2Star_8TeV-madgraph/Summer12_DR53X-PU_S10_START53_V7C-v1/AODSIM", "DY2JetsToLL_M-50", "7"],
    ["/DY3JetsToLL_M-50_TuneZ2Star_8TeV-madgraph/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM", "DY3JetsToLL_M-50", "6"],
    ["/DY4JetsToLL_M-50_TuneZ2Star_8TeV-madgraph/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM", "DY4JetsToLL_M-50", "6"],
    # diboson
    ["/WW_TuneZ2star_8TeV_pythia6_tauola/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM", "WW-incl", "15"],
    ["/WZ_TuneZ2star_8TeV_pythia6_tauola/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM", "WZ-incl", "22"],
    ["/ZZ_TuneZ2star_8TeV_pythia6_tauola/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM", "ZZ-incl", "25"],
    # ttbar other
    ["/TTWJets_8TeV-madgraph/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM", "TTWJets", "11"],
    ["/TTWWJets_8TeV-madgraph/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM", "TTWWJets", "5"],
    ["/TTZJets_8TeV-madgraph_v2/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM", "TTZJets", "11"],
    # single top 
    ## central
    ["/T_s-channel_TuneZ2star_8TeV-powheg-tauola/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM", "T_s-channel", "22"],
    ["/T_t-channel_TuneZ2star_8TeV-powheg-tauola/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM", "T_t-channel", "20"],
    ["/T_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM", "T_tW-channel", "10"],
    ["/Tbar_s-channel_TuneZ2star_8TeV-powheg-tauola/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM", "Tbar_s-channel", "22"],
    ["/Tbar_t-channel_TuneZ2star_8TeV-powheg-tauola/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM", "Tbar_t-channel", "20"],
    ["/Tbar_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM", "Tbar_tW-channel", "10"], 
    ## single top t-chanel, top mass variations
    ["/TToLeptons_t-channel_mass166_5_8TeV-powheg-tauola/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM", "TToLeptons_t-channel_mass166_5", "20"],
    ["/TToLeptons_t-channel_mass169_5_8TeV-powheg-tauola/Summer12_DR53X-PU_S10_START53_V19-v1/AODSIM", "TToLeptons_t-channel_mass169_5", "20"],
    ["/TToLeptons_t-channel_mass171_5_8TeV-powheg-tauola/Summer12_DR53X-PU_S10_START53_V19-v1/AODSIM", "TToLeptons_t-channel_mass171_5", "20"],
    ["/TToLeptons_t-channel_mass173_5_8TeV-powheg-tauola/Summer12_DR53X-PU_S10_START53_V19-v1/AODSIM", "TToLeptons_t-channel_mass173_5", "20"],
    ["/TToLeptons_t-channel_mass175_5_8TeV-powheg-tauola/Summer12_DR53X-PU_S10_START53_V19-v1/AODSIM", "TToLeptons_t-channel_mass175_5", "20"],
    ["/TToLeptons_t-channel_mass178_5_8TeV-powheg-tauola/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM", "TToLeptons_t-channel_mass178_5", "20"],
    ["/TBarToLeptons_t-channel_mass166_5_8TeV-powheg-tauola/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM", "TBarToLeptons_t-channel_mass166_5", "20"],
    ["/TBarToLeptons_t-channel_mass169_5_8TeV-powheg-tauola/Summer12_DR53X-PU_S10_START53_V19-v1/AODSIM", "TBarToLeptons_t-channel_mass169_5", "20"],
    ["/TBarToLeptons_t-channel_mass171_5_8TeV-powheg-tauola/Summer12_DR53X-PU_S10_START53_V19-v1/AODSIM", "TBarToLeptons_t-channel_mass171_5", "20"],
    ["/TBarToLeptons_t-channel_mass173_5_8TeV-powheg-tauola/Summer12_DR53X-PU_S10_START53_V19-v1/AODSIM", "TBarToLeptons_t-channel_mass173_5", "20"],
    ["/TBarToLeptons_t-channel_mass175_5_8TeV-powheg-tauola/Summer12_DR53X-PU_S10_START53_V19-v1/AODSIM", "TBarToLeptons_t-channel_mass175_5", "20"],
    ["/TBarToLeptons_t-channel_mass178_5_8TeV-powheg-tauola/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM", "TBarToLeptons_t-channel_mass178_5", "20"],
    ## 166.5
    ["/TBarToLeptons_s-channel_mass166_5_8TeV-powheg-tauola/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM", "TBarToLeptons_s-channel_mass166_5", "22"],
    ["/TBarToLeptons_t-channel_mass166_5_8TeV-powheg-tauola/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM", "TBarToLeptons_t-channel_mass166_5", "20"],
    ["/TBarToTlepWhad_tW-channel-DR_mass166_5_8TeV-powheg-tauola/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM", "TBarToTlepWhad_tW-channel-DR_mass166_5", "10"],
    ["/TBarToThadWlep_tW-channel-DR_mass166_5_8TeV-powheg-tauola/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM", "TBarToThadWlep_tW-channel-DR_mass166_5", "10"],
    ["/TBarToDilepton_tW-channel-DR_mass166_5_8TeV-powheg-tauola/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM", "TBarToDilepton_tW-channel-DR_mass166_5", "10"],
    ["/TToLeptons_s-channel_mass166_5_8TeV-powheg-tauola/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM", "TToLeptons_s-channel_mass166_5", "22"],
    ["/TToLeptons_t-channel_mass166_5_8TeV-powheg-tauola/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM", "TToLeptons_t-channel_mass166_5", "20"],
    ["/TToTlepWhad_tW-channel-DR_mass166_5_8TeV-powheg-tauola/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM", "TToTlepWhad_tW-channel-DR_mass166_5", "10"],
    ["/TToThadWlep_tW-channel-DR_mass166_5_8TeV-powheg-tauola/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM", "TToThadWlep_tW-channel-DR_mass166_5", "10"],
    ["/TToDilepton_tW-channel-DR_mass166_5_8TeV-powheg-tauola/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM", "TToDilepton_tW-channel-DR_mass166_5", "10"],
    ## 178.5
    ["/TBarToLeptons_s-channel_mass178_5_8TeV-powheg-tauola/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM", "TBarToLeptons_s-channel_mass178_5", "22"],
    ["/TBarToLeptons_t-channel_mass178_5_8TeV-powheg-tauola/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM", "TBarToLeptons_t-channel_mass178_5", "20"],
    ["/TBarToTlepWhad_tW-channel-DR_mass178_5_8TeV-powheg-tauola/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM", "TBarToTlepWhad_tW-channel-DR_mass178_5", "10"],
    ["/TBarToThadWlep_tW-channel-DR_mass178_5_8TeV-powheg-tauola/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM", "TBarToThadWlep_tW-channel-DR_mass178_5", "10"],
    ["/TBarToDilepton_tW-channel-DR_mass178_5_8TeV-powheg-tauola/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM", "TBarToDilepton_tW-channel-DR_mass178_5", "10"],
    ["/TToLeptons_s-channel_mass178_5_8TeV-powheg-tauola/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM", "TToLeptons_s-channel_mass178_5", "22"],
    ["/TToLeptons_t-channel_mass178_5_8TeV-powheg-tauola/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM", "TToLeptons_t-channel_mass178_5", "20"],
    ["/TToTlepWhad_tW-channel-DR_mass178_5_8TeV-powheg-tauola/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM", "TToTlepWhad_tW-channel-DR_mass178_5", "10"],
    ["/TToThadWlep_tW-channel-DR_mass178_5_8TeV-powheg-tauola/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM", "TToThadWlep_tW-channel-DR_mass178_5", "10"],
    ["/TToDilepton_tW-channel-DR_mass178_5_8TeV-powheg-tauola/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM", "TToDilepton_tW-channel-DR_mass178_5", "10"],
    ]

print("Creating configs for crab. Today is %s, you are %s and it's version %d" % (d, user_name, version))
print("")

if not os.path.exists(d):
    os.mkdir(d)

pset_name = "\'patTuple_PF2PAT_MC_cfg.py\'"

for dataset in datasets:

    dataset_path = "\'"+dataset[0]+"\'"
    dataset_name = dataset[1]
    dataset_quanta = dataset[2]

    task_name = ("\'MC_PF2PAT_%s\'") % (dataset_name)
    publish_name = "\'%s_%s-v%d\'" % (dataset_name, d, version)
    output_file = "%s/crab_MC_PF2PAT_%s.py" % (d, dataset_name)
    output_dir = ("\'crab_tasks/%s\'") % (d)

    print("\tCreating config file for %s" % (dataset_path))
    print("\t\tName: \'%s\'" % dataset_name)
    print("\t\tPublishing name: %s" % publish_name)
    print("")

    os.system("sed -e \"s#@datasetname@#%s#\" -e \"s#@taskname@#%s#g\" -e \"s#@outputdir@#%s#g\" -e \"s#@username@#%s#g\" -e \"s#@psetname@#%s#g\" -e \"s#@publishname@#%s#g\" -e \"s#@datasetquanta@#%s#g\" crab_MC.cfg.template.ipnl > %s" % (dataset_path, task_name, output_dir, user_name, pset_name, publish_name, dataset_quanta, output_file))
    
    cmd = "crab submit %s" % (output_file)
    if options.run:
        os.system(cmd)

