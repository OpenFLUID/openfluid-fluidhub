
__license__ = "AGPLv3"
__author__ = "Jean-Christophe Fabre <jean-christophe.fabre@inra.fr>"


import hashlib

from flask import render_template,request,abort,session,url_for,g,redirect,flash,get_flashed_messages,send_file
from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,TextAreaField
from wtforms.validators import DataRequired

from FluidHub import Constants
from FluidHub import Tools
from FluidHub.ConfigManager import ConfigMan
from FluidHub.WaresOperations import WaresOperations

import uiCommon


################################################################################
################################################################################


class SearchForm(FlaskForm):
  Terms = StringField('Searched terms', validators=[DataRequired()])
  Search = SubmitField("Search")


class EditForm(FlaskForm):
  ShortDesc = TextAreaField('Short description')
  UsersRO = StringField('Read-only users')
  UsersRW = StringField('Read-write users')
  MailingList = StringField('Mailing list')

class AddForm(EditForm):
  ID = StringField('ID', validators=[DataRequired()])
  SubmitAdd = SubmitField("Add")

class UpdateForm(EditForm):
  SubmitUpdate = SubmitField("Update")

class DeleteForm(FlaskForm):
  ID = StringField('ID', validators=[DataRequired()])
  SubmitDelete = SubmitField("Delete")


WaresOps = WaresOperations()


################################################################################
################################################################################


def initTemplateVariables():
  Vars = uiCommon.initTemplateVariables()
  Vars["Breadcrumbs"].append({ "Label" : "Wares", "URL" : url_for(".WaresHome")})
  return Vars


################################################################################


def buildWaresListVars(WareType,WaresInfos,WaresDetails) :

  WaresCount = len(WaresInfos[WareType])

  WaresList = []
  for Key in sorted(WaresDetails) :
    Infos = dict()
    Infos["ID"] = Key
    Infos["Doc"] = WaresOps.getWareDocPDFPath(WareType,Key) is not None
    if "git-branches" in WaresDetails[Key]:
      Versions = Tools.getVersionsFromGitBranches(WaresDetails[Key]["git-branches"])
      if Versions :
        Infos["HigherVersion"] = Versions[0]
      else:
        Infos["HigherVersion"] = None
    else:
      Infos["HigherVersion"] = None

    WaresList.append(Infos)


  Vars = initTemplateVariables()
  Vars["CurrentOFVersion"] = ConfigMan.get("global","openfluid.currentversion","0.0")
  Vars["WaresType"] = WareType
  Vars["WaresTypeSingular"] = Constants.WareTypesNamesSingular[WareType]
  Vars["WaresCount"] = WaresCount
  Vars["WaresList"] = WaresList

  return Vars


################################################################################


def renderWaresHome():
  Code,WaresInfos = WaresOps.getAllWaresInfo()
  if Code != 200 :
    # REVIEW manage this better
    abort(500)

  TypesButtons = []
  for WType in Constants.WareTypes :
    TypesButtons.append(dict(Name=WType,
                             Title=Constants.WareTypesNames[WType].capitalize(),
                             Count=len(WaresInfos[WType])))

  Vars = initTemplateVariables()
  Vars["TypesButtons"] = TypesButtons

  return render_template("wareshome.html",**Vars)


################################################################################


def renderWaresList(WaresType):

  SearchF = SearchForm()

  if WaresType not in Constants.WareTypes :
    # REVIEW manage this better
    abort(404)

  SearchFilter = None
  if SearchF.validate_on_submit():
    SearchFilter = SearchF.Terms.data

  Code,WaresInfos = WaresOps.getAllWaresInfo()
  if Code != 200 :
    # REVIEW manage this better
    abort(500)

  Code,WaresDetails = WaresOps.getWaresInfo(WaresType)
  if Code != 200 :
    # REVIEW manage this better
    abort(500)

  Vars = buildWaresListVars(WaresType,WaresInfos,WaresDetails)
  Vars["Breadcrumbs"].append({ "Label" : Vars["WaresType"], "URL" : url_for(".WaresList",ware_type=WaresType)})
  Vars["SearchF"] = SearchF

  if g.IsAdmin :
    AddF = AddForm()
    if AddF.SubmitAdd.data and request.method == 'POST':
      if AddF.validate():
        OK = True

        UsersRO = Tools.getAsValidList(AddF.UsersRO.data,Tools.isValidUsername,True,",")
        if UsersRO is None:
          OK = False
          flash("invalid read-only users list")

        UsersRW = Tools.getAsValidList(AddF.UsersRW.data,Tools.isValidUsername,True,",")
        if UsersRW is None:
          OK = False
          flash("invalid read-write users list")

        MailingList = Tools.getAsValidList(AddF.MailingList.data,Tools.isValidEmail,False,",")
        if MailingList is None:
          OK = False
          flash("invalid mailing list")

        if OK :
          Def = dict()
          Def["shortdesc"] = AddF.ShortDesc.data
          Def["users-ro"] = UsersRO
          Def["users-rw"] = UsersRW
          Def["mailinglist"] = MailingList
          Code,ErrMsg = WaresOps.createWare(WaresType,AddF.ID.data,Def)
          if Code != 201:
            flash(ErrMsg)
      else:
        flash("invalid or incomplete form for adding %s" % Constants.WareTypesNamesSingular[WaresType])
      return redirect(url_for(".WaresList",ware_type=WaresType))

    Vars["AddF"] = AddF

  return render_template("wareslist.html",**Vars)


