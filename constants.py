email_standard = '^([a-zA-Z0-9_\-\.]+)@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.)|(([a-zA-Z0-9\-]+\.)+))([a-zA-Z]{2,6}|[0-9]{1,3})(\]?)$'
phone_standard = '^[2-9]{2}[0-9]{8}$'
id_standard = "^[1-9][0-9]*$"
pass_standard = "[A-Za-z0-9@#$%^&+=]{8,}"
name_standard = "^[a-zA-Z]+(([',. -][a-zA-Z ]{2,20})?[a-zA-Z]*)*$"
sname_standard = "{[a-zA-Z]+(([',. -][a-zA-Z ]{2,20})?[a-zA-Z]*)*}"
price_standard = "^[+]?([0-9]{1,2})*[.]([0-9]{1,1})?$"
sender_email = "mail@souravtests.online"
smtp_ssl = "mail.souravtests.online"
port = 465
EMAIL_TEMPLATE = """
<html>
      <body>
        <p>Hi {},<br>
          <p> This is your temporary password - {}. </p><br>
          <p>Note: Please change your password as soon as possible. </p>
        </p>
      </body>
</html>
"""