// -*- C++ -*-
//
// Package:    FlagProducer
// Class:      FlagProducer
// 
/**\class FlagProducer FlagProducer.cc EBouvier/FlagProducer/src/FlagProducer.cc

 Description: Flag events wether they contain a D^0 or a J/psi->mu+mu-

 Implementation:
 get charged PF from jets
*/
//
// Original Author:  Elvire BOUVIER
//         Created:  Thu Mar 26 14:09:50 CET 2015
// $Id$
//
//


// system include files
#include <memory>

// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDProducer.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Framework/interface/ESHandle.h"
#include "FWCore/MessageLogger/interface/MessageLogger.h"

#include "DataFormats/ParticleFlowCandidate/interface/PFCandidate.h"
#include "DataFormats/ParticleFlowCandidate/interface/PFCandidateFwd.h"
#include "DataFormats/PatCandidates/interface/Jet.h"


inline bool compareParticlesByPt(reco::PFCandidate first, reco::PFCandidate second)
{
  if (first.pt() > second.pt()) 
    return true; 
  else 
    return false;
}

//
// class declaration
//

class FlagProducer : public edm::EDProducer {
   public:
      explicit FlagProducer(const edm::ParameterSet&);
      ~FlagProducer();

      static void fillDescriptions(edm::ConfigurationDescriptions& descriptions);

   private:
      virtual void beginJob() ;
      virtual void produce(edm::Event&, const edm::EventSetup&);
      virtual void endJob() ;
      
      virtual void beginRun(edm::Run&, edm::EventSetup const&);
      virtual void endRun(edm::Run&, edm::EventSetup const&);
      virtual void beginLuminosityBlock(edm::LuminosityBlock&, edm::EventSetup const&);
      virtual void endLuminosityBlock(edm::LuminosityBlock&, edm::EventSetup const&);

      // ----------member data ---------------------------
    std::string theJetLabel; // label of jets
    double muJpsiMinPt;
    double jpsiMassMin;
    double jpsiMassMax;
    unsigned int nTrD0Max;
    double trD0MinPt;
    double d0MassMin;
    double d0MassMax;

