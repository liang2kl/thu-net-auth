from requests import post, get
from getpass import getpass
from hashlib import md5
import keyring, json, re, sys, argparse

URL_BASE = "http://auth4.tsinghua.edu.cn"
NET_URL = "http://net.tsinghua.edu.cn"
PATTERN = re.compile(r"index_(\d+).html")
KEYRING_SERVICE_NAME = "thu-net-auth"
KEYRING_USERNAME = "user"

user_name = ""
password_hash = ""

def login(persistent):
    global user_name, password_hash
    if not user_name:
        user_name = input("Username: ")
    
    if not password_hash:
        password = getpass()
        password_hash = md5(password.encode("utf-8")).hexdigest()
    
    if persistent:
        set_credential(user_name, password_hash)
    
    ac_id = ""
    
    with get(NET_URL) as response:
        match = PATTERN.search(response.text)
        if not match:
            print("Cannot parse response. Maybe you are already online.")
            exit(0)
        
        ac_id = match.group(1)

    pararms = {
        "action": "login",
        "username": user_name,
        "password": "{MD5_HEX}" + password_hash,
        "ac_id": ac_id
    }
    with post(URL_BASE + "/do_login.php", params=pararms) as response:
        print(response.text)

def logout():
    global user_name
    
    params = {
        "action": "logout",
        "username": user_name,
        "ip": "",
        "double_stack": "1"
    }
    with post(URL_BASE + "/cgi-bin/srun_portal", params=params) as response:
        print(response.text)

def set_credential(user_name, password_hash):
    pair = {
        "user": user_name,
        "pass": password_hash
    }
    keyring.set_password(KEYRING_SERVICE_NAME, KEYRING_USERNAME, json.dumps(pair))

def get_credential():
    credential = keyring.get_password(KEYRING_SERVICE_NAME, KEYRING_USERNAME)
    if not credential:
        return None
    pair = json.loads(credential)
    return (pair["user"], pair["pass"])

def init_keychain():
    global user_name, password_hash
    pair = get_credential()
    if pair:
        user_name = pair[0]
        password_hash = pair[1]

if __name__ == "__main__":
    parser = argparse.ArgumentParser("Login to and logout from THU network service.")
    parser.add_argument("--logout", "-o", action="store_true", help="Logout from the network service.")
    parser.add_argument("--persistent", "-p", action="store_true", help="Store your credentials in local keychain.")
    parser.add_argument("--clear", "-c", action="store_true", help="Clear stored credentials")
    result = parser.parse_args(sys.argv[1:])
    
    if result.clear:
        try:
            keyring.delete_password(KEYRING_SERVICE_NAME, KEYRING_USERNAME)
        except keyring.errors.PasswordDeleteError as e:
            print(e)
        exit(0)
    
    init_keychain()

    if not result.logout:
        login(persistent=result.persistent)
    else:
        logout()
