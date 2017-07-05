from HiggsAnalysis.CombinedLimit.PhysicsModel import *

class ttbbttjjFitModel(PhysicsModel):
    def __init__(self):
        pass
    def setModelBuilder(self, modelBuilder):
        "Connect to the ModelBuilder to get workspace, datacard and options. Should not be overloaded."
        self.modelBuilder = modelBuilder
        self.DC = modelBuilder.DC
        self.options = modelBuilder.options
    def setPhysicsOptions(self,physOptions):
        "Receive a list of strings with the physics options from command line"
        pass
    def doParametersOfInterest(self):
        """Create POI and other parameters, and define the POI set."""
        # --- Signal Strength as only POI --- 
        self.modelBuilder.doVar("k_ttjj[1.0,0.0,5.0]");
        self.modelBuilder.doVar("R_ttbbttjj[0.02,0.0,0.5]");
        self.modelBuilder.doSet("POI",",k_ttjj,R_ttbbttjj")
        #self.modelBuilder.doSet("POI","R_ttbbttjj,k_ttjj")
        # R_ttbb/ttjj (MC) = 0.0698204 -> 1/R_ttbb/ttjj (MC) = 14.32246
        self.modelBuilder.factory_("expr::r_ttbb(\"14.32*@0*@1\",k_ttjj,R_ttbbttjj)")
        # R_ttbj/ttjj (MC) = 0.108879 -> 1/R_ttbj/ttjj (MC) = 9.184508
        # R_ttbj/ttbb (MC) = 1.55941
        # R_ttbj/ttjj*R_ttbj/ttbb = 
        self.modelBuilder.factory_("expr::r_ttbj(\"14.32*@0*@1\",k_ttjj,R_ttbbttjj)")
        # R_ttccLF/ttjj (MC) = 0.821301 -> 1/R_ttccLF/ttjj (MC) = 1.217580
        # 1.0 + R_ttbj/ttbb (MC) = 2.55941
        self.modelBuilder.factory_("expr::r_ttccLF(\"1.22*@0*(1.0-2.55941*@1)\",k_ttjj,R_ttbbttjj)")
        self.modelBuilder.factory_("expr::r_Bkgtt(\"@0\",k_ttjj)")
        # -------------------------------------------------------------
        # --- Higgs Mass as other parameter ----
        if self.options.mass != 0:
            if self.modelBuilder.out.var("MH"):
              self.modelBuilder.out.var("MH").removeRange()
              self.modelBuilder.out.var("MH").setVal(self.options.mass)
            else:
              self.modelBuilder.doVar("MH[%g]" % self.options.mass); 
    def preProcessNuisances(self,nuisances):
        "receive the usual list of (name,nofloat,pdf,args,errline) to be edited"
        pass # do nothing by default
    def getYieldScale(self,bin,process):
        "Return the name of a RooAbsReal to scale this yield by or the two special values 1 and 0 (don't scale, and set to zero)"
        if process in ['ttbar_LepJetsPowhegPythiattbb']:
            return "r_ttbb"
        if process in ['ttbar_LepJetsPowhegPythiattbj']:
            return "r_ttbj"
        if process in ['ttbar_LepJetsPowhegPythiattcc']:
            return "r_ttccLF"
        if process in ['ttbar_LepJetsPowhegPythiattLF']:
            return "r_ttccLF"
        if process in ['ttbar_PowhegPythiaBkgtt']:
            return "r_Bkgtt"
        else:
            return 1
    def getChannelMask(self, bin):
        "Return the name of a RooAbsReal to mask the given bin (args != 0 => masked)"
        name = 'mask_%s' % bin
        # Check that the mask expression does't exist already, it might do
        # if it was already defined in the datacard
        if not self.modelBuilder.out.arg(name):
            self.modelBuilder.doVar('%s[0]' % name)
        return name
    def done(self):
        "Called after creating the model, except for the ModelConfigs"
        pass
