
__license__ = "AGPLv3"
__author__ = "Jean-Christophe Fabre <jean-christophe.fabre@inra.fr>"


from flask import Blueprint,jsonify,request,g

from fluidhubcommon import Constants
from fluidhubcommon.UsersManager import UsersMan
from fluidhubcommon.TokenManager import TokenManager
from fluidhubcommon.RoutesAuth import tokenAuth
from fluidhubcommon.RoutesAuth import basicAuth


################################################################################
################################################################################


apiUsers = Blueprint('apiUsers', __name__)


################################################################################
################################################################################


@apiUsers.route('/users/registry', methods=['GET'])
def GetAllUsers() :

  Code,Data = UsersMan.getUsers()

  return jsonify(Data),Code


################################################################################


@apiUsers.route('/users/registry/<string:username>', methods=['GET'])
def GetUser(username) :

  Code, Data = UsersMan.getUser(username)

  return jsonify(Data),Code


################################################################################


@apiUsers.route('/users/registry/<string:username>', methods=['PUT'])
@tokenAuth.login_required
def CreateUser(username) :

  if g.username != "admin":
    abort(403)

  Data = request.get_json(silent=True)

  Code, Res = UsersMan.createUser(username,Data)

  return Res,Code


################################################################################


@apiUsers.route('/users/registry/<string:username>', methods=['PATCH'])
@tokenAuth.login_required
def UpdateUser(username) :

  if g.username != "admin":
    abort(403)

  abort(501)


################################################################################


@apiUsers.route('/users/registry/<string:username>', methods=['DELETE'])
@tokenAuth.login_required
def DeleteUser(username) :

  if g.username != "admin":
    abort(403)

  Code,Res = UsersMan.deleteUser(username)

  return Res,Code


################################################################################


@apiUsers.route('/users/auth', methods=['GET'])
@basicAuth.login_required
def AuthUser() :
  Token = TokenManager.generate(basicAuth.username(),60)

  if Token :
    return jsonify({ "token" : Token }),200

  return "",500
