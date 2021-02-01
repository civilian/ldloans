import unittest
import json
from project.tests.base import BaseTestCase
from project.tests.test_auth import register_user, login_user
from project.server.models import LoanApplication, User

def create_loan_application(self, auth_token, loan_application):
    """Helper function, creates a loan application via api rest, given the auth_token and the loan application object"""
    return self.client.post(
        '/loan/apply',
        data=json.dumps(dict(
            business_name=loan_application.business_name, 
            tax_id=loan_application.tax_id,
            requested_amount=loan_application.requested_amount
        )),
        headers=dict(
            Authorization='Bearer ' + auth_token
        ),
        content_type='application/json',
    )

class TestLoanApplicationBlueprint(BaseTestCase):

    def _test_loan_application_boilerplate(self, loan_application, status, message, status_code, function_access=register_user):
        """Helper function to test for loan application"""
        with self.client:
            response = function_access(self, 'joe@gmail.com', '123456')
            data = json.loads(response.data.decode())
            response_loan = create_loan_application(self, auth_token=data['auth_token'], 
                loan_application=loan_application)
            data_loan = json.loads(response_loan.data.decode())
            self.assertTrue(data_loan['status'] == status)
            self.assertTrue(data_loan['data']['message'] == message)
            self.assertTrue(response_loan.content_type == 'application/json')
            self.assertEqual(response_loan.status_code, status_code)

    def test_loan_application_creation_accepts(self):
        """ Test loan application for success """
        loan_application = LoanApplication(creator_id=1,
                business_name="small waltmart", tax_id='1234-5678-9012',
                requested_amount=49999, application_status=u'approved')
        self._test_loan_application_boilerplate(loan_application=loan_application,status='success',
                                                message='Your loan application was approved, Congratulations!!.',
                                                status_code=200)
    
    def test_loan_application_creation_denied(self):
        """ Test loan application for denied """
        loan_application = LoanApplication(creator_id=1,
                business_name="small waltmart", tax_id='1234-5678-9012',
                requested_amount=50001, application_status=u'denied')
        message = f"The amount requested is bigger than 50000 so your Loan was " \
                                "rejected."
        self._test_loan_application_boilerplate(loan_application=loan_application,status='fail',
                                                message=message,
                                                status_code=208)
    
    def test_loan_application_creation_denied(self):
        """ Test loan application for pending """
        loan_application = LoanApplication(creator_id=1,
                business_name="small waltmart", tax_id='1234-5678-9012',
                requested_amount=50000, application_status=u'pending')
        message = f"We are reviewing your loan application."
        self._test_loan_application_boilerplate(loan_application=loan_application,status='success',
                                                message=message,
                                                status_code=200)
    
    def test_loan_application_creation_tells_you_to_wait_an_hour(self):
        """ Test loan application too fast and tells you to wait an hour."""
        loan_application = LoanApplication(creator_id=1,
                business_name="small waltmart", tax_id='1234-5678-9012',
                requested_amount=40000, application_status=u'denied')
        message = f"Your loan application was approved, Congratulations!!."
        self._test_loan_application_boilerplate(loan_application=loan_application,status='success',
                                                message=message,
                                                status_code=200)
        message_wait_an_hour = f"You requested a Loan Application for the company " \
                        f"{loan_application.business_name} for that same amount " \
                        "less than an hour ago, you need to wait to ask for it again."
        self._test_loan_application_boilerplate(loan_application=loan_application, status='fail',
                                                message=message_wait_an_hour,
                                                status_code=208, function_access=login_user)
    

    def test_loan_application_creation_tells_you_there_is_a_pending_one(self):
        """ Test loan application too fast and tells you there is one loan application pending."""
        loan_application = LoanApplication(creator_id=1,
                business_name="small waltmart", tax_id='1234-5678-9012',
                requested_amount=50000, application_status=u'pending')
        message = f"We are reviewing your loan application."
        self._test_loan_application_boilerplate(loan_application=loan_application, status='success',
                                                message=message,
                                                status_code=200)
        message_pending = 'You already have a pending loan application with the same data'
        self._test_loan_application_boilerplate(loan_application=loan_application, status='fail',
                                                message=message_pending,
                                                status_code=208, function_access=login_user)

if __name__ == '__main__':
    unittest.main()