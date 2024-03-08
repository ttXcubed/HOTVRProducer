import FWCore.ParameterSet.Config as cms

from RecoJets.JetProducers.GenJetParameters_cfi import *
from RecoJets.JetProducers.AnomalousCellParameters_cfi import *

packedGenParticlesForJetsNoNu = cms.EDFilter("CandPtrSelector",
    src=cms.InputTag("packedGenParticles"),
    cut=cms.string("abs(pdgId) != 12 && abs(pdgId) != 14 && abs(pdgId) != 16")
)

hotvrGenJets = cms.EDProducer("GenHOTVRProducer",
    src=cms.InputTag("packedGenParticlesForJetsNoNu"),
    mu=cms.double(30),
    theta=cms.double(0.7),
    max_r=cms.double(1.5),
    min_r=cms.double(0.1),
    rho=cms.double(600),
    hotvr_pt_min=cms.double(30),
)
