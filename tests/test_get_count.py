#!/usr/bin/python3
""" Test .get() and .count() methods
"""
import unittest
from models import storage
from models.state import State

class TestGetCountMethods(unittest.TestCase):
    """Test case for get() and count() methods"""

    def test_get_count(self):
        """Test get() and count() methods"""
        state_obj = State(name="California")
        storage.new(state_obj)
        storage.save()
        state_id = state_obj.id

        self.assertEqual(storage.get(State, state_id), state_obj)
        self.assertEqual(storage.count(State), 1)

if __name__ == '__main__':
    unittest.main()

