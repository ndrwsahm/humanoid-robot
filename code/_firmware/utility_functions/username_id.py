import getpass
import re

def get_robot_id_from_username():
    username = getpass.getuser()  # "humanoid39"
    match = re.search(r"(\d+)", username)
    return match.group(1) if match else None