################################################################################


def renderWareDetails(WareType,WareID):

    Username = None
    if "username" in session:
      Username = session["username"]

    if WareType not in Constants.WareTypes :
      # REVIEW manage this better
      abort(404)

    WareDef = WaresOps.getWareDefinition(WareType,WareID)
    if not WareDef :
      # REVIEW manage this better
      abort(404)

    # TODO show informations by git branch (tags, status, commits, issues)

    Vars = initTemplateVariables()
    Vars["Breadcrumbs"].append({ "Label" : WareType, "URL" : url_for(".WaresList",ware_type=WareType)})
    Vars["Breadcrumbs"].append({ "Label" : WareID, "URL" : ""})
    Vars["WaresType"] = WareType
    Vars["WaresTypeSingular"] = Constants.WareTypesNamesSingular[WareType]
    Vars["WareID"] = WareID
    Vars["FallbackType"] = Constants.WareTypes[0]
    Vars["Def"] = {
                    'ShortDesc' : WareDef["shortdesc"],
                    'UsersRO' : WareDef["users-ro"],
                    'UsersRW' : WareDef["users-rw"],
                    'MailingList' : WareDef["mailinglist"]
                  }
    Vars["WareDoc"] = WaresOps.getWareDocPDFPath(WareType,WareID) is not None
    Vars["GitURL"] = WaresOps.getWareGitURL(WareType,WareID,Username)

    Vars["GitStats"] = dict()
    Vars["HigherVersion"] = None
    Vars["OtherVersions"] = None
    Vars["CurrentOFVersion"] = ConfigMan.get("global","openfluid.currentversion","0.0")

    Code,GitStats = WaresOps.getWareGitStats(WareType,WareID)
    if Code == 200:
      Vars["GitStats"] = GitStats
      if "branches" in GitStats:
        Versions = Tools.getVersionsFromGitBranches(GitStats["branches"])
        if Versions :
          Vars["HigherVersion"] = Versions[0]
          Vars["OtherVersions"] = Versions[1:]
        else:
          Vars["HigherVersion"] = None
          Vars["OtherVersions"] = None
      else:
        Vars["HigherVersion"] = None
        Vars["OtherVersions"] = None
      if "committers" in GitStats:
        for name in GitStats['committers']:
          GitStats['committers'][name]["hashedemail"] = hashlib.md5(GitStats['committers'][name]["email"].lower()).hexdigest()

    Vars["SelectedGitBranch"] = request.args.get("branch",None)

    if g.IsAdmin :
      UpdF = UpdateForm()
      DelF = DeleteForm()

      if request.method == 'GET':
        UpdF.ShortDesc.data = WareDef["shortdesc"]
        UpdF.UsersRO.data = ",".join(WareDef["users-ro"])
        UpdF.UsersRW.data = ",".join(WareDef["users-rw"])
        UpdF.MailingList.data = ",".join(WareDef["mailinglist"])

      if request.method == 'POST':

        if DelF.SubmitDelete.data :
          if DelF.validate():
            if DelF.ID.data == WareID:
              Code,ErrMsg = WaresOps.deleteWare(WareType,DelF.ID.data)
              if Code != 200:
                flash(ErrMsg)
            else:
              flash("wrong confirmation ID for deleting %s %s" % (Constants.WareTypesNamesSingular[WareType],WareID))
              return redirect(url_for(".WareDetails",ware_type=WareType,ware_id=WareID))
          else:
            flash("invalid or incomplete form for deleting %s %s" % (Constants.WareTypesNamesSingular[WareType],WareID))
            return redirect(url_for(".WareDetails",ware_type=WareType,ware_id=WareID))

          return redirect(url_for(".WaresList",ware_type=WareType))

        elif UpdF.SubmitUpdate.data :

          if UpdF.validate():
            OK = True

            UsersRO = Tools.getAsValidList(UpdF.UsersRO.data,Tools.isValidUsername,True,",")
            if UsersRO is None:
              OK = False
              flash("invalid read-only users list for updating %s" % WareID)

            UsersRW = Tools.getAsValidList(UpdF.UsersRW.data,Tools.isValidUsername,True,",")
            if UsersRW is None:
              OK = False
              flash("invalid read-write users list for updating %s" % WareID)

            MailingList = Tools.getAsValidList(UpdF.MailingList.data,Tools.isValidEmail,False,",")
            if MailingList is None:
              OK = False
              flash("invalid mailing list for updating %s" % WareID)

            if OK :
              Def = dict()
              Def["shortdesc"] = UpdF.ShortDesc.data
              Def["users-ro"] = UsersRO
              Def["users-rw"] = UsersRW
              Def["mailinglist"] = MailingList

              Code,ErrMsg = WaresOps.updateWare(WareType,WareID,Def)
              if Code != 200:
                flash(ErrMsg)
          else:
            flash("invalid or incomplete form for updating %s %s" % (Constants.WareTypesNamesSingular[WareType],WareID))
          return redirect(url_for(".WareDetails",ware_type=WareType,ware_id=WareID))

      Vars["UpdF"] = UpdF
      Vars["DelF"] = DelF

    return render_template("waredetails.html",**Vars)



################################################################################


def renderWarePDFDoc(WareType,WareID):
  FilePath = WaresOps.getWareDocPDFPath(WareType,WareID)
  if FilePath :
    return send_file(FilePath, as_attachment=True)
  else:
    abort(404)
