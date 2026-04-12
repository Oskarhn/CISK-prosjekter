import secrets
n=secrets.randbelow(100)+1
while 1:
 try:
  a,b=map(int,input("Two nums that sum to secret (1-100): ").split())
  print(['Too low','Too high','Win! Secret=%d'%n][(a+b<n)+(a+b==n)*2])
 except:print('Ints only')