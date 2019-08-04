import socket
import _common
import multiprocessing
import threading
import time

def recv_message(s):
	while True:
		buf_all = _common.unpack_recv(s)
		print(buf_all['username'] + ': ' + buf_all['data'])

def idx():
	i = int(time.time() * 10)
	time.sleep(1)
	return str(i)

def login():
	_username = input('username: ')
	if _username == '':
		_username = 'anonymous-' + idx()
	return _username

if __name__ == "__main__":
	username = login()
	s = socket.socket()
	s.connect(_common.IP_PORT)
	p = threading.Thread(target=recv_message, args=(s, ))
	p.daemon = True
	p.start()
	while True:
		_data = input().strip()
		if _data == 'q':
			break
		elif _data == '':
			continue
		data = {
			'data': _data,
			'username': username,
		}
		_common.pack_send(data, s)
		time.sleep(1)
	s.close()