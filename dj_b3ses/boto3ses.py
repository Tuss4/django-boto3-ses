"""Boto3 SES email backend class"""
from django.core.mail.backends.base import BaseEmailBackend
from django.conf import settings
import boto3


client = boto3.client('ses')


class SESEmailBackend(BaseEmailBackend):

    def send_messages(self, email_messages):
        if not email_messages:
            return
        num_sent = 0
        for message in email_messages:
            sent = self._send(message)
            if sent:
                num_sent += 1
        return num_sent

    def _send(self, email_message):
        """
        Private message to send out an email message instance
        via boto3 SES
        """
        try:
            client.send_email(
                Source=email_message.from_email,
                Destination={
                    'ToAddresses': email_message.to,
                    'CcAddresses': email_message.cc,
                    'BccAddresses': email_message.bcc,
                },
                Message={
                    'Subject': {
                        'Data': email_message.subject,
                        'Charset': 'utf-8'
                    },
                    'Body': {
                        'Text': {
                            'Data': email_message.body,
                            'Charset': 'utf-8'
                        }
                    }
                },
                SourceArn=settings.AWS_SES_ARN
            )
        except Exception:
            if not self.fail_silently:
                raise
            return False
        return True
