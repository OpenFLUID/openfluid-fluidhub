
__license__ = "AGPLv3"
__author__ = "Jean-Christophe Fabre <jean-christophe.fabre@inra.fr>"


from flask import Blueprint,jsonify

from fluidhubcommon.ConfigManager import ConfigMan


################################################################################
################################################################################


apiRoot = Blueprint('apiRoot', __name__)


################################################################################


@apiRoot.route('/')
def GetRoot(methods=['GET']):
  Capabilities = []

  if ConfigMan.getboolean("wareshub","enabled") :
    Capabilities.append('wares')

  return jsonify({ 'nature' : 'OpenFLUID FluidHub',
                   'name' : ConfigMan.get("global","name"),
                   'api-version' : ConfigMan.get("api","version"),
                   'capabilities' : Capabilities,
                   'status' : ConfigMan.get("global","status")
                 })
