import unittest
from app import app
import io
from unittest.mock import patch, MagicMock

# print("HI ")
class TestAPI(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
    # print("Hello")
    def test_valid_login(self):
        # print("dl")
        response = self.app.post('/login', data=dict(inp_start1='bcarpenter', inp_start2='Uyxhq@7'))
        # print("ML")
        self.assertEqual(response.status_code, 302) # Successful redirect
        
    def test_invalid_username(self):
        response = self.app.post('/login', data=dict(inp_start1='invalid_username', inp_start2='valid_password'))
        self.assertEqual(response.status_code, 200) # Bad Request
        
    def test_invalid_password(self):
        response = self.app.post('/login', data=dict(inp_start1='bcarpenter', inp_start2='invalid_password'))
        self.assertEqual(response.status_code, 200) # Bad Request
    
    def test_create_account_success(self):
        data = {
            'username_signup': 'tp2',
                'email_signup': 'tp2@gmail.com',
                'otp_signup': '',
                'password_signup': '',
                'confirm_signup': '',
                'country_signup': '',
                'state_signup': '',
                'city_signup': '',
                'web_signup': '',
                'git_signup': '',
                'org_signup': '',
                'name_signup': '',
                'send_button_signup': 'send_otp_signup'
        }
        response = self.app.post('/signup', data=data)
        # print("For otp_send: ",response.status_code)
        self.assertEqual(response.status_code, 200)
        # print("good")
        # print(response.data)
        self.assertIn(b"Enter OTP", response.data)
        with open('DefaultPhoto.png', 'rb') as f:
            image_data = f.read()
        print("Okay ")
        data = {
            'username_signup': 'tp2',
                'email_signup': 'tp2@gmail.com',
                'otp_signup': '123456',
                'password_signup': 'Test@31234',
                'confirm_signup': 'Test@31234',
                'country_signup': 'testcountry',
                'state_signup': 'teststate',
                'city_signup': 'testcity',
                'web_signup': 'testweb',
                'git_signup': 'testgit',
                'org_signup': 'testorg',
                'image_profile_signup': 'testimage',
                'name_signup': 'testname',
                'image_profile_signup': (io.BytesIO(image_data), 'test_image.jpg'),
            'send_button_signup': 'create_account_signup'
        }
        response = self.app.post('/signup', data=data)
        # print("kksdf \n")
        # print("kksdf \n")
        # print(response)
        # print("kksdf \n")
        # print("kksdf \n")
        self.assertEqual(response.status_code, 302)
        # print(response.headers['Location'])
        self.assertEqual(response.headers['Location'], '/')
    
    def test_home_route_with_valid_username(self):
        response = self.app.get('/home/bcarpenter')
        self.assertEqual(response.status_code, 200)
        # self.assertIn(b'testuser', response.data)
        # self.assertIn(b'Home Page', response.data)

    def test_post_input(self):
        response = self.app.get('/home/bcarpenter')
        self.assertEqual(response.status_code, 200)
        response = self.app.post('/home/post', data={
            'posttit': 'Test Post',
            'posttags': 'test; unit; flask',
            'post_description': 'This is a test post for unit testing Flask',
            'postinst': 'IIT Delhi',
            'zipfile': (io.BytesIO(b'some_zip_file_contents'), 'test.zip'),
            'imagefile': (io.BytesIO(b'some_image_file_contents'), 'test.jpg')
        })
        self.assertEqual(response.status_code, 302)
    
    def test_post(self):
        # with client.session_transaction() as session:
        #     session['user'] = {'id_uniq': 'aaaaaaaaaa1111112057'}
        response = self.app.get('/home/bcarpenter')
        self.assertEqual(response.status_code, 200)
        print("cp3")
        response = self.app.get('/post/pppppppppp1111111147')
        print("cp4")
        self.assertEqual(response.status_code, 200)
    
    def test_search(self):
        response = self.app.get('/home/bcarpenter')
        self.assertEqual(response.status_code, 200)
        print("cp3")
        response = self.app.post('/search', data={'query': 'II'})
        print("cp4")
        self.assertEqual(response.status_code, 200)
    
    def test_valid_email(self):
        response = self.app.post('/login/otp', data={'email_start': 'daviddaniels@example.org', 'submit_button_start': 'submit_start1'})
        self.assertIn(b'Enter OTP', response.data)

    def test_invalid_email(self):
        response = self.app.post('/login/otp', data={'email_start': 'invalid@example.com', 'submit_button_start': 'submit_start1'})
        self.assertIn(b'Email not Registered, Please SignUp', response.data)
    
    def test_valid_otp(self):
        response = self.app.post('/login/otp', data={'email_start': 'daviddaniels@example.org', 'otp_start': '123456', 'submit_button_start': 'submit_start2'})
        self.assertEqual(response.status_code, 200)
    
    def test_invalid_otp(self):
        response = self.app.post('/login/otp', data={'email_start': 'daviddaniels@example.org', 'submit_button_start': 'submit_start1'})
        self.assertIn(b'Enter OTP', response.data)
        response = self.app.post('/login/otp', data={'email_start': 'daviddaniels@example.org', 'otp_start': '654321', 'submit_button_start': 'submit_start2'})
        self.assertIn(b'Invalid OTP', response.data)

    # def test_sort(self):
    #     response = self.app.post('/search/bcarpenter/time')
    #     print(response)
    #     print("hi")
    #     self.assertEqual(response.status_code, 302)



if __name__ == '__main__':
    unittest.main()
