import unittest
from app import app


print("HI ")
class TestAPI(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
    print("Hello")
    def test_valid_login(self):
        print("dl")
        response = self.app.post('/login', data=dict(inp_start1='wernertheresa', inp_start2='Ccvxg@4'))
        print("ML")
        self.assertEqual(response.status_code, 302) # Successful redirect
        
    def test_invalid_username(self):
        response = self.app.post('/login', data=dict(inp_start1='invalid_username', inp_start2='valid_password'))
        self.assertEqual(response.status_code, 200) # Bad Request
        
    def test_invalid_password(self):
        response = self.app.post('/login', data=dict(inp_start1='wernertheresa', inp_start2='invalid_password'))
        self.assertEqual(response.status_code, 200) # Bad Request



if __name__ == '__main__':
    unittest.main()
