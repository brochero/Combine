# Fit Parameters (From TablesYields.run)
# Luminosity
Par_Lum="--PO Luminosity=35870.0" 
# Efficiencies and Acceptances for ttbb and ttjj
Par_EffAcc="--PO E_ttbb=0.20 --PO E_ttjj=0.05 --PO A_ttbb=0.30 --PO A_ttjj=0.24"
# R_tt*/ttjj from MC (used to setup the model)
Par_MCRatios="--PO RMC_ttbbttjj=0.0696869 --PO RMC_ttbjttjj=0.109244 --PO RMC_ttccLFttjj=0.821069 --PO RMC_ttbjttbb=1.56764"

# DataCard reference name
DCRefName=${1}

# Go to DataCards directory (to avoid additional directories in the input files of the DC)
cd DataCards

# Combine DataCards of mu+Jets and e+Jets
echo "--------------------------------------------------------------------------------------"
echo "Combined DataCards for both decay modes: muon+Jets and e+Jets"
echo "--------------------------------------------------------------------------------------"
combineCards.py Name1=DataCard_mujets_${DCRefName}.txt Name2=DataCard_ejets_${DCRefName}.txt > DataCard_ljets_${DCRefName}.txt

# Create WorkSpace with the Lep+Jets DataCard
echo "--------------------------------------------------------------------------------------"
echo "Creating WS using ttbbttjjFullPhSp model"
echo "--------------------------------------------------------------------------------------"
text2workspace.py -P HiggsAnalysis.CombinedLimit.Rttbbttjj_kttjj:ttbbttjjFullPhSpFitModel $Par_MCRatios $Par_EffAcc $Par_Lum DataCard_ljets_${DCRefName}.txt -o ../CombineWS/DataCard_ljets_${DCRefName}.root

# Return to main directory
cd ../

# Perfore Fit
FitOutDir=CombineResults/FitResults_Xsec_${DCRefName}
mkdir ${FitOutDir}
echo "--------------------------------------------------------------------------------------"
echo "Fitting WS: MultiDimFit "
echo "--------------------------------------------------------------------------------------"
#combine -M MaxLikelihoodFit --saveShapes --saveWithUncertainties --plot --out CombineResults CombineWS/DataCard_ljets_${DCRefName}.root

# Performe Fit
echo "--------------------------------------------------------------------------------------"
echo "Fitting WS: MaxLikelihoodFitcombine -M MultiDimFit "
echo "--------------------------------------------------------------------------------------"

# Expected with --expectSignal=1
mkdir ${FitOutDir}/EXPECTED
echo "------------------------------------"
echo "Fitting WS: Expected................"
echo "------------------------------------"
combine CombineWS/DataCard_ljets_${DCRefName}.root -M MaxLikelihoodFit --saveShapes --saveWithUncertainties --plot -m 0 -t -1 --expectSignal=1 --out ${FitOutDir}/EXPECTED
# Impacts: to produce the breackdown of systematics (in EXPECTED):
# - Initial Fit
echo "Initial Fit"
combineTool.py -M Impacts -d CombineWS/DataCard_ljets_${DCRefName}.root -m 0 -t -1 --expectSignal=1 --doInitialFit 
# - Fit
echo "Fit"
combineTool.py -M Impacts -d CombineWS/DataCard_ljets_${DCRefName}.root -m 0 -t -1 --expectSignal=1 --doFits --parallel 4 
# - Extract impact of the nuisance parameters
echo "Extracting impact of the nuisance parameters"
combineTool.py -M Impacts -d CombineWS/DataCard_ljets_${DCRefName}.root -m 0 -o ${FitOutDir}/EXPECTED/impacts_${DCRefName}.json
# - Create plot with the impacts
echo "Ploting impact of the nuisance parameters"
plotImpacts.py -i ${FitOutDir}/EXPECTED/impacts_${DCRefName}.json -o ${FitOutDir}/EXPECTED/impacts_${1}
# - after run all the EXPECTED fits, move files to CombineResults
echo "Moving files"
mv higgsCombineTest.MaxLikelihoodFit.mH0.root higgsCombine_initialFit_Test.MultiDimFit.mH0.root higgsCombine_paramFit_Test_*.MultiDimFit.mH0.root ${FitOutDir}/EXPECTED/

