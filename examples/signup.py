from email.utils import parseaddr

from aprompt import prompt
from aprompt.prompts import text, number, pin, confirm

age = prompt("Please enter your age.", number(minimum=0, maximum=150))
username = prompt("Please enter a username.", text(placeholder="funkydog12"), validate=lambda name: bool(name))
email = prompt("Please enter your email.", text(placeholder="john.doe@example.com"), validate=lambda e: "@" in parseaddr(e)[1])
prompt("Please enter a password.", text(hide=True), validate=lambda pw: bool(pw))
if prompt("Are these details correct?\n" + "\n".join(f"{k}: {v}" for k, v in {
    "username": username,
    "age": age,
    "email": email
}.items()), confirm()):
    prompt("Please provide the code sent to your email.", pin(6))
