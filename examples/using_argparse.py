from argparse import ArgumentParser
from aprompt.ext.argparse import Namespace, PromptIfAbsent
from aprompt.prompts import number

parser = ArgumentParser(description="Example of argparse extension.")

parser.add_argument(
    "--age",
    default=PromptIfAbsent(
        "Please enter your age.",
        number(minimum=0, maximum=150)
    )
)

args = parser.parse_args(namespace=Namespace()).prompt()
print(args)
