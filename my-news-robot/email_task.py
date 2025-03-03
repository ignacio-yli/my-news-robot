
import smtplib
from email.message import EmailMessage
import ssl
import smtplib

#This function takes the collected data and sends the email with the data.
def send_email(to_email, articles):
    subject = "Latest Research Articles"
    from_email = "my.news.robot123@gmail.com"
    password = "pswrd"

    body = format_email_content_html(articles)

    msg = EmailMessage()
    msg["From"] = from_email
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.set_content(body)
    msg.add_alternative(body, subtype="html")  
    context = ssl.create_default_context()

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(from_email, password)
            server.send_message(msg)

        print(f"Email successfully sent to {to_email}")

    except Exception as e:
        print(f"Failed to send email: {e}")



#This function formats the body of the email using html so it looks a bit better. 
def format_email_content_html(articles):
    email_content = "<html><body>"
    email_content += "<p>Hi there,</p>"
    email_content += "<p>Here are the top scientific articles for you:</p><ul>"
    
    for i, article in enumerate(articles, 1):
        email_content += f"<li><strong>Title:</strong> <a href='{article['link']}'>{article['title']}</a><br>"
        email_content += f"<strong>Date:</strong> {article['date'].replace('�', '').strip()}<br>"
        email_content += f"<strong>AI Review:</strong> {article['review']}</li><br><br>"
    
    email_content += "</ul><p>Best regards,<br>Your Research Bot</p>"
    email_content += "</body></html>"
    
    return email_content



def send_error_email(e):
    admin_email = "my.news.robot123@gmail.com"
    subject = "Error in News Bot"
    from_email = "my.news.robot123@gmail.com"
    password = "bfcx bibl zxzo hafo"

    body = f"""
    An error occurred in the research article email bot:

    Error Details:
    {str(e)}

    Please investigate.

    Best,  
    The News Bot
    """

    msg = EmailMessage()
    msg["From"] = from_email
    msg["To"] = admin_email
    msg["Subject"] = subject
    msg.set_content(body)

    context = ssl.create_default_context()

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(from_email, password)
            server.send_message(msg)

        print(f"Error email successfully sent to {admin_email}")

    except Exception as email_error:
        print(f"Failed to send error email: {email_error}")
