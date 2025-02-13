F=input
D=print
C=range
import base64 as E,os,secrets as H,uuid,zlib,hashlib as S,marshal as T
from getpass import getpass
from cryptography.hazmat.primitives.ciphers import Cipher as I,algorithms as J,modes
from cryptography.hazmat.primitives import hashes as K
from cryptography.hazmat.backends import default_backend as B
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC as L
from binascii import hexlify
from random import randint,shuffle
def U(password,salt,iterations=1000000):A=L(algorithm=K.SHA256(),length=32,salt=salt,iterations=iterations,backend=B());return A.derive(password.encode())
def V(data,keys,ivs):
	A=data
	for(D,E)in zip(keys,ivs):F=I(J.AES(D),modes.CTR(E),backend=B());C=F.encryptor();A=C.update(A)+C.finalize()
	return A
def M(file_path,encryption_rounds):
	B=file_path;A='utf-8'
	try:
		N=F('Do you want to add a password for encryption? (Y/N): ').strip().upper()
		if N=='Y':O=F('Enter a password to secure the encryption: ');G=[H.token_bytes(16)for A in C(3)];P=[U(O,A)for A in G];I=[H.token_bytes(16)for A in C(3)]
		else:O=None;G=I=[H.token_bytes(16)for A in C(3)];P=G
		W=B
		for X in C(1,encryption_rounds+1):
			with open(B,'r')as Y:Q=Y.read()
			n=S.sha256(Q.encode()).hexdigest();Z=zlib.compress(Q.encode(A));a=V(Z,P,I);b=E.b64encode(a).decode(A);o=str(uuid.uuid4()).replace('-','')[:8];c,p=os.path.split(B);d=f"{X}.py";J=os.path.join(c,d);e=f"""
import base64
import zlib
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from getpass import getpass
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

def derive_key(password, salt, iterations=1000000):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=iterations,
        backend=default_backend()
    )
    return kdf.derive(password.encode())

def multi_decrypt(data, keys, ivs):
    decrypted_data = data
    for key, iv in zip(reversed(keys), reversed(ivs)):
        cipher = Cipher(algorithms.AES(key), modes.CTR(iv), backend=default_backend())
        decryptor = cipher.decryptor()
        decrypted_data = decryptor.update(decrypted_data) + decryptor.finalize()
    return decrypted_data

def hidden_execute():
    password = input(\"Enter the password to decrypt the code: \") if '{N}' == 'Y' else None
    salts = {list(G)}
    ivs = {list(I)}
    encoded_code = \"{b}\"
    encrypted_code = base64.b64decode(encoded_code.encode('utf-8'))
    keys = [derive_key(password, bytes(salt)) if password else bytes(salt) for salt in salts]
    decrypted_code = multi_decrypt(encrypted_code, keys, [bytes(iv) for iv in ivs])
    decompressed_code = zlib.decompress(decrypted_code)
    exec(decompressed_code.decode('utf-8'), globals(), globals())

hidden_execute()
""";f=E.b64encode(e.encode(A)).decode(A);g=f"""
import base64
import marshal

def hidden_execute():
    encoded_code = \"{f}\"
    decoded_code = base64.b64decode(encoded_code).decode('utf-8')
    exec(decoded_code, globals(), globals())

hidden_execute()
""";h=E.b64encode(g.encode(A)).decode(A);i=f"""
import base64

def hidden_execute():
    encoded_final_code = \"{h}\"
    decoded_final_code = base64.b64decode(encoded_final_code).decode('utf-8')
    exec(decoded_final_code, globals(), globals())

hidden_execute()
""";j=T.dumps(i);K=E.b64encode(j).decode(A);L=[];M=len(K)//10
			for R in C(10):L.append(K[R*M:(R+1)*M])
			L.append(K[10*M:]);k='\n    parts = [\n        '+',\n        '.join(f'"{A}"'for A in L)+'\n    ]'
			with open(J,'w')as l:l.write(f"""
import base64
import marshal

def hidden_execute():{k}
    encoded_final_code = ''.join(parts)
    decoded_code = base64.b64decode(encoded_final_code)
    marshaled_code = marshal.loads(decoded_code)
    exec(marshaled_code, globals(), globals())

hidden_execute()
""")
			D(f"Encrypted file created: {J}")
			if B!=W:os.remove(B)
			B=J
	except Exception as m:D(f"An error occurred: {m}")
if __name__=='__main__':
	A=F('Enter the path of the Python file (must end with .py): ').strip().strip('"')
	if os.path.isfile(A)and A.endswith('.py'):
		try:
			G=int(F('Enter the number of times to encrypt the file: ').strip())
			if G>0:M(A,G)
			else:D('The number of encryption rounds must be greater than 0.')
		except ValueError:D('Invalid input for the number of encryption rounds.')
	else:D('Invalid file path or the file does not end with .py.')