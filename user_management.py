#--- START OF FILE user_management.py ---
import json
import uuid
import random
import os
from config import ADMIN_IDS as INITIAL_ADMIN_IDS

ADMIN_IDS_FILE = "admin_ids.json"

REFERRER_BONUS_CREDITS = 50
REFERRED_BONUS_CREDITS = 25

_ADMIN_IDS = []

def _load_admin_ids():
    global _ADMIN_IDS
    try:
        if os.path.exists(ADMIN_IDS_FILE):
            with open(ADMIN_IDS_FILE, 'r') as f:
                loaded_ids = json.load(f)
                if isinstance(loaded_ids, list):
                    _ADMIN_IDS = loaded_ids
                else:
                    print(f"Warning: {ADMIN_IDS_FILE} contains invalid data format. Using initial admin IDs from config.")
                    _ADMIN_IDS = list(INITIAL_ADMIN_IDS)
        else:
            print(f"Info: {ADMIN_IDS_FILE} not found. Initializing admin IDs from config.")
            _ADMIN_IDS = list(INITIAL_ADMIN_IDS)
    except FileNotFoundError:
        print(f"Info: {ADMIN_IDS_FILE} not found. Initializing admin IDs from config (FileNotFoundError).")
        _ADMIN_IDS = list(INITIAL_ADMIN_IDS)
    except json.JSONDecodeError:
        print(f"Warning: {ADMIN_IDS_FILE} is corrupted or empty. Using initial admin IDs from config.")
        _ADMIN_IDS = list(INITIAL_ADMIN_IDS)
    except Exception as e:
        print(f"Error loading admin IDs from {ADMIN_IDS_FILE}: {e}. Using initial admin IDs from config.")
        _ADMIN_IDS = list(INITIAL_ADMIN_IDS)

    if not _ADMIN_IDS:
        print("Warning: Admin list is empty after loading and fallback. Ensure config.py has initial ADMIN_IDS set.")
        _ADMIN_IDS = list(INITIAL_ADMIN_IDS)

    _save_admin_ids()

def _save_admin_ids():
    try:
        with open(ADMIN_IDS_FILE, 'w') as f:
            json.dump(_ADMIN_IDS, f, indent=4)
    except Exception as e:
        print(f"Error saving admin IDs to {ADMIN_IDS_FILE}: {e}")

_load_admin_ids()

