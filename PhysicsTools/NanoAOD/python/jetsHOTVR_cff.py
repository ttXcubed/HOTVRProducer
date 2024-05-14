import FWCore.ParameterSet.Config as cms

from PhysicsTools.NanoAOD.nano_eras_cff import *
from PhysicsTools.NanoAOD.common_cff import *
from PhysicsTools.NanoAOD.simpleCandidateFlatTableProducer_cfi import simpleCandidateFlatTableProducer

from RecoJets.JetProducers.hotvrJets_cfi import *

###### JEC corrections for subjet
#############################################################
# Hack START
# Note: Do this so we can add "JetCorrFactors" to patJets
# that do not have JetCorrFactors addded in them.
#
#############################################################
# from PhysicsTools.PatAlgos.recoLayer0.jetCorrFactors_cfi import *
# jetCorrFactorsForSubjetTemp = patJetCorrFactors.clone(
#   src=cms.InputTag('hotvrPFJets','SubJets'),
#   levels = cms.vstring(), #Don't apply any correction.
#   payload = cms.string('AK4PFPuppi'),
#   primaryVertices = cms.InputTag("offlineSlimmedPrimaryVertices"),
# )

# from PhysicsTools.PatAlgos.producersLayer1.jetProducer_cfi import _patJets as patJets
# hotvrPFSubJets = patJets.clone(
#   jetSource=cms.InputTag('hotvrPFJets','SubJets'),
#   addJetCorrFactors = True,
#   jetCorrFactorsSource = ["jetCorrFactorsForSubjetTemp"],
#   addGenJetMatch = False,
#   addGenPartonMatch = False,
#   embedGenPartonMatch = False,
#   getJetMCFlavour = False,
#   addJetFlavourInfo = False,
#   addBTagInfo = False,
#   addDiscriminators = False,
#   addTagInfos = False,
#   addAssociatedTracks    = False,
#   addJetCharge    = False,
#   addJetID = False,
# )
# #############################################################
# jetCorrFactorshotvrPFSubJets = patJetCorrFactors.clone(src=cms.InputTag('hotvrPFSubJets'),
#   levels = cms.vstring('L1FastJet','L2Relative','L3Absolute','L2L3Residual'),
#   payload = cms.string('AK4PFPuppi'),
#   primaryVertices = cms.InputTag("offlineSlimmedPrimaryVertices"),
# )

# from  PhysicsTools.PatAlgos.producersLayer1.jetUpdater_cfi import *
# updatedhotvrPFSubJets = updatedPatJets.clone(
#   jetSource=cms.InputTag('hotvrPFSubJets'),
#   jetCorrFactorsSource=cms.VInputTag(cms.InputTag("jetCorrFactorshotvrPFSubJets") ),
#   sort=False,
#   addBTagInfo=False,
# )
######

#hotvrPFJets are already puppi jets --> RecoJets/JetProducers/plugins/VirtualJetProducer.cc
hotvrJetTable = simpleCandidateFlatTableProducer.clone(
    src = cms.InputTag("hotvrPFJets"),
    cut = cms.string(" pt > 30"), #probably already applied in miniaod
    name = cms.string("HOTVRJet"),
    variables = cms.PSet(P4Vars,
        area = Var("jetArea()", float, doc="jet catchment area, for JECs",precision=10),
        # msoftdrop = Var("groomedMass('SoftDropPuppi')",float, doc="Corrected soft drop mass with PUPPI",precision=10),
        tau1 = Var("userFloat('tau1')",float, doc="Nsubjettiness (1 axis)",precision=10),
        tau2 = Var("userFloat('tau2')",float, doc="Nsubjettiness (2 axis)",precision=10),
        tau3 = Var("userFloat('tau3')",float, doc="Nsubjettiness (3 axis)",precision=10),

        nMuons = Var("?hasOverlaps('muons')?overlaps('muons').size():0", int, doc="number of muons in the jet"),
        muonIdx1 = Var("?overlaps('muons').size()>0?overlaps('muons')[0].key():-1", int, doc="index of first matching muon"),
        muonIdx2 = Var("?overlaps('muons').size()>1?overlaps('muons')[1].key():-1", int, doc="index of second matching muon"),
        electronIdx1 = Var("?overlaps('electrons').size()>0?overlaps('electrons')[0].key():-1", int, doc="index of first matching electron"),
        electronIdx2 = Var("?overlaps('electrons').size()>1?overlaps('electrons')[1].key():-1", int, doc="index of second matching electron"),
        nElectrons = Var("?hasOverlaps('electrons')?overlaps('electrons').size():0", int, doc="number of electrons in the jet"),
        nConstituents = Var("numberOfDaughters()","uint8",doc="Number of particles in the jet"),

        btagDeepB = Var("?(bDiscriminator('pfDeepCSVJetTags:probb')+bDiscriminator('pfDeepCSVJetTags:probbb'))>=0?bDiscriminator('pfDeepCSVJetTags:probb')+bDiscriminator('pfDeepCSVJetTags:probbb'):-1",float,doc="DeepCSV b+bb tag discriminator",precision=10),
        btagDeepFlavB = Var("bDiscriminator('pfDeepFlavourJetTags:probb')+bDiscriminator('pfDeepFlavourJetTags:probbb')+bDiscriminator('pfDeepFlavourJetTags:problepb')",float,doc="DeepJet b+bb+lepb tag discriminator",precision=10),

        nsubJets = Var("subjets().size()", int, doc="number of subjets"),
        subJetIdx1 = Var("?nSubjetCollections()>0 && subjets().size()>0?subjets()[0].key():-1", int, doc="index of first subjet"),
        subJetIdx2 = Var("?nSubjetCollections()>0 && subjets().size()>1?subjets()[1].key():-1", int, doc="index of second subjet"),
        subJetIdx3 = Var("?nSubjetCollections()>0 && subjets().size()>2?subjets()[2].key():-1", int, doc="index of third subjet"),
        subJetIdx4 = Var("?nSubjetCollections()>0 && subjets().size()>3?subjets()[3].key():-1", int, doc="index of third subjet"),

        rawFactor = Var("1.",float,doc="1 - Factor to get back to raw pT",precision=6),
        chHEF = Var("chargedHadronEnergyFraction()", float, doc="charged Hadron Energy Fraction", precision= 6),
        neHEF = Var("neutralHadronEnergyFraction()", float, doc="neutral Hadron Energy Fraction", precision= 6),
        chEmEF = Var("chargedEmEnergyFraction()", float, doc="charged Electromagnetic Energy Fraction", precision= 6),
        neEmEF = Var("neutralEmEnergyFraction()", float, doc="neutral Electromagnetic Energy Fraction", precision= 6),
        muEF = Var("muonEnergyFraction()", float, doc="muon Energy Fraction", precision= 6),

    ),
)

