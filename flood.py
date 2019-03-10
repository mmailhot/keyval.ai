import socket
import random
import string

randomkeys = [''.join(random.choices(string.ascii_lowercase, k=18)) for _ in range(25)]
randomvalues = [''.join(random.choices(string.ascii_lowercase, k=200)) for _ in range(25)]
randomkeys2 = [''.join(random.choices(string.ascii_lowercase, k=18)) for _ in range(1)]
randomvalues2 = [''.join(random.choices(string.ascii_lowercase, k=200)) for _ in range(1)]

fixedkeys = [
    "beemovie",
    "princessleia",
    "lolsorandomxD",
    "datgoodshit",
    "datbadshit"
]

keys = randomkeys + fixedkeys + randomkeys2

fixedvalues = [
    "According to all known laws of aviation, there is no way a bee should be able to fly. Its wings are too small to get its fat little body off the ground. The bee, of course, flies anyway because bees don't care what humans think is impossible. Yellow, black.",
    "You must see this droid safely delivered to him on Alderaan. This is our most desperate hour. Help me, Obi-Wan Kenobi; you’re my only hope.",
    "hi every1 im new!!!!!!! *holds up spork* my name is katy but u can call me t3h PeNgU1N oF d00m!!!!!!!! lol…as u can see im very random!!!! thats why i came here, 2 meet random ppl like me ^_^…",
    "👌👀👌👀👌👀 good shit go౦ԁ sHit👌 thats ✔ some good👌👌shit right👌👌th 👌 ere👌👌👌 right✔there ✔✔if i do ƽaү so my selｆ 💯 i say so 💯",
    "do NOT sign me the FUCK up 👎👀👎👀👎👀👎👀👎👀  bad shit ba̷̶ ԁ sHit 👎 thats ❌ some bad 👎👎shit right 👎👎 th   👎 right ❌ there ❌ ❌ if i do ƽaү so my selｆ🚫 i say so 🚫"
]

values = randomvalues + fixedvalues + randomvalues2

TCP_IP = '127.0.0.1'
TCP_PORT = 3030
BUFFER_SIZE = 4096

def make_raw_string(v):
    b = v.encode('utf-8')
    return b'$%b\r\n%b\r\n' % (str(len(b)).encode("ascii"), b)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))


for (k, v) in zip(keys,values):
    msg = b'*3\r\n$3\r\nSET\r\n%b%b' % (make_raw_string(k), make_raw_string(v))
    s.send(msg)
    _ = s.recv(BUFFER_SIZE)

s.close()
