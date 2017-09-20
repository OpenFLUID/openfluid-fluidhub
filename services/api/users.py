
__license__ = "AGPLv3"
__author__ = "Jean-Christophe Fabre <jean-christophe.fabre@inra.fr>"


from flask import Blueprint,jsonify,request

from fluidhubcommon import Constants
from fluidhubcommon.UsersManager import UsersMan
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

  Data = request.get_json(silent=True)

  Code, Res = UsersMan.createUser(username,Data)

  return Res,Code


################################################################################


@apiUsers.route('/users/registry/<string:username>', methods=['PATCH'])
@tokenAuth.login_required
def UpdateUser(username) :
  abort(501)


################################################################################


@apiUsers.route('/users/registry/<string:username>', methods=['DELETE'])
@tokenAuth.login_required
def DeleteUser(username) :

  Code,Res = UsersMan.deleteUser(username)

  return Res,Code


################################################################################


@apiUsers.route('/users/auth', methods=['POST'])
@basicAuth.login_required
def AuthUser() :
  abort(501)
