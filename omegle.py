import os
from random import choice
import requests
from threading import Thread

topics = ['tiktok']
servers = ["front13", "front32", "front12", "front2", "front18", "front29", "front7", "front45", "front44", "front11", "front37", "front46", "front23", "front35", "front19", "front8", "front17", "front47", "front14", "front25", "front22", "front31", "front34", "front48", "front40", "front27", "front33", "front5", "front24", "front10", "front26", "front20", "front42", "front6", "front41", "front39", "front30", "front38", "front36", "front3", "front28", "front4", "front9", "front21", "front15", "front43", "front16"]


def proxy():
    proxy_list = []
    with open('proxies.txt', 'r') as f:
        for line in f:
            proxy_list.append(line)
    proxy_value = choice(proxy_list)
    return {'http': f'http://{proxy_value}'.replace('\n', ''), 'https': f'http://{proxy_value}'.replace('\n', '')}


def start():
    try:
        server = choice(servers)
        user_id = os.urandom(8).hex()[:7]
        url = f"https://%s.omegle.com/start?caps=recaptcha2,t3&firstevents=1&spid=&randid=&topics={topics}%s&lang=en&cc={requests.post('https://waw4.omegle.com/check').text}" % (server, user_id)
        session = requests.Session()
        response = session.post(url=url, proxies=proxy())
        if 'connected' in response.text:
            client_id = response.json()['clientID']
            send(client_id, message='YOUR MESSAGE!', session=session, server=server)
        elif 'antinudeBanned' in response.text:
            print(f"[-] Banned proxy")
        else:
            print(f'[-] Something went wrong')
    except Exception as e:
        print(f'[-] {e}')


def disconnect(client_id, session, server):
    try:
        data = {
            "id": client_id
        }
        response = session.post("https://%s.omegle.com/disconnect" % server, data=data)
        if 'win' in response.text:
            print(f'[+] Disconnected | {client_id} | {server}')
        else:
            print(f'[-] Failed to disconnect | {client_id} | {server}')
    except Exception as e:
        print(f'[-] {e}')


def send(client_id, message, session, server):
    try:
        data = {
            'id': client_id,
            'msg': message
        }
        response = session.post("https://%s.omegle.com/send" % server, data=data)
        if 'win' in response.text:
            print(f"[+] Sent message | {client_id} | {message} | {server}")
            disconnect(client_id, session, server)
        else:
            print(f"[-] Failed to send message | {client_id} | {message} | {server}")
            disconnect(client_id, session, server)
    except Exception as e:
        print(f'[-] {e}')


def main():
    #while True:
    #    Thread(target=start).start()
    start()


if __name__ == "__main__":
    main()
