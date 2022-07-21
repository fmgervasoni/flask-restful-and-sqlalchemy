"""
blocklist.py
This file just contains the denylist of the JWT tokens. it will be imported by
app and the logout resource so that tokens can be added to the denylist when the
user logs out.
"""

BLOCKLIST = set()
