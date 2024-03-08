import FWCore.ParameterSet.Config as cms

from RecoJets.JetProducers.PFJetParameters_cfi import *
from RecoJets.JetProducers.AnomalousCellParameters_cfi import *

from CommonTools.PileupAlgos.Puppi_cff import puppi

packedpuppi = puppi.clone(
    useExistingWeights = True,
    candName = 'packedPFCandidates',
    vertexName = 'offlineSlimmedPrimaryVertices'
)

hotvrPFJets = cms.EDProducer("HOTVRProducer",
    src=cms.InputTag("packedPFCandidates"),
    weights=cms.InputTag("packedpuppi"),
    doRekey=cms.bool(True),
    rekeyCandidateSrc = cms.InputTag("packedPFCandidates") # constituents point to rekeyCandidateSrc
)

# hotvrPFJets = cms.EDProducer("HOTVRProducer",
#     src=cms.InputTag("packedPFCandidates"),
#     doRekey=cms.bool(True),
#     rekeyCandidateSrc = cms.InputTag("packedPFCandidates") # constituents point to rekeyCandidateSrc
# )

# hotvrPFJetsPuppi = hotvrPFJets.clone(
#     applyWeight = True,
#     weights=cms.InputTag("packedpuppi"),
# )