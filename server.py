import model
import socket

TCP_IP = '127.0.0.1'
TCP_PORT = 3030
BUFFER_SIZE = 4096

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(1)

def eat_till_crlf(b):
    (before, _, after) = b.partition(b'\r\n')
    return (before, after)

# Returns parsed value one
def parse_redis_value(b):
    if b[0] == b'*'[0]:
        (num, rem) = eat_till_crlf(b[1:])
        res = []
        for _ in range(int(num)):
            (x, r2) = parse_redis_value(rem)
            res.append(x)
            rem = r2
        return res, rem
    elif b[0] == b'+'[0]:
        return eat_till_crlf(b[1:])
    elif b[0] == b'-'[0]:
        raise Exception(eat_till_crlf(b[1:]))
    elif b[0] == b':'[0]:
        (x, rem) = eat_till_crlf(b[1:])
        return (int(x), rem)
    elif b[0] == b'$'[0]:
        (l, rem) = eat_till_crlf(b[1:])
        if l == b'-1':
            return (None, rem)
        else:
            return (rem[:int(l)], rem[int(l) + 2:])

NULL = b'$-1\r\n'

def handle_command(c):
    print(c[0])
    print(c)
    if c[0] == b'COMMAND':
        return NULL
    elif c[0] == b'SET':
        key = c[1]
        val = c[2]
        model.insert(key, val, epochs=13)
        return NULL
    elif c[0] == b'GET':
        key = c[1]
        v = model.get(key)
        return b'$%b\r\n%b\r\n' % (str(len(v)).encode("ascii"), v)
    elif c[0] == b'INCR':
        key = c[1]
        v = model.get(key)
        i = int(v.decode("ascii"))
        model.insert(key, str(i + 1).encode("ascii"), epochs=10)
        return NULL
    elif c[0] == b'DECR':
        key = c[1]
        v = model.get(key)
        i = int(v.decode("ascii"))
        model.insert(key, str(i - 1).encode("ascii"), epochs=10)
        return NULL
    elif c[0] == b'INCRBY':
        key = c[1]
        v = model.get(key)
        i = int(v.decode("ascii"))
        model.insert(key, str(i + int(c[2].decode("ascii"))).encode("ascii"), epochs=10)
        return NULL
    else:
        return b'-ERROR: Unsupported command\r\n'

while True:
    conn, addr = s.accept()
    print('Connection address:', addr)
    try:
        while 1:
            data = conn.recv(BUFFER_SIZE)
            if not data: break
            conn.send(handle_command((parse_redis_value(data)[0])))
    except KeyboardInterrupt:
        pass
    conn.close()
s.close()
