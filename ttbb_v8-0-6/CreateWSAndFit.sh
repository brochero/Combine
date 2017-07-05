# Create WS
text2workspace.py -P HiggsAnalysis.CombinedLimit.Rttbbttjj_kttjj:ttbbttjjFitModel ${1}.txt

# Perfore Fit
combine -M MaxLikelihoodFit --saveShapes --saveWithUncertainties --plot --out CombineResults ${1}.root

# Change Name Result
mv CombineResults/mlfit.root CombineResults/mlfit_k_${1}.root

# Root File with info from nuisance Parameters
python $CMSSW_BASE/src/HiggsAnalysis/CombinedLimit/test/diffNuisances.py -g CombineResults/nuisances_k_${1}.root CombineResults/mlfit_k_${1}.root

combineTool.py -M Impacts -d ${1}.root -m 125 --doInitialFit
combineTool.py -M Impacts -d ${1}.root -m 125 --doFits --parallel 4
combineTool.py -M Impacts -d ${1}.root -m 125 -o CombineResults/impacts_k_${1}.json
plotImpacts.py -i CombineResults/impacts_k_${1}.json -o CombineResults/impacts_k_${1}

