
__license__ = "AGPLv3"
__author__ = "Jean-Christophe Fabre <jean-christophe.fabre@inra.fr>"


import os
import jwt
from datetime import datetime, timedelta

from FluidHub import Constants
from FluidHub.ConfigManager import ConfigMan


################################################################################
################################################################################


class TokenManager:


  @staticmethod
  def generate(Subject,ExpDelaySecs):
    Payload = {
                'exp': datetime.utcnow() + timedelta(seconds=ExpDelaySecs),
                'iat': datetime.utcnow(),
                'sub': Subject
              }

    try:
      JWTString = jwt.encode(Payload,
                             ConfigMan.get("global","secret",""),
                             algorithm='HS256')
      return JWTString

    except Exception as e:
       return None



################################################################################


  @staticmethod
  def decode(Token):
    try:
      Payload = jwt.decode(Token,
                           ConfigMan.get("global","secret",""),
                           algorithm='HS256')
      if "sub" in Payload.keys():
        return Payload["sub"]
      else :
        return None

    except jwt.ExpiredSignatureError:
      return None

    except jwt.InvalidTokenError:
      return None
