import os, sys
import subprocess
import argparse
import yaml
import pexpect
import pdb

# Constants
CUR_USER = os.getlogin()
PLATFORM = sys.platform

def initalization():
    if "linux" in PLATFORM:
	if CUR_USER != "root":
            return "/home/%s/.ssh" % (CUR_USER)
	else:
	    return "/%s/.ssh" % (CUR_USER)

def key_present(PRIV_SSH_DIR):
    """Checks to see if there is an RSA already present. Returns a bool."""
    if "id_rsa" in os.listdir(PRIV_SSH_DIR):
        return True
    else:
        return False

def show(msg):
    """Local print() function."""
    print(msg)

def gen_key(PRIV_SSH_DIR):
    """Generate a SSH Key."""
    os.chdir(PRIV_SSH_DIR)
    if key_present(PRIV_SSH_DIR):
        show("A key is already present.")
    else:
        # Genarate private key
        subprocess.call('ssh-keygen', shell=True)


def push_key(user, host, password, PRIV_SSH_DIR, port=22):
    """Push a SSH Key to a remote server."""
    os.chdir(PRIV_SSH_DIR)
    if key_present(PRIV_SSH_DIR):
        if "linux" in PLATFORM:
            try:
                child =  pexpect.spawn("ssh-copy-id '%s@%s'" % (user,host))
                i = child.expect(['password:', r'\(yes\/no\)',r'.*[$#] ',pexpect.EOF])
                if i == 0:
                    child.sendline(password)
                elif i == 1:
                    child.sendline("yes")
                    ret1 = child.expect(["password:",pexpect.EOF])
                    if ret1 == 0:
                        child.sendline(password)
                    else:
                        pass
                else:
                    pass
                data = child.read()
                print data
                child.close()
                return True
            except Exception as error:
                print error
                return False


def main():
    """Start of script."""
    file_name = os.getcwd()+"/"+sys.argv[1]
    port=22
    priv_dir=initalization()
    gen_key(priv_dir)

    with open(file_name, 'r') as ymlfile:
        cfg = yaml.load(ymlfile)

    i=1
    for section in cfg['host']:
        user=cfg['user']
        host=cfg['host']['worker'+str(i)]['host_name']
        password=cfg['host']['worker'+str(i)]['password']
	i+=1
        if user and host:
             push_key(user, host, password, priv_dir, port)
        else:
             show("Config file is required !!!!!")

if __name__ == "__main__":
    main()

