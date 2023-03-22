from aprompt import prompt
from aprompt.prompts import confirm

answer = prompt("Continue?", confirm(default=False))
