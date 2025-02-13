import marshal

def decrypt_and_execute(input_file):
    with open(input_file, "rb") as f:
        encrypted_data = f.read()

    exec(marshal.loads(encrypted_data))

# Run the encrypted script
decrypt_and_execute("bot_core_marshal.py")
