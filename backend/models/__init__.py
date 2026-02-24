from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .user import User
from .child import Child
from .growth import GrowthRecord
from .risk import RiskAssessment
from .intervention import Intervention
from .hospital import Hospital
from .resource import Resource
from .verification_code import VerificationCode

__all__ = ['db', 'User', 'Child', 'GrowthRecord', 'RiskAssessment', 'Intervention', 'Hospital', 'Resource', 'VerificationCode']
