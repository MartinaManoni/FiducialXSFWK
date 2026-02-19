import sys
sys.path.append('../helperstuff/')
from split import split

DO_SPLIT = False #do split false for step 2 and 3, and Run this again 

#obsNames=["mass4l", "pT4l", "rapidity4l", "massZ1", "massZ2", "pTj1", "pTj2", "Nj", "mjj", "absdetajj", "dphijj", "pTHj", "pTHjj", "mHj", "massZ1_massZ2", "rapidity4l_pT4l", "pTj1_pTj2", "Nj_pT4l", "pT4l_pTHj", "absdetajj_mjj", "phi", "phi1", "costhetaZ1", "costhetaZ2", "costhetastar"]   

#obsNames=["rapidity4l", "costhetaZ1"]
#obsNames=["pT4l", "rapidity4l", "massZ1", "massZ2"]
#obsNames=["mass4l","pT4l", "rapidity4l", "massZ1", "massZ2","phi", "phi1", "costhetaZ1", "costhetaZ2", "costhetastar"]
#obsNames=["pTj1", "pTj2", "mjj", "absdetajj", "dphijj", "pTHjj","Nj","pTHj", "mHj", "TCjmax", "TBjmax"]
#obsNames=["massZ1_massZ2", "rapidity4l_pT4l", "pTj1_pTj2", "Nj_pT4l", "pT4l_pTHj", "absdetajj_mjj","TCjmax_pT4l"]

obsNames= ["mass4l"]

#obsNames=["pTj1_pTj2", "Nj_pT4l", "pT4l_pTHj", "absdetajj_mjj","TCjmax_pT4l"]
#obsNames=["pTj1_pTj2"]
#obsNames=["Nj","pTHj", "mHj", "TCjmax", "TBjmax"] #2024 _3
#obsNames=["TCjmax", "TBjmax"]
#obsNames=["mjj"]
#obsNames=["absdetajj_mjj","massZ1_massZ2,TCjmax_pT4l]
#obsNames=["mass4l"]

#"pT4l", "rapidity4l"

#YEARS = ["2022","2022EE","2023preBPix", "2023postBPix", "2024"]
#YEARS = ["2024"]
#YEARS = ["2022EE"]
YEARS = ["Run3"]

#YEARS = ["2022", "2022EE"]
#YEARS = ["2022full"] 

years = []


if DO_SPLIT:
    for YEAR in YEARS:
        if split[YEAR]:
            nSplit = split[YEAR]
            for i in range(0,nSplit):
                years.append(YEAR+"_"+str(i+1))
else:
    years = YEARS
    
with open("input_args.txt", "w") as f:
    for obs in obsNames:
        for year in years:
            f.write(f'{obs} {year}\n')
