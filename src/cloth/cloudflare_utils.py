#! /usr/bin/env python

import re
import requests
import json
import os

from utils import use as ec2_use

CF_EMAIL = os.environ.get('CLOUDFLARE_EMAIL')
CF_KEY = os.environ.get('CLOUDFLARE_API_KEY')
CF_ZONE = os.environ.get('CLOUDFLARE_ZONE')
CF_PREFIX = os.environ.get('CLOUDFLARE_PREFIX')

# We don't want to operate on all the instances
# in our zone
API_BASE = 'https://www.cloudflare.com/api_json.html'

class Node(object):
  def __init__(self, name, ip_address):
    "All we care about are tags (bit between PREFIX and first .) and IP"
    self.tags = {'Name': name}
    self.ip_address = ip_address
    self.private_ip_address = None # API compatibility

  def __unicode__(self):
    return '%s: %s' % (self.tags['Name'], self.ip_address)

  def __repr__(self):
    return self.__unicode__()

class CloudflareClient(object):
  def __init__(self, email, key, zone, prefix):
    self.email = email
    self.key = key
    self.zone = zone
    self.prefix = prefix

  def cloudflare_instances(self):
    """
    Use the cloudflare API to get a list of all instances
    """
    data = {'a': 'rec_load_all',
        'tkn': self.key,
        'email': self.email,
        'z': self.zone}
    resp = requests.post(API_BASE, data=data)
    objs = json.loads(resp.content)['response']['recs']['objs']
    return objs

  def instances(self, exp=".*"):
    "Return a list of instances matching exp"
    expression = re.compile('(?u)' + self.prefix + exp)
    instances = []
    for node in self.cloudflare_instances():
      # Instead of tags we look at anything before the first . in domain name
      if node['type'] == 'A':
        if expression.match(node['display_name']):
          name = node['display_name'][len(self.prefix):]
          instances.append(
              Node(
                name=name,
                ip_address=node['content'])
              )
    return instances

def instances(exp=".*"):
  try:
    cf = CloudflareClient(CF_EMAIL, CF_KEY, CF_ZONE, CF_PREFIX)
  except:
    return []
  return cf.instances(exp)
