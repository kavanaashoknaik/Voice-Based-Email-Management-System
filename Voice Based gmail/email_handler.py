import smtplib
import imaplib
import email
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from config import Config

class EmailHandler:
    """Handles email operations using Gmail"""

    def __init__(self, gmail_address, gmail_app_password):
        self.gmail_address = gmail_address
        self.gmail_app_password = gmail_app_password
        self.smtp_server = Config.SMTP_SERVER
        self.smtp_port = Config.SMTP_PORT

    def send_email(self, to_email, subject, message):
        """Send an email using Gmail SMTP"""
        try:
            # Create message
            msg = MIMEMultipart()
            msg['From'] = self.gmail_address
            msg['To'] = to_email
            msg['Subject'] = subject
            msg.attach(MIMEText(message, 'plain'))

            # Connect to Gmail SMTP server
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.gmail_address, self.gmail_app_password)

            # Send email
            text = msg.as_string()
            server.sendmail(self.gmail_address, to_email, text)
            server.quit()

            return True, "Email sent successfully"

        except smtplib.SMTPAuthenticationError:
            return False, "Authentication failed. Please check your app password."
        except smtplib.SMTPException as e:
            return False, f"SMTP error: {str(e)}"
        except Exception as e:
            return False, f"Error sending email: {str(e)}"

    def get_inbox_emails(self, max_emails=10):
        """Fetch inbox emails using IMAP"""
        try:
            # Connect to Gmail IMAP server
            mail = imaplib.IMAP4_SSL('imap.gmail.com')
            mail.login(self.gmail_address, self.gmail_app_password)
            mail.select('inbox')

            # Search for all emails
            status, messages = mail.search(None, 'ALL')

            if status != 'OK':
                return False, "Failed to retrieve emails", [], 0

            email_ids = messages[0].split()
            total_count = len(email_ids)  # Total number of emails
            email_ids.reverse()  # Get latest first

            emails = []
            count = 0

            for email_id in email_ids:
                if count >= max_emails:
                    break

                try:
                    status, msg_data = mail.fetch(email_id, '(RFC822)')

                    if status != 'OK':
                        continue

                    # Parse email
                    msg = email.message_from_bytes(msg_data[0][1])

                    # Extract email details
                    from_email = self._decode_header(msg.get('From'))
                    subject = self._decode_header(msg.get('Subject'))
                    date = msg.get('Date')

                    # Get email body
                    body = self._get_email_body(msg)

                    emails.append({
                        'id': email_id.decode(),
                        'from': from_email,
                        'subject': subject,
                        'date': date,
                        'body': body,
                        'seen': 'SEEN' in str(msg_data)
                    })

                    count += 1

                except Exception as e:
                    print(f"Error parsing email {email_id}: {e}")
                    continue

            mail.close()
            mail.logout()

            return True, f"Retrieved {len(emails)} of {total_count} emails", emails, total_count

        except imaplib.IMAP4.error as e:
            return False, f"IMAP error: {str(e)}", [], 0
        except Exception as e:
            return False, f"Error retrieving emails: {str(e)}", [], 0

    def get_sent_emails(self, max_emails=10):
        """Fetch sent emails using IMAP"""
        try:
            # Connect to Gmail IMAP server
            mail = imaplib.IMAP4_SSL('imap.gmail.com')
            mail.login(self.gmail_address, self.gmail_app_password)

            # Select sent folder (Gmail uses [Gmail]/Sent Mail)
            status, _ = mail.select('"[Gmail]/Sent Mail"')

            if status != 'OK':
                # Try alternative folder name
                status, _ = mail.select('Sent')

            if status != 'OK':
                return False, "Failed to access sent folder", [], 0

            # Search for all emails
            status, messages = mail.search(None, 'ALL')

            if status != 'OK':
                return False, "Failed to retrieve sent emails", [], 0

            email_ids = messages[0].split()
            total_count = len(email_ids)  # Total number of sent emails
            email_ids.reverse()  # Get latest first

            emails = []
            count = 0

            for email_id in email_ids:
                if count >= max_emails:
                    break

                try:
                    status, msg_data = mail.fetch(email_id, '(RFC822)')

                    if status != 'OK':
                        continue

                    # Parse email
                    msg = email.message_from_bytes(msg_data[0][1])

                    # Extract email details
                    to_email = self._decode_header(msg.get('To'))
                    subject = self._decode_header(msg.get('Subject'))
                    date = msg.get('Date')

                    # Get email body
                    body = self._get_email_body(msg)

                    emails.append({
                        'id': email_id.decode(),
                        'to': to_email,
                        'subject': subject,
                        'date': date,
                        'body': body
                    })

                    count += 1

                except Exception as e:
                    print(f"Error parsing sent email {email_id}: {e}")
                    continue

            mail.close()
            mail.logout()

            return True, f"Retrieved {len(emails)} of {total_count} sent emails", emails, total_count

        except imaplib.IMAP4.error as e:
            return False, f"IMAP error: {str(e)}", [], 0
        except Exception as e:
            return False, f"Error retrieving sent emails: {str(e)}", [], 0

    def delete_email(self, email_id):
        """Delete an email by moving it to trash"""
        try:
            mail = imaplib.IMAP4_SSL('imap.gmail.com')
            mail.login(self.gmail_address, self.gmail_app_password)
            mail.select('inbox')

            # Mark email for deletion
            mail.store(email_id, '+FLAGS', '\\Deleted')

            # Permanently remove deleted emails
            mail.expunge()

            mail.close()
            mail.logout()

            return True, "Email deleted successfully"

        except Exception as e:
            return False, f"Error deleting email: {str(e)}"

    def reply_to_email(self, original_from, original_subject, reply_message):
        """Reply to an email"""
        # Add "Re:" prefix if not already present
        if not original_subject.startswith('Re:'):
            subject = f"Re: {original_subject}"
        else:
            subject = original_subject

        return self.send_email(original_from, subject, reply_message)

    def _decode_header(self, header):
        """Decode email header"""
        if header is None:
            return ""

        decoded_parts = email.header.decode_header(header)
        decoded_header = ""

        for part, encoding in decoded_parts:
            if isinstance(part, bytes):
                try:
                    decoded_header += part.decode(encoding or 'utf-8')
                except:
                    decoded_header += part.decode('utf-8', errors='ignore')
            else:
                decoded_header += part

        return decoded_header

    def _get_email_body(self, msg):
        """Extract email body from message"""
        body = ""

        if msg.is_multipart():
            for part in msg.walk():
                content_type = part.get_content_type()
                content_disposition = str(part.get('Content-Disposition'))

                if content_type == 'text/plain' and 'attachment' not in content_disposition:
                    try:
                        body = part.get_payload(decode=True).decode()
                        break
                    except:
                        pass
        else:
            try:
                body = msg.get_payload(decode=True).decode()
            except:
                body = str(msg.get_payload())

        return body.strip()

    def get_unread_count(self):
        """Get count of unread emails"""
        try:
            mail = imaplib.IMAP4_SSL('imap.gmail.com')
            mail.login(self.gmail_address, self.gmail_app_password)
            mail.select('inbox')

            status, messages = mail.search(None, 'UNSEEN')

            if status == 'OK':
                count = len(messages[0].split())
            else:
                count = 0

            mail.close()
            mail.logout()

            return count

        except Exception as e:
            print(f"Error getting unread count: {e}")
            return 0
