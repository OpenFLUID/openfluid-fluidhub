
__license__ = "AGPLv3"
__author__ = "Jean-Christophe Fabre <jean-christophe.fabre@inra.fr>"


from flask import Flask,jsonify,request
from flask_httpauth import HTTPTokenAuth

from fluidhubcommon import ConfigManager
from fluidhubcommon import Constants
from fluidhubcommon import AccessToken
from fluidhubcommon.WaresOperations import WaresOperations


################################################################################
################################################################################


app = Flask(__name__)


tokenAuth = HTTPTokenAuth(scheme='Token')

Config = ConfigManager.get()


################################################################################
################################################################################


@tokenAuth.verify_token
def verify_token(token) :
  if token == AccessToken.get() :
    return True
  return False


################################################################################
################################################################################


@app.route("/")
def root():
  Capabilities = []

  if Config.getboolean("wareshub","enabled") :
    Capabilities.append('wares')

  return jsonify({ 'nature' : 'OpenFLUID FluidHub',
                   'name' : Config.get("global","name"),
                   'api-version' : Config.get("api","version"),
                   'capabilities' : Capabilities,
                   'status' : Config.get("global","status")
                 })


################################################################################
################################################################################


if Config.getboolean("wareshub","enabled") :

  @app.route('/wares', methods=['GET'])
  def GetAllWares() :
        WaresOps = WaresOperations()

        Code,Data = WaresOps.getAllWaresInfo()
        return jsonify(Data),Code


################################################################################


  @app.route('/wares/<string:ware_type>', methods=['GET'])
  def GetWares(ware_type) :

    if ware_type not in Constants.WareTypes :
      return "invalid ware type",404

    WaresOps = WaresOperations()

    Code,Data = WaresOps.getWaresInfo(ware_type,request.args.get("username",""))
    return jsonify(Data),Code


################################################################################


  @app.route('/wares/<string:ware_type>/<string:ware_id>', methods=['GET'])
  def GetWare(ware_type,ware_id) :

    if ware_type not in Constants.WareTypes :
      return "invalid ware type",404

    WaresOps = WaresOperations()

    Code,Data = WaresOps.getWareInfo(ware_type,ware_id)
    return jsonify(Data),Code


################################################################################


  @app.route('/wares/<string:ware_type>/<string:ware_id>', methods=['PUT'])
  @tokenAuth.login_required
  def CreateWare(ware_type,ware_id) :

    if ware_type not in Constants.WareTypes :
      return "invalid ware type",404

    WaresOps = WaresOperations()

    if request.method == 'PUT' :
      Code,Data = WaresOps.createWare(ware_type,ware_id,request.get_json(silent=True))
      return Data,Code


################################################################################


  @app.route('/wares/<string:ware_type>/<string:ware_id>', methods=['PATCH'])
  @tokenAuth.login_required
  def UpdateWare(ware_type,ware_id) :

    if ware_type not in Constants.WareTypes :
      return "invalid ware type",404

    WaresOps = WaresOperations()

    if request.method == 'PATCH' :
      Code,Data = WaresOps.updateWare(ware_type,ware_id,request.get_json(silent=True))
      return Data,Code


################################################################################


  @app.route('/wares/<string:ware_type>/<string:ware_id>', methods=['DELETE'])
  @tokenAuth.login_required
  def DeleteWare(ware_type,ware_id) :

    if ware_type not in Constants.WareTypes :
      return "invalid ware type",404

    WaresOps = WaresOperations()

    if request.method == 'DELETE' :
      Code,Data = WaresOps.deleteWare(ware_type,ware_id)
      return Data,Code



################################################################################
################################################################################


if __name__ == '__main__':
  app.run(port=Config.get("api","port"))
