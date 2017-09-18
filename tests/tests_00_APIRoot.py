
__license__ = "AGPLv3"
__author__ = "Jean-Christophe Fabre <jean-christophe.fabre@inra.fr>"


import unittest

import TestsHelpers as helpers


################################################################################
################################################################################


class tests_APIRoot(unittest.TestCase):

  @classmethod
  def setUpClass(cls):
    pass


  def setUp(self):
    pass


################################################################################
################################################################################


  def test_getRoot(self):
    Response = helpers.executeGetRequest("http://127.0.0.1:3447/api")
    helpers.printResponse(Response)
    self.assertEqual(Response.status_code,200)


################################################################################
################################################################################


if __name__ == '__main__':
    unittest.main()