# Scan (EXPECTED)
combine CombineWS/DataCard_ljets_${DCRefName}.root -M MultiDimFit -P xsec_FullPhSp_ttjj -t -1 --expectSignal=1 --algo=grid --points=100 -m 0 
mv higgsCombineTest.MultiDimFit.mH0.root ${FitOutDir}/EXPECTED/Scan_EXPECTED_xsec_FullPhSp_ttjj.root
# Scan with Statistical error ONLY (-S 0) (EXPECTED)
combine CombineWS/DataCard_ljets_${DCRefName}.root -M MultiDimFit -P xsec_FullPhSp_ttjj -t -1 --expectSignal=1 --algo=grid --points=100 -m 0 -S 0
mv higgsCombineTest.MultiDimFit.mH0.root ${FitOutDir}/EXPECTED/Scan_EXPECTED_xsec_FullPhSp_ttjj_Stat.root


# Observed
mkdir ${FitOutDir}/OBSERVED
echo "------------------------------------"
echo "Fitting WS: Observed................"
echo "------------------------------------"
combine CombineWS/DataCard_ljets_${DCRefName}.root -M MaxLikelihoodFit --saveShapes --saveWithUncertainties -m 0 --plot --out ${FitOutDir}/OBSERVED
# Impacts: to produce the breackdown of systematics (in OBSERVED):
# - Initial Fit
echo "Initial Fit"
combineTool.py -M Impacts -d CombineWS/DataCard_ljets_${DCRefName}.root -m 0 --doInitialFit 
# - Fit
echo "Fit"
combineTool.py -M Impacts -d CombineWS/DataCard_ljets_${DCRefName}.root -m 0 --doFits --parallel 4 
# - Extract impact of the nuisance parameters
echo "Extracting impact of the nuisance parameters"
combineTool.py -M Impacts -d CombineWS/DataCard_ljets_${DCRefName}.root -m 0 -o ${FitOutDir}/OBSERVED/impacts_${DCRefName}.json
# - Create plot with the impacts
echo "Ploting impact of the nuisance parameters"
plotImpacts.py -i ${FitOutDir}/OBSERVED/impacts_${DCRefName}.json -o ${FitOutDir}/OBSERVED/impacts_${1}
# - after run all the OBSERVED fits, move files to CombineResults
echo "Moving files"
mv higgsCombineTest.MaxLikelihoodFit.mH0.root higgsCombine_initialFit_Test.MultiDimFit.mH0.root higgsCombine_paramFit_Test_*.MultiDimFit.mH0.root ${FitOutDir}/OBSERVED/

# Scan (OBSERVED)
combine CombineWS/DataCard_ljets_${DCRefName}.root -M MultiDimFit -P xsec_FullPhSp_ttjj --saveWorkspace --algo=grid --points=100 -m 0 
mv higgsCombineTest.MultiDimFit.mH0.root ${FitOutDir}/OBSERVED/Scan_OBSERVED_xsec_FullPhSp_ttjj.root
# Scan with Statistical error ONLY (-S 0) (OBSERVED)
combine ${FitOutDir}/OBSERVED/Scan_OBSERVED_xsec_FullPhSp_ttjj.root -M MultiDimFit -P xsec_FullPhSp_ttjj --algo=grid --points=100 -m 0 --freezeNuisances all --snapshotName "MultiDimFit"
mv higgsCombineTest.MultiDimFit.mH0.root ${FitOutDir}/OBSERVED/Scan_OBSERVED_xsec_FullPhSp_ttjj_Stat.root



