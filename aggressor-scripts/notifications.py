#! /usr/bin/env python
# notifications.py

import argparse
import slackweb
import socket
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText


def get_args():
    parser = argparse.ArgumentParser(description='beacon info')
    parser.add_argument('--computer_name')
    parser.add_argument('--internal_ip')
    parser.add_argument('--user_name')
    parser.add_argument('--external_ip')

    return parser.parse_args()


def get_notification_body(args):
    return "Check your Team Server! \nComputer Name" \
           " - {}\nInternal IP - {}\nExternal IP - {}\nUser - {}" \
        .format(args.computer_name, args.internal_ip, args.external_ip, args.user_name)


def send_slack_notification():
    slack_url = "https://hooks.slack.com/services/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"
    slack = slackweb.Slack(url=slack_url)
    message = get_notification_body(get_args())
    slack.notify(text=message)


def send_email_notification():
    from_address = "matthydework@gmail.com"
    to_address = ["7035859687@messaging.sprintpcs.com", "2409978171@vtext.com"]
    msg = MIMEMultipart()
    msg['From'] = from_address
    msg['To'] = ", ".join(to_address)
    msg['Subject'] = "INCOMING BEACON"
    body = get_notification_body(get_args())
    msg.attach(MIMEText(body, 'plain'))
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(from_address, "IwtbAmsfb5h!")
    text = msg.as_string()
    server.sendmail(from_address, to_address, text)
    server.quit()


def send_notifications():
    send_slack_notification()
    send_email_notification()


send_notifications()