#! /usr/bin/env python

import os, copy, datetime, pwd, re

from optparse import OptionParser
parser = OptionParser()
parser.add_option("", "--run", action="store_true", dest="run", default=False, help="run crab")
(options, args) = parser.parse_args()

global_json = "Cert_190456-208686_8TeV_22Jan2013ReReco_Collisions12_JSON.txt"

# Load each json files and build dataset array
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
    ["/MuHad/Run2012A-22Jan2013-v1/AOD", "MuHad_Run2012A-22Jan2013","Cert_190456-208686_8TeV_22Jan2013ReReco_Collisions12_JSON.txt", "100",[190456, 193621]],
    ["/ElectronHad/Run2012A-22Jan2013-v1/AOD", "ElectronHad_Run2012A-22Jan2013","Cert_190456-208686_8TeV_22Jan2013ReReco_Collisions12_JSON.txt", "100",[190456, 193621]],
    #["/SingleMu/Run2012A-22Jan2013-v1/AOD", "SingleMu_Run2012A-22Jan2013","Cert_190456-208686_8TeV_22Jan2013ReReco_Collisions12_JSON.txt", "100",[190456, 193621]],
    #["/SingleElectron/Run2012A-22Jan2013-v1/AOD", "SingleElectron_Run2012A-22Jan2013","Cert_190456-208686_8TeV_22Jan2013ReReco_Collisions12_JSON.txt", "100",[190456, 193621]],
    ["/SingleMu/Run2012B-22Jan2013-v1/AOD", "SingleMu_Run2012B-22Jan2013", "Cert_190456-208686_8TeV_22Jan2013ReReco_Collisions12_JSON.txt", "100",[193833, 196531]],
    ["/SingleElectron/Run2012B-22Jan2013-v1/AOD", "SingleElectron_Run2012B-22Jan2013", "Cert_190456-208686_8TeV_22Jan2013ReReco_Collisions12_JSON.txt", "100",[193833, 196531]],
    ["/SingleMu/Run2012C-22Jan2013-v1/AOD", "SingleMu_Run2012C-22Jan2013", "Cert_190456-208686_8TeV_22Jan2013ReReco_Collisions12_JSON.txt", "100",[198022, 203742]],
    ["/SingleElectron/Run2012C-22Jan2013-v1/AOD", "SingleElectron_Run2012C-22Jan2013", "Cert_190456-208686_8TeV_22Jan2013ReReco_Collisions12_JSON.txt", "100",[198022, 203742]],
    ["/SingleMu/Run2012D-22Jan2013-v1/AOD","SingleMu_Run2012D-22Jan2013", "Cert_190456-208686_8TeV_22Jan2013ReReco_Collisions12_JSON.txt", "100", [203777, 208686]],
    ["/SingleElectron/Run2012D-22Jan2013-v1/AOD","SingleElectron_Run2012D-22Jan2013", "Cert_190456-208686_8TeV_22Jan2013ReReco_Collisions12_JSON.txt", "100", [203777, 208686]]
    ]

print("Creating configs for crab. Today is %s, you are %s and it's version %d" % (d, user_name, version))
print("")

if not os.path.exists(d):
    os.mkdir(d)

pset_name = "\'patTuple_PF2PAT_data_cfg.py\'"

for dataset in datasets:

    dataset_path = "\'"+dataset[0]+"\'"
    dataset_name = dataset[1]
    dataset_json = "\'"+dataset[2]+"\'"
    if len(dataset_json) == 0:
        dataset_json = global_json
    dataset_quanta = dataset[3]

    runselection = ""
    if len(dataset) > 4 and len(dataset[4]) == 2:
        runselection = "%d-%d" % (dataset[4][0], dataset[4][1])

    task_name = ("\'Data_PF2PAT_%s\'") % (dataset_name)
    publish_name = "\'%s_%s-v%d\'" % (dataset_name, d, version)
    output_file = "%s/crab_Data_PF2PAT_%s.py" % (d, dataset_name)
    output_dir = ("\'crab_tasks/%s\'") % (d)

    print("\tCreating config file for %s" % (dataset_path))
    print("\t\tName: \'%s\'" % dataset_name)
    print("\t\tJSON: %s" % dataset_json)
    print("\t\tRun selection: %s" % runselection)
    print("\t\tPublishing name: %s" % publish_name)
    print("")

    os.system("sed -e \"s#@datasetname@#%s#g\" -e \"s#@taskname@#%s#g\" -e \"s#@outputdir@#%s#g\" -e \"s#@username@#%s#g\" -e \"s#@psetname@#%s#g\" -e \"s#@datasetquanta@#%s#g\" -e \"s#@jsonfile@#%s#g\" -e \"s#@publishname@#%s#g\" crab_data.cfg.template.ipnl > %s" % (dataset_path, task_name, output_dir, user_name, pset_name, dataset_quanta, dataset_json, publish_name, output_file))

    cmd = "crab submit %s" % (output_file)
    if options.run:
        os.system(cmd)
