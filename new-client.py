import os
import sys

wg_conf_path = '/etc/wireguard/wg0.conf'
server_ip = os.environ.get("SERVER_IP")

user_conf_for_client_dir = '/root/vpn_confs'
user_keys_dir = '/etc/wireguard/clients'
wg_publickey_path = '/etc/wireguard/publickey'
count_path = '/etc/wireguard/count'

def increment_count_and_get(count_file_path):
    count_file_object = open(count_file_path, 'r')
    count = int(count_file_object.read().strip()) + 1
    count_file_object.close()

    count_file_object = open(count_file_path, 'w')
    count_file_object.write(str(count))
    count_file_object.close()

    return count

def write_user_conf_for_server_to_wireguard_conf(wg_conf_path, user_conf_for_server):
    wg_conf_file_object = open(wg_conf_path, 'a')
    wg_conf_file_object.write(user_conf_for_server + "\n")
    wg_conf_file_object.close()

def write_user_conf_for_client_to_file(user_conf_for_client_dir, prefix, user_conf_for_client):
    user_conf_for_client_name = prefix + '_wg.conf'
    user_conf_for_client_file_object = open(user_conf_for_client_dir + '/' + user_conf_for_client_name, 'w')

    user_conf_for_client_file_object.write(user_conf_for_client + "\n")

def get_wg_publickey(wg_publickey_path):
    wg_publickey_file_object = open(wg_publickey_path, 'r')
    
    return wg_publickey_file_object.read().strip()

def get_user_conf_for_server():
    return """
[Peer]
PublicKey = %client_public_key%
AllowedIPs = 10.0.0.%client_count%/32
    """

def get_user_conf_for_client():
    return """
[Interface]
PrivateKey = %client_private_key%
Address = 10.0.0.%client_count%/32
DNS = 8.8.8.8

[Peer]
PublicKey = %server_public_key%
Endpoint = %server_ip%:51830
AllowedIPs = 0.0.0.0/0
PersistentKeepalive = 20    
    """

if len(sys.argv) != 2:
    print("Required only one arguments: prefix for your config name")
    exit()

user_conf_for_client_prefix = sys.argv[1]

private_key_process = os.popen('wg genkey | tee ' + user_keys_dir + '/' + user_conf_for_client_prefix + '_private_key');
private_key = private_key_process.read().strip();
private_key_process.close();

public_key_process = os.popen('echo "' + private_key + '" | wg pubkey | tee ' + user_keys_dir + '/' + user_conf_for_client_prefix + '_public_key');
public_key = public_key_process.read().strip();
public_key_process.close()

count = increment_count_and_get(count_path)
user_conf_for_server = get_user_conf_for_server().replace("%client_public_key%", public_key).replace("%client_count%", str(count)).strip()
write_user_conf_for_server_to_wireguard_conf(wg_conf_path, user_conf_for_server)


wg_publickey = get_wg_publickey(wg_publickey_path)
user_conf_for_client = get_user_conf_for_client().replace("%client_private_key%", private_key).replace("%client_count%", str(count)).replace("%server_public_key%", wg_publickey).replace("%server_ip%", server_ip).strip()
write_user_conf_for_client_to_file(user_conf_for_client_dir, user_conf_for_client_prefix, user_conf_for_client)

restart_wg_process = os.popen('systemctl restart wg-quick@wg0.service')
restart_wg_process.close()
