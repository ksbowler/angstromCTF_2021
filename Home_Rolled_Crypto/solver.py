from Crypto.Util.number import *
#import sympy
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


#128bit ans[2*i],ans[2*i+1] -> i bit目が0の時の値。1の時の値
ans = ["0" for _ in range(256)]
#HOSTはIPアドレスでも可
HOST, PORT = "crypto.2021.chall.actf.co", 21602
s, f = sock(HOST, PORT)

#各bitについて、0を暗号化するとどうなるかを記憶する
cri = "0"*32
read_until(f,"[2]? ")
s.send(b"1\n")
read_until(f,"encrypt: ")
s.send(cri.encode()+b"\n")
cri_ans = read_until(f).strip()
assert len(cri_ans) == 32
x = int(cri_ans,16)
x = str(bin(x))[2:]
x = "0"*(128-len(x)) + x
print(x)
assert len(x) == 128
for i in range(128):
	if x[i] == "1": ans[2*i] = "1"

#各bitについて、1を暗号化するとどうなるかを記憶する
crif = "f"*32
read_until(f,"[2]? ")
s.send(b"1\n")
read_until(f,"encrypt: ")
s.send(crif.encode()+b"\n")
crif_ans = read_until(f).strip()
assert len(crif_ans) == 32
x = int(crif_ans,16)
x = str(bin(x))[2:]
x = "0"*(128-len(x)) + x
print(x)
assert len(x) == 128
for i in range(128):
	if x[i] == "1": ans[2*i+1] = "1"

print("oracle complete")
#あとは暗号化をこちらでも行い10連続で当てる
read_until(f,"[2]? ")
s.send(b"2\n")
for _ in range(10):
	#read_until(f,"[2]? ")
	#s.send(b"2\n")
	recv_m = read_until(f).split()
	print(recv_m)
	ques = recv_m[-1]
	print(ques)
	#quesは暗号化すべき文章
	q1 = ques[:32]
	q2 = ques[32:]
	assert len(q1) == len(q2)
	x1 = int(q1,16)
	x1 = str(bin(x1))[2:]
	x1 = "0"*(128-len(x1)) + x1
	assert len(x1) == 128
	x2 = int(q2,16)
	x2 = str(bin(x2))[2:]
	x2 = "0"*(128-len(x2)) + x2
	assert len(x2) == 128
	sen = ""
	for i in range(len(x1)):
		if x1[i] == "0": sen += ans[2*i]
		else: sen += ans[2*i+1]
	for i in range(len(x2)):
		if x2[i] == "0": sen += ans[2*i]
		else: sen += ans[2*i+1]
	#senは2進数
	sen = int(sen,2)
	sen = hex(sen)
	sen = str(sen)[2:]
	sen = "0"*(64-len(sen)) + sen
	print(sen[:32],sen[32:])
	s.send(sen.encode()+b"\n")

while True:
	print(read_until(f))

#read_untilの使い方
#返り値があるのでprintするか、何かの変数に入れる
#1行読む：read_until(f)
#特定の文字まで読む：read_until(f,"input")
#配列に格納する：recv_m = read_until(f).split() ot .strip()

#サーバーに何か送るとき
#s.send(b'1\n') : 1を送っている
#バイト列で送ること。str->bytesにするには、変数の後に.encode()
#必ず改行を入れること。終了ポイントが分からなくなる。ex) s.send(flag.encode() + b'\n')

