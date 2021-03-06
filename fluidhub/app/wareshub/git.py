
__license__ = "AGPLv3"
__author__ = "Jean-Christophe Fabre <jean-christophe.fabre@inra.fr>"


import subprocess

from flask import Blueprint, make_response, request, abort
from StringIO import StringIO
from dulwich.pack import PackStreamReader

from FluidHub.WaresOperations import WaresOperations
from FluidHub.RoutesAuth import basicAuth

from FluidHub.GitInfosWriter import GitInfosWriter
from GitMailManager import GitMailManager


################################################################################
################################################################################


WaresOps = WaresOperations()

wareshubGit = Blueprint('wareshubGit', __name__)


################################################################################
################################################################################


@wareshubGit.route('/<string:ware_type>/<string:ware_id>/info/refs')
@basicAuth.login_required
def processInfoRefs(ware_type,ware_id):

  # Check if user is granted in RO mode for this ware
  if not WaresOps.isUserGranted(ware_type,ware_id,basicAuth.username(),False) :
    abort(403)

  # Run service
  Service = request.args.get('service')
  if Service[:4] != 'git-':
    abort(500)

  P = subprocess.Popen([Service, '--stateless-rpc', '--advertise-refs',WaresOps.getWareGitReposPath(ware_type,ware_id)],
                       stdout=subprocess.PIPE)

  # Prepare data for response
  Packet = '# service=%s\n' % Service
  Length = len(Packet) + 4
  _hex = '0123456789abcdef'
  Prefix = ''
  Prefix += _hex[Length >> 12 & 0xf]
  Prefix += _hex[Length >> 8  & 0xf]
  Prefix += _hex[Length >> 4 & 0xf]
  Prefix += _hex[Length & 0xf]
  Data = Prefix + Packet + '0000'
  Data += P.stdout.read()

  # Build response
  Res = make_response(Data)
  Res.headers['Expires'] = 'Fri, 01 Jan 1980 00:00:00 GMT'
  Res.headers['Pragma'] = 'no-cache'
  Res.headers['Cache-Control'] = 'no-cache, max-age=0, must-revalidate'
  Res.headers['Content-Type'] = 'application/x-%s-advertisement' % Service

  P.wait()

  return Res


################################################################################


@wareshubGit.route('/<string:ware_type>/<string:ware_id>/git-receive-pack', methods=['POST'])
@basicAuth.login_required
def processGitReceivePack(ware_type,ware_id):

  # Check if user is granted in RW mode for this ware
  if not WaresOps.isUserGranted(ware_type,ware_id,basicAuth.username(),True) :
    abort(403)

  P = subprocess.Popen(['git-receive-pack', '--stateless-rpc',WaresOps.getWareGitReposPath(ware_type,ware_id)],
                       stdin=subprocess.PIPE, stdout=subprocess.PIPE)
  DataIn = request.data
  PackFile = DataIn[DataIn.index('PACK'):]
  Objects = PackStreamReader(StringIO(PackFile).read)

  P.stdin.write(DataIn)
  DataOut = P.stdout.read()
  Res = make_response(DataOut)

  Res.headers['Expires'] = 'Fri, 01 Jan 1980 00:00:00 GMT'
  Res.headers['Pragma'] = 'no-cache'
  Res.headers['Cache-Control'] = 'no-cache, max-age=0, must-revalidate'
  Res.headers['Content-Type'] = 'application/x-git-receive-pack-result'

  P.wait()

  # Rebuild git info data
  InfosWriter = GitInfosWriter(ware_type,ware_id,WaresOps.getWareGitReposPath(ware_type,ware_id))
  InfosWriter.rebuildInfos()

  # Send mail to mailing list
  MailMan = GitMailManager(ware_type,ware_id)
  MailMan.sendMail(Objects)

  return Res


################################################################################


@wareshubGit.route('/<string:ware_type>/<string:ware_id>/git-upload-pack', methods=['POST'])
@basicAuth.login_required
def processGitUploadPack(ware_type,ware_id):

  # Check if user is granted in RW mode for this ware
  if not WaresOps.isUserGranted(ware_type,ware_id,basicAuth.username(),True) :
    abort(403)

  P = subprocess.Popen(['git-upload-pack', '--stateless-rpc', WaresOps.getWareGitReposPath(ware_type,ware_id)],
                      stdin=subprocess.PIPE, stdout=subprocess.PIPE)
  P.stdin.write(request.data)
  Data = P.stdout.read()
  Res = make_response(Data)

  Res.headers['Expires'] = 'Fri, 01 Jan 1980 00:00:00 GMT'
  Res.headers['Pragma'] = 'no-cache'
  Res.headers['Cache-Control'] = 'no-cache, max-age=0, must-revalidate'
  Res.headers['Content-Type'] = 'application/x-git-upload-pack-result'

  P.wait()

  return Res
