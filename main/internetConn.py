# internet_check.py


import socket

def is_internet_available():
    try:
        # Try to connect to a well-known website
        socket.create_connection(("www.google.com", 80))
        return True
    except OSError:
        pass
    return False
#rty = is_internet_available()
if __name__ == "__main__":
#print(rty)
    is_internet_available()
