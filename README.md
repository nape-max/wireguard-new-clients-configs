# Python script to automation create configuration for clients of your Wireguard VPN server

## { How to use }
### **If your Wireguard server already configured, then just**
1) Clone this repository and change paths to yours in lines 7-10:
```
user_conf_for_client_dir = 'DIR_TO_STORE_WIREGUARD_CLIENT_CONFS'
user_keys_dir = 'DIR_TO_STORE_PRIVATE_PUBLIC_KEYS_OF_CLIENTS'
wg_publickey_path = 'PATH_TO_WIREGUARD_SERVER_PUBLICKEY'
count_path = 'PATH_TO_COUNT_FILE'
```

2) Add `1` to count file if you are haven't clients, or add number of clients plus one to this file. For example, file contents:
```
1
```

3) Add environment variable of your server IP

    1) For only one run:

    ```
    export SERVER_IP=YOUR_SERVER_IP
    ```
    2) To make it accessible always, add it to `.bashrc` or `.zshrc` in your home directory:
    ```
    # for ZSH
    echo "export SERVER_IP=YOUR_SERVER_IP" >> ~/.zshrc
    # for BASH
    echo "export SERVER_IP=YOUR_SERVER_IP" >> ~/.bashrc
    
4) Now just run this script, it's accept only one parameter: prefix of your config name, after complete, your config will have name like this: `YOUR_PREFIX_wg.conf`:
```
# generated config for Wireguard client will be available in specified user_conf_for_client_dir directory.

python3 new-client.py YOUR_PREFIX
```

<hr />
<br />

## { How to install Wireguard and use }
0) (not necessary) Update your server if it's new:
```
sudo apt-get update && sudo apt-get upgrade
```
1) Install Wireguard:
```
sudo apt-get install wireguard
```
2) Generate Wireguard keys for server:
```
wg genkey | tee YOUR_DIRECTORY/privatekey | wg pubkey | tee YOUR_DIRECTORY/publickey
```
3) Add `wg0.conf` to your server with this configuration:
```
[Interface]
PrivateKey = YOUR_PRIVATE_KEY_FROM_STEP_2
Address = 10.0.0.1/24
ListenPort = 51830
PostUp = iptables -A FORWARD -i %i -j ACCEPT; iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
PostDown = iptables -D FORWARD -i %i -j ACCEPT; iptables -t nat -D POSTROUTING -o eth0 -j MASQUERADE
```

4) Then enable IP forwarding on your server by this:
```
echo "net.ipv4.ip_forward=1" >> /etc/sysctl.conf
```

5) Enable Wireguard as service:
```
systemctl enable wg-quick@wg0.service
systemctl start wg-quick@wg0.service
```

6) Clone this repository and change paths to yours in lines 7-10:
```
user_conf_for_client_dir = 'DIR_TO_STORE_WIREGUARD_CLIENT_CONFS'
user_keys_dir = 'DIR_TO_STORE_PRIVATE_PUBLIC_KEYS_OF_CLIENTS'
wg_publickey_path = 'PATH_TO_WIREGUARD_SERVER_PUBLICKEY'
count_path = 'PATH_TO_COUNT_FILE'
```

7) Add `1` to count file if you are haven't clients, or add number of clients plus one to this file. For example, file contents:
```
1
```

8) Add environment variable of your server IP

    1) For only one run:

    ```
    export SERVER_IP=YOUR_SERVER_IP
    ```
    2) To make it accessible always, add it to `.bashrc` or `.zshrc` in your home directory:
    ```
    # for ZSH
    echo "export SERVER_IP=YOUR_SERVER_IP" >> ~/.zshrc
    # for BASH
    echo "export SERVER_IP=YOUR_SERVER_IP" >> ~/.bashrc

9) Now just run this script, it's accept only one parameter: prefix of your config name, after complete, your config will have name like this: `YOUR_PREFIX_wg.conf`:
```
# generated config for Wireguard client will be available in specified user_conf_for_client_dir directory.

python3 new-client.py YOUR_PREFIX
```