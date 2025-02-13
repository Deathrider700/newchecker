# session_manager.py - Manages session files for requests

import requests
import os

SESSION_FILE_NAME = "bot_session.pkl" # Define session file name here for easy modification

def manage_session_file():
    """
    Manages a session file using requests.Session and pickle for persistence.
    Loads session from file if it exists, otherwise creates a new session.
    Returns a requests.Session object.
    """
    session = requests.Session()
    session_file_path = os.path.join(os.getcwd(), SESSION_FILE_NAME) # Session file in bot's working directory

    if os.path.exists(session_file_path):
        try:
            import pickle # Import pickle only when needed to manage session
            with open(session_file_path, 'rb') as f:
                session_dict = pickle.load(f)
                if isinstance(session_dict, dict): # Basic check for loaded data type
                    session.cookies.update(session_dict.get('cookies', {}))
                    session.headers.update(session_dict.get('headers', {}))
                    print(f"Session loaded from {SESSION_FILE_NAME}")
                else:
                    print(f"Warning: Invalid session data format in {SESSION_FILE_NAME}. Starting new session.")
        except Exception as e:
            print(f"Error loading session from {SESSION_FILE_NAME}: {e}. Starting new session.")
            session = requests.Session() # Ensure new session is created in case of load failure

    def save_session():
        try:
            import pickle # Import pickle here, only when saving
            session_data = {
                'cookies': requests.utils.dict_from_cookiejar(session.cookies),
                'headers': session.headers.copy()
            }
            with open(session_file_path, 'wb') as f:
                pickle.dump(session_data, f)
            print(f"Session saved to {SESSION_FILE_NAME}")
        except Exception as e:
            print(f"Error saving session to {SESSION_FILE_NAME}: {e}")

    session.save = save_session # Attach save function to session object

    return session

# --- Example usage (for testing - can be removed later) ---
if __name__ == '__main__':
    test_session = manage_session_file()
    print("Initial session cookies:", test_session.cookies.get_dict())

    # Example: Set a cookie and header
    test_session.cookies.set('test_cookie', 'cookie_value', domain='example.com')
    test_session.headers.update({'X-Test-Header': 'header_value'})

    test_session.save() # Save the session

    loaded_session = manage_session_file() # Load the session back
    print("Loaded session cookies:", loaded_session.cookies.get_dict())
    print("Loaded session headers:", loaded_session.headers)

    # Verify if cookies and headers are persisted
    if 'test_cookie' in loaded_session.cookies and loaded_session.headers.get('X-Test-Header') == 'header_value':
        print("Session data successfully persisted and loaded!")
    else:
        print("Session data persistence test failed.")