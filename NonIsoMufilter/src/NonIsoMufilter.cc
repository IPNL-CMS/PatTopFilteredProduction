// -*- C++ -*-
//
// Package:    NonIsoMufilter
// Class:      NonIsoMufilter
// 
/**\class NonIsoMufilter NonIsoMufilter.cc EBouvier/NonIsoMufilter/src/NonIsoMufilter.cc

Description: EDFilter to select non iso mu

Implementation:
inspect PFs from patJets
*/
//
// Original Author:  Elvire BOUVIER
//         Created:  Tue Mar 17 14:53:10 CET 2015
// $Id$
//
//


// system include files
#include <memory>

// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDFilter.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Framework/interface/ESHandle.h"
#include "FWCore/MessageLogger/interface/MessageLogger.h"

#include "DataFormats/ParticleFlowCandidate/interface/PFCandidate.h"
#include "DataFormats/ParticleFlowCandidate/interface/PFCandidateFwd.h"
#include "DataFormats/PatCandidates/interface/Jet.h"

/* C++ Headers */
using namespace std;
using namespace edm;

//
// class declaration
//

class NonIsoMufilter : public edm::EDFilter {
  public:
    explicit NonIsoMufilter(const edm::ParameterSet&);
    ~NonIsoMufilter();

    static void fillDescriptions(edm::ConfigurationDescriptions& descriptions);

  private:
    virtual void beginJob() ;
    virtual bool filter(edm::Event&, const edm::EventSetup&);
    virtual void endJob() ;

    virtual bool beginRun(edm::Run&, edm::EventSetup const&);
    virtual bool endRun(edm::Run&, edm::EventSetup const&);
    virtual bool beginLuminosityBlock(edm::LuminosityBlock&, edm::EventSetup const&);
    virtual bool endLuminosityBlock(edm::LuminosityBlock&, edm::EventSetup const&);

    // ----------member data ---------------------------
    std::string thePFLabel; // label of pf particles
    double theMinPt;    // minimum pt required 

    long int ntotevt;
    long int nselevt;

};

//
// constants, enums and typedefs
//

//
// static data member definitions
//

//
// constructors and destructor
//
NonIsoMufilter::NonIsoMufilter(const edm::ParameterSet& iConfig)
{
  //now do what ever initialization is needed
  thePFLabel = iConfig.getParameter<std::string>("src");

  theMinPt  = iConfig.getParameter<double>("minPt"); // pt min (GeV/c)

  LogDebug("NonIsoMufilter") << " PFLabel  : " << thePFLabel 
    << " MinPt    : " << theMinPt;
  ntotevt = 0;
  nselevt = 0;

}


NonIsoMufilter::~NonIsoMufilter()
{

  // do anything here that needs to be done at desctruction time
  // (e.g. close files, deallocate resources etc.)
  std::cout << "===================== NonIsoMufilter::~NonIsoMufilter ======================" << std::endl;
  std::cout << " Number of events processed = " << ntotevt << std::endl;
  std::cout << " Number of events selected  = " << nselevt << std::endl;
  std::cout << "===================== NonIsoMufilter::~NonIsoMufilter ======================" << std::endl;
}


//
// member functions
//

// ------------ method called on each new Event  ------------
  bool
NonIsoMufilter::filter(edm::Event& iEvent, const edm::EventSetup& iSetup)
{
  ++ntotevt;

  bool accept = false;

  unsigned int nJets=0;
  edm::Handle<std::vector<pat::Jet>> patJets;

  try
  {
    iEvent.getByLabel(thePFLabel, patJets);
    nJets = patJets->size(); 
  }
  catch (cms::Exception& exception)
  {
    return accept;
  }

  bool muFound  = false;

  for (unsigned int j = 0; j < nJets; ++j) {  
    int nMu = 0;

    const pat::Jet* jet = &((*patJets)[j]);
    const std::vector<reco::PFCandidatePtr>& PFpart = jet->getPFConstituents();
    unsigned int nPFs = PFpart.size(); 

    if (nPFs < 2) continue;

    for (unsigned int k = 0; k < nPFs; k++) {
      if (PFpart[k]->charge() == 0) continue;
      if (abs(PFpart[k]->pdgId()) != 13) continue;
      if (PFpart[k]->pt() < theMinPt) continue;
      muFound = true;
      ++nMu;
    }
    // Warn if several non iso mu in a jet
    /*
    if (nMu > 1) {
      cout << "Number of non iso mu found = " << nMu   << endl;
    }
    */
    
  }

  if (muFound) {
    accept = true;
    ++nselevt;
  }
  return accept;
}

// ------------ method called once each job just before starting event loop  ------------
  void 
NonIsoMufilter::beginJob()
{
}

// ------------ method called once each job just after ending the event loop  ------------
void 
NonIsoMufilter::endJob() {
}

// ------------ method called when starting to processes a run  ------------
  bool 
NonIsoMufilter::beginRun(edm::Run&, edm::EventSetup const&)
{ 
  return true;
}

// ------------ method called when ending the processing of a run  ------------
  bool 
NonIsoMufilter::endRun(edm::Run&, edm::EventSetup const&)
{
  return true;
}

// ------------ method called when starting to processes a luminosity block  ------------
  bool 
NonIsoMufilter::beginLuminosityBlock(edm::LuminosityBlock&, edm::EventSetup const&)
{
  return true;
}

// ------------ method called when ending the processing of a luminosity block  ------------
  bool 
NonIsoMufilter::endLuminosityBlock(edm::LuminosityBlock&, edm::EventSetup const&)
{
  return true;
}

// ------------ method fills 'descriptions' with the allowed parameters for the module  ------------
void
NonIsoMufilter::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
  //The following says we do not know what parameters are allowed so do no validation
  // Please change this to state exactly what you do use, even if it is no parameters
  edm::ParameterSetDescription desc;
  desc.setUnknown();
  descriptions.addDefault(desc);
}
//define this as a plug-in
DEFINE_FWK_MODULE(NonIsoMufilter);
