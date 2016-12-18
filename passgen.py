from __future__ import print_function
import re
import os
import sys
import hashlib
from select import select
from getpass import getpass
from base64 import b64encode
from os.path import expanduser

b64c = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/="
secc = "ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz123456789?!#@&$="

def dump_secret(secret):
   try:
      from pyperclip import copy
      copy(secret)
      print("Secret copied to clipboard")
   except ImportError:
      print("Can't copy secret to clipboard, dumping to screen ['pyperclip' missing]",
	   file=sys.stderr)
      print(secret)

def encrypt(text):
   secret = "".join(secc[b64c.index(chr(t))] for t in bytearray(text))
   if not re.search("[0-9]", secret):
      secret = os.getenv('D', '1') + secret[1:]
   if not re.search("[a-zA-Z]", secret):
      secret = secret[0] + os.getenv('L', 'a') + secret[2:]
   if not re.search("[^a-zA-Z0-9]", secret):
      secret = secret[:2] + os.getenv('S', '@') + secret[3:]
   return secret
 
def generate_password(domain, password):
    data = "{}:{}".format(password.strip(), domain.lower().strip())
    data_bytes = data.encode("utf-8")
    hashed = hashlib.sha1(data_bytes).digest()
    return encrypt(b64encode(hashed)[:10])

def print_usage():
   script_name = sys.argv[0].replace(expanduser("~"), "~")
   print("Domain wasn't passed - pass via pipe or command line argument.",
	 file=sys.stderr)
   print("Usage: 'echo <domain> | {0}' OR '{0} <domain>'".format(script_name),
	 file=sys.stderr)

def get_domain():
   # get the domain from stdin or argv
   if select([sys.stdin,],[],[],0.0)[0]:
      return "".join(sys.stdin)
   if len(sys.argv) > 1:
      return sys.argv[1]    
   return ""

if __name__ == '__main__':
   # get the domain from stdin or argv
   domain = get_domain()
   if not domain:
       print_usage() 
       sys.exit(1)

   # generate the password
   passwd = getpass("Enter your password: ")
   secret = generate_password(domain=domain, 
			      password=passwd)

   # dump the secret to clipboard or stdout
   dump_secret(secret)
