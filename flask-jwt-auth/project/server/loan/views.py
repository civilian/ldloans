from datetime import datetime, timedelta

from flask import Blueprint, request, make_response, jsonify
from flask.views import MethodView

from project.server import bcrypt, db
from project.server.models import Loan, LoanApplication
from project.server.auth.decorators import handle_request_with_authorisation_token

loan_blueprint = Blueprint('loans', __name__)

class LoanApplicationsApi(MethodView):
    """
    Loan Application Resource
    """
    requested_amount_limit = 50000

    def _create_loan(self, loan_application):
        """Creates a loan if the loan application was approved"""
        if loan_application.application_status == u'approved':
            loan = Loan(loan_application_id=loan_application.id,
                requested_amount=loan_application.requested_amount,
                loan_status=u'active')
            db.session.add(loan)
            db.session.commit()


    @handle_request_with_authorisation_token
    def post(self, *args, **kwargs):
        post_data = request.get_json()
        user = kwargs['user']
        
        message = ""

        loan_application_pending = LoanApplication.query.filter_by(
                creator_id=user.id,
                business_name=post_data['business_name'],
                tax_id=post_data['tax_id'],
                requested_amount=post_data['requested_amount'],
                application_status=u'pending').first()
        if loan_application_pending:
            response_status = 208
            message = 'You already have a pending loan application with the same data'
            status = 'fail'
        else:
            an_hour_ago = datetime.now() - timedelta(hours=1)
            loan_application_same_time = LoanApplication.query.filter_by(
                creator_id=user.id,
                business_name=post_data['business_name'],
                requested_amount=post_data['requested_amount'],
                tax_id=post_data['tax_id'],
            ).filter(LoanApplication.requested_on > an_hour_ago).first()
            if loan_application_same_time:
                response_status = 208
                message = f"You requested a Loan Application for the company " \
                        f"{post_data['business_name']} for that same amount " \
                        "less than an hour ago, you need to wait to ask for it again."
                status = 'fail'
            else:
                requested_amount = int(post_data['requested_amount'])
                if requested_amount > self.requested_amount_limit:
                    loan_status = u'denied'
                    status = 'fail'
                    response_status = 208
                    message = f"The amount requested is bigger than 50000 so your Loan was " \
                                "rejected."
                elif requested_amount == self.requested_amount_limit:
                    loan_status = u'pending'
                    status = 'success'
                    response_status = 200
                    message = f"We are reviewing your loan application."
                else:
                    loan_status = u'approved'
                    status = 'success'
                    response_status = 200
                    message = f"Your loan application was approved, Congratulations!!."
                
                loan_application = LoanApplication(
                        creator_id=user.id,
                        business_name=post_data['business_name'],
                        requested_amount=post_data['requested_amount'],
                        tax_id=post_data['tax_id'],
                        application_status=loan_status)
                
                db.session.add(loan_application)
                db.session.commit()

                self._create_loan(loan_application)
        
        responseObject = {
            'status': status,
            'data': {
                'user_id': user.id,
                'message': message,
                'status': status,
            }
        }
        return make_response(jsonify(responseObject)), response_status

# define the API resources
loan_application_view = LoanApplicationsApi.as_view('loan_application_api')

# add Rules for API Endpoints
loan_blueprint.add_url_rule(
    '/loan/apply',
    view_func=loan_application_view,
    methods=['POST']
)