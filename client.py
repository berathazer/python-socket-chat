import socket

host = "127.0.0.1"
port = 12345
buffer_size = 2048

# Sunucuya bağlan
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientSocket.connect((host, port))

# Kullanıcı adını al ve sunucuya gönder
username = input("Lütfen kullanıcı adınızı girin: ")
clientSocket.send(username.encode())

# Sunucudan hoş geldin mesajını al ve yazdır
welcome_message = clientSocket.recv(buffer_size).decode()

if "500" in welcome_message:
    print(welcome_message)
    exit()

choice = input("Chat'e Merhaba Mesajı Göndermek İstermisiniz (E , H):")
if choice == "E":
    clientSocket.send(f"Merhaba, benim adım {username} Sohbet odasına yeni katıldım".encode())



print(welcome_message)


# Sürekli mesaj gönderme döngüsü
while True:

    # Kullanıcıdan mesajı al
    message = input("Mesajınızı girin: ")

    # Mesajı sunucuya gönder
    clientSocket.send(message.encode())

    # Sunucudan gelen cevabı al ve yazdır
    response = clientSocket.recv(buffer_size).decode()

    if response != "M":
        print("girdi",response)






