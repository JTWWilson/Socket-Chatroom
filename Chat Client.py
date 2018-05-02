import socket
import threading
import pygame
import datetime
import json

pygame.init()
pygame.font.init()

# Pygame constants
FONT_SIZE = 20
ARIEL_FONT = pygame.font.SysFont('Ariel', FONT_SIZE)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
WINDOW_SIZE = (500, 500)

window = pygame.display.set_mode(WINDOW_SIZE)


# get local machine name
HOST = socket.gethostbyname('DellXPS15')
PORT = 9999             # The same port as used by the server

#import json

#data_string = json.dumps(data) #data serialized
#data_loaded = json.loads(data) #data loaded


def display_messages(screen, font, message_history, typing_message):
    screen.fill(BLACK)
    for index, message in enumerate(message_history[(-(WINDOW_SIZE[1] // (FONT_SIZE + 5)) + 1):] if len(message_history) > (WINDOW_SIZE[1] // (FONT_SIZE + 5)) + 1 else message_history):
        screen.blit(font.render(message['text'], True, WHITE), (0, index * (FONT_SIZE + 5)))
    pygame.draw.line(screen, WHITE, (0, WINDOW_SIZE[1] - (FONT_SIZE + 15)), (WINDOW_SIZE[0], WINDOW_SIZE[1] - (FONT_SIZE + 15)))
    screen.blit(font.render(typing_message, True, WHITE), (0, WINDOW_SIZE[1] - (FONT_SIZE + 5 )))
    pygame.display.flip()


def listener(sock):
    """
    Listens to given socket 'sock' and prints any data received
    :param sock: socket to listen to
    """
    while True:
        data = sock.recv(1024)
        if data:
            messages.append(json.loads(data.decode()))
            print(json.loads(data.decode()))


if __name__ == '__main__':
    messages = [{'sender': 'server', 'text': 'You joined the chat!', 'timestamp': str(datetime.datetime.today())}]
    typing = ''
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        # create separate thread to listen to socket
        listening_thread = threading.Thread(target=listener, args=(s,))
        listening_thread.start()
        while True:
            if not listening_thread.isAlive:
                # close socket
                s.close()
                # clean thread and kill
                listening_thread.daemon = True
                pygame.quit()
                quit()
            display_messages(window, ARIEL_FONT, messages, typing)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    # close socket
                    s.close()
                    # clean thread and kill
                    listening_thread.daemon = True
                    pygame.quit()
                    quit()
                elif event.type == pygame.KEYDOWN:
                    if event.unicode == '\r':
                        message = json.dumps({'sender': (HOST, PORT),'text': typing, 'timestamp': str(datetime.datetime.today())}).encode()
                        s.sendall(message)
                        # messages.append({'sender': (HOST, PORT),'text': typing, 'timestamp': str(datetime.datetime.today())})
                        typing = ''
                    elif event.unicode == "\x08":
                        typing = typing[:-1]
                    else:
                        typing += event.unicode

