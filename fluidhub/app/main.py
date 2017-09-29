
# TODO add python encoding tag in each python file

__license__ = "AGPLv3"
__author__ = "Jean-Christophe Fabre <jean-christophe.fabre@inra.fr>"


from flask import Flask,redirect,url_for

from FluidHub.ConfigManager import ConfigMan

from api.root import apiRoot
from api.wares import apiWares
from api.users import apiUsers
from wareshub.git import wareshubGit
from ui.ui import ui


################################################################################
################################################################################


app = Flask(__name__)

app.config['SECRET_KEY'] = ConfigMan.get("global","secret","")


app.register_blueprint(apiRoot,url_prefix='/'+ConfigMan.get("api","url-prefix"))
app.register_blueprint(apiWares,url_prefix='/'+ConfigMan.get("api","url-prefix"))
app.register_blueprint(apiUsers,url_prefix='/'+ConfigMan.get("api","url-prefix"))

app.register_blueprint(wareshubGit,url_prefix='/'+ConfigMan.get("wareshub","url-prefix")+'/'+
                                                  ConfigMan.get("wareshub","gitserver.url-prefix"))
app.register_blueprint(ui,url_prefix='/'+ConfigMan.get("ui","url-prefix"))


################################################################################
################################################################################


@app.route("/")
def Root():
  return redirect(url_for('ui.Root'))



################################################################################
################################################################################


if __name__ == '__main__':
  app.run()
