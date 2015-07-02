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
    #["/TTJets_FullLeptMGDecays_8TeV-madgraph-tauola/Summer12_DR53X-PU_S10_START53_V7C-v2/AODSIM", "TTJets_FullLeptMGDecays", "4"],
    #["/TTJets_SemiLeptMGDecays_8TeV-madgraph-tauola/Summer12_DR53X-PU_S10_START53_V19_ext1-v1/AODSIM", "TTJets_SemiLeptMGDecays", "4"],
    #["/TTJets_HadronicMGDecays_8TeV-madgraph/Summer12_DR53X-PU_S10_START53_V7A_ext-v1/AODSIM", "TTJets_HadronicMGDecays", "5"],
    # W + jets
    #["/WJetsToLNu_TuneZ2Star_8TeV-madgraph-tarball/Summer12_DR53X-PU_S10_START53_V7A-v2/AODSIM", "WJetsToLNu", "8"],
    #["/W1JetsToLNu_TuneZ2Star_8TeV-madgraph/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM", "W1JetsToLNu", "10"],
    #["/W2JetsToLNu_TuneZ2Star_8TeV-madgraph/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM", "W2JetsToLNu", "10"],
    #["/W3JetsToLNu_TuneZ2Star_8TeV-madgraph/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM", "W3JetsToLNu", "10"],
    #["/W4JetsToLNu_TuneZ2Star_8TeV-madgraph/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM", "W4JetsToLNu", "10"],
    # Z + jets
    #["/DYJetsToLL_M-10To50filter_8TeV-madgraph/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM", "DYJetsToLL_M-10To50", "5"],
    #["/DYJetsToLL_M-50_TuneZ2Star_8TeV-madgraph-tarball/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM", "DYJetsToLL_M-50", "5"],
    #["/DY1JetsToLL_M-50_TuneZ2Star_8TeV-madgraph/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM", "DY1JetsToLL_M-50", "7"],
    #["/DY2JetsToLL_M-50_TuneZ2Star_8TeV-madgraph/Summer12_DR53X-PU_S10_START53_V7C-v1/AODSIM", "DY2JetsToLL_M-50", "7"],
    #["/DY3JetsToLL_M-50_TuneZ2Star_8TeV-madgraph/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM", "DY3JetsToLL_M-50", "6"],
    #["/DY4JetsToLL_M-50_TuneZ2Star_8TeV-madgraph/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM", "DY4JetsToLL_M-50", "6"],
    # diboson
    #["/WW_TuneZ2star_8TeV_pythia6_tauola/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM", "WW-incl", "7"],
    #["/WZ_TuneZ2star_8TeV_pythia6_tauola/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM", "WZ-incl", "7"],
    #["/ZZ_TuneZ2star_8TeV_pythia6_tauola/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM", "ZZ-incl", "7"],
    # ttbar other
    #["/TTWJets_8TeV-madgraph/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM", "TTWJets", "7"],
    #["/TTWWJets_8TeV-madgraph/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM", "TTWWJets", "5"],
    #["/TTZJets_8TeV-madgraph_v2/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM", "TTZJets", "7"],
    # single top 
    ## central
    #["/T_s-channel_TuneZ2star_8TeV-powheg-tauola/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM", "T_s-channel", "6"],
    #["/T_t-channel_TuneZ2star_8TeV-powheg-tauola/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM", "T_t-channel", "5"],
    #["/T_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM", "T_tW-channel", "10"],
    #["/Tbar_s-channel_TuneZ2star_8TeV-powheg-tauola/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM", "Tbar_s-channel", "5"],
    #["/Tbar_t-channel_TuneZ2star_8TeV-powheg-tauola/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM", "Tbar_t-channel", "6"],
    #["/Tbar_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM", "Tbar_tW-channel", "10"], 
    ## single top t-chanel, top mass variations
    #["/TToLeptons_t-channel_mass166_5_8TeV-powheg-tauola/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM", "TToLeptons_t-channel_mass166_5", "5"],
    #["/TToLeptons_t-channel_mass169_5_8TeV-powheg-tauola/Summer12_DR53X-PU_S10_START53_V19-v1/AODSIM", "TToLeptons_t-channel_mass169_5", "5"],
    #["/TToLeptons_t-channel_mass171_5_8TeV-powheg-tauola/Summer12_DR53X-PU_S10_START53_V19-v1/AODSIM", "TToLeptons_t-channel_mass171_5", "5"],
    #["/TToLeptons_t-channel_mass173_5_8TeV-powheg-tauola/Summer12_DR53X-PU_S10_START53_V19-v1/AODSIM", "TToLeptons_t-channel_mass173_5", "5"],
    #["/TToLeptons_t-channel_mass175_5_8TeV-powheg-tauola/Summer12_DR53X-PU_S10_START53_V19-v1/AODSIM", "TToLeptons_t-channel_mass175_5", "5"],
    #["/TToLeptons_t-channel_mass178_5_8TeV-powheg-tauola/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM", "TToLeptons_t-channel_mass178_5", "5"],
    #["/TBarToLeptons_t-channel_mass166_5_8TeV-powheg-tauola/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM", "TBarToLeptons_t-channel_mass166_5", "5"],
    #["/TBarToLeptons_t-channel_mass169_5_8TeV-powheg-tauola/Summer12_DR53X-PU_S10_START53_V19-v1/AODSIM", "TBarToLeptons_t-channel_mass169_5", "5"],
    #["/TBarToLeptons_t-channel_mass171_5_8TeV-powheg-tauola/Summer12_DR53X-PU_S10_START53_V19-v1/AODSIM", "TBarToLeptons_t-channel_mass171_5", "5"],
    #["/TBarToLeptons_t-channel_mass173_5_8TeV-powheg-tauola/Summer12_DR53X-PU_S10_START53_V19-v1/AODSIM", "TBarToLeptons_t-channel_mass173_5", "5"],
    #["/TBarToLeptons_t-channel_mass175_5_8TeV-powheg-tauola/Summer12_DR53X-PU_S10_START53_V19-v1/AODSIM", "TBarToLeptons_t-channel_mass175_5", "5"],
    #["/TBarToLeptons_t-channel_mass178_5_8TeV-powheg-tauola/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM", "TBarToLeptons_t-channel_mass178_5", "5"],
    ## 166.5
    #["/TBarToLeptons_s-channel_mass166_5_8TeV-powheg-tauola/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM", "TBarToLeptons_s-channel_mass166_5", "6"],
    #["/TBarToLeptons_t-channel_mass166_5_8TeV-powheg-tauola/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM", "TBarToLeptons_t-channel_mass166_5", "5"],
    #["/TBarToTlepWhad_tW-channel-DR_mass166_5_8TeV-powheg-tauola/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM", "TBarToTlepWhad_tW-channel-DR_mass166_5", "10"],
    #["/TBarToThadWlep_tW-channel-DR_mass166_5_8TeV-powheg-tauola/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM", "TBarToThadWlep_tW-channel-DR_mass166_5", "10"],
    #["/TBarToDilepton_tW-channel-DR_mass166_5_8TeV-powheg-tauola/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM", "TBarToDilepton_tW-channel-DR_mass166_5", "10"],
    #["/TToLeptons_s-channel_mass166_5_8TeV-powheg-tauola/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM", "TToLeptons_s-channel_mass166_5", "6"],
    #["/TToLeptons_t-channel_mass166_5_8TeV-powheg-tauola/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM", "TToLeptons_t-channel_mass166_5", "5"],
    #["/TToTlepWhad_tW-channel-DR_mass166_5_8TeV-powheg-tauola/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM", "TToTlepWhad_tW-channel-DR_mass166_5", "10"],
    #["/TToThadWlep_tW-channel-DR_mass166_5_8TeV-powheg-tauola/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM", "TToThadWlep_tW-channel-DR_mass166_5", "10"],
    #["/TToDilepton_tW-channel-DR_mass166_5_8TeV-powheg-tauola/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM", "TToDilepton_tW-channel-DR_mass166_5", "10"],
    ## 178.5
    #["/TBarToLeptons_s-channel_mass178_5_8TeV-powheg-tauola/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM", "TBarToLeptons_s-channel_mass178_5", "6"],
    #["/TBarToLeptons_t-channel_mass178_5_8TeV-powheg-tauola/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM", "TBarToLeptons_t-channel_mass178_5", "5"],
    #["/TBarToTlepWhad_tW-channel-DR_mass178_5_8TeV-powheg-tauola/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM", "TBarToTlepWhad_tW-channel-DR_mass178_5", "10"],
    #["/TBarToThadWlep_tW-channel-DR_mass178_5_8TeV-powheg-tauola/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM", "TBarToThadWlep_tW-channel-DR_mass178_5", "10"],
    #["/TBarToDilepton_tW-channel-DR_mass178_5_8TeV-powheg-tauola/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM", "TBarToDilepton_tW-channel-DR_mass178_5", "10"],
    #["/TToLeptons_s-channel_mass178_5_8TeV-powheg-tauola/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM", "TToLeptons_s-channel_mass178_5", "6"],
    #["/TToLeptons_t-channel_mass178_5_8TeV-powheg-tauola/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM", "TToLeptons_t-channel_mass178_5", "5"],
    #["/TToTlepWhad_tW-channel-DR_mass178_5_8TeV-powheg-tauola/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM", "TToTlepWhad_tW-channel-DR_mass178_5", "10"],
    #["/TToThadWlep_tW-channel-DR_mass178_5_8TeV-powheg-tauola/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM", "TToThadWlep_tW-channel-DR_mass178_5", "10"],
    #["/TToDilepton_tW-channel-DR_mass178_5_8TeV-powheg-tauola/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM", "TToDilepton_tW-channel-DR_mass178_5", "10"],
    #Jpsi ttbar samples
    #["/TTJets_MSDecays_JpsiFilter_1665_TuneZ2star_8TeV-madgraph-tauola/Summer12DR53X-PU_S10_START53_V19-v1/AODSIM", "TTJets_MSDecays_JpsiFilter_1665", "4"],
    #["/TTJets_MSDecays_JpsiFilter_1695_TuneZ2star_8TeV-madgraph-tauola/Summer12DR53X-PU_S10_START53_V19-v2/AODSIM", "TTJets_MSDecays_JpsiFilter_1695", "4"],
    #["/TTJets_MSDecays_JpsiFilter_1715_TuneZ2star_8TeV-madgraph-tauola/Summer12DR53X-PU_S10_START53_V19-v2/AODSIM", "TTJets_MSDecays_JpsiFilter_1715", "4"],
    #["/TTJets_MSDecays_JpsiFilter_central_TuneZ2star_8TeV-madgraph-tauola/Summer12DR53X-PU_S10_START53_V19-v2/AODSIM", "TTJets_MSDecays_JpsiFilter_1725", "4"],
    #["/TTJets_MSDecays_JpsiFilter_1735_TuneZ2star_8TeV-madgraph-tauola/Summer12DR53X-PU_S10_START53_V19-v1/AODSIM", "TTJets_MSDecays_JpsiFilter_1735", "4"],
    #["/TTJets_MSDecays_JpsiFilter_1755_TuneZ2star_8TeV-madgraph-tauola/Summer12DR53X-PU_S10_START53_V19-v2/AODSIM", "TTJets_MSDecays_JpsiFilter_1755", "4"],
    #["/TTJets_MSDecays_JpsiFilter_1785_TuneZ2star_8TeV-madgraph-tauola/Summer12DR53X-PU_S10_START53_V19-v1/AODSIM", "TTJets_MSDecays_JpsiFilter_1785", "4"],
    #["/TTJets_MSDecays_JpsiFilter_matchingdown_TuneZ2star_8TeV-madgraph-tauola/Summer12DR53X-PU_S10_START53_V19-v1/AODSIM", "TTJets_MSDecays_JpsiFilter_matchingdown", "4"],
    #["/TTJets_MSDecays_JpsiFilter_matchingup_TuneZ2star_8TeV-madgraph-tauola/Summer12DR53X-PU_S10_START53_V19-v2/AODSIM", "TTJets_MSDecays_JpsiFilter_matchingup", "4"],
    #["/TTJets_MSDecays_JpsiFilter_scaledown_TuneZ2star_8TeV-madgraph-tauola/Summer12DR53X-PU_S10_START53_V19-v1/AODSIM", "TTJets_MSDecays_JpsiFilter_scaledown", "4"],
    #["/TTJets_MSDecays_JpsiFilter_scaleup_TuneZ2star_8TeV-madgraph-tauola/Summer12DR53X-PU_S10_START53_V19-v2/AODSIM", "TTJets_MSDecays_JpsiFilter_scaleup", "4"],
    # P11 ttbar
    ## central tune
    #["/TTJets_FullLeptMGDecays_TuneP11_8TeV-madgraph-tauola/Summer12_DR53X-PU_S10_START53_V19-v1/AODSIM", "TTJets_FullLeptMGDecays_TuneP11", "4"],
    #["/TTJets_SemiLeptMGDecays_TuneP11_8TeV-madgraph-tauola/Summer12_DR53X-PU_S10_START53_V19-v1/AODSIM", "TTJets_SemiLeptMGDecays_TuneP11", "4"],
    ["/TTJets_HadronicMGDecays_TuneP11_8TeV-madgraph-tauola/Summer12_DR53X-PU_S10_START53_V19-v1/AODSIM", "TTJets_HadronicMGDecays_TuneP11", "5"],
    ## mpiHi tune
    #["/TTJets_FullLeptMGDecays_TuneP11mpiHi_8TeV-madgraph-tauola/Summer12_DR53X-PU_S10_START53_V19-v1/AODSIM", "TTJets_FullLeptMGDecays_TuneP11mpiHi", "4"],
    #["/TTJets_SemiLeptMGDecays_TuneP11mpiHi_8TeV-madgraph-tauola/Summer12_DR53X-PU_S10_START53_V19-v1/AODSIM", "TTJets_SemiLeptMGDecays_TuneP11mpiHi", "4"],
    ["/TTJets_HadronicMGDecays_TuneP11mpiHi_8TeV-madgraph-tauola/Summer12_DR53X-PU_S10_START53_V19-v1/AODSIM", "TTJets_HadronicMGDecays_TuneP11mpiHi", "5"],
    ## Tevatron tune
    #["/TTJets_FullLeptMGDecays_TuneP11TeV_8TeV-madgraph-tauola/Summer12_DR53X-PU_S10_START53_V19-v1/AODSIM", "TTJets_FullLeptMGDecays_TuneP11TeV", "4"],
    #["/TTJets_SemiLeptMGDecays_TuneP11TeV_8TeV-madgraph-tauola/Summer12_DR53X-PU_S10_START53_V19-v1/AODSIM", "TTJets_SemiLeptMGDecays_TuneP11TeV", "4"],
    ["/TTJets_HadronicMGDecays_TuneP11TeV_8TeV-madgraph-tauola/Summer12_DR53X-PU_S10_START53_V19-v1/AODSIM", "TTJets_HadronicMGDecays_TuneP11TeV", "5"],
    ## noCR tune
    #["/TTJets_FullLeptMGDecays_TuneP11noCR_8TeV-madgraph-tauola/Summer12_DR53X-PU_S10_START53_V19-v1/AODSIM", "TTJets_FullLeptMGDecays_TuneP11noCR", "4"],
    #["/TTJets_SemiLeptMGDecays_TuneP11noCR_8TeV-madgraph-tauola/Summer12_DR53X-PU_S10_START53_V19-v1/AODSIM", "TTJets_SemiLeptMGDecays_TuneP11noCR", "4"],
    ["/TTJets_HadronicMGDecays_TuneP11noCR_8TeV-madgraph-tauola/Summer12_DR53X-PU_S10_START53_V19-v1/AODSIM", "TTJets_HadronicMGDecays_TuneP11noCR", "5"],
    # POWHEG ttbar
    #["/TT_CT10_TuneZ2star_8TeV-powheg-tauola/Summer12_DR53X-PU_S10_START53_V7A-v2/AODSIM", "TTJets_Powheg", "4"],
    # MC@NLO
    #["/TT_8TeV-mcatnlo/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM", "TTJets_MCatNLO", "4"]
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