# subjets with JEC correction
# hotvrSubJetTable = simpleCandidateFlatTableProducer.clone(
#     src = cms.InputTag("updatedhotvrPFSubJets"),
#     name = cms.string("HOTVRSubJet"),
#     # doc  = cms.string("slimmedJetsAK8, i.e. ak8 fat jets for boosted analysis"),
#     variables = cms.PSet(P4Vars,
#         btagDeepB = Var("bDiscriminator('pfDeepCSVJetTags:probb')+bDiscriminator('pfDeepCSVJetTags:probbb')",float,doc="DeepCSV b+bb tag discriminator",precision=10),
#         rawFactor = Var("1.-jecFactor('Uncorrected')",float,doc="1 - Factor to get back to raw pT",precision=6),
#         # tau1 = Var("userFloat('tau1')",float, doc="Nsubjettiness (1 axis)",precision=10),
#         # tau2 = Var("userFloat('tau2')",float, doc="Nsubjettiness (2 axis)",precision=10),
#         # tau3 = Var("userFloat('tau3')",float, doc="Nsubjettiness (3 axis)",precision=10),
#         area = Var("jetArea()", float, doc="jet catchment area, for JECs",precision=10),
#         nConstituents = Var("numberOfDaughters()","uint8",doc="Number of particles in the jet"),
#         # chHEF = Var("chargedHadronEnergyFraction()", float, doc="charged Hadron Energy Fraction", precision= 6),
#         # neHEF = Var("neutralHadronEnergyFraction()", float, doc="neutral Hadron Energy Fraction", precision= 6),
#         # chEmEF = Var("chargedEmEnergyFraction()", float, doc="charged Electromagnetic Energy Fraction", precision= 6),
#         # neEmEF = Var("neutralEmEnergyFraction()", float, doc="neutral Electromagnetic Energy Fraction", precision= 6),
#         # muEF = Var("muonEnergyFraction()", float, doc="muon Energy Fraction", precision= 6),
#     )
# )

hotvrSubJetTable = simpleCandidateFlatTableProducer.clone(
    src = cms.InputTag("hotvrPFJets","SubJets"),
    name = cms.string("HOTVRSubJet"),
    # doc  = cms.string("slimmedJetsAK8, i.e. ak8 fat jets for boosted analysis"),
    variables = cms.PSet(P4Vars,
        btagDeepB = Var("bDiscriminator('pfDeepCSVJetTags:probb')+bDiscriminator('pfDeepCSVJetTags:probbb')",float,doc="DeepCSV b+bb tag discriminator",precision=10),
        # rawFactor = Var("1.-jecFactor('Uncorrected')",float,doc="1 - Factor to get back to raw pT",precision=6),
        # tau1 = Var("userFloat('tau1')",float, doc="Nsubjettiness (1 axis)",precision=10),
        # tau2 = Var("userFloat('tau2')",float, doc="Nsubjettiness (2 axis)",precision=10),
        # tau3 = Var("userFloat('tau3')",float, doc="Nsubjettiness (3 axis)",precision=10),
        area = Var("jetArea()", float, doc="jet catchment area, for JECs",precision=10),
        nConstituents = Var("numberOfDaughters()","uint8",doc="Number of particles in the jet"),
        chHEF = Var("chargedHadronEnergyFraction()", float, doc="charged Hadron Energy Fraction", precision= 6),
        neHEF = Var("neutralHadronEnergyFraction()", float, doc="neutral Hadron Energy Fraction", precision= 6),
        chEmEF = Var("chargedEmEnergyFraction()", float, doc="charged Electromagnetic Energy Fraction", precision= 6),
        neEmEF = Var("neutralEmEnergyFraction()", float, doc="neutral Electromagnetic Energy Fraction", precision= 6),
        muEF = Var("muonEnergyFraction()", float, doc="muon Energy Fraction", precision= 6),
    )
)

#jets are not as precise as muons
hotvrJetTable.variables.pt.precision=10
hotvrSubJetTable.variables.pt.precision=10

# jetHOTVRUserDataTask = cms.Task(tightJetIdHOTVR,tightJetIdLepVetoHOTVR)
# jetHOTVRTask = cms.Task(packedpuppi, hotvrPFJets, jetCorrFactorsForSubjetTemp, hotvrPFSubJets, jetCorrFactorshotvrPFSubJets, updatedhotvrPFSubJets)
jetHOTVRTask = cms.Task(packedpuppi, hotvrPFJets)

#after lepton collections have been run
# jetHOTVRLepTask = cms.Task(lepInHOTVRJetVars)

jetHOTVRTablesTask = cms.Task(hotvrJetTable, hotvrSubJetTable)
