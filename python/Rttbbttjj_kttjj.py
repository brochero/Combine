##-------------------------------------
class ttbbttjjFullPhSpFitModel(PhysicsModel):
    def __init__(self):
        pass
    def setModelBuilder(self, modelBuilder):
        "Connect to the ModelBuilder to get workspace, datacard and options. Should not be overloaded."
        self.modelBuilder = modelBuilder
        self.DC = modelBuilder.DC
        self.options = modelBuilder.options
    def setPhysicsOptions(self,physOptions):
        "Receive a list of strings with the physics options from command line"
        
        self.Ettbb = float(0.20)
        self.Attbb = float(0.30)
        self.Ettjj = float(0.05)
        self.Attjj = float(0.24)
        self.Lumin = float(3500.0)

        self.RMC_ttbbttjj   = float(0.0698204)
        self.RMC_ttbjttjj   = float(0.108879)
        self.RMC_ttccLFttjj = float(0.821301)
        self.RMC_ttbjttbb   = float(1.55941)

        self.xsecFullttjj = float(290.0)
        
        for po in physOptions:

            if po.startswith("RMC_ttbbttjj"): 
                self.RMC_ttbbttjj = float((po.replace("RMC_ttbbttjj=","").split(","))[0])
            if po.startswith("RMC_ttbjttjj"): 
                self.RMC_ttbjttjj = float((po.replace("RMC_ttbjttjj=","").split(","))[0])
            if po.startswith("RMC_ttccLFttjj"): 
                self.RMC_ttccLFttjj = float((po.replace("RMC_ttccLFttjj=","").split(","))[0])
            if po.startswith("RMC_ttbjttbb"): 
                self.RMC_ttbjttbb = float((po.replace("RMC_ttbjttbb=","").split(","))[0])

            if po.startswith("E_ttbb"): 
                self.Ettbb = float((po.replace("E_ttbb=","").split(","))[0])
            if po.startswith("A_ttbb"): 
                self.Attbb = float((po.replace("A_ttbb=","").split(","))[0])
            if po.startswith("E_ttjj"): 
                self.Ettjj = float((po.replace("E_ttjj=","").split(","))[0])
            if po.startswith("A_ttjj"): 
                self.Attjj = float((po.replace("A_ttjj=","").split(","))[0])

            if po.startswith("Luminosity"): 
                self.Lumin = float((po.replace("Luminosity=","").split(","))[0])

            if po.startswith("xsecFullttjj"): 
                self.xsecFullttjj = float((po.replace("xsecFullttjj=","").split(","))[0])
                
        print "ttjj Efficiency set to " + str(self.Ettjj) 
        print "ttjj Acceptance set to " + str(self.Attjj) 
        print "ttbb Efficiency set to " + str(self.Ettbb) 
        print "ttbb Acceptance set to " + str(self.Attbb) 
        print "Luminosity set to " + str(self.Lumin) 

        pass
    def doParametersOfInterest(self):
        """Create POI and other parameters, and define the POI set."""

        # --- Signal Strength as only POI --- 
        self.modelBuilder.doVar("r_FullPhSp[0.013,0.001,0.04]");
        self.modelBuilder.doVar("xsec_FullPhSp_ttjj[290.0, 150.0, 400.0]");

        self.modelBuilder.doVar("xsec_FullPhSp_ttjj_MC[%s]" % (self.xsecFullttjj));
        self.modelBuilder.doVar("E_ttbb[%s]" % (self.Ettbb));
        self.modelBuilder.doVar("E_ttjj[%s]" % (self.Ettjj));
        self.modelBuilder.doVar("A_ttbb[%s]" % (self.Attbb));
        self.modelBuilder.doVar("A_ttjj[%s]" % (self.Attjj));
        self.modelBuilder.doVar("Lumi[%s]" % (self.Lumin));

        self.modelBuilder.factory_("expr::R_ttbbttjj(\"@0*((@1*@2)/(@3*@4))\",r_FullPhSp,E_ttbb,A_ttbb,E_ttjj,A_ttjj)")
        self.modelBuilder.factory_("expr::k_ttjj(\"@0/@1\",xsec_FullPhSp_ttjj,xsec_FullPhSp_ttjj_MC)")
        # Setup of the POI
        # self.modelBuilder.doSet("POI","r_FullPhSp,xsec_FullPhSp_ttjj")
        self.modelBuilder.doSet("POI","xsec_FullPhSp_ttjj,r_FullPhSp")

        self.modelBuilder.factory_("expr::r_ttbb(\"%s*@0*@1\",k_ttjj,R_ttbbttjj)" % (1.0/self.RMC_ttbbttjj))

        self.modelBuilder.factory_("expr::r_ttbj(\"%s*@0*@1\",k_ttjj,R_ttbbttjj)" % (self.RMC_ttbjttbb/self.RMC_ttbjttjj))

        self.modelBuilder.factory_("expr::r_ttccLF(\"%s*@0*(1.0-%s*@1)\",k_ttjj,R_ttbbttjj)" % (1.0/self.RMC_ttccLFttjj,(1.0+self.RMC_ttbjttbb)))

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

ttbbttjjFullPhSpFitModel = ttbbttjjFullPhSpFitModel()
