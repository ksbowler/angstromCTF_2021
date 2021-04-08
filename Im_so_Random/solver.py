from Crypto.Util.number import *
import sympy
from functools import reduce
from operator import mul
from itertools import combinations
import sys
import socket, struct, telnetlib
import gmpy2

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

def find_root(r):
	#与えられたrは8桁の数字で、前4桁後ろ4桁を付けると平方数になるかbrute forceで確認
	candi = []
	r = "0"*(8-len(r)) + r
	for a in range(10000):
		if a%1000 == 0: print(a)
		ae = str(a)
		for b in range(10000):
			be = str(b)
			be = "0"*(4-len(be)) + be
			x = int(ae+r+be)
			p,ch = gmpy2.iroot(x,2)
			if ch:
				#xが平方数であるのでp*p=xとなるpをcandiに追加
				candi.append(int(p))

	return candi

def getNum(seed):
	ret = int(str(seed**2).rjust(16, "0")[4:12])
	return ret


while True:	
#HOSTはIPアドレスでも可
	HOST, PORT = "crypto.2021.chall.actf.co", 21600
	s, f = sock(HOST, PORT)
	ch = True
	print(read_until(f,"[g]? "))
	s.send(b"r\n")
	m = read_until(f).strip()
	fac = sympy.factorint(int(m))
	print(fac)

	#素因数分解して8桁の素数出てきたらr1と断定する(それがr1出ない時もあるので注意)
	for i in fac.keys():
		if len(str(i)) == 8:
			ch = False
			r1 = i
			r2 = int(m)//i
			break
	if ch: s.close()
	else:
		print(r1,r2)
		#seedを求める
		r1_candi = find_root(str(r1))
		print(r1_candi)
		r2_candi = find_root(str(r2))
		#print(r1_candi)
		print(r2_candi)
		print(read_until(f,"[g]? "))
		s.send(b"r\n")
		m = read_until(f).strip()
		seed1 = 0
		seed2 = 0
		for r1c in r1_candi:
			#r1のseedの候補
			rr1 = getNum(r1c)
			rrr1 = getNum(rr1)
			for r2c in r2_candi:
				#r2のseedの候補
				rr2 = getNum(r2c)
				rrr2 = getNum(rr2)
				if int(m) == rrr1*rrr2:
					print("match! ",rrr1,rrr2)
					seed1 = r1c
					seed2 = r2c
					break

		#各seedより乱数を生成する
		n1 = getNum(seed1)
		nn1 = getNum(n1)
		nnn1 = getNum(nn1)
		n2 = getNum(seed2)
		nn2 = getNum(n2)
		nnn2 = getNum(nn2)
		print(read_until(f,"[g]? "))
		s.send(b"g\n")
		print(read_until(f,"generated? "))
		ret = str(nnn1*nnn2)
		s.send(ret.encode()+b"\n")
		#print(read_until(f,"[g]? "))
		print(read_until(f,"generated? "))
		fi1 = getNum(nnn1)
		fi2 = getNum(nnn2)
		ret = str(fi1*fi2)
		s.send(ret.encode()+b"\n")
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

