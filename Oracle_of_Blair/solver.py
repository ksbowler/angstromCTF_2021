from Crypto.Util.number import *
from functools import reduce
from operator import mul
from itertools import combinations
import sys
import socket, struct, telnetlib

# --- common funcs ---
def sock(remoteip, remoteport):
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((remoteip, remoteport))
	return s, s.makefile('rw')

def read_until(f, delim='\n'):
	data = ''
	while not data.endswith(delim):
		data += f.read(1)
	return data

	
#HOSTはIPアドレスでも可
HOST, PORT = "crypto.2021.chall.actf.co", 21112
s, f = sock(HOST, PORT)
print(read_until(f,"input: "))
#c1 = c2 = "00"*16
#"00"*16をkeyによって暗号化した値を求める
test = "00"*32
s.send(test.encode()+b"\n")
temp = read_until(f).strip()
c2 = bytes.fromhex("00"*16)
c2 = bytes_to_long(c2)
p3 = int(temp[len(temp)//2:],16)
c_enc3 = c2^p3
#c_enc3とは"00"*16をkeyによって暗号化したもの
print(c_enc3)

#求めたc_enc3により、flagの後半部分を求める
print(read_until(f,"input: "))
test = "7b7d07070707070707" + ("00"*16)
s.send(test.encode()+b"\n")
temp = read_until(f).strip()
assert len(temp) == 96
p3 = temp[-32:]
c2 = c_enc3^int(p3,16)
print(long_to_bytes(c2))
flag2 = long_to_bytes(c2)
#flagの後半部分が求まった。

#flagの後半部分をkeyによって暗号化した値を求める
m2 = str(hex(c2))[2:]
print(m2) #m2とはflagの後半部分
#p2 = temp[32:64]
print(read_until(f,"input: "))
test = "00"*16 + m2
s.send(test.encode()+b"\n")
temp = read_until(f).strip()
cc1 = bytes.fromhex("00"*16)
cc1 = bytes_to_long(cc1)
pp2 = int(temp[len(temp)//2:],16)
c_enc2 = cc1^pp2
#c_enc2 = flagの後半部分をkeyによって暗号化した値

#flagの前半部分を求める
print(read_until(f,"input: "))
test = "7b7d07070707070707"
s.send(test.encode()+b"\n")
temp = read_until(f).strip()
p2 = int(temp[32:],16)
c1 = c_enc2^p2
print(long_to_bytes(c1))
flag1 = long_to_bytes(c1)
#求まった

#flagを綺麗な形に
print(flag1+flag2)

#read_untilの使い方
#返り値があるのでprintするか、何かの変数に入れる
#1行読む：read_until(f)
#特定の文字まで読む：read_until(f,"input")
#配列に格納する：recv_m = read_until(f).split() ot .strip()

#サーバーに何か送るとき
#s.send(b'1\n') : 1を送っている
#バイト列で送ること。str->bytesにするには、変数の後に.encode()
#必ず改行を入れること。終了ポイントが分からなくなる。ex) s.send(flag.encode() + b'\n')

