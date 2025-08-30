import os
from mailersend import emails
from loguru import logger

from .config import smtp_server_config, app_config
from .template import Template
from .metrics.email_metrics import metric_email_client


class EmailClient:
    """A class for creating and send Gmail message.

      Methods
      -------
      create()
          returns the finished letter in base64 format
      send()
          Sends a message
      make_template()
          Processes a template using the Template class. Returns the processing result
      """

    def __init__(
            self,
            email: str,
            subject: str = '',
            template: str = 'default_mail.html',
            template_vars: dict = {}
    ):
        """Initialize a message

        Parameters
        ----------
        email : str
            Destination e-mail address
        subject : str
            Subject your e-mail. Default subject vars contains in mails package
        template : str
            Name of template. F.e. 'default.html'. Templates finds in TEMPLATES_DIR
            (this parameter can be change in __init__ file mails package)
        template_vars : dict
            Dictionary with names and values of variables for the passed template
       """

        self.logger = logger
        self.template = ""
        self.smtp_server = smtp_server_config.SMTP_SERVER
        self.port = smtp_server_config.SMTP_SERVER_PORT
        self.sender_email = smtp_server_config.MASTER_EMAIL
        self.password = smtp_server_config.SMTP_SERVER_PASSWORD
        self.email = email
        self.template_vars = template_vars
        self.subject = subject
        self.templated_message = Template(
            template=template,
            template_vars=self.template_vars
        ).render()
        if self.templated_message:
            self.logger.info(
                f"self.templated_message: {self.templated_message}"
            )
            self.logger.info("template rendered")
        else:
            self.logger.error("Problem with email template")
            raise Exception("Problem with email template")

    @metric_email_client
    def send(self):
        """
        Sends a message with object parameters
        """
        self.logger.info(f'Try to send to: {self.email}')
        try:
            token = os.getenv('MAILERSEND_API_KEY')
            mailer = emails.NewEmail(token)
            self.logger.info(f"token: {token}")
            mail_body = {}

            mail_from = {
                "name": app_config.APP_NAME,
                "email": self.sender_email
            }
            recipients = [
                {
                    "name": "Client",
                    "email": self.email
                }
            ]

            # reply_to = {
            #     "name": "Name",
            #     "email": "reply@domain.com",
            # }

            mailer.set_mail_from(mail_from, mail_body)
            mailer.set_mail_to(recipients, mail_body)
            mailer.set_subject(self.subject, mail_body)
            mailer.set_html_content(self.templated_message, mail_body)
            # mailer.set_reply_to(reply_to, mail_body)

            self.logger.info(f"mail_body: {mail_body}")

            # using print() will also return status code and data
            result = mailer.send(mail_body)
            self.logger.info(f"result sending: {result}")

        except Exception as e:
            self.logger.error(f'Email Client error: {e}')
            raise e
        self.logger.info(f'Succesful sent: {self.email}')
        return True

    def __repr__(self):
        return f'<Message obj {self.email}>'
