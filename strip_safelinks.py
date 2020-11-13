#!/usr/bin/env python3
from urllib.parse import urlparse, parse_qs
from email import parser,policy
from quopri import encodestring as to_quopri
import re
import sys

def replace_safelink(candidate):
  rv = candidate
  try:
    up = urlparse(candidate.strip())
    qs = parse_qs(up.query)
    orig = qs['url'][0]
    if orig.lower().startswith("http"):
      rv = orig
  except:
    pass
  return rv

def replace_safelink_multiplex(match, subtype):
  prefix = ""
  postfix = ""
  candidate = match.group(0).decode('utf8', errors='backslashreplace')
  if candidate.startswith("safelink: "):
    return candidate.encode("utf8")
  if candidate.startswith("<"):
    prefix = "<"
    candidate = candidate[1:]
  if candidate.endswith(">"):
    postfix = ">"
    candidate = candidate[:-1]
  rv = replace_safelink(candidate)
# Uncomment to preserve the original safelinks URL if desired.
#  if rv != candidate and subtype.lower() == "plain":
#    postfix += " (safelink: " + candidate.strip() + " )"
  rv = prefix + rv + postfix
  return rv.encode('utf8')

inp = sys.stdin.buffer.read()
try:
  # compat32 makes sure we do not re-encode any headers unnecessarily, but also make sure we don't reflow long (unmodified) lines
  pol = policy.compat32.clone(max_line_length=0)
  msg = parser.BytesParser(policy=pol).parsebytes(inp)
  for part in msg.walk():
    if (part.get_content_type() == "text/plain" or part.get_content_type() == "text/html") and not (part.get_content_disposition() == "attachment"):
      cnt = part.get_payload(decode=True)
      rv = re.sub(rb"((?:safelink\: )?[<]?http[s]?://[a-zA-Z0-9]+\.safelinks\.protection\.outlook\.com/[^ <>]+reserved=[0-9][>]?)",lambda x: replace_safelink_multiplex(x,part.get_content_subtype()),cnt,flags=re.MULTILINE)
      cte = '7bit'
      try:
        rv.decode('ascii')
      except UnicodeError:
        rv = to_quopri(rv) # .replace(b' ', b'=20') # per email.encoders logic
        cte = 'quoted-printable'
      part.set_payload(rv)
      try:
        part.replace_header("Content-Transfer-Encoding", cte)
      except KeyError:
        part.add_header("Content-Transfer-Encoding", cte)
  sys.stdout.buffer.write(msg.as_bytes())
except Exception as e:
  print(e, file=sys.stderr)
  sys.stdout.buffer.write(inp)
