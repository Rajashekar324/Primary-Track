import unittest
from app import app

class FlaskAppTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_hello(self):
        response = self.app.get('/hello')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {"message": "Hello, World!"})

    def test_add(self):
        response = self.app.post('/add', json={'a': 5, 'b': 3})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {"result": 8})

if __name__ == '__main__':
    unittest.main()