// -*- C++ -*-
//
// Package:    TestBranches
// Class:      TestBranches
// 
/**\class TestBranches TestBranches.cc PatTopProduction/TestBranches/src/TestBranches.cc

Description: check wether we can access everything we need

Implementation:
use the same parameter as in PAT to check the filters and the access to branches
*/
//
// Original Author:  Elvire BOUVIER
//         Created:  Tue Mar 17 18:19:02 CET 2015
// $Id$
//
//


// system include files
#include <memory>

// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Framework/interface/ESHandle.h"
#include "FWCore/MessageLogger/interface/MessageLogger.h"
#include "DataFormats/Common/interface/MergeableCounter.h"
#include "FWCore/Framework/interface/LuminosityBlock.h"

#include "DataFormats/ParticleFlowCandidate/interface/PFCandidate.h"
#include "DataFormats/ParticleFlowCandidate/interface/PFCandidateFwd.h"
#include "DataFormats/PatCandidates/interface/Jet.h"
#include "DataFormats/PatCandidates/interface/Muon.h"
#include "DataFormats/PatCandidates/interface/Electron.h"
#include "DataFormats/TrackReco/interface/TrackFwd.h"
#include "DataFormats/HepMCCandidate/interface/GenParticle.h"
#include "DataFormats/JetReco/interface/GenJet.h"

#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"

#include "TFile.h"
#include "TH1D.h"
#include "TLorentzVector.h"

/* C++ Headers */
using namespace std;
using namespace edm;

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

class TestBranches : public edm::EDAnalyzer {
  public:
    explicit TestBranches(const edm::ParameterSet&);
    ~TestBranches();

    static void fillDescriptions(edm::ConfigurationDescriptions& descriptions);


  private:
    virtual void beginJob() ;
    virtual void analyze(const edm::Event&, const edm::EventSetup&);
    virtual void endJob() ;

    virtual void beginRun(edm::Run const&, edm::EventSetup const&);
    virtual void endRun(edm::Run const&, edm::EventSetup const&);
    virtual void beginLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&);
    virtual void endLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&);

    // ----------member data ---------------------------
    std::string theMuLabel; 
    std::string theElLabel;     
    std::string theJetLabel;
    double nonIsoMuMinPt;
    double muJpsiMinPt;
    double jpsiMassMin;
    double jpsiMassMax;
    unsigned int nTrD0Max;
    double trD0MinPt;
    double d0MassMin;
    double d0MassMax;

    int nEventsTotal;
    int nEventsFiltered;
    int nevt[8];
    TH1D* h_Mu_Pt;
    TH1D* h_El_Pt;
    TH1D* h_Tr_N;
    TH1D* h_GenTr_N;
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
TestBranches::TestBranches(const edm::ParameterSet& iConfig)

{
  //now do what ever initialization is needed
  theMuLabel    = iConfig.getParameter<std::string>("muSrc");
  theElLabel    = iConfig.getParameter<std::string>("elSrc");
  theJetLabel   = iConfig.getParameter<std::string>("jetSrc");
  nonIsoMuMinPt = iConfig.getParameter<double>("nonIsoMuMinPt"); // pt min non iso mu (GeV/c)
  muJpsiMinPt   = iConfig.getParameter<double>("muJpsiMinPt"); // pt min mu jpsi(GeV/c)
  jpsiMassMin   = iConfig.getParameter<double>("jpsiMassMin"); // mass min jpsi (GeV/c^2)
  jpsiMassMax   = iConfig.getParameter<double>("jpsiMassMax"); // mass max jpsi (GeV/c^2)
  nTrD0Max      = iConfig.getParameter<unsigned int>("nTrD0Max"); // number of particles considered for d0
  trD0MinPt     = iConfig.getParameter<double>("trD0MinPt"); // pt min pf for d0 (GeV/c)
  d0MassMin     = iConfig.getParameter<double>("d0MassMin"); // mass min d0 (GeV/c^2)
  d0MassMax     = iConfig.getParameter<double>("d0MassMax"); // mass max d0 (GeV/c^2)

  nEventsTotal    = 0;
  nEventsFiltered = 0;
  for (unsigned int i = 0; i < 8; i++) nevt[i] = 0;
}


