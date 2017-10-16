

__license__ = "AGPLv3"
__author__ = "Jean-Christophe Fabre <jean-christophe.fabre@inra.fr>"


from FluidHub.ConfigManager import ConfigMan


################################################################################
################################################################################


def initTemplateVariables() :
  Vars = dict()
  Vars["Breadcrumbs"] = list()
  Vars["Title"] = ConfigMan.get("ui","title","no title")

  return Vars
