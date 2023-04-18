from server import server

print(server.send_message('login'))

server.socket.close()
