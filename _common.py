import json

IP = '127.0.0.1'
PORT = 9876
IP_PORT = (IP, PORT)

SUCCESS = 1
FAIL = 2

cmdlist = [
	':ls',
	':in',
	':mk',
]

def pack_send(data, conn):
	try:
		conn.send(bytes(pack(data), encoding='utf-8'))
		return SUCCESS
	except ConnectionResetError:
		return FAIL
	return FAIL

def unpack_recv(conn, bfsz = 1024):
	data = conn.recv(bfsz).decode()
	return unpack(data)

def unpack_recv_srv(conn, bfsz = 1024):
	try:
		buf = conn.recv(bfsz).decode()
		return SUCCESS, unpack(buf)
	except ConnectionResetError:
		return FAIL, None
	return FAIL, None

def pack(Data):
	return json.dumps(Data)

def unpack(JsonData):
	return json.loads(JsonData)

if __name__ == "__main__":
	data = {'status': 1, 'info': 'oooooo'}
	j_data = pack(data)
	r_data = unpack(j_data)
	print(type(j_data), type(r_data))