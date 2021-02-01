import datetime
import jwt

from sqlalchemy_utils import ChoiceType
from sqlalchemy.orm import relationship

from project.server import app, db, bcrypt


class User(db.Model):
    """ User Model for storing user related details """
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    registered_on = db.Column(db.DateTime, nullable=False)
    admin = db.Column(db.Boolean, nullable=False, default=False)
    loan_applications = relationship("LoanApplication")

    def __init__(self, email, password, admin=False):
        self.email = email
        self.password = bcrypt.generate_password_hash(
            password, app.config.get('BCRYPT_LOG_ROUNDS')
        ).decode()
        self.registered_on = datetime.datetime.now()
        self.admin = admin
    
    def encode_auth_token(self, user_id):
        """
        Generates the Auth Token
        :return: string
        """
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, seconds=60*60),
                'iat': datetime.datetime.utcnow(),
                'sub': user_id
            }
            return jwt.encode(
                payload,
                app.config.get('SECRET_KEY'),
                algorithm='HS256'
            )
        except Exception as e:
            return e

    
    @staticmethod
    def decode_auth_token(auth_token):
        """
        Validates the auth token
        :param auth_token:
        :return: integer|string
        """
        try:
            is_blacklisted_token = BlacklistToken.check_blacklist(auth_token)
            payload = jwt.decode(jwt=auth_token,  key=app.config.get('SECRET_KEY'), algorithms=['HS256'])
            if is_blacklisted_token:
                return 'Token blacklisted. Please log in again.'
            else:
                return payload['sub']
        except jwt.ExpiredSignatureError:
            return 'Signature expired. Please log in again.'
        except jwt.InvalidTokenError:
            return 'Invalid token. Please log in again.'

class LoanApplication(db.Model):
    """Model for storing the loan applications of the users."""
    __tablename__ = 'loan_applications'

    STATES = [
        (u'pending', u'Pending'),
        (u'approved', u'Approved'),
        (u'denied', u'Denied'),
    ]
    

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    creator_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    creator = relationship("User", back_populates="loan_applications")
    business_name = db.Column(db.String(255), nullable=False)
    tax_id = db.Column(db.String(20), nullable=False)
    requested_amount = db.Column(db.Numeric(12,4), nullable=False)
    application_status = db.Column(ChoiceType(STATES), nullable=False)
    requested_on = db.Column(db.DateTime, nullable=False)
    loan = relationship("Loan", uselist=False, back_populates="loan_application")


    def __init__(self, creator_id, business_name, requested_amount, tax_id, application_status):
        self.creator_id = creator_id
        self.business_name = business_name
        self.requested_amount = requested_amount
        self.tax_id = tax_id
        self.application_status = application_status
        self.requested_on = datetime.datetime.now()

    def __repr__(self):
        return f"{self.business_name}, {self.requested_amount}, {self.application_status}"


class Loan(db.Model):
    """Represents the loans that have been accepted."""
    __tablename__ = 'loans'

    STATES = [
        (u'active', u'Active'),
        (u'closed', u'Closed'),
    ]

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    loan_application_id = db.Column(db.Integer, db.ForeignKey('loan_applications.id'))
    loan_application = relationship("LoanApplication", back_populates="loan")
    loan_status = db.Column(ChoiceType(STATES), nullable=False)
    accepted_on = db.Column(db.DateTime, nullable=False)
    requested_amount = db.Column(db.Numeric(12,4), nullable=False)

    def __init__(self, loan_application_id, loan_status, requested_amount):
        self.loan_application_id = loan_application_id
        self.loan_status = loan_status
        self.accepted_on = datetime.datetime.now()
        self.requested_amount = requested_amount

    def __repr__(self):
        return f"{self.loan_application}, accepted_on={self.accepted_on}"

class BlacklistToken(db.Model):
    """Token Model for storing JWT tokens that have been blacklisted."""
    __tablename__ = 'blacklist_tokens'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    token = db.Column(db.String(500), unique=True, nullable=False)
    blacklisted_on = db.Column(db.DateTime, nullable=False)

    def __init__(self, token):
        self.token = token
        self.blacklisted_on = datetime.datetime.now()

    def __repr__(self):
        return '<id: token: {}'.format(self.token)

    @staticmethod
    def check_blacklist(auth_token):
        # check whether auth token has been blacklisted
        res = BlacklistToken.query.filter_by(token=str(auth_token)).first()
        if res:
            return True
        else:
            return False
