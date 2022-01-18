import dns.resolver
import socket
import smtplib


def check(email):
	try:
		addressToVerify = str(email)
		domain = addressToVerify.split('@')[1]
		records =  dns.resolver.Resolver()
		records = records.resolve(domain, "MX")
		mxRecord = records[0].exchange
		mxRecord = str(mxRecord)
		print(mxRecord)
		# Get local server hostname
		host = socket.gethostname()
		print(host)
		# SMTP lib setup (use debug level for full output)
		server = smtplib.SMTP(timeout=10)
		server.set_debuglevel(0)

		# SMTP Conversation
		server.connect(mxRecord)
		# send helo with local server hostname
		server.helo(host)
		server.mail('me@domain.com')
		code, message = server.rcpt(str(addressToVerify))
		server.quit()

		# Assume 250 as Success
		if code == 250:
			print(f' [+] Valid {email}')
		else:
			print(f' [-] Invalid {email} , Error Code: {code}')
	except Exception as e:
		print(e)


email = input(' [+] Enter email to check : ')
check(email)
