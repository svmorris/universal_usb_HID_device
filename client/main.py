import os
import sys
import requests
import argparse

SCRIPT_PATH = os.path.expanduser("~/.config/hidserver/")


def build_parser():
    parser = argparse.ArgumentParser(
        prog=sys.argv[0],
        description="Keyboard controller tool.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""Examples:
  {arg0} -t "Hello World"
  {arg0} -t "SUPER r" "calc\\n"

  {arg0} -f ./custom_macro.txt
  {arg0} -s linux_revshell [script arguments (if any)]
""".format(arg0=sys.argv[0]),
    )

    # Mutually exclusive group ensures user picks one "mode"
    modes = parser.add_mutually_exclusive_group(required=True)

    # -t: type string(s)
    modes.add_argument(
        "-t",
        nargs="+",  # one or more strings
        metavar="STRING",
        help="Send one or more strings for the keyboard to type.",
    )

    # -f: file
    modes.add_argument(
        "-f",
        metavar="FILE",
        help="Specify a file from which to read commands (each line = command).",
    )

    # -s: scripts
    modes.add_argument(
        "-s",
        metavar="SCRIPT",
        nargs=argparse.REMAINDER,  # everything after goes to the script
        help="Choose from a set of pre-defined scripts (can have their own args).",
    )

    # -sl: list scripts
    modes.add_argument(
        "-sl",
        action="store_true",
        help="List pre-defined scripts.",
    )

    return parser


def send_command(text: str) -> bool:
    """ Send a command to the server """
    url = "http://172.237.117.207:31337/68d26871-87e0-8330-9f47-f4fafb389302/typedata"
    data = {
            "text": text
            }

    res = requests.post(url=url, json=data)

    if res.status_code == 200:
        return True
    else:
        return False


def send_from_file(path: str) -> bool:
    """ Send commands from a file """
    if not os.path.isfile(path):
        print(f"Could not open file: {path}", file=sys.stderr)
        sys.exit(-1)

    with open(path, "r", encoding="utf-8")as infile:
        file_data = infile.read()

    return send_command(file_data)



def list_scripts():
    """ List the available scripts """
    # Make it if it doesn't already exists
    if not os.path.isdir(SCRIPT_PATH):
        os.mkdir(SCRIPT_PATH)

    print("Available scripts:")
    for script in os.listdir(SCRIPT_PATH):
        print(f"- {script}")


def send_script(script_name: str):
    """ Send a script """
    # Make it if it doesn't already exists
    if not os.path.isdir(SCRIPT_PATH):
        os.mkdir(SCRIPT_PATH)

    if not os.path.isfile(SCRIPT_PATH + script_name):
        print(f"No such script file: {SCRIPT_PATH+script_name}", file=sys.stderr)
        sys.exit(-2)

    return send_from_file(SCRIPT_PATH+script_name)


def main():
    parser = build_parser()
    args = parser.parse_args()

    if args.t:
        send_command("\n".join(args.t))
    elif args.f:
        send_from_file(args.f)
    elif args.s:
        send_script(args.s[0])
    elif args.sl:
        list_scripts()

if __name__ == "__main__":
    main()