def _load_user_data():
    try:
        with open('user_data.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError as e:
        print(f"JSONDecodeError: user_data.json - Possible file corruption: {e}. Attempting to reset user data file.")
        try:
            os.rename('user_data.json', 'user_data.json.backup')
            with open('user_data.json', 'w') as f:
                json.dump({}, f)
            print("user_data.json has been reset to an empty state. Corrupted file backed up as user_data.json.backup.")
        except Exception as reset_e:
            print(f"Error resetting user_data.json: {reset_e}. Please check file permissions and disk space.")
        return {}

def _save_user_data(user_data):
    with open('user_data.json', 'w') as f:
        json.dump(user_data, f, indent=4)

def _load_redeem_data():
    try:
        with open('redeem_codes.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError as e:
        print("JSONDecodeError: redeem_codes.json - Possible file corruption. Returning empty redeem data.")
        return {}

def _save_redeem_data(redeem_data):
    with open('redeem_codes.json', 'w') as f:
        json.dump(redeem_data, f, indent=4)

def generate_redeem_codes(amount, num_codes, code_format="xxxx-xxxx-xxxx", premium=False):
    codes = []
    redeem_data = _load_redeem_data()
    for _ in range(num_codes):
        if code_format == "xxxx-xxxx-xxxx":
            code_parts = []
            for _ in range(3):
                code_parts.append(''.join(random.choices('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=4)))
            code = '-'.join(code_parts)
        else:
            code = str(uuid.uuid4()).split('-')[0].upper()
        codes.append(code)
        redeem_data[code] = {
            "credits": amount,
            "used": False,
            "premium": premium,
            "redeemed_by": None
        }
    _save_redeem_data(redeem_data)
    return codes

def redeem_credits(user_id, code):
    user_data = _load_user_data()
    redeem_data = _load_redeem_data()

    code_str = code.strip()

    if code_str not in redeem_data:
        return "invalid"

    if redeem_data[code_str]['used']:
        return "used"

    user_id_str = str(user_id)
    if user_id_str not in user_data:
        user_data[user_id_str] = {'credits': 0, 'gate_preference': 'auth', 'stats': {'approved': 0, 'declined': 0, 'ccn': 0, 'cvv': 0}, 'is_premium': False, 'registered': False, 'referral_code': generate_referral_code()}

    if redeem_data[code_str]['premium']:
        user_data[user_id_str]['is_premium'] = True
        redeem_data[code_str]['credits'] = 0
    else:
        user_data[user_id_str]['credits'] += redeem_data[code_str]['credits']

    redeem_data[code_str]['used'] = True
    redeem_data[code_str]['redeemed_by'] = user_id
    _save_user_data(user_data)
    _save_redeem_data(redeem_data)
    return "success"

def generate_referral_code():
    return str(uuid.uuid4()).replace('-', '')[:10]

def register_user(user_id, referrer_id=None):
    user_data = _load_user_data()
    user_id_str = str(user_id)

    if user_id_str in user_data and user_data[user_id_str].get('registered', False):
        return "already_registered"

    if user_id_str not in user_data:
        user_data[user_id_str] = {'credits': 0, 'gate_preference': 'auth', 'stats': {'approved': 0, 'declined': 0, 'ccn': 0, 'cvv': 0}, 'is_premium': False, 'registered': False, 'referral_code': generate_referral_code()}

    initial_credits = 100
    user_data[user_id_str]['credits'] += initial_credits
    user_data[user_id_str]['registered'] = True

    if referrer_id:
        referrer_bonus = get_referrer_bonus()
        referred_bonus = get_referred_bonus()

        referrer_id_str = str(referrer_id)
        if referrer_id_str in user_data:
            user_data[referrer_id_str]['credits'] += referrer_bonus
            user_data[user_id_str]['credits'] += referred_bonus
            user_data[user_id_str]['referrer_id'] = referrer_id

    _save_user_data(user_data)
    return "success"

def add_credits_to_user(user_id, amount):
    user_data = _load_user_data()
    user_id_str = str(user_id)
    if user_id_str not in user_data:
        user_data[user_id_str] = {'credits': 0, 'gate_preference': 'auth', 'stats': {'approved': 0, 'declined': 0, 'ccn': 0, 'cvv': 0}, 'is_premium': False, 'registered': False, 'referral_code': generate_referral_code()}
    user_data[user_id_str]['credits'] += amount
    _save_user_data(user_data)

def get_user_credits(user_id):
    user_data = _load_user_data()
    user_id_str = str(user_id)
    if user_id_str in user_data:
        if user_data[user_id_str].get('is_premium', False):
            return "Unlimited"
        return user_data[user_id_str]['credits']
    return 0

def deduct_credits(user_id):
    user_data = _load_user_data()
    user_id_str = str(user_id)
    if user_id_str in user_data and not user_data[user_id_str].get('is_premium', False):
        if user_data[user_id_str]['credits'] > 0:
            user_data[user_id_str]['credits'] -= 1
            _save_user_data(user_data)
            return True
        else:
            return False
    return True

def update_user_stats(user_id, status):
    user_data = _load_user_data()
    user_id_str = str(user_id)
    if user_id_str not in user_data:
        user_data[user_id_str] = {'credits': 0, 'gate_preference': 'auth', 'stats': {'approved': 0, 'declined': 0, 'ccn': 0, 'cvv': 0}, 'is_premium': False, 'registered': False, 'referral_code': generate_referral_code()}

    stats = user_data[user_id_str]['stats']
    if status == 'APPROVED':
        stats['approved'] = stats.get('approved', 0) + 1
    elif status == 'DECLINED':
        stats['declined'] = stats.get('declined', 0) + 1
    elif status == 'CCN':
        stats['ccn'] = stats.get('ccn', 0) + 1
    elif status == 'CVV':
        stats['cvv'] = stats.get('cvv', 0) + 1
    _save_user_data(user_data)

def get_user_stats(user_id):
    user_data = _load_user_data()
    user_id_str = str(user_id)
    if user_id_str in user_data:
        return user_data[user_id_str]['stats']
    return None

def set_user_gate_preference(user_id, gate_name):
    user_data = _load_user_data()
    user_id_str = str(user_id)
    if user_id_str not in user_data:
        user_data[user_id_str] = {'credits': 0, 'gate_preference': 'auth', 'stats': {'approved': 0, 'declined': 0, 'ccn': 0, 'cvv': 0}, 'is_premium': False, 'registered': False, 'referral_code': generate_referral_code()}
    user_data[user_id_str]['gate_preference'] = gate_name
    _save_user_data(user_data)

def get_user_gate_preference(user_id):
    user_data = _load_user_data()
    user_id_str = str(user_id)
    return user_data[user_id_str].get('gate_preference', 'auth') if user_id_str in user_data else "auth"

def is_admin(user_id):
    return user_id in _ADMIN_IDS

def add_admin_user(user_id):
    global _ADMIN_IDS
    if user_id not in _ADMIN_IDS:
        _ADMIN_IDS.append(user_id)
        _save_admin_ids()
        return True
    return False

def remove_admin_user(user_id):
    global _ADMIN_IDS
    if user_id in _ADMIN_IDS and user_id != INITIAL_ADMIN_IDS[0]:
        _ADMIN_IDS.remove(user_id)
        _save_admin_ids()
        return True
    return False

def get_admin_list():
    return list(_ADMIN_IDS)

def is_premium(user_id):
    user_data = _load_user_data()
    user_id_str = str(user_id)
    return user_data[user_id_str].get('is_premium', False) if user_id_str in user_data else False

def is_registered(user_id):
    user_data = _load_user_data()
    user_id_str = str(user_id)
    return user_data[user_id_str].get('registered', False) if user_id_str in user_data else False

def get_user_referral_link(user_id, bot_username):
    user_data = _load_user_data()
    user_id_str = str(user_id)
    if user_id_str in user_data:
        referral_code = user_data[user_id_str].get('referral_code')
        if not referral_code:
            referral_code = generate_referral_code()
            user_data[user_id_str]['referral_code'] = referral_code
            _save_user_data(user_data)
        if referral_code:
            return f"https://t.me/{bot_username}?start={referral_code}"
    return None

def get_referrer_bonus():
    return REFERRER_BONUS_CREDITS

def get_referred_bonus():
    return REFERRED_BONUS_CREDITS

def set_referral_bonuses(referrer_bonus, referred_bonus):
    global REFERRER_BONUS_CREDITS, REFERRED_BONUS_CREDITS
    REFERRER_BONUS_CREDITS = referrer_bonus
    REFERRED_BONUS_CREDITS = referred_bonus
#--- END OF FILE user_management.py ---