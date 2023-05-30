import threading
import socket


class Server(object):
    def __init__(self, host, port, buffer_size):
        self.serverSocket = None
        self.host = host
        self.port = port
        self.buffer_size = buffer_size
        self.clientConnections = {}
        self.clientUsernames = {}
        self.maxUser = 2

    def setupServer(self):
        print("System: Server başlatılıyor...")
        self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serverSocket.bind((self.host, self.port))
        self.serverSocket.listen()

        while True:
            conn, addr = self.serverSocket.accept()

            _, clientPort = addr

            if len(self.clientConnections) == self.maxUser:
                print("Server fully connected")
                conn.send(f"Bu sohbet odası {self.maxUser} adet kullanıcı ile sınırlandırılmıştır, lütfen daha sonra tekrar deneyin. Hata Kodu: 500".encode())
                continue

            if self.clientConnections.get(clientPort) is None:
                self.clientConnections[clientPort] = clientPort


            # Her bir istemci bağlantısı için ayrı bir thread başlat
            threading.Thread(target=self.receiveMessages, args=(conn,clientPort,)).start()

    def receiveMessages(self, conn, clientPort):

        username = conn.recv(2048).decode()
        print(len(self.clientConnections))

        if self.clientUsernames.get(username) is None:


            # Kullanıcı adını sakla
            self.clientUsernames[username] = conn

            # İstemciye hoş geldin mesajı gönder
            serverTime = "2 saat"
            othersFromChat = ["beraa","hans","john"]
            welcome_message = f"System: Merhaba, {username}! Chat'e hoş geldin!\nChat {serverTime} süredir çalışıyor.\nChatteki Diğer İnsanlar: {othersFromChat} "
            print(f"System: {username} Chat'e katıldı, Hoşgeldin {username}! Anlık Kullanıcı Sayısı: {len(self.clientConnections)}")

            conn.send(welcome_message.encode())

        else:
            conn.send(f"{username} Kullanıcısı chatte zaten mevcut yeni bir isim giriniz.".encode())
        while True:
            try:
                message = conn.recv(2048).decode()
                if message != "":
                    if message[0] == '@':
                        messageList = message.split()

                        receiverName = messageList[0].replace('@', '')
                        senderMessage = message.replace(messageList[0], '')


                        if self.clientUsernames.get(receiverName) is None:
                            conn.send(f"Chatte {receiverName} isimli bir kullanıcı yok!!!".encode())
                            continue

                        if receiverName == username:
                            conn.send(f"Kendinize Mesaj Gönderemezsiniz!!!".encode())
                            continue

                        receiverConn = self.clientUsernames.get(receiverName)

                        receiverConn.send(f"{username} kişisinden özel mesaj: {senderMessage}".encode())

                    else:
                        print(f"{username}: {message}")

                    conn.send("M".encode())

            except ConnectionResetError:
                del self.clientConnections[conn]
                del self.clientUsernames[username]
                print(f"System: {username} kullanıcısı chatten ayrıldı! Kullanıcı Sayısı: {len(self.clientConnections)}")
                break

        conn.close()

    def closeServer(self):
        for conn in self.clientConnections:
            conn.close()

        self.serverSocket.close()


server = Server("127.0.0.1", 12345, 2048)

threading.Thread(target=server.setupServer).start()
