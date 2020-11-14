import socket
from threading import Thread
from Game import Game
import pickle

server = "192.168.1.221"
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen()
print("Waiting for a connection, Server Started")

connected = set()
games = {}
idCount = 0

game = Game(0,3,8 - 1,3)

def threaded_client(conn,p,gameId):
    global idCount
    conn.send(str.encode(str(p)))

    reply = ""
    while True:
        try:
            data = pickle.loads(conn.recv(4096).decode())

            if gameId in games:
                game = games[gameId]
                if not data:
                    break
                else:
                    if data == "reset":
                        game.resetWent()

                    elif data != "get":
                        game.play(p, data)

                    reply = game
                    conn.sendall(pickle.dumps(reply))
            else:
                break

        except:
            break
    print("lost Connection")


    try:
        del games[gameId]
        print("Closing game", gameId)
    except:
        pass
    idCount -= 1
    conn.close()


while True:
    conn, addr = s.accept()
    print("connected to:", addr)

    idCount += 1
    p = 0
    gameId = int((idCount - 1)/2)
    if idCount%2 == 1:
        games[gameId] = Game(gameId)
        print("creating a new game...")
    else:
        games[gameId].ready = True
        p = 1

    print(p)

    t = Thread(target = threaded_client, args = (conn,p, gameId))
    #start_new_thread(threaded_client, (conn,p, gameId))
