from twilio.rest import Client
import os


def send_otp(phone):
    client = Client(os.getenv('TWILIO_ACCOUNT_SID'), os.getenv('TWILIO_AUTH_TOKEN'))
    verification = client.verify.services(os.getenv('TWILIO_SERVICE_SID')).verifications.create(
        to=phone,
        channel='sms'
    )
    return verification.sid


def verify_otp(phone, code):
    client = Client(os.getenv('TWILIO_ACCOUNT_SID'), os.getenv('TWILIO_AUTH_TOKEN'))
    verification_check = client.verify.services(os.getenv('TWILIO_SERVICE_SID')).verification_checks.create(
        to=phone,
        code=code
    )
    return verification_check.status == 'approved'
