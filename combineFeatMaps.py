#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May  5 10:37:35 2020

@author: Warren

Merge feat maps and get feat map score for
John Chodera's docked conformers
"""

import os
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem.FeatMaps import FeatMaps
from rdkit.Chem.FeatMaps.FeatMapUtils import CombineFeatMaps
from rdkit import RDConfig
import csv

# We need to start by building a FeatureFactory object which defines 
# the set of pharmacophore features being used. 
# We'll use this to find features on the molecules.
fdef = AllChem.BuildFeatureFactory(os.path.join(RDConfig.RDDataDir, 
                                                'BaseFeatures.fdef'))


# Set default paramters for selecting points in feature map
fmParams = {}
for k in fdef.GetFeatureFamilies():
    fparams = FeatMaps.FeatMapParams()
    fmParams[k] = fparams

# List of feature families that we want to use
keep = ('Donor', 'Acceptor', 'NegIonizable', 'PosIonizable', 'ZnBinder',
        'Aromatic', 'Hydrophobe', 'LumpedHydrophobe')


def getFeatureMap(mol_list):
    if isinstance(mol_list, list):
        allFeats = []
        for m in mol_list:
            rawFeats = fdef.GetFeaturesForMol(m)
            allFeats.append([f for f in rawFeats if f.GetFamily() in keep])
    else:
        allFeats = []
        rawFeats = fdef.GetFeaturesForMol(mol_list)
        allFeats.append([f for f in rawFeats if f.GetFamily() in keep])
        
    fms = [FeatMaps.FeatMap(feats=x, weights=[1] * len(x), 
                            params=fmParams) for x in allFeats]

    return fms, allFeats


def getFeatureMerge(fms, mergeTol):
    for i in range(len(fms)):
        if i == 0:
            fm1 = fms[0]
            fm2 = fms[1]
            fm1 = CombineFeatMaps(fm1, fm2, 
                                  mergeMetric=1, 
                                  mergeTol=mergeTol, 
                                  dirMergeMode=0)
        if i >= 1 and i < len(fms)-1:
            fm2 = fms[i+1]
            fm1 = CombineFeatMaps(fm1, fm2, 
                      mergeMetric=1, 
                      mergeTol=mergeTol, 
                      dirMergeMode=0)
        
    return fm1
            
            
def getFeatureMapScore(frag_fms_merged, docked_allFeats, 
                       score_mode=FeatMaps.FeatMapScoreMode.All):    
    
    frag_fms_merged.scoreMode = score_mode
    fm_score = frag_fms_merged.ScoreFeats(docked_allFeats[0]) / min(frag_fms_merged.GetNumFeatures(), len(docked_allFeats[0]))
    
    return fm_score      
  
            
def getScores(frag_mol_folder_path, docked_sdf_file_path):
    
    path  = frag_mol_folder_path + '/'    
    
    frag_mol_list =  [Chem.MolFromMolFile((path + mol_file), sanitize=True) for mol_file in os.listdir(frag_mol_folder_path)]
        
    docked_mol_list = Chem.SDMolSupplier(docked_sdf_file_path, sanitize=True)
     
    docked_mol_list = [mol for mol in docked_mol_list if mol is not None]
    
    # Get fragment feature maps
    frag_fms, frag_allFeats = getFeatureMap(frag_mol_list)
    
    # Merge fragment feature maps
    frag_fms_merged = getFeatureMerge(frag_fms, mergeTol=1)
    
    # Let's do some scoring
    all_info = []
    
    for docked_mol in docked_mol_list:
        docked_name = docked_mol.GetProp('_Name')
        print('Getting values for {}'.format(docked_name))
        
        # Get docked feature maps
        fms, docked_allFeats = getFeatureMap(docked_mol)
        
        # Now let's score
        score = getFeatureMapScore(frag_fms_merged, docked_allFeats)
        
        # Let's get some meta data to help review data
        docked_SMILES = Chem.MolToSmiles(docked_mol)
               
        # Get all scores and info for writing to file
        all_info.append((docked_name,
                         docked_SMILES,
                         score,))
               
        with open('Feat_map_merge_scores.csv', 'w') as f:
            writer = csv.writer(f)
            writer.writerow(['Compound_name','SMILES', 'Score'])                             
            writer.writerows(all_info)            
            

            
    
    
