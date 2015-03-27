How-to use PatTopFilteredProduction
===========================

This is a PAT configuration adapted for Top analysis, skimming events with an isolated electron/muon, 2 jets, and a non isolated muon.

## Instructions

### Step 1 - Setup dependencies

Follow the [dependencies][1] instructions, handling carefully merging conflicts.

### Step 2 - Install the PatTopFilteredProduction package

Be sure to be in the `src` directory of the CMSSW release.

    git clone https://github.com/IPNL-CMS/PatTopFilteredProduction.git

### Step 3 - Post-installation instructions

Follow the [post-installation][2] instructions.

### Step 4 - Build

In the `src` directory of the CMSSW package, run

    scram b -j8

  [1]: https://github.com/IPNL-CMS/PatTopFilteredProduction/DEPENDENCIES.md
  [2]: https://github.com/IPNL-CMS/PatTopFilteredProduction/POST_INSTALL.md


# How-to use and run Pat

Once Pat has been setup, you can start using the tool as indicated below.

## Specify the datasets you want to run on

Do not forget to source Crab3 (i.e. /cvmfs/cms.cern.ch/crab3/crab.sh)

**For MC:**

List the datasets and [globalTags](https://twiki.cern.ch/twiki/bin/view/CMSPublic/SWGuideFrontierConditions#Winter13_2012_A_B_C_D_datasets_r) in createAndRunMCCrab.py. Adapt the number of events per job in crab_MC.cfg.template.ipnl.

**For data:**

List the primary dataset, the [globalTag](https://twiki.cern.ch/twiki/bin/view/CMSPublic/SWGuideFrontierConditions#Winter13_2012_A_B_C_D_datasets_r), the [run range](https://twiki.cern.ch/twiki/bin/view/CMS/PdmV2012Analysis) in createAndRunDataCrab.py, and the [golden Json file](https://twiki.cern.ch/twiki/bin/viewauth/CMS/PdmV2012Analysis#Analysis_using_the_Golden_JSON_f). Adapt the number of lumi sections per job in crab_data.cfg.template.ipnl.

## Run your code with crab

Create your crab configuration files `.cfg` and submit your jobs by running the following command:

**for MC:**
```bash
PatTopFilteredProduction> ./createAndRunMCCrab.py --run
```

**for data:**
```bash
PatTopFilteredProduction> ./createAndRunDataCrab.py --run
```

## Once your crab jobs are done

You can use getReportPublishPurge.py to handle the your crab tasks.

### Especially for MC

You can compute the real number of processed events (which can be different from the number of generated AOD events or the number of events at the end of Pat obtained by the `crab -publish` command) using the following command:
```bash
PatTopFilteredProduction> curl -o crabNumberOfProcessedEvents.py https://raw.github.com/blinkseb/cms-utilities/master/crabNumberOfProcessedEvents.py
PatTopFilteredProduction> crabNumberOfProcessedEvents.py myWorkingDir
```


### Especially for data

**Luminosity**

You can compute the equivalent luminosity following these [instructions](https://twiki.cern.ch/twiki/bin/viewauth/CMS/LumiCalc). First, you have to generate your `/res/lumiSummary.json` file:
```bash
PatTopFilteredProduction> crab -report -c myWorkingDir
```
Then compute the luminosity:
```bash
PatTopFilteredProduction> pixelLumiCalc.py -i /<path>/myWorkingDir/res/lumiSummary.json overview
```


***

**Remark**:

Finally, you can merge all the `json` files thus obtained using the `mergeJSON.py` script:

_Usage: mergeJSON.py alpha1.json [alpha2.json:142300-145900]_

_Options:_

_-h, --help show this help message and exit_

_--output=OUTPUT Save output to file OUTPUT_

For example: 
```bash
PatTopFilteredProduction> mergedJSON.py myWorkingDir1/res/lumiSummary.json myWorkingDir2/res/lumiSummary.json
```

You can then use the merged json file to compute the prescale factor of a given HLT trigger. For example, if you are interested in HLT_PFJet200 trigger, execute this command:
```bash
PatTopFilteredProduction> pixelLumiCalc.py recorded -i mergedLumiSummaryData.json --hltpath "HLT_PFJet200_*"
```

***

**Pileup profile**

You can get the pileup profile from the data PAttuples as follows:
```bash
PatTopFilteredProduction> curl -O https://cms-service-dqm.web.cern.ch/cms-service-dqm/CAF/certification/Collisions12/8TeV/PileUp/pileup_latest.txt  
PatTopFilteredProduction> pileupCalc.py -i myWorkingDir1/res/lumiSummary.json --inputLumiJSON pileup_latest.txt --calcMode true --minBiasXsec 69400 --maxPileupBin 80 --numPileupBins 80 MyDataPileupHistogram_1.root
```
If you have several datasets, repeat the command for the over working directories and merge all the final histogramms:
```bash
PatTopFilteredProduction> hadd MyFinalDataPileupHistogram MyDataPileupHistogram_1.root MyDataPileupHistogram_2.root
```