    long int nTotEvt;
    long int nJpsiEvt;
    long int nD0Evt;
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
FlagProducer::FlagProducer(const edm::ParameterSet& iConfig)
{
   //now do what ever other initialization is needed
  theJetLabel = iConfig.getParameter<std::string>("src");
  muJpsiMinPt = iConfig.getParameter<double>("muJpsiMinPt"); // pt min mu jpsi(GeV/c)
  jpsiMassMin = iConfig.getParameter<double>("jpsiMassMin"); // mass min jpsi (GeV/c^2)
  jpsiMassMax = iConfig.getParameter<double>("jpsiMassMax"); // mass max jpsi (GeV/c^2)
  nTrD0Max    = iConfig.getParameter<unsigned int>("nTrD0Max"); // number of particles considered for d0
  trD0MinPt   = iConfig.getParameter<double>("trD0MinPt"); // pt min pf for d0 (GeV/c)
  d0MassMin   = iConfig.getParameter<double>("d0MassMin"); // mass min d0 (GeV/c^2)
  d0MassMax   = iConfig.getParameter<double>("d0MassMax"); // mass max d0 (GeV/c^2)

  LogDebug("FlagProducer") << " Jet label  : " << theJetLabel
    << " MuJpsi Min Pt  : " << muJpsiMinPt
    << " J/psi Mass Min : " << jpsiMassMin
    << " J/psi Mass Max : " << jpsiMassMax
    << " N PF D0 Max    : " << nTrD0Max
    << " PF D0 Min Pt   : " << trD0MinPt
    << " D0 Mass Min    : " << d0MassMin
    << " D0 Mass Max    : " << d0MassMax;

  nTotEvt = 0;
  nJpsiEvt = 0;
  nD0Evt = 0;

   //register your products
   produces<bool>("ContainsJpsi");
   produces<bool>("ContainsD0");
/* Examples
   produces<ExampleData2>();

   //if do put with a label
   produces<ExampleData2>("label");
 
   //if you want to put into the Run
   produces<ExampleData2,InRun>();
*/
  
}


FlagProducer::~FlagProducer()
{
 
   // do anything here that needs to be done at desctruction time
   // (e.g. close files, deallocate resources etc.)
  std::cout << "===================== FlagProducer::~FlagProducer =====================" << std::endl;
  std::cout << " Number of events processed       = " << nTotEvt << std::endl;
  std::cout << " Number of J/psi events selected  = " << nJpsiEvt << std::endl;
  std::cout << " Number of D0 events selected     = " << nD0Evt << std::endl;
  std::cout << "===================== FlagProducer::~FlagProducer =====================" << std::endl;

}


//
// member functions
//

// ------------ method called to produce the data  ------------
void
FlagProducer::produce(edm::Event& iEvent, const edm::EventSetup& iSetup)
{
  ++nTotEvt;

  bool jpsiFound = false;
  bool d0Found = false;

  unsigned int nJets=0;
  edm::Handle<std::vector<pat::Jet>> patJets;

  try
  {
    iEvent.getByLabel(theJetLabel, patJets);
    nJets = patJets->size(); 

    for (unsigned int j = 0; j < nJets; ++j) {  
      const pat::Jet* jet = &((*patJets)[j]);
      const std::vector<reco::PFCandidatePtr>& PFpart = jet->getPFConstituents();
      unsigned int nPFs = PFpart.size(); 
      std::vector<reco::PFCandidate> myD0PFs;
      std::vector<reco::PFCandidate> myJpsiPFs;

      for (unsigned int j = 0; j < nPFs; ++j) {  

        if (PFpart[j]->charge() == 0) continue;

        // take care of pf for D0
        if (abs(PFpart[j]->pdgId()) != 13) {
          if (PFpart[j]->pt() >= trD0MinPt)
            myD0PFs.push_back(*PFpart[j]);
        }

        // take care of pf for jpsi
        else {
          if (PFpart[j]->pt() >= muJpsiMinPt) 
            myJpsiPFs.push_back(*PFpart[j]);
        }
      } // PFpart[j] loop

      LogDebug("FlagProducer") << "Nbre D0 PF   = " << myD0PFs.size()
        << "Nbre Jpsi PF = " << myJpsiPFs.size();

      // take care of D0
      sort(myD0PFs.begin(), myD0PFs.end(), compareParticlesByPt);
      for (unsigned int k1 = 0; k1 < std::min((unsigned int)myD0PFs.size(), nTrD0Max); ++k1) {  
        int nD0 = 0;

        for (unsigned int k2 = 0; k2 < std::min((unsigned int)myD0PFs.size(), nTrD0Max); ++k2) {

          if (k1 == k2) continue;
          if (myD0PFs[k1].charge()*myD0PFs[k2].charge() > 0) continue;

          double e  = myD0PFs[k1].energy()+myD0PFs[k2].energy();
          double px = myD0PFs[k1].px()+myD0PFs[k2].px();
          double py = myD0PFs[k1].py()+myD0PFs[k2].py();
          double pz = myD0PFs[k1].pz()+myD0PFs[k2].pz();
          double m = pow(e,2)-pow(px,2)-pow(py,2)-pow(pz,2);
          if (m > 0.) m = sqrt(m);

          if (m >= d0MassMin && m < d0MassMax) {
            d0Found = true;
            ++nD0;
          }
        } // myD0PFs[k2] loop
        // Warn if several D0 for one PF
        if (nD0 > 2) {
          std::cout << "Number of D0 found = " << nD0 << std::endl;
        }
      } // myD0PFs[k1] loop

      // take care of Jpsi
      for (unsigned int j1 = 0; j1 < myJpsiPFs.size(); ++j1) {
        int nJpsi = 0;

        for (unsigned int j2 = j1+1; j2 < myJpsiPFs.size(); ++j2) {

          if (myJpsiPFs[j1].charge()*myJpsiPFs[j2].charge() >= 0) continue;

          double e  = myJpsiPFs[j1].energy()+myJpsiPFs[j2].energy();
          double px = myJpsiPFs[j1].px()+myJpsiPFs[j2].px();
          double py = myJpsiPFs[j1].py()+myJpsiPFs[j2].py();
          double pz = myJpsiPFs[j1].pz()+myJpsiPFs[j2].pz();
          double m = pow(e,2)-pow(px,2)-pow(py,2)-pow(pz,2);
          if (m > 0.) m = sqrt(m);

          if (m >= jpsiMassMin && m < jpsiMassMax) {
            jpsiFound = true;
            ++nJpsi;
          }
        } // myJpsiPFs[j2] loop
        // Warn if several JPsi for a PF
        if (nJpsi > 1) {
          std::cout << "Number of J/Psi found = " << nJpsi << std::endl;
        }
      } // myJpsiPFs[j1] loop

    } // jet loop
    if (d0Found) 
      ++nD0Evt;
    if (jpsiFound) 
      ++nJpsiEvt;
  }
  catch (cms::Exception& exception)
  {
    jpsiFound = false;
    d0Found = false;
  }

  std::auto_ptr<bool> jpsiResult(new bool(false));
  (*jpsiResult) = jpsiFound;
  std::auto_ptr<bool> d0Result(new bool(false));
  (*d0Result) = d0Found;
  iEvent.put(jpsiResult, "ContainsJpsi");
  iEvent.put(d0Result, "ContainsD0");
  
/* This is an event example
   //Read 'ExampleData' from the Event
   Handle<ExampleData> pIn;
   iEvent.getByLabel("example",pIn);

   //Use the ExampleData to create an ExampleData2 which 
   // is put into the Event
   std::auto_ptr<ExampleData2> pOut(new ExampleData2(*pIn));
   iEvent.put(pOut);
*/

/* this is an EventSetup example
   //Read SetupData from the SetupRecord in the EventSetup
   ESHandle<SetupData> pSetup;
   iSetup.get<SetupRecord>().get(pSetup);
*/
 
}

// ------------ method called once each job just before starting event loop  ------------
void 
FlagProducer::beginJob()
{
}

// ------------ method called once each job just after ending the event loop  ------------
void 
FlagProducer::endJob() {
}

// ------------ method called when starting to processes a run  ------------
void 
FlagProducer::beginRun(edm::Run&, edm::EventSetup const&)
{
}

// ------------ method called when ending the processing of a run  ------------
void 
FlagProducer::endRun(edm::Run&, edm::EventSetup const&)
{
}

// ------------ method called when starting to processes a luminosity block  ------------
void 
FlagProducer::beginLuminosityBlock(edm::LuminosityBlock&, edm::EventSetup const&)
{
}

// ------------ method called when ending the processing of a luminosity block  ------------
void 
FlagProducer::endLuminosityBlock(edm::LuminosityBlock&, edm::EventSetup const&)
{
}

// ------------ method fills 'descriptions' with the allowed parameters for the module  ------------
void
FlagProducer::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
  //The following says we do not know what parameters are allowed so do no validation
  // Please change this to state exactly what you do use, even if it is no parameters
  edm::ParameterSetDescription desc;
  desc.setUnknown();
  descriptions.addDefault(desc);
}

//define this as a plug-in
DEFINE_FWK_MODULE(FlagProducer);
