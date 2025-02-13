import os

def load_env(file_path=".env"):
    if not os.path.exists(file_path):
        print(f"Error: {file_path} not found.")
        return
    
    with open(file_path, "r") as file:
        for line in file:
            line = line.strip()
            if line and not line.startswith("#"):
                key, value = line.split("=", 1)
                os.environ[key] = value
                print(f"Loaded: {key}")

if __name__ == "__main__":
    load_env()