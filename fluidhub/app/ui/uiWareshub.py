
__license__ = "AGPLv3"
__author__ = "Jean-Christophe Fabre <jean-christophe.fabre@inra.fr>"


from flask import render_template,request,abort,session
from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField
from wtforms.validators import DataRequired

from FluidHub import Constants
from FluidHub.ConfigManager import ConfigMan
from FluidHub.WaresOperations import WaresOperations

import uiCommon


################################################################################
################################################################################


class SearchForm(FlaskForm):
    Terms = StringField('Searched terms', validators=[DataRequired()])
    Search = SubmitField("Search")



WaresOps = WaresOperations()


################################################################################
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

  Vars = uiCommon.initTemplateVariables()
  Vars["WaresType"] = WareType
  Vars["WaresTypeSingular"] = Constants.WareTypesNamesSingular[WareType]
  Vars["ClientURL"] = "".join(ClientURL)
  Vars["TypesButtons"] = TypesButtons
  Vars["WaresCount"] = WaresCount
  Vars["WaresList"] = WaresList

  return Vars


################################################################################


def renderWaresList(WaresType):

  SearchF = SearchForm()

  if WaresType not in Constants.WareTypes :
    # TODO manage this better
    abort(404)

  SearchFilter = None
  if SearchF.validate_on_submit():
    SearchFilter = SearchF.Terms.data

  Code,WaresInfos = WaresOps.getAllWaresInfo()
  if Code != 200 :
    # TODO manage this better
    abort(500)

  Code,WaresDetails = WaresOps.getWaresInfo(WaresType)
  if Code != 200 :
    # TODO manage this better
    abort(500)

  Vars = buildWaresListVars(WaresType,WaresInfos,WaresDetails)

  Vars["SearchF"] = SearchF

  return render_template("wareslist.html",**Vars)


################################################################################


def renderWareDetails(WareType,WareID):


    Username = None
    if "username" in session:
      Username = session["username"]

    if WareType not in Constants.WareTypes :
      # TODO manage this better
      abort(404)

    WareDef = WaresOps.getWareDefinition(WareType,WareID)
    if not WareDef :
      # TODO manage this better
      abort(404)

    # TODO display compatibility info based on git branches
    # TODO display contributors
    # TODO show informations (tags, status, commits, issues) by git branch

    Vars = uiCommon.initTemplateVariables()
    Vars["WaresType"] = WareType
    Vars["WaresTypeSingular"] = Constants.WareTypesNamesSingular[WareType]
    Vars["WareID"] = WareID
    Vars["FallbackType"] = Constants.WareTypes[0]
    Vars["Def"] = {
                    'ShortDesc' : WareDef["shortdesc"],
                    'UsersRO' : WareDef["users-ro"],
                    'UsersRW' : WareDef["users-rw"]
                  }
    Vars["WareDoc"] = None
    Vars["GitURL"] = WaresOps.getWareGitURL(WareType,WareID,Username)
    Vars["GitInfos"] = dict()
    Vars["SelectedGitBranch"] = request.args.get("branch",None)

    return render_template("waredetails.html",**Vars)
