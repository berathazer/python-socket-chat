# 20010011071 Berat Hazer
# Hocam ödeve ek puan için yazdığım kodların satır bilgileri dosyanın en altında gösterilmiştir.

import socket





host = "127.0.0.1"
port = 12345
buffer_size = 2048

try:
    # Sunucuya bağlandım.
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientSocket.connect((host, port))

    # İlk başta kullanıcı adını aldık ve sunucuya gönderdik
    username = input("Lütfen kullanıcı adınızı girin: ")
    clientSocket.send(username.encode())

    # sunucudan gelecek olan mesajı alıyoruz.
    welcome_message = clientSocket.recv(buffer_size).decode()

    # Eğer chatte böyle bir isim varsa veya sunucu dolu ise serverdan hata kodu 500 döndürüyorum ve client'ın bağlantısını kesiyorum.
    if "500" in welcome_message:
        print(welcome_message)
        exit()

    # eğer dönen mesajda hata kodu 500 yoksa artık client bağlantısını kurabiliriz.
    # kullanıcıya chate merhaba mesajı göndermek istermi diye soruyoruz.
    choice = input("Chat'e Merhaba Mesajı Göndermek İstermisiniz (E , H):")
    if choice == "E":
        clientSocket.send(f"Merhaba, benim adım {username} Sohbet odasına yeni katıldım".encode())

    print(welcome_message)

    # client <-> sunucu arasındaki mesaj döngüsü.
    while True:
        try:
            # dönen cevabı alıp yazdırıyoruz.
            response = clientSocket.recv(buffer_size).decode()
            if response != "M":
                print(response)

            # Kullanıcıdan mesajı aldık.
            message = input("Mesajınızı girin: ")
            # sunucuya gönderdik.
            clientSocket.send(message.encode())


        except:
            # eğer bir hata oluşursa server'a kullanıcıcın ayrıldığı bilgisini gönderiyoruz.
            clientSocket.send(f"Ben {username} Chatten Ayrıldım!".encode())

            break

except Exception as e:
    print(str(e))


"""
    3-) İlk defa bağlanan kullanıcıların servera hoşgeldin mesajı gönderme işlemi 34.Satırda kontrol ediliyor.
"""