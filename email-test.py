#!/usr/bin/env python3

import smtplib, ssl
import _email_creds_

port = 465  # For SSL
message = """\
Subject: Hi there

This message is sent from Python."""

context = ssl.create_default_context()
with smtplib.SMTP_SSL(_email_creds_.smtp_server, port, context=context) as server:
    server.login(_email_creds_.sender_email, _email_creds_.password)
    server.sendmail(_email_creds_.sender_email, _email_creds_.receiver_email, message)


