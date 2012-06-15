#! /usr/bin/env python

from collections import defaultdict
import os

from fabric.api import run, env, sudo, task, runs_once, roles

env.nodes = []
env.roledefs = defaultdict(list)

BACKEND = os.environ.get('CLOTH_BACKEND') or 'ec2'
CF_EMAIL = os.environ.get('CLOUDFLARE_EMAIL')
CF_KEY = os.environ.get('CLOUDFLARE_API_KEY')
CF_ZONE = os.environ.get('CLOUDFLARE_ZONE')
CF_PREFIX = os.environ.get('CLOUDFLARE_PREFIX')
#! /usr/bin/env python

class Backend(object):
  """Lets us plug in ec2 or Cloudflare as we need
  Instantiate this with
  """
  def __init__(self, backend):
    if backend == 'ec2':
      from cloth.utils import instances, use
      self.instances = instances
      self.use = use
    elif backend == 'cloudflare':
      from cloth.cloudflare_utils import CloudflareClient
      self.cf = CloudflareClient(CF_EMAIL, CF_KEY, CF_ZONE, CF_PREFIX)
      self.instances = cf.instances
      self.use = cf.use

backend = Backend(BACKEND)

@task
def all():
    "All nodes"
    for node in backend.instances():
        backend.use(node)

@task
def preview():
    "Preview nodes"
    for node in instances('preview-'):
        use(node)

@task
def production():
    "Production nodes"
    for node in instances('production-'):
        use(node)

@task
def nodes(exp):
    "Select nodes based on a regular expression"
    for node in instances(exp):
        use(node)

@task
@runs_once
def list():
    "List EC2 name and public and private ip address"
    for node in env.nodes:
        print "%s (%s, %s)" % (node.tags["Name"], node.ip_address,
            node.private_ip_address)

@task
def uptime():
    "Show uptime and load"
    run('uptime')

@task
def free():
    "Show memory stats"
    run('free')

@task
def updates():
    "Show package counts needing updates"
    run("cat /var/lib/update-notifier/updates-available")

@task
def upgrade():
    "Upgrade packages with apt-get"
    sudo("apt-get update; apt-get upgrade -y")

