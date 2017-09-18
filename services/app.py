
# TODO add python encoding tag in each python file

__license__ = "AGPLv3"
__author__ = "Jean-Christophe Fabre <jean-christophe.fabre@inra.fr>"


from flask import Flask

from fluidhubcommon import ConfigManager

from api.root import apiRoot
from api.wares import apiWares
from wareshub.git import wareshubGit
from wareshub.ui import wareshubUI


################################################################################
################################################################################


Config = ConfigManager.get()


app = Flask(__name__)

app.register_blueprint(apiRoot,url_prefix='/'+Config.get("api","url-prefix"))
app.register_blueprint(apiWares,url_prefix='/'+Config.get("api","url-prefix"))

app.register_blueprint(wareshubGit,url_prefix='/'+Config.get("wareshub","url-prefix")+'/'+
                                                  Config.get("wareshub","gitserver.url-prefix"))
app.register_blueprint(wareshubUI,url_prefix='/'+Config.get("wareshub","url-prefix")+'/'+
                                                 Config.get("wareshub","ui.url-prefix"))


################################################################################
################################################################################


if __name__ == '__main__':
  app.run()