TestBranches::~TestBranches()
{

  // do anything here that needs to be done at desctruction time
  // (e.g. close files, deallocate resources etc.)
  std::cout << "===================== TestBranches::~TestBranches =========================" << std::endl;
  std::cout << "nEventsTotal                              = " << nEventsTotal << std::endl;
  std::cout << "nEventsFiltered                           = " << nEventsFiltered << std::endl;
  std::cout << std::endl;
  std::cout << " Number of events processed               = " << nevt[0] << std::endl;
  std::cout << " Number of events with a e/mu and 2 jets  = " << nevt[1] << std::endl;
  std::cout << " Number of events with a mu               = " << nevt[2] << std::endl;
  std::cout << " Number of events with a all              = " << nevt[3] << std::endl;
  std::cout << std::endl;
  std::cout << " Number of events J/psi tagged            = " << nevt[4] << std::endl;
  std::cout << " Number of events with a reco J/psi       = " << nevt[5] << std::endl;
  std::cout << " Number of events D^0 tagged              = " << nevt[6] << std::endl;
  std::cout << " Number of events with a reco D^0         = " << nevt[7] << std::endl;
  std::cout << "===================== TestBranches::~TestBranches =========================" << std::endl;

}


//
// member functions
//

// ------------ method called for each event  ------------
  void
TestBranches::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup)
{
  ++nevt[0];

  // Count "iso" lepton and jets
  unsigned int nMus=0;
  edm::Handle<std::vector<pat::Muon>>  patMus;
  iEvent.getByLabel(theMuLabel, patMus);
  nMus = patMus->size(); 

  unsigned int nEls=0;
  edm::Handle<std::vector<pat::Electron>>  patEls;
  iEvent.getByLabel(theElLabel, patEls);
  nEls = patEls->size(); 

  // Count jets
  unsigned int nJets=0;
  edm::Handle<std::vector<pat::Jet>> patJets;
  edm::InputTag tagJets(theJetLabel,"","PAT");
  iEvent.getByLabel(tagJets, patJets);
  nJets = patJets->size(); 

  if ((nMus > 0 || nEls > 0) && nJets > 1)
    ++nevt[1];

  // Count non iso mu
  int nMu = 0;

  for (unsigned int j = 0; j < nJets; ++j) {  

    const pat::Jet* jet = &((*patJets)[j]);
    const std::vector<reco::PFCandidatePtr>& PFpart = jet->getPFConstituents();
    unsigned int npfs = PFpart.size(); 

    if (npfs < 2) continue;

    for (unsigned int k = 0; k < npfs; k++) {
      if (PFpart[k]->charge() == 0) continue;
      if (abs(PFpart[k]->pdgId()) != 13) continue;
      if (PFpart[k]->pt() < nonIsoMuMinPt) continue; 
      ++nMu;
    }
  }

  if (nMu > 0) 
    ++nevt[2];
  if ((nMus > 0 || nEls > 0) && nJets > 1 && nMu > 0)
    ++nevt[3];

  // Check flags
  edm::Handle<bool> jpsiTagged;
  edm::InputTag tagJpsi("jpsid0flag","ContainsJpsi","PAT");
  iEvent.getByLabel(tagJpsi, jpsiTagged);
  if ((bool)*jpsiTagged)
    ++nevt[4];
  edm::Handle<bool> d0Tagged;
  edm::InputTag tagD0("jpsid0flag","ContainsD0","PAT");
  iEvent.getByLabel(tagD0, d0Tagged);
  if ((double)*d0Tagged)
    ++nevt[6];

  // Get (gen) track multiplicity and pT(mu/e) for each jet
  // Access jets
  bool jpsiFound = false;
  bool d0Found = false;
  for (unsigned int j = 0; j < nJets; ++j) {  
    int nTr = 0;

    const pat::Jet* jet = &((*patJets)[j]);
    const std::vector<reco::PFCandidatePtr>& PFpart = jet->getPFConstituents();
    unsigned int npfs = PFpart.size(); 
    std::vector<reco::PFCandidate> myD0PFs;
    std::vector<reco::PFCandidate> myJpsiPFs;
    for (unsigned int k = 0; k < npfs; k++) {
      // Plot PFmu pT
      reco::MuonRef muonRef = PFpart[k]->muonRef();
      if (muonRef.isNonnull())
        h_Mu_Pt->Fill(muonRef->pt());
      // Plot PFel pT
      reco::GsfElectronRef electronRef = PFpart[k]->gsfElectronRef();
      if (electronRef.isNonnull())
        h_El_Pt->Fill(electronRef->pt());
      // Get track from PF
      reco::TrackRef trackRef = PFpart[k]->trackRef();
      if (trackRef.isNonnull() && trackRef->pt() > 0.2 && trackRef->eta() < 2.4)
        nTr++;
      // Select potential D0 and Jpsi daughters 
      if (PFpart[k]->charge() == 0) continue;
      if (abs(PFpart[k]->pdgId()) !=13) {
        if (PFpart[k]->pt() >= trD0MinPt) 
          myD0PFs.push_back(*PFpart[k]);
      }
      else {
        if (PFpart[k]->pt() >= muJpsiMinPt) 
          myJpsiPFs.push_back(*PFpart[k]);
      }
    } // PF loop
    h_Tr_N->Fill((double)nTr);

    // take care of D0
    sort(myD0PFs.begin(), myD0PFs.end(), compareParticlesByPt);
    for (unsigned int k1 = 0; k1 < std::min((unsigned int)myD0PFs.size(), nTrD0Max); ++k1) {
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
        }
      } // myD0PFs[k2] loop
    } // myD0PFs[k1] loop

    // take care of Jpsi
    for (unsigned int j1 = 0; j1 < myJpsiPFs.size(); ++j1) {
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
        }
      } // myJpsiPFs[j2] loop
    } // myJpsiPFs[j1] loop    
  } // jet loop

  if (jpsiFound)
    ++nevt[5];
  if (d0Found)
    ++nevt[7];

  // Access genJet    
  unsigned int nGenJets=0;
  edm::Handle<std::vector<reco::GenJet>> patGenJets;
  edm::InputTag tagGenJets("selectedPatJetsPFlow","genJets","PAT");
  iEvent.getByLabel(tagGenJets, patGenJets);
  nGenJets = patGenJets->size(); 
  for (unsigned int j = 0; j < nGenJets; ++j) {  
    int nGenTr = 0;

    // Get gen particles
    const reco::GenJet* genJet = &((*patGenJets)[j]);
    const std::vector<const reco::GenParticle*> GenPart = genJet->getGenConstituents();
    unsigned int ngcs = GenPart.size(); 
    for (unsigned int k = 0; k < ngcs; k++) {
      if (GenPart[k]->charge() != 0 && GenPart[k]->pt() > 0.2 && GenPart[k]->eta() < 2.4) 
        nGenTr++;
    }
    h_GenTr_N->Fill((double)nGenTr);
  } // genJet loop

}


