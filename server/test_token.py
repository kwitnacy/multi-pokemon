import os 

# print(bytes(os.urandom(16), 'utf-8'))

b = os.urandom(16).hex()
print(b)
