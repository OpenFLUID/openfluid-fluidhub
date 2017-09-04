
__license__ = "AGPLv3"
__author__ = "Jean-Christophe Fabre <jean-christophe.fabre@inra.fr>"


import glob, os

from flask import Flask,render_template,request,abort

from fluidhubcommon import ConfigManager
from fluidhubcommon import Constants

from fluidhubcommon.WaresOperations import WaresOperations


################################################################################
################################################################################


app = Flask(__name__,template_folder=os.path.join(os.path.dirname(os.path.abspath(__file__)),"templates"))

Config = ConfigManager.get()
WaresOps = WaresOperations()


################################################################################
################################################################################


def initTemplateVariables(WareType) :
  Vars = dict()
  Vars["WaresType"] = WareType
  Vars["WaresTypeSingular"] = Constants.WareTypesNamesSingular[WareType]
  Vars["Title"] = Config.get("wareshub","ui.title","no title")

  return Vars


################################################################################


def buildWaresListVars(WareType,WaresInfos,WaresDetails) :

  # TODO check if generated URL is correct
  PortColon = ""
  Port = Config.get("wareshub","gitserver.url-port","")
  if Port :
    PortColon = ":%s" % Port

  ClientURL = [ Config.get("global","url-protocol"),"://",
                Config.get("global","url-host"),PortColon,
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
    # TODO to be completed
    WaresList.append(Infos)

  Vars = initTemplateVariables(WareType)
  Vars["WelcText"] = Config.get("wareshub","ui.welctext","no title")
  Vars["ClientURL"] = "".join(ClientURL)
  Vars["TypesButtons"] = TypesButtons
  Vars["WaresCount"] = WaresCount
  Vars["WaresList"] = WaresList

  return Vars


################################################################################
################################################################################


@app.errorhandler(404)
def Manage404(e):
  Vars = initTemplateVariables(Constants.WareTypes[0])
  return render_template('404.html',**Vars), 404


################################################################################


@app.route("/")
def root():

  Code,WaresInfos = WaresOps.getAllWaresInfo()
  if Code != 200 :
   # TODO manage this better
   abort(404)

  Code,WaresInfos = WaresOps.getAllWaresInfo()
  if Code != 200 :
   # TODO manage this better
   abort(404)

  Code,WaresDetails = WaresOps.getWaresInfo(Constants.WareTypes[0])
  if Code != 200 :
   # TODO manage this better
   abort(404)


  Vars = buildWaresListVars(Constants.WareTypes[0],WaresInfos,WaresDetails)

  return render_template("wareslist.html",**Vars)


################################################################################


@app.route("/<string:ware_type>")
def GetWares(ware_type):

  if ware_type not in Constants.WareTypes :
    # TODO manage this better
    abort(404)

  Code,WaresInfos = WaresOps.getAllWaresInfo()
  if Code != 200 :
   # TODO manage this better
   abort(404)

  Code,WaresDetails = WaresOps.getWaresInfo(ware_type)
  if Code != 200 :
   # TODO manage this better
   abort(404)


  Vars = buildWaresListVars(ware_type,WaresInfos,WaresDetails)

  return render_template("wareslist.html",**Vars)


################################################################################


@app.route("/<string:ware_type>/<string:ware_id>")
def GetWare(ware_type,ware_id):

  if ware_type not in Constants.WareTypes :
    # TODO manage this better
    abort(404)

  WareDef = WaresOps.getWareDefinition(ware_type,ware_id)

  if not WareDef :
    # TODO manage this better
    abort(404)

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


################################################################################
################################################################################


if __name__ == '__main__':
  app.run(port=Config.get("wareshub","ui.port"))