##-------------------------------------
# class ttbbttjjVisFitModel(PhysicsModel):
#     def __init__(self):
#         pass
#     def setModelBuilder(self, modelBuilder):
#         "Connect to the ModelBuilder to get workspace, datacard and options. Should not be overloaded."
#         self.modelBuilder = modelBuilder
#         self.DC = modelBuilder.DC
#         self.options = modelBuilder.options
#     def setPhysicsOptions(self,physOptions):
#         "Receive a list of strings with the physics options from command line"
#         pass
#     def doParametersOfInterest(self):
#         """Create POI and other parameters, and define the POI set."""
#         # --- Signal Strength as only POI --- 
#         self.modelBuilder.doVar("k_ttjj[1.0,0.0,5.0]");
#         self.modelBuilder.doVar("R_ttbbttjj[0.02,0.0,0.5]");
#         self.modelBuilder.doVar("xsec_ttjj[]");
#         self.modelBuilder.doVar("Eff_ttjj[]");
#         self.modelBuilder.doVar("Acc_ttjj[]");
#         self.modelBuilder.doVar("Eff_ttbb[]");
#         self.modelBuilder.doVar("Acc_ttbb[]");
#         self.modelBuilder.doVar("N_ttjj[]");
#         self.modelBuilder.doSet("POI","R_ttbbttjj,k_ttjj")
#         # R_ttbb/ttjj (MC) = 0.0698204 -> 1/R_ttbb/ttjj (MC) = 14.32246
#         self.modelBuilder.factory_("expr::r_ttbb(\"14.32*@0*@1\",k_ttjj,R_ttbbttjj)")
#         # R_ttbj/ttjj (MC) = 0.108879 -> 1/R_ttbj/ttjj (MC) = 9.184508
#         # R_ttbj/ttbb (MC) = 1.55941
#         # R_ttbj/ttjj*R_ttbj/ttbb = 
#         self.modelBuilder.factory_("expr::r_ttbj(\"14.32*@0*@1\",k_ttjj,R_ttbbttjj)")
#         # R_ttccLF/ttjj (MC) = 0.821301 -> 1/R_ttccLF/ttjj (MC) = 1.217580
#         # 1.0 + R_ttbj/ttbb (MC) = 2.55941
#         self.modelBuilder.factory_("expr::r_ttccLF(\"1.22*@0*(1.0-2.55941*@1)\",k_ttjj,R_ttbbttjj)")
#         self.modelBuilder.factory_("expr::r_Bkgtt(\"@0\",k_ttjj)")
#         # -------------------------------------------------------------
#         # --- Higgs Mass as other parameter ----
#         if self.options.mass != 0:
#             if self.modelBuilder.out.var("MH"):
#               self.modelBuilder.out.var("MH").removeRange()
#               self.modelBuilder.out.var("MH").setVal(self.options.mass)
#             else:
#               self.modelBuilder.doVar("MH[%g]" % self.options.mass); 
#     def preProcessNuisances(self,nuisances):
#         "receive the usual list of (name,nofloat,pdf,args,errline) to be edited"
#         pass # do nothing by default
#     def getYieldScale(self,bin,process):
#         "Return the name of a RooAbsReal to scale this yield by or the two special values 1 and 0 (don't scale, and set to zero)"
#         if process in ['ttbar_LepJetsPowhegPythiattbb']:
#             return "r_ttbb"
#         if process in ['ttbar_LepJetsPowhegPythiattbj']:
#             return "r_ttbj"
#         if process in ['ttbar_LepJetsPowhegPythiattcc']:
#             return "r_ttccLF"
#         if process in ['ttbar_LepJetsPowhegPythiattLF']:
#             return "r_ttccLF"
#         if process in ['ttbar_PowhegPythiaBkgtt']:
#             return "r_Bkgtt"
#         else:
#             return 1
#     def getChannelMask(self, bin):
#         "Return the name of a RooAbsReal to mask the given bin (args != 0 => masked)"
#         name = 'mask_%s' % bin
#         # Check that the mask expression does't exist already, it might do
#         # if it was already defined in the datacard
#         if not self.modelBuilder.out.arg(name):
#             self.modelBuilder.doVar('%s[0]' % name)
#         return name
#     def done(self):
#         "Called after creating the model, except for the ModelConfigs"
#         pass

