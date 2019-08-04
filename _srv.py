import socket
import threading
import _common
import logging
logging.basicConfig(level = logging.INFO,format = '%(asctime)s - %(name)s - [%(levelname)s] %(message)s')
logger = logging.getLogger(__name__)


def cmdHandler(buf, connManager):
	cl = buf.split()
	if cl[0] == ':ls':
		_data = 'name: %s, online: %d' % (connManager['name'], len(connManager['conns']))
	elif cl[0] == ':in':
		_data = 'unimpl'
	elif cl[0] == ':mk':
		_data = 'unimpl'
	else:
		_data = 'error cmd request!'
	data = {
		'data': _data,
		'username': '[server]',
	}
	return data

def addrfmt(addr):
	return '<%s:%d>' % addr

def handler(conn, addr, connManager):
	while True:
		status, buf = _common.unpack_recv_srv(conn)
		if status != _common.SUCCESS:
			logger.warning('fail, call unpack_recv_srv ' + addrfmt(addr))
			connManager['conns'].remove(conn)
			break
		_data = buf['data']
		logger.info(addrfmt(addr) + ': ' + _data)
		if _data[0] == ":" and _data.split()[0] in _common.cmdlist:
			data = cmdHandler(_data, connManager)
			status = _common.pack_send(data, conn)
			if status != _common.SUCCESS:
				logger.warning('fail, call pack_send' + addrfmt(addr))
				connManager['conns'].remove(conn)
				break
			logger.info('[server]: ' + data['data'])
			continue
		for e in connManager['conns']:
			status = _common.pack_send(buf, e)

if __name__ == "__main__":
	s = socket.socket()
	s.bind(_common.IP_PORT)
	s.listen()
	roomList = []
	connManager = {
		'name': 'forest',
		'conns': [],
	}
	while True:
		logger.info('server listen, ...')
		conn, addr = s.accept()
		connManager['conns'].append(conn)
		p = threading.Thread(target=handler, args=(conn, addr, connManager))
		p.daemon = True
		p.start()