import socket
import select
import sys
import os

def Socket():
	ServerSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	ServerSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	host = '127.0.0.1'
	port = 61616
	ServerSocket.bind((host, port))
	ServerSocket.listen(5)
	return ServerSocket

def StatusCode(status, filesize):
	if (status==200):
		response_header = 'HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=UTF-8\r\nContent-Length:'+ str(filesize) + '\r\n\r\n'
	if (status==404):
		response_header = 'HTTP/1.1 404 Not Found\r\nContent-Type: text/html; charset=UTF-8\r\nContent-Length:' + str(filesize) + '\r\n\r\n'
	return response_header

def main():
	ServerSocket = Socket()
	inputSocket = [ServerSocket]

	try:
		while True:
			read_ready, write_ready, exception = select.select(inputSocket, [], [])
			for sock in read_ready:
				if sock == ServerSocket: 
					client_socket, client_address = ServerSocket.accept()
					inputSocket.append(client_socket)
				else: 
					request = sock.recv(4096)
					print request
					request_header = request.split('\r\n')
					request_file = request_header[0].split(' ')
					request_name = request_file[1].split('/')
					response_content = ''
					if request_file[1] == '/index.html' or request_file[1] == '/':
						f = open('index.html', 'r')
						response_content = f.read()
						f.close()
						content_length = len(response_content)
						response_header = StatusCode(200, content_length)
						print response_header
						sock.sendall(response_header + response_content)
					else:
						f = open('404.html','r')
						response_content = f.read()
						f.close()
						content_length = len(response_content)
						response_header = StatusCode(404,content_length)
						print response_header
						sock.sendall(response_header + response_content)
	except KeyboardInterrupt:
		ServerSocket.close()
		sys.exit(0)

main()