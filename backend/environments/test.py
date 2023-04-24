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
        self.assertNotEqual(response.status_code, 302) # Successful redirect
        
    def test_invalid_username(self):
        response = self.app.post('/login', data=dict(inp_start1='invalid_username', inp_start2='valid_password'))
        self.assertEqual(response.status_code, 200) # Bad Request
        
    def test_invalid_password(self):
        response = self.app.post('/login', data=dict(inp_start1='asdfgh12345', inp_start2='password'))
        self.assertEqual(response.status_code, 200) # Bad Request

if __name__ == '__main__':
    unittest.main()


# import pytest
# from app import app

# @pytest.fixture
# def client():
#     app.config['TESTING'] = True
#     with app.test_client() as client:
#         yield client

# def test_signup_form(client):
#     rv = client.post('/signup', data=dict(
#         username_signup='testuser',
#         email_signup='testuser@example.com',
#         otp_signup='123456',
#         password_signup='Test1234',
#         confirm_signup='Test1234',
#         country_signup='USA',
#         state_signup='CA',
#         city_signup='Los Angeles',
#         web_signup='http://example.com',
#         git_signup='https://github.com/testuser',
#         org_signup='Example Org',
#         image_profile_signup='testuser.jpg',
#         name_signup='Test User',
#         send_button_signup='send_otp_signup'
#     ))
#     assert b'Enter OTP' in rv.data
#     assert b'Please enter Email' not in rv.data

#     rv = client.post('/signup', data=dict(
#         username_signup='testuser',
#         email_signup='testuser@example.com',
#         otp_signup='123456',
#         password_signup='Test1234',
#         confirm_signup='Test1234',
#         country_signup='USA',
#         state_signup='CA',
#         city_signup='Los Angeles',
#         web_signup='http://example.com',
#         git_signup='https://github.com/testuser',
#         org_signup='Example Org',
#         image_profile_signup='testuser.jpg',
#         name_signup='Test User',
#         send_button_signup='create_account_signup'
#     ))
#     assert b'Please enter Email' not in rv.data
#     assert b'Invalid OTP' not in rv.data
#     assert b'Password and Confirm Password do not match' not in rv.data
#     assert b'Password strength is low' not in rv.data
#     assert b'Welcome to Synergy' in rv.data



# # import unittest

# # class SimpleTest(unittest.TestCase):

# # 	# Returns True or False.
# # 	def test(
# self):		
# # 		self.assertTrue(True)

# # if __name__ == '__main__':
# # 	unittest.main()

# # Python code to demonstrate working of unittest
# import unittest
# import helper as app

# # class TestStringMethods(unittest.TestCase):
	
# # 	def setUp(self):
# # 		pass

# # 	# Returns True if the string contains 4 a.
# # 	def test_strings_a(self):
# # 		self.assertEqual( 'a'*4, 'aaaa')

# # 	# Returns True if the string is in upper case.
# # 	def test_upper(self):		
# # 		self.assertEqual('foo'.upper(), 'FOO')

# # 	# Returns TRUE if the string is in uppercase
# # 	# else returns False.
# # 	def test_isupper(self):		
# # 		self.assertTrue('FOO'.isupper())
# # 		self.assertFalse('Foo'.isupper())

# # 	# Returns true if the string is stripped and
# # 	# matches the given output.
# # 	def test_strip(self):		
# # 		s = 'geeksforgeeks'
# # 		self.assertFalse(s.strip('geek') + 'sforgeeks' ==  s)

# # 	# Returns true if the string splits and matches
# # 	# the given output.
# # 	def test_split(self):		
# # 		s = 'hello world'
# # 		self.assertEqual(s.split(), ['hello', 'world'])
# # 		with self.assertRaises(TypeError):
# # 			s.split(2)




# class TestActual(unittest.TestCase):
	
#     def test_follow(self):
# 	    self.assertIsNone(app.follow(str("asdfgh12987"),str("asdfgh12345")))

# if __name__ == '__main__':
# 	# app.run(debug = True)
#     app.init_db()
#     unittest.main()