# ##-------------------------------------
# class ttbbttjjFullFitModel(PhysicsModel):
#     def __init__(self):
#         pass
#     def setModelBuilder(self, modelBuilder):
#         "Connect to the ModelBuilder to get workspace, datacard and options. Should not be overloaded."
#         self.modelBuilder = modelBuilder
#         self.DC = modelBuilder.DC
#         self.options = modelBuilder.options
#     def setPhysicsOptions(self,physOptions):
#         "Receive a list of strings with the physics options from command line"
#         pass
#     def doParametersOfInterest(self):
#         """Create POI and other parameters, and define the POI set."""
#         # --- Signal Strength as only POI --- 
#         self.modelBuilder.doVar("k_ttjj[1.0,0.0,5.0]");
#         self.modelBuilder.doVar("R_ttbbttjj[0.02,0.0,0.5]");
#         self.modelBuilder.doSet("POI","R_ttbbttjj,k_ttjj")
#         # R_ttbb/ttjj (MC) = 0.0698204 -> 1/R_ttbb/ttjj (MC) = 14.32246
#         self.modelBuilder.factory_("expr::r_ttbb(\"14.32*@0*@1\",k_ttjj,R_ttbbttjj)")
#         # R_ttbj/ttjj (MC) = 0.108879 -> 1/R_ttbj/ttjj (MC) = 9.184508
#         # R_ttbj/ttbb (MC) = 1.55941
#         # R_ttbj/ttjj*R_ttbj/ttbb = 
#         self.modelBuilder.factory_("expr::r_ttbj(\"14.32*@0*@1\",k_ttjj,R_ttbbttjj)")
#         # R_ttccLF/ttjj (MC) = 0.821301 -> 1/R_ttccLF/ttjj (MC) = 1.217580
#         # 1.0 + R_ttbj/ttbb (MC) = 2.55941
#         self.modelBuilder.factory_("expr::r_ttccLF(\"1.22*@0*(1.0-2.55941*@1)\",k_ttjj,R_ttbbttjj)")
#         self.modelBuilder.factory_("expr::r_Bkgtt(\"@0\",k_ttjj)")
#         # -------------------------------------------------------------
#         # --- Higgs Mass as other parameter ----
#         if self.options.mass != 0:
#             if self.modelBuilder.out.var("MH"):
#               self.modelBuilder.out.var("MH").removeRange()
#               self.modelBuilder.out.var("MH").setVal(self.options.mass)
#             else:
#               self.modelBuilder.doVar("MH[%g]" % self.options.mass); 
#     def preProcessNuisances(self,nuisances):
#         "receive the usual list of (name,nofloat,pdf,args,errline) to be edited"
#         pass # do nothing by default
#     def getYieldScale(self,bin,process):
#         "Return the name of a RooAbsReal to scale this yield by or the two special values 1 and 0 (don't scale, and set to zero)"
#         if process in ['ttbar_LepJetsPowhegPythiattbb']:
#             return "r_ttbb"
#         if process in ['ttbar_LepJetsPowhegPythiattbj']:
#             return "r_ttbj"
#         if process in ['ttbar_LepJetsPowhegPythiattcc']:
#             return "r_ttccLF"
#         if process in ['ttbar_LepJetsPowhegPythiattLF']:
#             return "r_ttccLF"
#         if process in ['ttbar_PowhegPythiaBkgtt']:
#             return "r_Bkgtt"
#         else:
#             return 1
#     def getChannelMask(self, bin):
#         "Return the name of a RooAbsReal to mask the given bin (args != 0 => masked)"
#         name = 'mask_%s' % bin
#         # Check that the mask expression does't exist already, it might do
#         # if it was already defined in the datacard
#         if not self.modelBuilder.out.arg(name):
#             self.modelBuilder.doVar('%s[0]' % name)
#         return name
#     def done(self):
#         "Called after creating the model, except for the ModelConfigs"
#         pass

ttbbttjjFitModel     = ttbbttjjFitModel()
# ttbbttjjVisFitModel  = ttbbttjjVisFitModel()
# ttbbttjjFullFitModel = ttbbttjjFullFitModel()
