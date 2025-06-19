import json
import subprocess
import os


def find_profile(targeted_account: str, log):
    print(os.environ.get("AWS_VAULT"))
    return os.environ.get("AWS_VAULT")

    profiles = []
    available_accounts = []
    print("Listing profiles")
    results = subprocess.run(
        "aws configure list-profiles", shell=True, stdout=subprocess.PIPE
    )
    text = results.stdout.decode()
    for line in text.splitlines():
        print("Listing profile " + line)
        profiles.append(line)
        cmd = f'aws sts get-caller-identity --profile="{line}" --output=json'
        try:
            results = subprocess.run(
                cmd, shell=True, stdout=subprocess.PIPE, check=True
            )
        except subprocess.CalledProcessError:
            # TODO make some log message that makes sense
            continue
        text = results.stdout.decode()
        identity = json.loads(text)
        account = identity["Account"]
        available_accounts.append(account)
        if str(account) == str(targeted_account):
            return line

    log(msg=profiles, tag="AWS Profiles")
    log(msg=available_accounts, tag="AWS Available Accounts")
    return None
