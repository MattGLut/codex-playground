import unittest
from app.main import app, read_root

class TestAuth(unittest.TestCase):
    def test_read_root(self):
        self.assertEqual(read_root(), {"message": "Hello, world!"})

if __name__ == "__main__":
    unittest.main()
