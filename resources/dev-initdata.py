
__license__ = "AGPLv3"
__author__ = "Jean-Christophe Fabre <jean-christophe.fabre@inra.fr>"


import sys
import os
import shutil

import common


################################################################################
################################################################################


print "Data directory for development:", common.DataDevPath

# Check if data directory does not exist
if os.path.exists(common.DataDevPath) :
  print "!!!",common.DataDevPath,"already exists. aborting."
  sys.exit(127)


# Install common data

shutil.copytree(os.path.join(common.ResourcesPath,"data-dev"),common.DataDevPath)

with open(os.path.join(common.DataDevPath,"common","access-token"), "w") as TokenFile:
    TokenFile.write("%s\n" % common.AccessToken)
