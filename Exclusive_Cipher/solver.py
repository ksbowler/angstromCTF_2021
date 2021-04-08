from Crypto.Util.number import *
enc = "ae27eb3a148c3cf031079921ea3315cd27eb7d02882bf724169921eb3a469920e07d0b883bf63c018869a5090e8868e331078a68ec2e468c2bf13b1d9a20ea0208882de12e398c2df60211852deb021f823dda35079b2dda25099f35ab7d218227e17d0a982bee7d098368f13503cd27f135039f68e62f1f9d3cea7c"

m = [0x61, 0x63, 0x74, 0x66, 0x7b]

for i in range(0,len(enc)-10,2):
	#enc[i],enc[i+1]を16進数に戻してxorにするとm[i]と同じになる
	k = []
	x = enc[i:]
	for j in range(5):
		k.append(int(x[2*j]+x[2*j+1],16)^m[j])

	flag = ""
	cnt = 0
	for j in range(i,len(enc),2):
		flag += chr(int(enc[j]+enc[j+1],16)^k[cnt%5])
		cnt += 1
	#flagの候補を出す。
	if "}" in flag: print(flag,k)

#keyの候補が一つに絞れたので完璧に復元する
k = [237, 72, 133, 93, 102]

for j in range(5):
	key = k[j:] + k[:j]
	flag = ""
	cnt = 0
	for i in range(0,len(enc),2):
		flag += chr(int(enc[i]+enc[i+1],16)^key[cnt%5])
		cnt += 1
	print(flag)
