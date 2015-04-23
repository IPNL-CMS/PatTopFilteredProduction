#!/usr/bin/env python

import os

from optparse import OptionParser
parser = OptionParser()
parser.add_option("-d", "--date", dest="date", type="string", default=False, help="date when crab tasks were created")
(options, args) = parser.parse_args()

if not options.date or not os.path.isdir(os.path.join("crab_tasks", options.date)):
    parser.error("you must specify a valid date")
dir = os.path.join("crab_tasks", options.date)
dir = os.path.join(dir, "LumiAndPU")
if not os.path.isdir(dir):
    os.mkdir(dir)

#Json files
dirJson = os.path.join(dir, "JsonFiles")
if not os.path.isdir(dirJson):
    raise Exception("you need json files")
jsonFiles = [name for name in os.listdir(dirJson) if name.endswith(".json")]

# PU profiles
dirPU = os.path.join(dir, "PUProfiles")
if not os.path.isdir(dirPU):
    os.mkdir(dirPU)
hadd = "hadd "+os.path.join(dirPU, "MyDataPileupHistogram.root ")
hadd_up = "hadd "+os.path.join(dirPU, "MyDataPileupHistogram_PUup.root ")
hadd_down = "hadd "+os.path.join(dirPU, "MyDataPileupHistogram_PUdown.root ")
for jsonFile in jsonFiles:
    print "Generating PU profiles for "+jsonFile[12:-5]
    puFile = "MyDataPileupHistogram_"+jsonFile[12:-5]+".root"
    hadd += os.path.join(dirPU, puFile)+" "
    cmd = "pileupCalc.py -i "+os.path.join(dirJson, jsonFile)+" --inputLumiJSON pileup_latest.txt --calcMode true --minBiasXsec 69400 --maxPileupBin 80 --numPileupBins 80 "+os.path.join(dirPU, puFile)
    os.system(cmd)
    puFile_up = "MyDataPileupHistogram_"+jsonFile[12:-5]+"_PUup.root"
    hadd_up += os.path.join(dirPU, puFile_up)+" "
    cmd_up = "pileupCalc.py -i "+os.path.join(dirJson, jsonFile)+" --inputLumiJSON pileup_latest.txt --calcMode true --minBiasXsec 72865 --maxPileupBin 80 --numPileupBins 80 "+os.path.join(dirPU, puFile_up)
    os.system(cmd_up)
    puFile_down = "MyDataPileupHistogram_"+jsonFile[12:-5]+"_PUdown.root"
    hadd_down += os.path.join(dirPU, puFile_down)+" "
    cmd_down = "pileupCalc.py -i "+os.path.join(dirJson, jsonFile)+" --inputLumiJSON pileup_latest.txt --calcMode true --minBiasXsec 65935 --maxPileupBin 80 --numPileupBins 80 "+os.path.join(dirPU, puFile_down)
    os.system(cmd_down)
os.system(hadd)    
print "-> Overall PU profile has been generated"
os.system(hadd_up)    
print "-> Overall PU up profile has been generated"
os.system(hadd_down)    
print "-> Overall PU down profile has been generated\n"

# Lumi for all paths
dirAll = os.path.join(dir, "LumiAllPaths") 
if not os.path.isdir(dirAll):
    os.mkdir(dirAll)
for jsonFile in jsonFiles:
    print "Computing lumi for "+jsonFile[12:-5]
    lumiFile = "pixelLumiCalc"+jsonFile[12:-5]+".log"
    cmd = "pixelLumiCalc.py -i "+os.path.join(dirJson, jsonFile)+" overview >& "+os.path.join(dirAll, lumiFile)
    os.system(cmd)
print ""

# Lummi for isolated lepton paths
dirIsoLep = os.path.join(dir, "LumiIsoLepPaths")
if not os.path.isdir(dirIsoLep):
    os.mkdir(dirIsoLep)
pathIsoMu = "HLT_IsoMu24_eta2p1*"
pathIsoEl = "HLT_Ele27_WP80*"
for jsonFile in jsonFiles:
    print "Computing lumi for "+jsonFile[12:-5]+" for isolated lepton paths"
    lumiFile = "pixelLumiCalc"+jsonFile[12:-5]+".log"
    cmd = "pixelLumiCalc.py -i "+os.path.join(dirJson, jsonFile)+" --hlt "
    if jsonFile.count("Mu"):
        cmd += pathIsoMu+" recorded >& "+os.path.join(dirIsoLep, lumiFile)
    if jsonFile.count("Electron"):
        cmd += pathIsoEl+" recorded >& "+os.path.join(dirIsoLep, lumiFile)
    os.system(cmd)
print ""

# Lumi for lepton+jets paths
dirLepJets = os.path.join(dir, "LumiLepJetsPaths")
if not os.path.isdir(dirLepJets):
    os.mkdir(dirLepJets)
pathMuJets = "HLT_IsoMu24_eta2p1*"
pathElJets = "HLT_Ele27_WP80*"
for jsonFile in jsonFiles:
    print "Computing lumi for "+jsonFile[12:-5]+" for lepton+jets paths"
    lumiFile = "pixelLumiCalc"+jsonFile[12:-5]+".log"
    cmd = "pixelLumiCalc.py -i "+os.path.join(dirJson, jsonFile)+" --hlt "
    if jsonFile.count("Mu"):
        cmd += pathMuJets+" recorded >& "+os.path.join(dirLepJets, lumiFile)
    if jsonFile.count("Electron"):
        cmd += pathElJets+" recorded >& "+os.path.join(dirLepJets, lumiFile)
    os.system(cmd)

