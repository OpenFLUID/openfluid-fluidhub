
__license__ = "AGPLv3"
__author__ = "Jean-Christophe Fabre <jean-christophe.fabre@inra.fr>"


import unittest
import os

import TestsHelpers as helpers


################################################################################
################################################################################


class tests_APIWaresCreate(unittest.TestCase):

  @classmethod
  def setUpClass(cls):
    pass


  def setUp(self):
    pass


################################################################################
################################################################################


  def createWare(self,Type,ID) :

    URL = "http://127.0.0.1:3447/api/wares/%s/%s" % (Type,ID)
    Headers = {
     'content-type': "application/json",
     'authorization': "Token %s" % helpers.AccessToken,
     'cache-control': "no-cache",
    }

    with open(os.path.join(helpers.TestsPath,"definitions",ID+".json")) as DefFile :
      Payload = DefFile.read()
      Response = helpers.executePutRequest(URL, Data=Payload, Headers=Headers)
      helpers.printResponse(Response)
      return Response


################################################################################


  def getWare(self,Type,ID) :

    URL = "http://127.0.0.1:3447/api/wares/%s/%s" % (Type,ID)

    Response = helpers.executeGetRequest(URL)
    helpers.printResponse(Response)
    return Response



################################################################################


  def getWares(self,Type,Username=None) :

    UserArg = ""
    if Username :
      UserArg = "?username=%s" % Username

    URL = "http://127.0.0.1:3447/api/wares/%s%s" % (Type,UserArg)

    Response = helpers.executeGetRequest(URL)
    helpers.printResponse(Response)
    return Response


################################################################################
################################################################################


  def test01_CreateWares(self):
    for Type, IDs in helpers.Wares.iteritems():
      for ID in IDs:
        Response = self.createWare(Type,ID)
        self.assertEqual(Response.status_code,201)


################################################################################


  def test10_GetWares(self):

    for Type, IDs in helpers.Wares.iteritems():
      for ID in IDs:
        Response = self.getWare(Type,ID)
        self.assertEqual(Response.status_code,200)
      Response = self.getWares(Type)
      self.assertEqual(Response.status_code,200)
      Response = self.getWares(Type,"admin")
      self.assertEqual(Response.status_code,200)


################################################################################


  def test11_GetAllWares(self):
    Response = helpers.executeGetRequest("http://127.0.0.1:3447/api/wares")
    helpers.printResponse(Response)
    self.assertEqual(Response.status_code,200)


################################################################################
################################################################################


if __name__ == '__main__':
    unittest.main()
