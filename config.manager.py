import requests
import json
import base64
import emoji
import os
from urllib.parse import urlparse, unquote, parse_qs

class Config_manager():
    def __init__(self, url):
        self.url =url
    
    def get_config(self):
        try:
            response = requests.get(self.url, timeout = 5)
            return response.text.strip().splitlines()
        except Exception as e:
            print(f'The error is {e}')
            return []
        
    def parse_ss(self, link, tag_index = None):
        if not link.startswith("ss://"):
            return None
        raw = link[5:]
        if '#' in raw:
            raw, tag = raw.split('#', 1)
            tag = unquote(tag)
        else:
            tag = 'Unknown'
        if '@' in raw:
            username, serverinfo = raw.split('@')
            try:
                method, password = base64.urlsafe_b64decode(username + '==').decode().split(':', 1)
            except:
                return None
            server, port = serverinfo.split(':') 
            
        if tag_index is not None:
            suffix = f'-{tag_index}'
        else:
            suffix = ""
        secound_tag = f'{tag}{suffix}'
        return {
            "type": "shadowsocks",
            "tag": secound_tag,
            "server": server,
            "server_port": int(port),
            "method": method,
            "password": password,
            "detour": "\ud83c\uddee\ud83c\uddf7IR\ud83d\ude80YourIP\uD83D\uDEE1\uFE0F"
        }

    def parse_vmess(self, link, tag_index=None):
        if not link.startswith("vmess://"):
            return None
        raw = link[8:]
        try:
            decoded = base64.urlsafe_b64decode(raw + '==').decode()
            data = json.loads(decoded)
        except:
            return None
    
        tag = data.get("ps", "Unknown")
        suffix = f'-{tag_index}' if tag_index is not None else ""
        secound_tag = f'{tag}{suffix}'
    
        transport_type = data.get("net", "tcp")
        transport = {}

        if transport_type == "ws":
            transport = {
                "type": "ws",
                "path": data.get("path", "/"),
                "headers": {
                    "Host": data.get("host", "")
                }
            }
        elif transport_type == "grpc":
            transport = {
                "type": "grpc",
                "service_name": data.get("path", "")
            }
        elif transport_type == "h2":
            transport = {
                "type": "http",
                "path": data.get("path", "/"),
                "host": data.get("host", "")
            }
        
        return {
            "type": "vmess",
            "tag": secound_tag,
            "server": data.get("add"),
            "server_port": int(data.get("port")),
            "uuid": data.get("id"),
            "tls": {
                "enabled": data.get("tls", "") == "tls",
                "server_name": data.get("add", ""),
                "insecure": False
            },
            "transport": transport,
            "detour": "\ud83c\uddee\ud83c\uddf7IR\ud83d\ude80YourIP\uD83D\uDEE1\uFE0F"
        }

    
    def parse_vless(self, link, tag_index=None):
        if not link.startswith("vless://"):
            return None
        raw = link[8:]
        if '#' in raw:
            raw, tag = raw.split('#', 1)
            tag = unquote(tag)
        else:
            tag = 'Unknown'
    
        parsed = urlparse("vless://" + raw)
        uuid = parsed.username
        server = parsed.hostname
        port = parsed.port
        params = parse_qs(parsed.query)
    
        suffix = f'-{tag_index}' if tag_index is not None else ""
        secound_tag = f'{tag}{suffix}'
        
        transport_type = params.get("type", ["tcp"])[0]
        transport = {}
      
        if transport_type == "ws":
              transport = {
                  "type": "ws",
                  "path": params.get("path", ["/"])[0],
                  "headers": {
                      "Host": params.get("host", [""])[0]
                  }
              }
        elif transport_type == "grpc":
              transport = {
                  "type": "grpc",
                  "service_name": params.get("serviceName", [""])[0]
              }
        elif transport_type == "h2":
              transport = {
                  "type": "http",
                  "path": params.get("path", ["/"])[0],
                  "host": params.get("host", [""])[0]
              }
        
        tls = {
            "enabled": params.get("security", [""]) == ["tls"],
            "server_name": server,
            "insecure": False
          }
        
        return {
              "type": "vless",
              "tag": secound_tag,
              "server": server,
              "server_port": int(port),
              "uuid": uuid,
              "tls": tls,
              "transport": transport,
              "detour": "\ud83c\uddee\ud83c\uddf7IR\ud83d\ude80YourIP\uD83D\uDEE1\uFE0F"
          }

    
    def parse_trojan(self, link, tag_index=None):
        if not link.startswith("trojan://"):
            return None
        raw = link[9:]
        if '#' in raw:
            raw, tag = raw.split('#', 1)
            tag = unquote(tag)
        else:
            tag = 'Unknown'
    
        parsed = urlparse("trojan://" + raw)
        password = parsed.username
        server = parsed.hostname
        port = parsed.port
        params = parse_qs(parsed.query)
    
        suffix = f'-{tag_index}' if tag_index is not None else ""
        secound_tag = f'{tag}{suffix}'
    
        return {
            "type": "trojan",
            "tag": secound_tag,
            "server": server,
            "server_port": int(port),
            "password": password,
            "tls": {
                "enabled": params.get("security", [""]) == ["tls"],
                "server_name": params.get("sni", [""])[0],
                "insecure": False
            },
            "detour": "\ud83c\uddee\ud83c\uddf7IR\ud83d\ude80YourIP\uD83D\uDEE1\uFE0F"
        }

        
    def build_config(self):
        first_outbounds = [
            {
              "type": "shadowsocks",
              "tag": "\ud83c\uddee\ud83c\uddf7IR\ud83d\ude80YourIP\uD83D\uDEE1\uFE0F",
              "server": "4.223.106.240",
              "server_port": 48172,
              "method": "chacha20-ietf-poly1305",
              "password": "51yloQC8D9w1Wae7FHtI65"
            },
            {
              "type": "shadowsocks",
              "tag": "\uD83E\uDDD1\u200D\uD83D\uDCBBDEVELOPED-BY-SINA-KSH\u26a1\ufe0f",
              "server": "127.0.0.1",
              "server_port": 8080,
              "method": "none",
              "password": "bcaacba-caba-aabc-badc-bcbccbbacaaa"
            }
          ]

        new_config = []
        Configs = self.get_config()
        tag_counter = 1
        for config in Configs:
            if config.startswith("ss://"):
                parsed = self.parse_ss(config, tag_index=tag_counter)
            elif config.startswith("vmess://"):
                parsed = self.parse_vmess(config, tag_index=tag_counter)
            elif config.startswith("vless://"):
                parsed = self.parse_vless(config, tag_index=tag_counter)
            elif config.startswith("trojan://"):
                parsed = self.parse_trojan(config, tag_index=tag_counter)
            else:
                parsed = None
            if parsed:
                new_config.append(parsed)
                tag_counter += 1
        final_outbounds = new_config + first_outbounds
        
        return {
            "outbounds": final_outbounds
        }
    
    def build_secound(self):
        new_config2 = []
        links = self.get_config()
        tag_counter = 1
        for link in links:
            if link.startswith("ss://"):
                parsed = self.parse_ss(link, tag_index=tag_counter)
            elif link.startswith("vmess://"):
                parsed = self.parse_vmess(link, tag_index=tag_counter)
            elif link.startswith("vless://"):
                parsed = self.parse_vless(link, tag_index=tag_counter)
            elif link.startswith("trojan://"):
                parsed = self.parse_trojan(link, tag_index=tag_counter)
            else:
                parsed = None
            if parsed:
                new_config2.append(parsed)
                tag_counter += 1
        return new_config2
        
    def save_to_file(self, filename = "configs"):
        if os.path.exists(filename):
            with open(filename, "r", encoding="utf-8") as file:
                old_data = json.load(file)
                old_outbounds = old_data.get("outbounds", [])
            new_links = self.build_secound()
            filtered = []
            for link in new_links:
                is_duplicate = False
                for old in old_outbounds:
                    if link["type"] == "shadowsocks":
                        if link["server"] == old["server"] and \
                            link["server_port"] == old["server_port"] and \
                            link["method"] == old["method"] and \
                            link["password"] == old["password"]:
                                is_duplicate = True
                                break
                        print(emoji.emojize('The configs (ss) is added :check_mark_button:'))
                        
                    elif link["type"] == "vmess":
                         if link["server"] == old["server"] and \
                            link["server_port"] == old["server_port"] and \
                            link["uuid"] == old.get("uuid"):
                             is_duplicate = True
                             break
                         print(emoji.emojize('The configs (vmess) is added :check_mark_button:'))
                         
                    elif link["type"] == "vless":
                         if link["server"] == old["server"] and \
                            link["server_port"] == old["server_port"] and \
                            link["uuid"] == old.get("uuid"):
                             is_duplicate = True
                             break
                         print(emoji.emojize('The configs (vless) is added :check_mark_button:'))
                         
                    elif link["type"] == "trojan":
                         if link["server"] == old["server"] and \
                            link["server_port"] == old["server_port"] and \
                            link["password"] == old.get("password"):
                             is_duplicate = True
                             break
                         print(emoji.emojize('The configs (trojan) is added :check_mark_button:'))
                         
                if not is_duplicate:
                    filtered.append(link)
                    print(emoji.emojize('The configs filtered :cross_mark:'))
                    
            outbounds_2 = filtered + old_outbounds
            final = {
                "outbounds": outbounds_2
                
                }
            try:
                with open(filename, 'w', encoding="utf-8") as file:
                    json.dump(final, file, indent = 4, ensure_ascii = True)
                print(emoji.emojize(f'It saved : {filename}:check_mark_button:'))
            except Exception as e:
                print(emoji.emojize(f' Error : {e} :cross_mark:'))     
        else:
            config = self.build_config()
            try:
                with open(filename, 'w', encoding="utf-8") as file:
                    json.dump(config, file, indent = 4, ensure_ascii = True)
                print(emoji.emojize(f'It saved : {filename}:check_mark_button:'))
            except Exception as e:
                print(emoji.emojize(f' Error : {e} :cross_mark:')) 

my_config = Config_manager('https://raw.githubusercontent.com/arshiacomplus/robinhood-v1-v2-v3ray/refs/heads/main/conf.txt#conf')
my_config.save_to_file()
