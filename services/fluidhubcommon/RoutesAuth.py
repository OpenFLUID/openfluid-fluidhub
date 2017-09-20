
from flask_httpauth import HTTPBasicAuth,HTTPTokenAuth

from fluidhubcommon import AccessToken
from fluidhubcommon.UsersManager import UsersMan


################################################################################
################################################################################


tokenAuth = HTTPTokenAuth(scheme='Token')
basicAuth = HTTPBasicAuth()


################################################################################
################################################################################


# TODO secure with better token system such as jwt
@tokenAuth.verify_token
def verify_token(token) :
  if token == AccessToken.get() :
    return True
  return False


################################################################################


@basicAuth.verify_password
def verify_pw(username, password):
  return UsersMan.authenticateUser(username, password)
