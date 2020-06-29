# xchem-xCOS

## Background
Using inspiration from the XChem [fragment screening experiment](https://www.diamond.ac.uk/covid-19/for-scientists/Main-protease-structure-and-XChem.html) at 
Diamond and a mass spectrometry screen of covalent fragments in the London Lab at the Weizmann Institute (Israel), the [COVID Moonshot project](https://discuss.postera.ai/c/covid)  
was born and the global scientific community invited to submit compound designs to inhibit the action of SARS-CoV-2 main protease (Mpro). 

What followed was an amazing response from a very diverse community of organic chemists, medicinal chemists and computational chemists. Thousands of compound 
designs have been submitted with different approaches. Using the geometery and chemical features, the ground truth, of the fragment screening experiment - 
a scoring method was needed to evaluate how much of this ground truth was retained in the compound designs (Fig. 1).

![unconnected](images/xcos_readme_intro.png)
Figure 1: XX


## Aim

## XCOS for evaluating compound designs

#### XCOS method summary

 1. Break designed compound into bits at rotable bonds
 2. Find total no of bit feats matching clustered frag feats with dist threshold
 3. SuCOS score these individual bits to all of the fragments
 4. Capture best matching fragment with bit 

![unconnected](images/xcos_step_1.png)

![unconnected](images/xcos_step_2_3.png)

#### Feature clustering summary

 1. Get all feats of all frags (feat_name, xyz coords)
 2. Group same features
 3. Nearest neighbors algorithim run until all neighbors within radius thresh are aggregated together. Average value of xyz coords used for clusters. 
 4. Calculate total features – assume each feature is equally important 

#### Scoring





## 