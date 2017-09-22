
__license__ = "AGPLv3"
__author__ = "Jean-Christophe Fabre <jean-christophe.fabre@inra.fr>"


import glob, os

from flask import Blueprint,render_template,request,abort

from FluidHub.ConfigManager import ConfigMan
from FluidHub import Constants

from FluidHub.WaresOperations import WaresOperations


################################################################################
################################################################################


wareshubUI = Blueprint('wareshubUI',__name__,
                       template_folder=os.path.join(os.path.dirname(os.path.abspath(__file__)),"templates"),
                       static_folder=os.path.join(os.path.dirname(os.path.abspath(__file__)),"static"))

WaresOps = WaresOperations()


################################################################################
################################################################################


def initTemplateVariables(WareType) :
  Vars = dict()
  Vars["WaresType"] = WareType
  Vars["WaresTypeSingular"] = Constants.WareTypesNamesSingular[WareType]
  Vars["Title"] = ConfigMan.get("wareshub","ui.title","no title")

  return Vars


################################################################################


def buildWaresListVars(WareType,WaresInfos,WaresDetails) :

  # TODO check if generated URL is correct
  PortColon = ""
  Port = ConfigMan.get("global","url-port","")
  if Port :
    PortColon = ":%s" % Port

  ClientURL = [ ConfigMan.get("global","url-protocol"),"://",
                ConfigMan.get("global","url-host"),PortColon,
              ]

  WaresCount = len(WaresInfos[WareType])

  TypesButtons = []
  for WType in Constants.WareTypes :
    TypesButtons.append(dict(Name=WType,
                             Title=Constants.WareTypesNames[WType].capitalize(),
                             Count=len(WaresInfos[WType]),
                             Active=(WType==WareType)))

  WaresList = []
  for Key in sorted(WaresDetails) :
    Infos = dict()
    Infos["ID"] = Key
    # TODO to be completed with versions, etc...
    WaresList.append(Infos)

  # TODO display doc availability
  # TODO display compatible versions based on git branches

  Vars = initTemplateVariables(WareType)
  Vars["WelcText"] = ConfigMan.get("wareshub","ui.welctext","no title")
  Vars["ClientURL"] = "".join(ClientURL)
  Vars["TypesButtons"] = TypesButtons
  Vars["WaresCount"] = WaresCount
  Vars["WaresList"] = WaresList

  return Vars


################################################################################
################################################################################


@wareshubUI.errorhandler(404)
def Manage404(e):
  Vars = initTemplateVariables(Constants.WareTypes[0])
  return render_template('404.html',**Vars), 404


################################################################################


@wareshubUI.errorhandler(500)
def Manage500(e):
  Vars = initTemplateVariables(Constants.WareTypes[0])
  return render_template('500.html',**Vars), 500


################################################################################


@wareshubUI.route("/")
def Root():

  Code,WaresInfos = WaresOps.getAllWaresInfo()
  if Code != 200 :
    # TODO manage this better
    abort(500)

  Code,WaresDetails = WaresOps.getWaresInfo(Constants.WareTypes[0])
  if Code != 200 :
    # TODO manage this better
    abort(500)


  Vars = buildWaresListVars(Constants.WareTypes[0],WaresInfos,WaresDetails)

  return render_template("wareslist.html",**Vars)


################################################################################


@wareshubUI.route("/<string:ware_type>")
def GetWares(ware_type):

  if ware_type not in Constants.WareTypes :
    # TODO manage this better
    abort(404)

  Code,WaresInfos = WaresOps.getAllWaresInfo()
  if Code != 200 :
    # TODO manage this better
    abort(500)

  Code,WaresDetails = WaresOps.getWaresInfo(ware_type)
  if Code != 200 :
    # TODO manage this better
    abort(500)


  Vars = buildWaresListVars(ware_type,WaresInfos,WaresDetails)

  return render_template("wareslist.html",**Vars)


################################################################################


@wareshubUI.route("/<string:ware_type>/<string:ware_id>")
def GetWare(ware_type,ware_id):

  if ware_type not in Constants.WareTypes :
    # TODO manage this better
    abort(404)

  WareDef = WaresOps.getWareDefinition(ware_type,ware_id)
  if not WareDef :
    # TODO manage this better
    abort(404)

  # TODO display compatibility info based on git branches
  # TODO display contributors
  # TODO show informations (tags, status, commits, issues) by git branch

  Vars = initTemplateVariables(ware_type)
  Vars["WareID"] = ware_id
  Vars["FallbackType"] = Constants.WareTypes[0]
  Vars["Def"] = {
                  'ShortDesc' : WareDef["shortdesc"],
                  'UsersRO' : WareDef["users-ro"],
                  'UsersRW' : WareDef["users-rw"]
                }
  print Vars["Def"]
  Vars["WareDoc"] = None
  Vars["GitURL"] = WaresOps.getWareGitURL(ware_type,ware_id)
  Vars["GitInfos"] = dict()
  Vars["SelectedGitBranch"] = request.args.get("branch",None)

  return render_template("waredetails.html",**Vars)
