
__license__ = "AGPLv3"
__author__ = "Jean-Christophe Fabre <jean-christophe.fabre@inra.fr>"


from flask import Blueprint,jsonify,request,g

from fluidhubcommon import Constants
from fluidhubcommon.WaresOperations import WaresOperations
from fluidhubcommon.RoutesAuth import tokenAuth


################################################################################
################################################################################


apiWares = Blueprint('apiWares', __name__)


################################################################################
################################################################################


@apiWares.route('/wares', methods=['GET'])
def GetAllWares() :
  WaresOps = WaresOperations()

  Code,Data = WaresOps.getAllWaresInfo()
  return jsonify(Data),Code


################################################################################


@apiWares.route('/wares/<string:ware_type>', methods=['GET'])
def GetWares(ware_type) :

  if ware_type not in Constants.WareTypes :
    return "invalid ware type",404

  WaresOps = WaresOperations()

  Code,Data = WaresOps.getWaresInfo(ware_type,request.args.get("username",""))
  return jsonify(Data),Code


################################################################################


@apiWares.route('/wares/<string:ware_type>/<string:ware_id>', methods=['GET'])
def GetWare(ware_type,ware_id) :

  if ware_type not in Constants.WareTypes :
    return "invalid ware type",404

  WaresOps = WaresOperations()

  Code,Data = WaresOps.getWareInfo(ware_type,ware_id)
  return jsonify(Data),Code


################################################################################


@apiWares.route('/wares/<string:ware_type>/<string:ware_id>', methods=['PUT'])
@tokenAuth.login_required
def CreateWare(ware_type,ware_id) :

  if g.username != "admin":
    abort(403)

  if ware_type not in Constants.WareTypes :
    return "invalid ware type",404

  WaresOps = WaresOperations()

  # TODO is method check necessary
  if request.method == 'PUT' :
    Code,Data = WaresOps.createWare(ware_type,ware_id,request.get_json(silent=True))
    return Data,Code


################################################################################


@apiWares.route('/wares/<string:ware_type>/<string:ware_id>', methods=['PATCH'])
@tokenAuth.login_required
def UpdateWare(ware_type,ware_id) :

  if g.username != "admin":
    abort(403)

  if ware_type not in Constants.WareTypes :
    return "invalid ware type",404

  WaresOps = WaresOperations()

  # TODO is method check necessary
  if request.method == 'PATCH' :
    Code,Data = WaresOps.updateWare(ware_type,ware_id,request.get_json(silent=True))
    return Data,Code


################################################################################


@apiWares.route('/wares/<string:ware_type>/<string:ware_id>', methods=['DELETE'])
@tokenAuth.login_required
def DeleteWare(ware_type,ware_id) :

  if g.username != "admin":
    abort(403)

  if ware_type not in Constants.WareTypes :
    return "invalid ware type",404

  WaresOps = WaresOperations()

  # TODO is method check necessary
  if request.method == 'DELETE' :
    Code,Data = WaresOps.deleteWare(ware_type,ware_id)
    return Data,Code
