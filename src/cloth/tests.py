from tasks import *
import unittest
from mock import Mock

class ClothTest(unittest.TestCase):

  def test_instances(self):
    # FIXME - these are running against the live server at the moment!
    # Need to stub out cloudflare API response
    ins = cf_instances()
    self.assertGreater(len(ins), 1, ins)

    ins = cf_instances(exp='production-.*')
    self.assertGreater(len(ins), 1, ins)
    self.assertEqual(ins[0].tags['Name'], 'production-es-1')

    self.assertEqual(len(env.nodes), 0)
    use(ins[0])
    use(ins[1])
    self.assertIn('5.9.37.103', env.roledefs['es'])

    self.assertGreater(len(env.nodes), 1)
    self.assertIn('5.9.37.103', env.hosts)

    ins = cf_instances(exp='staging-.*')
    self.assertEqual(len(ins), 0, ins)


class TaskTest(unittest.TestCase):
  def setUp(self):
    env.nodes = []

  def test_tasks(self):
    self.assertFalse(env.nodes)
    all()
    self.assertGreater(len(env.nodes), 1)

  def test_production(self):
    self.assertFalse(env.nodes)
    production()
    self.assertGreater(len(env.nodes), 1)

  def test_preview(self):
    self.assertFalse(env.nodes)
    preview()
    self.assertFalse(env.nodes)

  def test_cloudflare(self):
    self.assertFalse(env.nodes)
    cloudflare()
    self.assertGreater(len(env.nodes), 1)

if __name__ == '__main__':
  unittest.main()
