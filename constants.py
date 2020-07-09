sender_email = "mail@souravtests.online"
smtp_ssl = "mail.souravtests.online"
port = 465
BLACKLIST_CLIENTS = {}
BLACKLIST_STYLISTS = {}
EMAIL_TEMPLATE = """
<html>
      <body>
        <p>Hi {},<br>
          <p> This is your temporary password - {}. </p></br>
          <p> Please change your password as soon as possible. </p>
        </p>
      </body>
    </html>
"""