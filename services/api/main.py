
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

  if Config["wareshub"]["enabled"] == True :
    Capabilities.append('wares')

  return jsonify({ 'nature' : 'OpenFLUID FluidHub',
                   'name' : Config["global"]["name"],
                   'api-version' : Config["api"]["version"],
                   'capabilities' : Capabilities,
                   'status' : Config["global"]["status"]
                 })


################################################################################
################################################################################


if Config["wareshub"]["enabled"] == True :

  @app.route('/wares', methods=['GET'])
  def WaresGet() :
    return "not implemented",501


################################################################################


  @app.route('/wares/<string:ware_type>', methods=['GET'])
  def ProcessWaresType(ware_type) :
    if ware_type not in Constants.WareTypes :
      return "invalid ware type",404
    return "not implemented",501


################################################################################


  @app.route('/wares/<string:ware_type>/<string:ware_id>', methods=['GET'])
  def GetWare(ware_type,ware_id) :

    if ware_type not in Constants.WareTypes :
      return "invalid ware type",404

    WaresOps = WaresOperations()

    Code,Data = WaresOps.GetWareInfo(ware_type,ware_id)
    return jsonify(Data),Code


################################################################################


  @app.route('/wares/<string:ware_type>/<string:ware_id>', methods=['PUT'])
  @tokenAuth.login_required
  def CreateWare(ware_type,ware_id) :

    if ware_type not in Constants.WareTypes :
      return "invalid ware type",404

    WaresOps = WaresOperations()

    if request.method == 'PUT' :
      Code,Data = WaresOps.CreateWare(ware_type,ware_id,request.get_json(silent=True))
      return Data,Code


################################################################################
################################################################################


if __name__ == '__main__':
  app.run(port=Config["api"]["port"])