// ------------ method called once each job just before starting event loop  ------------
  void 
TestBranches::beginJob()
{
  edm::Service<TFileService> fs;
  h_Mu_Pt      = fs->make<TH1D>("h_Mu_Pt", "h_Mu_pT", 100, 0., 100.);
  h_El_Pt      = fs->make<TH1D>("h_El_Pt", "h_El_pT", 100, 0., 100.);
  h_Tr_N       = fs->make<TH1D>("h_Tr_N", "h_Tr_N", 50, 0, 50.);
  h_GenTr_N    = fs->make<TH1D>("h_GenTr_N", "h_GenTr_N", 50, 0, 50.);
}

// ------------ method called once each job just after ending the event loop  ------------
  void 
TestBranches::endJob() 
{
}

// ------------ method called when starting to processes a run  ------------
  void 
TestBranches::beginRun(edm::Run const&, edm::EventSetup const&)
{
}

// ------------ method called when ending the processing of a run  ------------
  void 
TestBranches::endRun(edm::Run const&, edm::EventSetup const&)
{
}

// ------------ method called when starting to processes a luminosity block  ------------
  void 
TestBranches::beginLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&)
{
}

// ------------ method called when ending the processing of a luminosity block  ------------
  void 
TestBranches::endLuminosityBlock(edm::LuminosityBlock const& lumi, edm::EventSetup const& setup)
{
  // Total number of events is the sum of the events in each of these luminosity blocks
  edm::Handle<edm::MergeableCounter> nEventsTotalCounter;
  lumi.getByLabel("nEventsTotal", nEventsTotalCounter);
  nEventsTotal += nEventsTotalCounter->value;

  edm::Handle<edm::MergeableCounter> nEventsFilteredCounter;
  lumi.getByLabel("nEventsFiltered", nEventsFilteredCounter);
  nEventsFiltered += nEventsFilteredCounter->value;
}

// ------------ method fills 'descriptions' with the allowed parameters for the module  ------------
void
TestBranches::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
  //The following says we do not know what parameters are allowed so do no validation
  // Please change this to state exactly what you do use, even if it is no parameters
  edm::ParameterSetDescription desc;
  desc.setUnknown();
  descriptions.addDefault(desc);
}

//define this as a plug-in
DEFINE_FWK_MODULE(TestBranches);
