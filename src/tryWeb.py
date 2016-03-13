import socket
import time
from get_data import get_data


def main():
    HOST, PORT = '', 9898
    
    listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    listen_socket.bind((HOST, PORT))
    listen_socket.listen(1)
    print('Serving HTTP on port %s ...' % PORT)
    reqNum = 0
    data = get_data()
    while True:
        client_connection, client_address = listen_socket.accept()
        request = client_connection.recv(1024)
        print(request.decode())
        http_response = genHttp(data, reqNum)
        reqNum += 1
        client_connection.sendall(http_response.encode())
        client_connection.close()


def genHttp(data, reqNum):
    dateStr = str(data[reqNum]['Date'])
    closeVal = float(data[reqNum]['Close'])
    prevVal = float(data[reqNum+1]['Close'])
    
    http_response = """\
HTTP/1.1 200 OK

Hello visitor, current time is %s

On %s, the close value was %.2f, it was %.2f on the previous day.

""" % (time.ctime(), dateStr, closeVal, prevVal)
    return http_response
        
if __name__ == '__main__':
    main()