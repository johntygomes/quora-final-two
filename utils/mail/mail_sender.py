################################################################
from .Google import Create_Service
import base64
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
################################################################
CLIENT_SECRET_FILE = 'client_secret2.json'
API_NAME = 'gmail'
API_VERSION = 'v1'
SCOPES = ['https://mail.google.com/']
################################################################
class MailSender:
    mail_sender     = "pchackr7@gmail.com"
    def __init__(self,mail_receiver):
        self.mail_receiver       = mail_receiver
    def sendUserAnswerNotification(self,question_object,response_object):
        self.question_object     = question_object
        self.response_object     = response_object
        service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)
        try:
            temp = "Check Out The Answer At:: https://quora-final.herokuapp.com/question/"+str(question_object.id)
            emailMsg = temp
            mimeMessage = MIMEMultipart()
            mimeMessage['to'] = question_object.author.email
            temp = question_object.title + " Got An Answer From:: " + response_object.username
            mimeMessage['subject'] = temp
            mimeMessage.attach(MIMEText(emailMsg, 'plain'))
            raw_string = base64.urlsafe_b64encode(mimeMessage.as_bytes()).decode()
            message = service.users().messages().send(userId='me', body={'raw': raw_string}).execute()
        except Exception as e:
            print("error",e)
