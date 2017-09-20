
__license__ = "AGPLv3"
__author__ = "Jean-Christophe Fabre <jean-christophe.fabre@inra.fr>"


import unittest
import json

import TestsHelpers as helpers


################################################################################
################################################################################


class tests_APIUsers(unittest.TestCase):

  @classmethod
  def setUpClass(cls):

    cls.Token = helpers.askForToken("admin","admin")


  def setUp(self):
    pass


################################################################################


  def CreateUser(self,Username, UserData) :
    Headers = {
     'content-type': "application/json",
     'authorization': "JWT %s" % self.Token
    }

    URL = "http://127.0.0.1:3447/api/users/registry/%s" % (Username)
    UserData["username"] = Username
    Payload = json.dumps(UserData)
    Response = helpers.executePutRequest(URL, Data=Payload, Headers=Headers)
    helpers.printResponse(Response)
    return Response



################################################################################


  def test01_DeleteUsers(self):
    Headers = {
     'content-type': "application/json",
     'authorization': "JWT %s" % self.Token
    }

    for Username in helpers.Users.keys():
      URL = "http://127.0.0.1:3447/api/users/registry/%s" % (Username)
      Response = helpers.executeDeleteRequest(URL, Headers=Headers)
      helpers.printResponse(Response)


################################################################################


  def test02_CreateUsers(self):
    for Username in helpers.Users.keys():
      Response = self.CreateUser(Username, helpers.Users[Username])
      self.assertEqual(Response.status_code,201)

    # check that malformed user names are rejected
    for Username in ["uSerxxx","0userxxx","user xxx","user!xxx"] :
      Response = self.CreateUser(Username, {"username" : Username, "password" : Username})
      self.assertEqual(Response.status_code,400)


################################################################################


  def test03_GetUsers(self):

    URL = "http://127.0.0.1:3447/api/users/registry"
    Response = helpers.executeGetRequest(URL)
    helpers.printResponse(Response)
    self.assertEqual(Response.status_code,200)

    for Username in helpers.Users.keys():
      URL = "http://127.0.0.1:3447/api/users/registry/%s" % Username
      Response = helpers.executeGetRequest(URL)
      helpers.printResponse(Response)
      self.assertEqual(Response.status_code,200)

################################################################################


if __name__ == '__main__':
    unittest.main()
