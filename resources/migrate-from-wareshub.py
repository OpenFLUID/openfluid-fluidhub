#!/usr/bin/env python


__license__ = "AGPLv3"
__author__ = "Jean-Christophe Fabre <jean-christophe.fabre@inra.fr>"


import os
import sys
import argparse
import json
import shutil

CurrentPath = os.path.dirname(os.path.abspath(__file__))
RootPath = os.path.dirname(CurrentPath)
FluidHubPath = os.path.join(RootPath,"fluidhub")
sys.path.append(FluidHubPath)

from FluidHub import Constants
from FluidHub.GitInfosWriter import GitInfosWriter


################################################################################
################################################################################


def migrateDefinitionFile(SrcFilePath,WareID,DestFilePath):
  with open(SrcFilePath, 'r') as SrcDefFile:
    Data = json.load(SrcDefFile)

    if not WareID in Data:
      return None

    OldDef = Data[WareID]
    NewDef = dict()

    # replace missing shortdesc value by empty one
    NewDef["shortdesc"] = ""
    if "shortdesc" in OldDef:
      NewDef["shortdesc"] = OldDef["shortdesc"]

    # replace missing list values value by empty ones
    for Prop in ["users-ro","users-rw","mailinglist"]:
      NewDef[Prop] = []
      if Prop in OldDef:
        NewDef[Prop] = OldDef[Prop]

    with open(DestFilePath, 'w') as DestDefFile:
      json.dump(NewDef, DestDefFile, indent=2)


################################################################################


def migrateRepository(SrcPath,DestPath):
  shutil.copytree(SrcPath,DestPath,symlinks=True)


################################################################################
################################################################################


Parser = argparse.ArgumentParser(description='Migrate from former wareshub data')
Parser.add_argument("--defs-path",help="Root path of former wares definitions",required=True)
Parser.add_argument("--repos-path",help="Root path of former wares repositories",required=True)
Parser.add_argument("--dest-path",help="Desitination path of wareshub data",required=True)
Parser.add_argument("--rebuild-git-infos", help="Rebuild git informations as metadata files during migration",
                    action="store_true")

Args = vars(Parser.parse_args())

print Args

if os.path.isdir(Args["dest_path"]) :
  print "Destination path already exist. Exiting."
  sys.exit(127)


DestDefsPath = os.path.join(Args["dest_path"],"definitions")
DestReposPath = os.path.join(Args["dest_path"],"repositories")
SrcDefsPath = Args["defs_path"]
SrcReposPath = Args["repos_path"]

print "Creating destination definitions path :",DestDefsPath
os.makedirs(DestDefsPath)
print "Creating destination repositories path :",DestDefsPath
os.makedirs(DestReposPath)

for WareType in Constants.WareTypes:

  CurrentSrcDefsPath = os.path.join(SrcDefsPath,WareType)
  CurrentSrcReposPath = os.path.join(SrcReposPath,WareType)
  CurrentDestDefsPath = os.path.join(DestDefsPath,WareType)
  CurrentDestReposPath = os.path.join(DestReposPath,WareType)
  os.makedirs(CurrentDestDefsPath)
  os.makedirs(CurrentDestReposPath)

  for CurrentSrcDefFile in os.listdir(CurrentSrcDefsPath):
    CurrentSrcDefPath = os.path.join(CurrentSrcDefsPath,CurrentSrcDefFile)
    if os.path.isfile(CurrentSrcDefPath) and CurrentSrcDefPath.endswith(".json"):
      CurrentWareID = CurrentSrcDefFile[:-5]
      print WareType,":",CurrentWareID,"...",
      if os.path.isdir(os.path.join(SrcReposPath,WareType,CurrentWareID)) :
        print "Processing ...",

        migrateDefinitionFile(CurrentSrcDefPath,CurrentWareID,os.path.join(CurrentDestDefsPath,CurrentSrcDefFile))
        migrateRepository(os.path.join(CurrentSrcReposPath,CurrentWareID),
                          os.path.join(CurrentDestReposPath,CurrentWareID))

        # rebuild of git stats
        if Args["rebuild_git_infos"] :
          GitInfosWriter(WareType,CurrentWareID,os.path.join(CurrentDestReposPath,CurrentWareID)).rebuildInfos()

        print "Done"
      else:
        print "Respository not found. Ignored."
