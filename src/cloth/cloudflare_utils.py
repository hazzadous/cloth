#! /usr/bin/env python

import re
import requests
import json

from .utils import use as ec2_use

# We don't want to operate on all the instances
# in our zone
PREFIX = 'cloth-'
API_BASE = 'https://www.cloudflare.com/api_json.html'

class Node(object):
  def __init__(self, name, ip_address):
    "All we care about are tags (bit between PREFIX and first .) and IP"
    self.tags = {'Name': name}
    self.ip_address = ip

class CloudflareClient(object):
  def __init__(self, email, key, zone):
    self.email = email
    self.key = key
    self.zone = zone

  def cloudflare_instances():
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

  def instances(self, exp='^' + PREFIX + ".*"):
    "Return a list of instances matching exp"
    expression = re.compile(exp)
    instances = []
    for node in self.cloudflare_instances():
      # Instead of tags we look at anything before the first . in domain name
      if node['type'] == 'A':
        name = node['name'].lsplit('.', 1)[0].lstrip(PREFIX)
        if expression.match(node['name']):
          instances.append(
              Node(
                name=name,
                ip=node['content'])
              )
    return instances

  def use(self, node):
    return ec2_use(node)
