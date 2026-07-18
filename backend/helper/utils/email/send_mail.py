import threading
from django.template.loader import render_to_string
from .email_backend import EmailBackEnd 
from django.conf import settings
data = EmailBackEnd()


class Email:
    
    @staticmethod
    def send_access_code_notification(email,code, name):
        """Sending Verification Email"""
        html_content = render_to_string(
            "email/notification/nin/new_access_code.html",
            {
                "email": email,
                "code": code,
                "title": "Your Access Code for NIN Enrolment",
                "name": name,
            },
        )
        """Call the Email Backend"""
        t1 = threading.Thread(
            args=data.send_grid(
                template=html_content, email=email, subject="Your Access Code for NIN Enrolment"
            )
        )
        t1.start()
        pass


    @staticmethod
    def send_2fa_access_code_notification(email,code, name):
        """Sending Verification Email"""
        html_content = render_to_string(
            "email/notification/account/2fa.html",
            {
                "email": email,
                "code": code,
                "title": "Security Alert: Enter Your 2FA Code to Continue",
                "name": name,
            },
        )
        """Call the Email Backend"""
        t1 = threading.Thread(
            args=data.send_grid(
                template=html_content, email=email, subject="Security Alert: Enter Your 2FA Code to Continue"
            )
        )
        t1.start()
        pass


    @staticmethod
    def send_account_setup_notification(email,link, name):
        """Sending Verification Email"""
        html_content = render_to_string(
            "email/notification/account/complete_setup.html",
            {
                "email": email,
                "link": link,
                "name": name,
            },
        )
        """Call the Email Backend"""
        t1 = threading.Thread(
            args=data.send_grid(
                template=html_content, email=email, subject="Complete Your Account Setup"
            )
        )
        t1.start()
        print("EMAIL ACCOUNT ACTIVATION")
        pass


    @staticmethod
    def send_account_creation_notification(email, name):
        """Sending Verification Email"""
        html_content = render_to_string(
            "email/notification/account/creation_success.html",
            {
                "email": email,
                "name": name,
            },
        )
        """Call the Email Backend"""
        t1 = threading.Thread(
            args=data.send_grid(
                template=html_content, email=email, subject="Your Account Has Been Successfully Created!"
            )
        )
        t1.start()
        print("EMAIL")
        pass



    @staticmethod
    def send_capturing_location_detail(email,**kwargs):
        """Sending Verification Email"""
        html_content = render_to_string(
            "email/notification/nin/new_capturing_location_details.html",
            {
                "email": email, **kwargs
            },
        )
        """Call the Email Backend"""
        t1 = threading.Thread(
            args=data.send_grid(
                template=html_content, email=email, subject="Capturing Center Details"
            )
        )
        t1.start()
        pass



# Email.send_capturing_location_detail('programmerolakay@gmail.com',name="Grace", center_name="portatble",code="918LDEIUEKD",city='',state='Lagos',location='Mainland',address_2='',capturing_date="",capturing_time="")
# Email.send_access_code_notification(
#     'lydia@prembly.com',"5000","Lydia"
# )