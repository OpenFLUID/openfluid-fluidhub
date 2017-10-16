

__license__ = "AGPLv3"
__author__ = "Jean-Christophe Fabre <jean-christophe.fabre@inra.fr>"


from flask import render_template,request,abort,session,url_for,g,flash, redirect
from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,PasswordField
from wtforms.validators import DataRequired

from FluidHub.ConfigManager import ConfigMan
from FluidHub.UsersManager import UsersMan
from FluidHub import Tools

import uiCommon


################################################################################
################################################################################


class EditUserForm(FlaskForm):
  FullName = StringField('Full name')
  EMail = StringField('Email')


class AddUserForm(EditUserForm):
  Username = StringField('Username', validators=[DataRequired()])
  Password1 = PasswordField('Password', validators=[DataRequired()])
  Password2 = PasswordField('Retype password', validators=[DataRequired()])
  SubmitAdd = SubmitField("Add")


class UpdateUserForm(EditUserForm):
  SubmitUpdate = SubmitField("Update")


class DeleteUserForm(FlaskForm):
  Username = StringField('Username', validators=[DataRequired()])
  SubmitDelete = SubmitField("Delete")


class ChPwdUserForm(EditUserForm):
  Password1 = PasswordField('Password', validators=[DataRequired()])
  Password2 = PasswordField('Retype password', validators=[DataRequired()])
  SubmitChPwd = SubmitField("Change")


################################################################################
################################################################################


def initTemplateVariables() :
  Vars = uiCommon.initTemplateVariables()
  Vars["Breadcrumbs"].append({ "Label" : "Administration", "URL" : url_for(".AdminHome")})

  return Vars


################################################################################


def renderAdminHome():
  Vars = initTemplateVariables()

  return render_template("adminhome.html",**Vars)



################################################################################


def renderAdminUsersList():
  Vars = initTemplateVariables()

  Vars["Breadcrumbs"].append({ "Label" : "Users", "URL" : url_for(".AdminUsersList")})

  Code, Data = UsersMan.getUsers()
  Data.sort()

  Vars["UsersList"] = list()
  for User in Data:
    Code,UserDetails = UsersMan.getUser(User)
    if Code == 200:
      Vars["UsersList"].append({
                                 "username" : User,
                                 "fullname" : UserDetails["fullname"],
                                 "isadmin" : UsersMan.isAdmin(User)
                               })

  if g.IsAdmin :
    AddF = AddUserForm()

    if AddF.SubmitAdd.data and request.method == 'POST':
      if AddF.validate():
        OK = True

        if not Tools.isValidUsername(AddF.Username.data):
          OK = False
          flash("invalid username")

        if AddF.Password1.data != AddF.Password2.data:
          OK = False
          flash("password mismatch")

        if AddF.EMail.data and not Tools.isValidEmail(AddF.EMail.data):
          OK = False
          flash("invalid email")

        if OK :
          Def = dict()
          Def["username"] = AddF.Username.data
          if AddF.EMail.data:
            Def["email"] = AddF.EMail.data
          Def["fullname"] = AddF.FullName.data
          Def["password"] = AddF.Password1.data
          Code,ErrMsg = UsersMan.createUser(AddF.Username.data,Def)
          if Code != 201:
            flash(ErrMsg)
      else:
        flash("invalid or incomplete form for adding user")
      return redirect(url_for(".AdminUsersList"))

    Vars["AddF"] = AddF

  return render_template("adminuserslist.html",**Vars)


################################################################################


def renderAdminUserDetails(Username):
  Vars = initTemplateVariables()

  Vars["Breadcrumbs"].append({ "Label" : "Users", "URL" : url_for(".AdminUsersList")})
  Vars["Breadcrumbs"].append({ "Label" : Username, "URL" : url_for(".AdminUserDetails",username=Username)})

  Code,UserDetails = UsersMan.getUser(Username)
  if Code == 200:
    Vars["UserDetails"] = UserDetails

  if g.IsAdmin :
    UpdF = UpdateUserForm()
    DelF = DeleteUserForm()
    ChPwdF = ChPwdUserForm()

    if request.method == 'GET':
      UpdF.FullName.data = UserDetails["fullname"]
      UpdF.EMail.data = UserDetails["email"]

    if request.method == 'POST':

       if DelF.SubmitDelete.data :
          if DelF.validate():
            if DelF.Username.data == Username:
              Code,ErrMsg = UsersMan.deleteUser(DelF.Username.data)
              if Code != 200:
                flash("internal error while deleting user %s" % Username)
              return redirect(url_for(".AdminUsersList"))
            else:
              flash("wrong confirmation username for deleting user %s " % Username)
              return redirect(url_for(".AdminUserDetails",username=Username))
          else:
            flash("invalid or incomplete form for deleting user %s" % Username)
            return redirect(url_for(".AdminUserDetails",username=Username))

       elif ChPwdF.SubmitChPwd.data :
          if ChPwdF.validate():
            if ChPwdF.Password1.data == ChPwdF.Password2.data:
              Code,ErrMsg = UsersMan.changePassword(Username,ChPwdF.Password1.data)
              if Code != 200:
                 flash("internal error while changing password for user %s" % Username)
              return redirect(url_for(".AdminUserDetails",username=Username))
            else:
              flash("password mismatch")
              return redirect(url_for(".AdminUserDetails",username=Username))
          else:
            flash("invalid or incomplete form for changing password for user %s" % Username)
            return redirect(url_for(".AdminUserDetails",username=Username))

       elif UpdF.SubmitUpdate.data :
          if UpdF.validate():

            if UpdF.EMail.data and not Tools.isValidEmail(UpdF.EMail.data):
              flash("invalid email")
            else:
              Def = dict()
              Def["fullname"] = UpdF.FullName.data
              Def["email"] = UpdF.EMail.data
              Code,ErrMsg = UsersMan.updateUser(Username,Def)
              if Code != 200:
                flash("internal error while updating user %s" % Username)

            return redirect(url_for(".AdminUserDetails",username=Username))


    Vars["UpdF"] = UpdF
    Vars["DelF"] = DelF
    Vars["ChPwdF"] = ChPwdF


  return render_template("adminuserdetails.html",**Vars)
