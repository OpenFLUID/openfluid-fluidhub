
__license__ = "AGPLv3"
__author__ = "Jean-Christophe Fabre <jean-christophe.fabre@inra.fr>"


import unittest

import TestsHelpers as helpers


################################################################################
################################################################################


class tests_APIWaresDelete(unittest.TestCase):

  @classmethod
  def setUpClass(cls):
    pass


  def setUp(self):
    pass


################################################################################
################################################################################


  def deleteWare(self,Type,ID) :
    URL = "http://127.0.0.1:3447/api/wares/%s/%s" % (Type,ID)
    Headers = {
       'content-type': "application/json",
       'authorization': "Token %s" % helpers.AccessToken,
    }

    Response = helpers.executeDeleteRequest(URL, Headers=Headers)
    helpers.printResponse(Response)
    return Response


################################################################################
################################################################################


  def test01_DeleteWares(self):
    for Type, IDs in helpers.Wares.iteritems():
      for ID in IDs:
        Response = self.deleteWare(Type,ID)


################################################################################
################################################################################


if __name__ == '__main__':
    unittest.main()