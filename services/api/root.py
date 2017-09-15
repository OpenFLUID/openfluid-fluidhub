
__license__ = "AGPLv3"
__author__ = "Jean-Christophe Fabre <jean-christophe.fabre@inra.fr>"


from flask import Blueprint,jsonify

from fluidhubcommon import ConfigManager


################################################################################
################################################################################


Config = ConfigManager.get()


################################################################################
################################################################################


apiRoot = Blueprint('apiRoot', __name__)


################################################################################


@apiRoot.route('/')
def GetRoot(methods=['GET']):
  Capabilities = []

  if Config.getboolean("wareshub","enabled") :
    Capabilities.append('wares')

  return jsonify({ 'nature' : 'OpenFLUID FluidHub',
                   'name' : Config.get("global","name"),
                   'api-version' : Config.get("api","version"),
                   'capabilities' : Capabilities,
                   'status' : Config.get("global","status")
                 })
