from tasks import *
import unittest
from mock import Mock

class ClothTest(unittest.TestCase):

  def test_instances(self):
    # FIXME - these are running against the live server at the moment!
    # Need to stub out cloudflare API response
    ins = instances()
    self.assertGreater(len(ins), 1, ins)

    ins = instances(exp='production-.*')
    self.assertGreater(len(ins), 1, ins)

    ins = instances(exp='staging-.*')
    self.assertEqual(len(ins), 0, ins)

if __name__ == '__main__':
  unittest.main()
