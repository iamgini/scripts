# to test email from python
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText

email_from_addr = "myfromemail@gmail.com"
email_to_addr = "mytoemail@gmail.com"
email_smtp_server = "smtp.gmail.com"
email_smtp_port = "587"
email_user = "myfromemail"
email_password = "mypassword"

# Email Subject
email_subject = "Welcome to Python Email Test"

# HTML + CSS for body
email_body = None

email_body_header = ' '
email_body_header = email_body_header + '<html><head></head><body>'
email_body_header = email_body_header + '<style type="text/css"></style>'
email_body_header = email_body_header + '<br><p>Hello Team,<br><br>This is a test email.<br>'

email_body_content = ' '
email_body_content = email_body_content + '<H1>This is main content area</h1>'

email_body_footer = ' '
email_body_footer = email_body_footer + '<br>Thank you'
email_body_footer = email_body_footer + '<br>Support Team<br>'

email_body = str(email_body_header) + str(email_body_content) + str(email_body_footer)

# Prepare email content - MIMEMultipart
message = MIMEMultipart('alternative')
message['From'] = email_from_addr
message['To'] = email_to_addr
message['Subject'] = email_subject
body = email_body
message.attach(MIMEText(body, 'html'))

#print (email_body)

server = smtplib.SMTP(email_smtp_server,int(email_smtp_port))
text = message.as_string()
server.starttls()
server.login(email_user, email_password)
server.sendmail(email_from_addr,email_to_addr,message.as_string())
server.quit()
