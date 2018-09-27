from common.myunit import StartEnd
from businessView.registerView import RegisterView
import logging,random,unittest

class RegisterTest(StartEnd):
    def test_user_register(self):
        logging.info('======test_user_register======')
        r=RegisterView(self.driver)

        username = 'zxw2018' + 'fly' + str(random.randint(1000, 9000))
        password = 'zxw2018' + str(random.randint(1000, 9000))
        email = '51zxw' + str(random.randint(1000, 9000)) + '@163.com'

        self.assertTrue(r.register_action(username,password,email))

if __name__ == '__main__':
    unittest.main()