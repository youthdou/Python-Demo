#https://doomzhou.github.io/coder/2015/03/09/Python-Requests-socks-proxy.html
import requests
import socket
import socks

socks.set_default_proxy(socks.SOCKS5, "192.168.1.132", 1080)
socket.socket = socks.socksocket

r = requests.get('https://www.google.com.hk/')
print(r.status_code)
print(r.text)