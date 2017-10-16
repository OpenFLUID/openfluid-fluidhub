

__license__ = "AGPLv3"
__author__ = "Jean-Christophe Fabre <jean-christophe.fabre@inra.fr>"


from flask import render_template,request,abort,session

from FluidHub.ConfigManager import ConfigMan

import uiCommon


################################################################################
################################################################################


def initTemplateVariables() :
  Vars = uiCommon.initTemplateVariables()

  Vars["WelcText"] = ConfigMan.get("ui","welctext","no text")

  # TODO check if generated URL is correct
  PortColon = ""
  Port = ConfigMan.get("global","url-port","")
  if Port :
    PortColon = ":%s" % Port

  ClientURL = [
                ConfigMan.get("global","url-protocol"),"://",
                ConfigMan.get("global","url-host"),PortColon,
              ]

  Vars["ClientURL"] = "".join(ClientURL)

  return Vars


################################################################################


def render():
  Vars = initTemplateVariables()

  return render_template("home.html",**Vars)
