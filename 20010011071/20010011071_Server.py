# 20010011071 Berat Hazer
# Hocam ödeve ek puan için yazdığım kodların satır bilgileri dosyanın en altında gösterilmiştir.

import threading
import socket
import datetime




class Server(object):
    def __init__(self, host, port, buffer_size):
        self.serverSocket = None
        self.host = host
        self.port = port
        self.buffer_size = buffer_size
        self.clientConnections = {}
        self.clientUsernames = {}
        self.maxUser = 6
        self.currentTime = datetime.datetime.now()
        self.control = 0

    def setupServer(self):
        try:
            print("System: Server Başlatıldı.")
            self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.serverSocket.bind((self.host, self.port))
            self.serverSocket.listen()

            while True:
                conn, addr = self.serverSocket.accept()

                _, clientPort = addr

                if len(self.clientConnections) >= self.maxUser:
                    print("Server fully connected")
                    conn.send(
                        f"Bu sohbet odası {self.maxUser} adet kullanıcı ile sınırlandırılmıştır, lütfen daha sonra tekrar deneyin. Hata Kodu: 500".encode())
                    continue

                if self.clientConnections.get(clientPort) is None:
                    self.clientConnections[clientPort] = clientPort

                # Her bir istemci bağlantısı için ayrı bir thread başlatıyorum.
                threading.Thread(target=self.receiveMessages, args=(conn, clientPort,)).start()
        except Exception as e:
            print(str(e))
            self.closeServer()

    def receiveMessages(self, conn, clientPort):
        try:
            username = conn.recv(self.buffer_size).decode()
            # KULLANICI SÖZLÜKTE YOKSA SERVERE İLK DEFA BAĞLANIYODUR KULLANICIYA HOŞGELDİN MESAJI VE CHAT HAKKINDA BİLGİLER GÖNDERİLİR.
            if self.clientUsernames.get(username) is None:

                self.clientUsernames[username] = conn

                # chatteki kişilerin bulunup listeye atılması.
                othersFromChat = list(self.clientUsernames.keys())
                othersFromChat.remove(username)
                if len(othersFromChat) > 0:
                    welcome_message = f"System: Merhaba, {username}! Chat'e hoş geldin!\n{self.calculateTime()}.\nChatteki Diğer İnsanlar: {othersFromChat}"
                else:
                    welcome_message = f"System: Merhaba, {username}! Chat'e hoş geldin!\n{self.calculateTime()}.\nChatteki Tek Kişi Sensin :)"

                print(
                    f"System: {username} Chat'e katıldı, Hoşgeldin {username}! Anlık Kullanıcı Sayısı: {len(self.clientUsernames)}")
                conn.send(welcome_message.encode())
                othersFromChat.append(username)
            else:
                conn.send(f"{username} Kullanıcısı chatte zaten mevcut yeni bir isim giriniz. (500)".encode())
                self.control = 1
            while True:
                try:
                    message = conn.recv(self.buffer_size).decode()

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
                            conn.send(f"{receiverName} kişisine olan mesajınız başarıyla gönderildi.".encode())
                            continue

                        else:
                            print(f"{username}: {message}")
                            conn.send("M".encode())

                    conn.send("".encode())

                except Exception as e:

                    if self.control == 0:
                        del self.clientUsernames[username]
                        print(
                            f"System: {username} kullanıcısı chatten ayrıldı! Kullanıcı Sayısı: {len(self.clientUsernames)}")
                    conn.close()
                    self.control = 0
                    break

        except Exception as e:
            print("ERROR receiveMessages function: ",str(e))
            self.closeServer()

    def calculateTime(self):
        try:
            timeDiff = datetime.datetime.now() - self.currentTime
            totalSeconds = timeDiff.total_seconds()

            days = totalSeconds // 86400
            hours = (totalSeconds % 86400) // 3600
            minutes = ((totalSeconds % 86400) % 3600) // 60
            seconds = ((totalSeconds % 86400) % 3600) % 60

            return f"Sunucu {days} gün {hours} saat {minutes} dakika {seconds} saniyedir çalışmakta!"
        except Exception as e:
            print("ERROR calculateTime function:",str(e))

    #Serveri kapatmak istersek tüm client bağlantılarını kapatıp en sonda server socketini kapatıyoruz.
    def closeServer(self):
        try:
            for key,conn in self.clientUsernames:
                conn.close()
            self.serverSocket.close()
            print("System: Server Kapatıldı!!!")
        except Exception as e:
            print("ERROR closeServer function: ",str(e))


server = Server("127.0.0.1", 12345, 2048)
#server'i başlatıyorum.
server.setupServer()

"""
    1-) Kullanıcılar arası özel mesaj kısmı 79-97. satırlar arasında ele alındı.
    
    2-) Sohbete bağlanan kullanıcı sohbetteki diğer kullanıcıların bilgisi ve serverin çalışma zamanını öğrenmesi işlemleri
        54-72. satırlar arasında ele alındı, serverin çalışma süresini hesaplayan fonksiyon 119. satırdaki calculateTime fonksiyonu.
    
    3-) Kullanıcının isteği halinde sohbete merhaba mesajı gönderme işlemi Client dosyasında 34.satırdaki ifte ele alındı
    
    4-) 19. satırda class içinde maxUser adında bir değişken belirledim. Satır 35'teki ifte client sayısını alıp bu değişkenle karşılaştırıyorum
        eğer client sayısı maxUser'ı geçerse server'a daha fazla kullanıcı almıyorum.
"""