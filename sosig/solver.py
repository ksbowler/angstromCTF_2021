def egcd(a,b):
    '''
    Extended Euclidean Algorithm
    returns x, y, gcd(a,b) such that ax + by = gcd(a,b)
    '''
    u, u1 = 1, 0
    v, v1 = 0, 1
    while b:
        q = a // b
        u, u1 = u1, u - q * u1
        v, v1 = v1, v - q * v1
        a, b = b, a - q * b
    return u, v, a

def gcd(a,b):
    '''
    2.8 times faster than egcd(a,b)[2]
    '''
    a,b=(b,a) if a<b else (a,b)
    while b:
        a,b=b,a%b
    return a

def modInverse(e,n):
    '''
    d such that de = 1 (mod n)
    e must be coprime to n
    this is assumed to be true
    '''
    return egcd(e,n)[0]%n

def totient(p,q):
    '''
    Calculates the totient of pq
    '''
    return (p-1)*(q-1)

def bitlength(x):
    '''
    Calculates the bitlength of x
    '''
    assert x >= 0
    n = 0
    while x > 0:
        n = n+1
        x = x>>1
    return n


def isqrt(n):
    '''
    Calculates the integer square root
    for arbitrary large nonnegative integers
    '''
    if n < 0:
        raise ValueError('square root not defined for negative numbers')
    
    if n == 0:
        return 0
    a, b = divmod(bitlength(n), 2)
    x = 2**(a+b)
    while True:
        y = (x + n//x)//2
        if y >= x:
            return x
        x = y


def is_perfect_square(n):
    '''
    If n is a perfect square it returns sqrt(n),
    
    otherwise returns -1
    '''
    h = n & 0xF; #last hexadecimal "digit"
    
    if h > 9:
        return -1 # return immediately in 6 cases out of 16.

    # Take advantage of Boolean short-circuit evaluation
    if ( h != 2 and h != 3 and h != 5 and h != 6 and h != 7 and h != 8 ):
        # take square root if you must
        t = isqrt(n)
        if t*t == n:
            return t
        else:
            return -1
    
    return -1

def rational_to_contfrac(x,y):
    '''
    Converts a rational x/y fraction into
    a list of partial quotients [a0, ..., an]
    '''
    a = x//y
    pquotients = [a]
    while a * y != x:
        x,y = y,x-a*y
        a = x//y
        pquotients.append(a)
    return pquotients

#TODO: efficient method that calculates convergents on-the-go, without doing partial quotients first
def convergents_from_contfrac(frac):
    '''
    computes the list of convergents
    using the list of partial quotients
    '''
    convs = [];
    for i in range(len(frac)):
        convs.append(contfrac_to_rational(frac[0:i]))
    return convs

def contfrac_to_rational (frac):
    '''Converts a finite continued fraction [a0, ..., an]
     to an x/y rational.
     '''
    if len(frac) == 0:
        return (0,1)
    num = frac[-1]
    denom = 1
    for _ in range(-2,-len(frac)-1,-1):
        num, denom = frac[_]*num+denom, num
    return (num,denom)

import random, sys

def miller_rabin_pass(a, s, d, n):
	''' 
	n is an odd number with
		n-1 = (2^s)d, and d odd
		and a is the base: 1 < a < n-1
	
	returns True iff n passes the MillerRabinTest for a 
	'''
	a_to_power = pow(a, d, n)
	i=0
	#Invariant: a_to_power = a^(d*2^i) mod n
	
	# we test whether (a^d) = 1 mod n
	if a_to_power == 1:
		return True
	
	# we test whether a^(d*2^i) = n-1 mod n
	# 	for 0<=i<=s-1
	while(i < s-1):
		if a_to_power == n - 1:
			return True
		a_to_power = (a_to_power * a_to_power) % n
		i+=1
	
	# we reach here if the test failed until i=s-2	
	return a_to_power == n - 1

def miller_rabin(n):
	'''
	Applies the MillerRabin Test to n (odd)
	
	returns True iff n passes the MillerRabinTest for
	K random bases
	'''
	#Compute s and d such that n-1 = (2^s)d, with d odd
	d = n-1
	s = 0
	while d%2 == 0:
		d >>= 1
		s+=1
	
	#Applies the test K times
	#The probability of a false positive is less than (1/4)^K
	K = 20
	
	i=1
	while(i<=K):
	# 1 < a < n-1
		a = random.randrange(2,n-1)
		if not miller_rabin_pass(a, s, d, n):
			return False
		i += 1

	return True

def gen_prime(nbits):
	'''
	Generates a prime of b bits using the
	miller_rabin_test
	'''
	while True:
			p = random.getrandbits(nbits)
			#force p to have nbits and be odd
			p |= 2**nbits | 1
			if miller_rabin(p):
				return p
				break

def gen_prime_range(start, stop):
	'''
	Generates a prime within the given range
	using the miller_rabin_test
	'''
	while True:
		p = random.randrange(start,stop-1)
		p |= 1
		if miller_rabin(p):
				return p
				break


def getPrimePair(bits=512):
    '''
    genera un par de primos p , q con 
        p de nbits y
        p < q < 2p
    '''
    
    assert bits%4==0
    
    p = gen_prime(bits)
    q = gen_prime_range(p+1, 2*p)
    
    return p,q

def generateKeys(nbits=1024):
    '''
    Generates a key pair
        public = (e,n)
        private = d 
    such that
        n is nbits long
        (e,n) is vulnerable to the Wiener Continued Fraction Attack
    '''
    # nbits >= 1024 is recommended
    assert nbits%4==0
    
    p,q = getPrimePair(nbits//2)
    n = p*q
    phi = totient(p, q)
        
    # generate a d such that:
    #     (d,n) = 1
    #    36d^4 < n
    good_d = False
    while not good_d:
        d = random.getrandbits(nbits//4)
        if (gcd(d,phi) == 1 and 36*pow(d,4) < n):
            good_d = True
                    
    e = modInverse(d,phi)
    return e,n,d

def hack_RSA(e,n):
    '''
    Finds d knowing (e,n)
    applying the Wiener continued fraction attack
    '''
    frac = rational_to_contfrac(e, n)
    convergents = convergents_from_contfrac(frac)
    
    for (k,d) in convergents:
        
        #check if d is actually the key
        if k!=0 and (e*d-1)%k == 0:
            phi = (e*d-1)//k
            s = n - phi + 1
            # check if the equation x^2 - s*x + n = 0
            # has integer roots
            discr = s*s - 4*n
            if(discr>=0):
                t = is_perfect_square(discr)
                if t!=-1 and (s+t)%2==0:
                    print("Hacked!")
                    return d
n = 14750066592102758338439084633102741562223591219203189630943672052966621000303456154519803347515025343887382895947775102026034724963378796748540962761394976640342952864739817208825060998189863895968377311649727387838842768794907298646858817890355227417112558852941256395099287929105321231423843497683829478037738006465714535962975416749856785131866597896785844920331956408044840947794833607105618537636218805733376160227327430999385381100775206216452873601027657796973537738599486407175485512639216962928342599015083119118427698674651617214613899357676204734972902992520821894997178904380464872430366181367264392613853
e = 1565336867050084418175648255951787385210447426053509940604773714920538186626599544205650930290507488101084406133534952824870574206657001772499200054242869433576997083771681292767883558741035048709147361410374583497093789053796608379349251534173712598809610768827399960892633213891294284028207199214376738821461246246104062752066758753923394299202917181866781416802075330591787701014530384229203479804290513752235720665571406786263275104965317187989010499908261009845580404540057576978451123220079829779640248363439352875353251089877469182322877181082071530177910308044934497618710160920546552403519187122388217521799
c = 13067887214770834859882729083096183414253591114054566867778732927981528109240197732278980637604409077279483576044261261729124748363294247239690562657430782584224122004420301931314936928578830644763492538873493641682521021685732927424356100927290745782276353158739656810783035098550906086848009045459212837777421406519491289258493280923664889713969077391608901130021239064013366080972266795084345524051559582852664261180284051680377362774381414766499086654799238570091955607718664190238379695293781279636807925927079984771290764386461437633167913864077783899895902667170959671987557815445816604741675326291681074212227
d = hack_RSA(e,n)
from Crypto.Util.number import *
m = pow(c,d,n)
print(long_to_bytes(m))
