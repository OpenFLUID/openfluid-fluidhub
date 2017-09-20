
__license__ = "AGPLv3"
__author__ = "Jean-Christophe Fabre <jean-christophe.fabre@inra.fr>"


from flask import Flask, g
from flask_httpauth import HTTPBasicAuth,HTTPTokenAuth

from fluidhubcommon.UsersManager import UsersMan
from fluidhubcommon.TokenManager import TokenManager


################################################################################
################################################################################


tokenAuth = HTTPTokenAuth(scheme='JWT')
basicAuth = HTTPBasicAuth()


################################################################################
################################################################################


@tokenAuth.verify_token
def verify_token(token) :
  Sub = TokenManager.decode(token)
  if Sub:
    g.username = Sub
    return True

  return False


################################################################################


@basicAuth.verify_password
def verify_pw(username, password):
  return UsersMan.authenticateUser(username, password)
