#--- START OF FILE bot.py ---

#--- START OF FILE bot_core.py ---
import telebot
import os
import re
import time
from telebot import types
import json
import logging
from collections import defaultdict
from datetime import datetime, timedelta
from threading import Timer
from user_management import get_user_credits, deduct_credits, update_user_stats, get_user_gate_preference, set_user_gate_preference, is_admin, get_user_stats, redeem_credits, generate_redeem_codes, is_premium, add_credits_to_user, is_registered, register_user, generate_referral_code, get_referrer_bonus, get_referred_bonus, set_referral_bonuses, get_user_referral_link, add_admin_user, remove_admin_user, get_admin_list # Import new user management functions, admin list functions
# Import modules (gates, user_management, utils, config)
from gates.stripe_gates import Tele, Tele_stripe2, Tele_stripe4
from user_management import *
from utils import *
from config import BOT_TOKEN, ADMIN_IDS

# --- Logging and Bot Initialization ---
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
if not BOT_TOKEN:
    logging.critical("BOT_TOKEN is missing! Check config.py or environment variables.")
    exit(1)

bot = telebot.TeleBot(BOT_TOKEN, parse_mode="HTML")
subscriber_ids = set(ADMIN_IDS)
BOT_USERNAME = "crimsonxcheckerbot"
ADMIN_IDS_FILE = "admin_ids.txt"
CHECK_LOG_FILE = "check_logs.json"
USER_NOTES_FILE = "user_notes.json"
RATE_LIMIT_TIME = 5
RATE_LIMIT_MAX_CALLS = 3
USER_PREFERENCES_FILE = "user_preferences.json"
LANGUAGES_FILE = "languages.json"
THEMES_FILE = "themes.json"
SCHEDULED_DOWNTIME_FILE = "scheduled_downtime.json"

# --- Data Loading Functions ---
def load_admin_ids():
    try:
        with open(ADMIN_IDS_FILE, 'r') as f:
            return set(int(line.strip()) for line in f if line.strip().isdigit())
    except FileNotFoundError:
        return set(ADMIN_IDS)
    except Exception as e:
        logging.error(f"Error loading admin IDs: {e}")
        return set(ADMIN_IDS)

def save_admin_ids(admin_ids_set):
    try:
        with open(ADMIN_IDS_FILE, 'w') as f:
            for admin_id in admin_ids_set:
                f.write(str(admin_id) + '\n')
    except Exception as e:
        logging.error(f"Error saving admin IDs: {e}")


def load_user_notes():
    try:
        with open(USER_NOTES_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError:
        logging.error("JSONDecodeError in user_notes.json, resetting notes.")
        return {}

def save_user_notes(user_notes):
    try:
        with open(USER_NOTES_FILE, 'w') as f:
            json.dump(user_notes, f, indent=4)
    except Exception as e:
        logging.error(f"Error saving user notes: {e}")

def load_user_preferences():
    try:
        with open(USER_PREFERENCES_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError:
        logging.error("JSONDecodeError in user_preferences.json, resetting preferences.")
        return {}

def save_user_preferences(user_preferences):
    try:
        with open(USER_PREFERENCES_FILE, 'w') as f:
            json.dump(user_preferences, f, indent=4)
    except Exception as e:
        logging.error(f"Error saving user preferences: {e}")

def load_languages():
    try:
        with open(LANGUAGES_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        logging.error(f"Language file {LANGUAGES_FILE} not found!")
        return {"en": {}}
    except json.JSONDecodeError:
        logging.error(f"JSONDecodeError in {LANGUAGES_FILE}!")
        return {"en": {}}

def load_themes():
    try:
        with open(THEMES_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        logging.error(f"Theme file {THEMES_FILE} not found!")
        return {"default": {}}
    except json.JSONDecodeError:
        logging.error(f"JSONDecodeError in {THEMES_FILE}!")
        return {"default": {}}

def load_scheduled_downtime():
    try:
        with open(SCHEDULED_DOWNTIME_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError:
        logging.error(f"JSONDecodeError in {SCHEDULED_DOWNTIME_FILE}!")
        return {}

def save_scheduled_downtime(downtime_data):
    try:
        with open(SCHEDULED_DOWNTIME_FILE, 'w') as f:
            json.dump(downtime_data, f, indent=4)
    except Exception as e:
        logging.error(f"Error saving scheduled downtime: {e}")

subscriber_ids = load_admin_ids()
user_notes = load_user_notes()
user_preferences = load_user_preferences()
languages = load_languages()
themes = load_themes()
scheduled_downtime = load_scheduled_downtime()

# --- Rate Limiting Function ---
user_last_call = defaultdict(list)
def is_rate_limited(user_id):
    now = time.time()
    calls = user_last_call[user_id]
    calls = [call_time for call_time in calls if call_time > now - RATE_LIMIT_TIME]
    user_last_call[user_id] = calls
    if len(calls) >= RATE_LIMIT_MAX_CALLS:
        return True
    user_last_call[user_id].append(now)
    return False

# --- Helper Functions ---
def handle_stop_signal(chat_id, message_id):
    current_dir = os.getcwd()
    if os.path.exists(os.path.join(current_dir, "stop.stop")):
        try:
            bot.edit_message_text(chat_id=chat_id, message_id=message_id, text='𝗦𝗧𝗢𝗣𝗣𝗘𝗗 ✅\n𝗕𝗢𝗧 𝗕𝗬 ➜ @CrImSon_WoLf777')
        except Exception as e:
            logging.error(f"Error editing message on stop signal: {e}")
        try:
            os.remove(os.path.join(current_dir, 'stop.stop'))
        except Exception as e:
            logging.error(f"Error removing stop file: {e}")
        return True
    return False

def get_gate_function_for_user(user_id):
    gate_preference = get_user_gate_preference(user_id)
    if gate_preference == "stripe2":
        return Tele_stripe2
    elif gate_preference == "stripe4":
        return Tele_stripe4
    else:
        return Tele

def log_check_details(user_id, cc_masked, gate_name, result, check_type):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    log_entry = {
        "timestamp": timestamp,
        "user_id": user_id,
        "cc_masked": cc_masked,
        "gate": gate_name,
        "result": result,
        "check_type": check_type
    }
    try:
        with open(CHECK_LOG_FILE, 'a') as f:
            json.dump(log_entry, f)
            f.write(os.linesep)
    except Exception as e:
        logging.error(f"Error logging check details: {e}")

def generate_credit_card_number():
    while True:
        bin_prefix = random.choice(['4', '5'])
        rest_of_number = ''.join(random.choices('0123456789', k=15))
        potential_cc = bin_prefix + rest_of_number

        if is_luhn_valid(potential_cc):
            return potential_cc

def is_luhn_valid(card_number_str):
    card_number = [int(digit) for digit in card_number_str]
    for i in range(len(card_number) - 2, -1, -2):
        card_number[i] *= 2
        if card_number[i] > 9:
            card_number[i] -= 9
        return sum(card_number) % 10 == 0

# --- UI Building Helper Functions ---
def build_quick_gate_markup(cc, user_id):
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(types.InlineKeyboardButton(get_translation('gate_auth_short', user_id), callback_data=f'reqchk_gate:auth|cc:{cc}'))
    markup.add(types.InlineKeyboardButton(get_translation('gate_2dollar_short', user_id), callback_data=f'reqchk_gate:stripe2|cc:{cc}'))
    markup.add(types.InlineKeyboardButton(get_translation('gate_4dollar_short', user_id), callback_data=f'reqchk_gate:stripe4|cc:{cc}'))
    markup.add(types.InlineKeyboardButton(f"🔄 {get_translation('button_recheck_same_gate', user_id)}", callback_data=f'reqchk_gate:{get_user_gate_preference(user_id)}|cc:{cc}'))
    return markup

# --- Command Handlers ---
@bot.message_handler(commands=['start', 'help', 'buy'])
def send_welcome(message): # (send_welcome function - same as before) ...
    user_id = message.chat.id

    user_name = message.from_user.first_name or get_translation('default_user_name', user_id)
    credits = get_user_credits(user_id)
    current_gate = get_user_gate_preference(user_id).capitalize()
    premium_status = get_translation('premium_status_prefix', user_id) + get_translation( 'premium_status_premium' if is_premium(user_id) else 'premium_status_free', user_id)
    command = message.text.split()[0][1:]

    if command == 'help' or command == 'start':
        help_text_base = get_translation('help_message_base', user_id)
        admin_commands_text = get_translation('help_message_admin_commands', user_id) if is_admin(user_id) else ""
        help_gate_credits = get_translation('help_message_gate_credits', user_id).format(current_gate=current_gate, credits=credits)

        help_text = help_text_base.format(user_name=user_name, premium_status=premium_status) + admin_commands_text + help_gate_credits

        enhanced_help_text = f"""
👋 {get_translation('emoji_wave', user_id)} <b>{get_translation('help_header_welcome', user_id).format(user_name=user_name)}</b> ({premium_status})\n
{get_translation('emoji_warning', user_id)} <b>{get_translation('help_warning_register', user_id)}</b>\n\n
💳 <b>{get_translation('help_section_commands', user_id)}</b>\n
/chk <code>cc|mm|yy|cvv</code> - {get_translation('help_cmd_chk', user_id)}\n
/gate - {get_translation('help_cmd_gate', user_id)}\n
/stats - {get_translation('help_cmd_stats', user_id)}\n
/credits - {get_translation('help_cmd_credits', user_id)}\n
/redeem <code>code</code> - {get_translation('help_cmd_redeem', user_id)}\n
/help - {get_translation('help_cmd_help', user_id)}\n
/gen <code>type</code> - {get_translation('help_cmd_gen', user_id)}\n
/referral - {get_translation('help_cmd_referral', user_id)}\n
/buy - {get_translation('help_cmd_buy', user_id)}\n
/bin <code>bin</code> - {get_translation('help_cmd_bin', user_id)}\n
/note <code>cc</code> <code>note</code> - {get_translation('help_cmd_note', user_id)}\n
/getnote <code>cc</code> - {get_translation('help_cmd_getnote', user_id)}\n
/delnote <code>cc</code> - {get_translation('help_cmd_delnote', user_id)}\n
/transfer <code>username/user_id</code> <code>amount</code> - {get_translation('help_cmd_transfer', user_id)}\n
"""
        if is_admin(user_id):
            enhanced_help_text += f"""
\n👑 <b>{get_translation('help_section_admin_commands', user_id)}</b>\n
/broadcast <code>message</code> - {get_translation('help_cmd_broadcast', user_id)}\n
/code <code>amount</code> - {get_translation('help_cmd_code', user_id)}\n
/add_credits <code>user_id</code> <code>amount</code> - {get_translation('help_cmd_add_credits', user_id)}\n
/userinfo <code>user_id</code> - {get_translation('help_cmd_userinfo', user_id)}\n
/bonus <code>referrer_bonus</code> <code>referred_bonus</code> - {get_translation('help_cmd_bonus', user_id)}\n
/addadmin <code>user_id</code> - {get_translation('help_cmd_addadmin', user_id)}\n
/deladmin <code>user_id</code> - {get_translation('help_cmd_deladmin', user_id)}\n
/botstats - {get_translation('help_cmd_botstats', user_id)}\n
/scheduledowntime - {get_translation('help_cmd_scheduledowntime', user_id)}\n
/finduser - {get_translation('help_cmd_finduser', user_id)}\n
"""
        enhanced_help_text += f"""
\n⚙️ <b>{get_translation('help_current_gate', user_id)}:</b> <code>{current_gate}</code>\n
💰 <b>{get_translation('help_your_credits', user_id)}:</b> <code>{credits}</code>
"""
        bot.reply_to(message, apply_theme(enhanced_help_text, get_user_theme(user_id)), parse_mode="HTML")

    elif command == 'buy':
        buy_text = get_translation('buy_message_text', user_id)
        markup = types.InlineKeyboardMarkup()
        buy_button = types.InlineKeyboardButton(get_translation('buy_button_label', user_id), callback_data='show_payment_methods')
        markup.add(buy_button)
        bot.reply_to(message, apply_theme(buy_text, get_user_theme(user_id)), reply_markup=markup, parse_mode="HTML")

@bot.callback_query_handler(func=lambda call: call.data == 'show_payment_methods')
def payment_methods_callback(call): # (payment_methods_callback function - same as before) ...
    payment_text = get_translation('payment_methods_text', call.message.chat.id)
    markup = types.InlineKeyboardMarkup()
    dm_button = types.InlineKeyboardButton(get_translation('payment_dm_button_label', call.message.chat.id), url="https://t.me/CrImSon_WoLf777")
    markup.add(dm_button)
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=apply_theme(payment_text, get_user_theme(call.message.chat.id)), reply_markup=markup, parse_mode="HTML", disable_web_page_preview=True)

@bot.message_handler(commands=['register', 'start'])
def register_command(message): # (register_command function - same as before) ...
    user_id = message.chat.id

    user_name = message.from_user.first_name or get_translation('default_user_name', user_id)

    if is_registered(user_id):
        bot.reply_to(message, apply_theme(get_translation('already_registered_message', user_id).format(user_name=user_name), get_user_theme(user_id)), parse_mode="HTML")
        return

    referrer_id = None # (register_command - referral logic - same as before) ...
    if message.text.startswith('/start') and len(message.text.split()) > 1:
        try:
            ref_code = message.text.split()[1]
            referrer_id = _get_user_id_from_referral_code(ref_code)
            if referrer_id == user_id or is_admin(referrer_id):
                referrer_id = None
        except:
            referrer_id = None

    register_result = register_user(user_id, referrer_id=referrer_id) # (register_command - register user - same as before) ...

    if register_result == "success": # (register_command - success message - same as before) ...
        with open("user_ids.txt", "a") as f:
            f.write(str(user_id) + "\n")

        initial_credits = get_user_credits(user_id)
        registration_message = get_translation('registration_success_message', user_id).format(user_name=user_name, initial_credits=initial_credits)
        if referrer_id:
            referrer_bonus = get_referrer_bonus()
            referred_bonus = get_referred_bonus()
            registration_message += get_translation('referral_bonus_received_message', user_id).format(referred_bonus=referred_bonus)

        enhanced_registration_message = f"""
✅ <b>{get_translation('registration_header_success', user_id)}</b> {get_translation('emoji_tada', user_id)}\n\n
{get_translation('emoji_user', user_id)} <b>{user_name}</b>, {get_translation('registration_message_registered', user_id)}\n\n
💰 {get_translation('emoji_credit_card', user_id)} <b>{get_translation('registration_message_credits_received', user_id).format(initial_credits=initial_credits)}</b>\n
"""
        if referrer_id:
            enhanced_registration_message += f"\n🎁 {get_translation('emoji_gift', user_id)} {get_translation('registration_message_referral_bonus', user_id).format(referred_bonus=referred_bonus)}\n"

        enhanced_registration_message += f"\n{get_translation('help_command_hint', user_id)}"

        bot.reply_to(message, apply_theme(enhanced_registration_message, get_user_theme(user_id)), parse_mode="HTML")
    elif register_result == "already_registered": # (register_command - already registered message - same as before) ...
        bot.reply_to(message, apply_theme(get_translation('already_registered_message', user_id).format(user_name=user_name), get_user_theme(user_id)), parse_mode="HTML")
    else: # (register_command - failed message - same as before) ...
        bot.reply_to(message, apply_theme(get_translation('registration_failed_message', user_id), get_user_theme(user_id)), parse_mode="HTML")

@bot.message_handler(commands=['referral'])
def referral_command(message): # (referral_command function - same as before) ...
    if not ensure_registered(message): return
    user_id = message.chat.id

    referral_link = get_user_referral_link(user_id, BOT_USERNAME)
    if referral_link:
        referral_message = get_translation('referral_link_message', user_id).format(referral_link=referral_link, referral_credits=get_user_stats(user_id).get('referral_credits', 0))
        enhanced_referral_message = f"""
🔗 <b>{get_translation('referral_header_link', user_id)}</b>\n\n
{referral_link}\n\n
{get_translation('referral_message_share_link', user_id)}\n\n
🎁 {get_translation('emoji_gift', user_id)} <b>{get_translation('referral_message_credits_earned', user_id).format(referral_credits=get_user_stats(user_id).get('referral_credits', 0))}</b>
"""
        bot.reply_to(message, apply_theme(enhanced_referral_message, get_user_theme(user_id)), parse_mode="HTML", disable_web_page_preview=True)
    else:
        bot.reply_to(message, apply_theme(get_translation('referral_link_error_message', user_id), get_user_theme(user_id)), parse_mode="HTML")

@bot.message_handler(commands=['bonus'])
def bonus_command(message): # (bonus_command function - same as before) ...
    user_id = message.chat.id
    if not is_admin(user_id):
        return bot.reply_to(message, apply_theme(get_translation('admin_command_only', user_id), get_user_theme(user_id)), parse_mode="HTML")

    try:
        args = message.text.split()
        if len(args) != 3:
            raise ValueError("Incorrect arguments")
        referrer_bonus = int(args[1])
        referred_bonus = int(args[2])

        if referrer_bonus < 0 or referred_bonus < 0:
            raise ValueError("Bonuses must be non-negative")

        set_referral_bonuses(referrer_bonus, referred_bonus)
        bonus_updated_message = get_translation('bonus_updated_message', user_id).format(referrer_bonus=referrer_bonus, referred_bonus=referred_bonus)
        enhanced_bonus_message = f"""
✅ <b>{get_translation('bonus_header_updated', user_id)}</b> {get_translation('emoji_success', user_id)}\n\n
👤 {get_translation('bonus_message_referrer_bonus', user_id)}: <code>{referrer_bonus}</code> {get_translation('credits_unit', user_id)}\n
👥 {get_translation('bonus_message_referred_bonus', user_id)}: <code>{referred_bonus}</code> {get_translation('credits_unit', user_id)}
"""
        bot.reply_to(message, apply_theme(enhanced_bonus_message, get_user_theme(user_id)), parse_mode="HTML")

    except ValueError as e:
        bot.reply_to(message, apply_theme(get_translation('bonus_usage_error_message', user_id).format(error=e), get_user_theme(user_id)), parse_mode="HTML")
    except Exception as e:
        logging.error(f"Error setting referral bonuses: {e}")
        bot.reply_to(message, apply_theme(get_translation('bonus_set_error_message', user_id), get_user_theme(user_id)), parse_mode="HTML")

# --- Middleware ---
def ensure_registered(message): # (ensure_registered function - same as before) ...
    user_id = message.chat.id
    if not is_registered(user_id) and message.text and not message.text.startswith('/start') and not message.text.startswith('/help') and not message.text.startswith('/register') and not message.text.startswith('/referral') and not message.text.startswith('/buy'):
        bot.reply_to(message, apply_theme(get_translation('must_register_message', user_id), get_user_theme(user_id)), parse_mode="HTML")
        return False
    return True

@bot.message_handler(commands=["gate"])
def gate_command(message): # (gate_command function - same as before) ...
    if not ensure_registered(message): return
    user_id = message.chat.id

    markup = types.InlineKeyboardMarkup(row_width=2)
    gates = [
        (get_translation('gate_stripe_auth', user_id), 'set_gate:auth'),
        (get_translation('gate_stripe_2dollar', user_id), 'set_gate:stripe2'),
        (get_translation('gate_stripe_4dollar', user_id), 'set_gate:stripe4')
    ]
    for gate_name, callback_data in gates:
        markup.add(types.InlineKeyboardButton(gate_name, callback_data=callback_data))
    current_gate = get_user_gate_preference(user_id).capitalize()

    enhanced_gate_message = f"""
⚙️ <b>{get_translation('gate_header_select', user_id)}</b>\n\n
{get_translation('gate_message_current_gate', user_id)}: <code>{current_gate}</code>
"""
    bot.reply_to(message, apply_theme(enhanced_gate_message, get_user_theme(user_id)), reply_markup=markup, parse_mode="HTML")

@bot.callback_query_handler(func=lambda call: call.data.startswith('set_gate:'))
def set_gate_callback(call): # (set_gate_callback function - same as before) ...
    user_id = call.message.chat.id

    gate_name = call.data.split(':')[1]
    set_user_gate_preference(user_id, gate_name)
    gate_display_name = gate_name.replace("stripe2", "2$").replace("stripe4", "4$").capitalize()
    bot.answer_callback_query(call.id, get_translation('gate_set_callback_answer', user_id).format(gate_display_name=gate_display_name))
    gate_selected_message = get_translation('gate_selected_message', user_id).format(gate_display_name=gate_display_name)
    enhanced_gate_selected_message = f"""
⚙️ <b>{get_translation('gate_header_selected', user_id)}</b> {get_translation('emoji_check_mark_button', user_id)}\n\n
{get_translation('gate_message_current_gate_is', user_id)}: <code>{gate_display_name}</code>\n\n
{get_translation('gate_message_gate_updated_to', user_id)}: <code>{gate_display_name}</code>
"""
    bot.edit_message_text(chat_id=user_id, message_id=call.message.message_id, text=apply_theme(enhanced_gate_selected_message, get_user_theme(user_id)), parse_mode="HTML", reply_markup=None)

@bot.message_handler(commands=['stats'])
def stats_command(message): # (stats_command function - same as before) ...
    if not ensure_registered(message): return
    user_id = message.chat.id

    user_stats = get_user_stats(user_id)
    if not user_stats:
        user_stats = {'approved': 0, 'declined': 0, 'ccn': 0, 'cvv': 0, 'referral_credits': 0}
    credits = get_user_credits(user_id)
    credits_display = credits if not isinstance(credits, str) else get_translation('unlimited_credits', user_id)

    stats_message = get_translation('stats_message', user_id).format(
        credits_display=credits_display,
        approved=user_stats.get('approved', 0),
        declined=user_stats.get('declined', 0),
        ccn=user_stats.get('ccn', 0),
        cvv=user_stats.get('cvv', 0),
        referral_credits=user_stats.get('referral_credits', 0)
    )
    enhanced_stats_message = f"""
📊 <b>{get_translation('stats_header_your_stats', user_id)}</b> 📊\n\n
💰 <b>{get_translation('stats_message_credits', user_id)}:</b> <code>{credits_display}</code>\n
✅ <b>{get_translation('stats_message_approved', user_id)}:</b> <code>{user_stats.get('approved', 0)}</code>\n
❌ <b>{get_translation('stats_message_declined', user_id)}:</b> <code>{user_stats.get('declined', 0)}</code>\n
⚠️ <b>{get_translation('stats_message_ccn', user_id)}:</b> <code>{user_stats.get('ccn', 0)}</code>\n
✅ <b>{get_translation('stats_message_cvv', user_id)}:</b> <code>{user_stats.get('cvv', 0)}</code>\n
🎁 <b>{get_translation('stats_message_referral_credits', user_id)}:</b> <code>{user_stats.get('referral_credits', 0)}</code>
"""
    bot.reply_to(message, apply_theme(enhanced_stats_message, get_user_theme(user_id)), parse_mode="HTML")

@bot.message_handler(commands=['credits'])
def credits_command(message): # (credits_command function - same as before) ...
    if not ensure_registered(message): return
    user_id = message.chat.id

    credits = get_user_credits(user_id)
    credits_display = credits if not isinstance(credits, str) else get_translation('unlimited_credits', user_id)
    credits_message = get_translation('credits_message', user_id).format(credits_display=credits_display)
    enhanced_credits_message = f"""
💰 <b>{get_translation('credits_header_your_credits', user_id)}</b>\n\n
{get_translation('credits_message_you_have', user_id)}: <code>{credits_display}</code>
"""
    bot.reply_to(message, apply_theme(enhanced_credits_message, get_user_theme(user_id)), parse_mode="HTML")

@bot.message_handler(commands=['redeem'])
def redeem_command(message): # (redeem_command function - same as before) ...
    if not ensure_registered(message): return
    user_id = message.chat.id

    try:
        code = message.text.split()[1]
    except IndexError:
        bot.reply_to(message, apply_theme(get_translation('redeem_usage_error_message', user_id), get_user_theme(user_id)), parse_mode="HTML")
        return

    if not re.match(r"^[a-zA-Z0-9]{4}-[a-zA-Z0-9]{4}-[a-zA-Z0-9]{4}$", code):
        bot.reply_to(message, apply_theme(get_translation('redeem_invalid_format_message', user_id), get_user_theme(user_id)), parse_mode="HTML")
        return

    redeem_result = redeem_credits(user_id, code)
    if redeem_result == "success":
        user_data = _load_user_data()
        is_premium_user = user_data.get(str(user_id), {}).get('is_premium', False)
        premium_message_part = get_translation('redeem_premium_message_part', user_id) if is_premium_user else ""
        redeem_success_message = get_translation('redeem_success_message', user_id).format(premium_message_part=premium_message_part)
        enhanced_redeem_message = f"""
✅ <b>{get_translation('redeem_header_success', user_id)}</b> {get_translation('emoji_success', user_id)}\n\n
🎁 {get_translation('redeem_message_code_redeemed', user_id)}{premium_message_part}
"""
        bot.reply_to(message, apply_theme(enhanced_redeem_message, get_user_theme(user_id)), parse_mode="HTML")
    elif redeem_result == "invalid":
        enhanced_redeem_message = f"""
❌ <b>{get_translation('redeem_header_invalid', user_id)}</b> {get_translation('emoji_warning', user_id)}\n\n
{get_translation('redeem_message_invalid_code', user_id)}
"""
        bot.reply_to(message, apply_theme(enhanced_redeem_message, get_user_theme(user_id)), parse_mode="HTML")
    elif redeem_result == "used":
        enhanced_redeem_message = f"""
⚠️ <b>{get_translation('redeem_header_used', user_id)}</b> {get_translation('emoji_warning', user_id)}\n\n
{get_translation('redeem_message_code_used', user_id)}
"""
        bot.reply_to(message, apply_theme(enhanced_redeem_message, get_user_theme(user_id)), parse_mode="HTML")
    else:
        enhanced_redeem_message = f"""
❌ <b>{get_translation('redeem_header_error', user_id)}</b> {get_translation('emoji_error', user_id)}\n\n
{get_translation('redeem_message_redeem_error', user_id)}
"""
        bot.reply_to(message, apply_theme(enhanced_redeem_message, get_user_theme(user_id)), parse_mode="HTML")

@bot.message_handler(commands=['code'])
def code_command(message): # (code_command function - same as before) ...
    if not ensure_registered(message): return
    user_id = message.chat.id
    if not is_admin(user_id):
        bot.reply_to(message, apply_theme(get_translation('admin_command_only', user_id), get_user_theme(user_id)), parse_mode="HTML")

    try:
        args = message.text.split()
        if len(args) < 2:
            raise ValueError("Amount not specified")
        amount_str = args[1]
        if amount_str.lower() == 'premium':
            amount = 0
            is_premium_code = True
        else:
            amount = int(amount_str)
            is_premium_code = False

        num_codes = 1
        codes = generate_redeem_codes(amount, num_codes, code_format="xxxx-xxxx-xxxx", premium=is_premium_code)
        code_list = "\n".join(codes)
        premium_note = get_translation('code_premium_note', user_id) if is_premium_code else get_translation('code_credits_note', user_id).format(amount=amount)

        code_generated_message = get_translation('code_generated_message', user_id).format(code_list=code_list, premium_note=premium_note)
        enhanced_code_generated_message = f"""
✅ <b>{get_translation('code_header_generated', user_id)}</b> {get_translation('emoji_success', user_id)}\n\n
🎫 <b>{get_translation('code_message_redeem_code', user_id)}:</b>\n<code>{code_list}</code>\n\n
{premium_note}\n\n
{get_translation('code_message_share_code', user_id)}
"""
        bot.reply_to(message, apply_theme(enhanced_code_generated_message, get_user_theme(user_id)), parse_mode="HTML")

    except (ValueError, IndexError):
        bot.reply_to(message, apply_theme(get_translation('code_usage_error_message', user_id), get_user_theme(user_id)), parse_mode="HTML")
    except Exception as e:
        logging.error(f"Error generating redeem code: {e}")
        bot.reply_to(message, apply_theme(get_translation('code_generation_error_message', user_id), get_user_theme(user_id)), parse_mode="HTML")

@bot.message_handler(commands=['gen'])
def gen_command(message): # (gen_command function - same as before) ...
    if not ensure_registered(message): return
    user_id = message.chat.id

    try:
        data_type = message.text.split()[1].lower()
    except IndexError:
        bot.reply_to(message, apply_theme(get_translation('gen_usage_error_message', user_id), get_user_theme(user_id)), parse_mode="HTML")
        return

    if data_type == 'email':
        email = generate_random_email()
        enhanced_gen_email_message = f"""
📧 <b>{get_translation('gen_header_email', user_id)}</b>\n\n
{get_translation('gen_message_generated_email', user_id)}: <code>{email}</code>
"""
        bot.reply_to(message, apply_theme(enhanced_gen_email_message, get_user_theme(user_id)), parse_mode="HTML")
    elif data_type == 'username':
        username = generate_username()
        enhanced_gen_username_message = f"""
👤 <b>{get_translation('gen_header_username', user_id)}</b>\n\n
{get_translation('gen_message_generated_username', user_id)}: <code>{username}</code>
"""
        bot.reply_to(message, apply_theme(enhanced_gen_username_message, get_user_theme(user_id)), parse_mode="HTML")
    elif data_type == 'password':
        password = generate_password()
        enhanced_gen_password_message = f"""
🔑 <b>{get_translation('gen_header_password', user_id)}</b>\n\n
{get_translation('gen_message_generated_password', user_id)}: <code>{password}</code>
"""
        bot.reply_to(message, apply_theme(enhanced_gen_password_message, get_user_theme(user_id)), parse_mode="HTML")
    elif data_type == 'address':
        address = generate_address()
        enhanced_gen_address_message = f"""
🏠 <b>{get_translation('gen_header_address', user_id)}</b>\n\n
{get_translation('gen_message_generated_address', user_id)}: <code>{address}</code>
"""
        bot.reply_to(message, apply_theme(enhanced_gen_address_message, get_user_theme(user_id)), parse_mode="HTML")
    elif data_type == 'phone':
        phone_number = generate_phone_number()
        enhanced_gen_phone_message = f"""
📞 <b>{get_translation('gen_header_phone', user_id)}</b>\n\n
{get_translation('gen_message_generated_phone', user_id)}: <code>{phone_number}</code>
"""
        bot.reply_to(message, apply_theme(enhanced_gen_phone_message, get_user_theme(user_id)), parse_mode="HTML")
    elif data_type == 'cc':
        cc_number = generate_credit_card_number()
        enhanced_gen_cc_message = f"""
💳 <b>{get_translation('gen_header_cc', user_id)}</b>\n\n
{get_translation('gen_message_generated_cc', user_id)}: <code>{cc_number}</code> {get_translation('gen_cc_note', user_id)}
"""
        bot.reply_to(message, apply_theme(enhanced_gen_cc_message, get_user_theme(user_id)), parse_mode="HTML")
    else:
        bot.reply_to(message, apply_theme(get_translation('gen_invalid_type_message', user_id), get_user_theme(user_id)), parse_mode="HTML")

@bot.message_handler(commands=['bin', '.bin', 'binlookup'])
def bin_lookup_command(message): # (bin_lookup_command function - same as before) ...
    if not ensure_registered(message): return
    user_id = message.chat.id

    try:
        bin_number = message.text.split(maxsplit=1)[1].strip()
        if not re.match(r'^\d{6,8}$', bin_number):
            bot.reply_to(message, apply_theme(get_translation('bin_invalid_format_message', user_id), get_user_theme(user_id)), parse_mode="HTML")
            return

        ko_msg = bot.reply_to(message, apply_theme(get_translation('bin_lookup_processing_message', user_id), get_user_theme(user_id))).message_id

        try:
            import requests
            data = requests.get(f'https://bins.antipublic.cc/bins/{bin_number}').json()
            if not data:
                bot.edit_message_text(chat_id=message.chat.id, message_id=ko_msg, text=apply_theme(get_translation('bin_not_found_message', user_id), get_user_theme(user_id)))
                return

            bin_info_text_base = get_translation('bin_info_message_base', user_id)
            bin_info_text = bin_info_text_base.format(
                bin_number=bin_number,
                brand=data.get('brand', get_translation('unknown', user_id)),
                card_type=data.get('type', get_translation('unknown', user_id)),
                card_level=data.get('level', get_translation('unknown', user_id)),
                bank=data.get('bank', get_translation('unknown', user_id)),
                country=data.get('country_name', get_translation('unknown', user_id)),
                country_flag=data.get('country_flag', get_translation('unknown', user_id)),
                iso=data.get('country_iso', get_translation('unknown', user_id))
            )
            enhanced_bin_info_text = f"""
🔎 <b>{get_translation('bin_header_lookup', user_id)}</b>\n
<a href='https://t.me/+GdWapjhiAG05OTk1'>┏━━━━━━━━━━━⍟</a>
<a href='https://t.me/+GdWapjhiAG05OTk1'>┃</a> <b>{get_translation('bin_message_bin', user_id)}:</b> <code>{bin_number}</code> <a href='https://t.me/+GdWapjhiAG05OTk1'>┗━━━━━━━⊛</a>\n
<a href='https://t.me/+GdWapjhiAG05OTk1'>-</a> <b>{get_translation('bin_message_brand', user_id)}:</b> <code>{data.get('brand', get_translation('unknown', user_id))}</code>\n
<a href='https://t.me/+GdWapjhiAG05OTk1'>-</a> <b>{get_translation('bin_message_type', user_id)}:</b> <code>{data.get('type', get_translation('unknown', user_id))} - {data.get('level', get_translation('unknown', user_id))}</code>\n
<a href='https://t.me/+GdWapjhiAG05OTk1'>-</a> <b>{get_translation('bin_message_bank', user_id)}:</b> <code>{data.get('bank', get_translation('unknown', user_id))}</code>\n
<a href='https://t.me/+GdWapjhiAG05OTk1'>-</a> <b>{get_translation('bin_message_country', user_id)}:</b> <code>{country} - {country_flag}</code>\n
<a href='https://t.me/+GdWapjhiAG05OTk1'>-</a> <b>{get_translation('bin_message_iso', user_id)}:</b> <code>{iso}</code>
"""
            bot.edit_message_text(chat_id=message.chat.id, message_id=ko_msg, text=apply_theme(enhanced_bin_info_text, get_user_theme(user_id)), parse_mode="HTML", disable_web_page_preview=True)

        except requests.exceptions.RequestException as e:
            logging.error(f"BIN lookup request error: {e}")
            bot.edit_message_text(chat_id=message.chat.id, message_id=ko_msg, text=apply_theme(get_translation('bin_lookup_connect_error_message', user_id), get_user_theme(user_id)))
        except Exception as e:
            logging.error(f"Error during BIN lookup: {e}")
            bot.edit_message_text(chat_id=message.chat.id, message_id=ko_msg, text=apply_theme(get_translation('bin_lookup_error_message', user_id), get_user_theme(user_id)))

    except IndexError:
        bot.reply_to(message, apply_theme(get_translation('bin_provide_bin_message', user_id), get_user_theme(user_id)), parse_mode="HTML")

@bot.message_handler(commands=["chk", "check", ".chk", "validate", "驗卡", "card", "cc"])
def check_card_command(message): # (check_card_command function - same as before) ...
    if not ensure_registered(message): return
    user_id = message.chat.id

    if is_rate_limited(user_id):
        rate_limit_message = get_translation('rate_limit_message', user_id).format(rate_limit_time=RATE_LIMIT_TIME)
        return bot.reply_to(message, apply_theme(rate_limit_message, get_user_theme(user_id)), parse_mode="HTML")

    credits = get_user_credits(user_id) # (check_card_command function - credits check - same as before) ...
    if credits != "Unlimited" and credits <= 0:
        insufficient_credits_message = get_translation('insufficient_credits_message', user_id).format(credits=credits)
        return bot.reply_to(message, apply_theme(insufficient_credits_message, get_user_theme(user_id)), parse_mode="HTML")

    if not deduct_credits(user_id): # (check_card_command function - deduct credits - same as before) ...
        deduct_credits_error_message = get_translation('deduct_credits_error_message', user_id)
        return bot.reply_to(message, apply_theme(deduct_credits_error_message, get_user_theme(user_id)))

    try: # (check_card_command function - card checking logic - same as before) ...
        cc_input = message.text.split(maxsplit=1)[1].strip()
        if not re.match(r'\d{13,19}\|\d{1,2}\|\d{2,4}\|\d{3,4}', cc_input):
            invalid_cc_format_message = get_translation('invalid_cc_format_message', user_id)
            return bot.reply_to(message, apply_theme(invalid_cc_format_message, get_user_theme(user_id)))
        cc = cc_input
        cc_masked = cc[:6] + "xxxxxx" + cc[-4:]
        session = manage_session_file()
        if not session:
            session_error_message = get_translation('session_error_message', user_id)
            return bot.reply_to(message, apply_theme(session_error_message, get_user_theme(user_id)))
        ko_msg = bot.reply_to(message, apply_theme(get_translation('checking_card_message', user_id), get_user_theme(user_id))).message_id

        try:
            import requests
            data = requests.get('https://bins.antipublic.cc/bins/' + cc[:6]).json()
        except:
            data = {}
        brand = data.get('brand', get_translation('unknown', user_id))
        card_type = data.get('type', get_translation('unknown', user_id))
        card_level = data.get('level', get_translation('unknown', user_id))
        country = data.get('country_name', get_translation('unknown', user_id))
        country_flag = data.get('country_flag', get_translation('unknown', user_id))
        bank = data.get('bank', get_translation('unknown', user_id))

        start_time = time.time()
        gate_function = get_gate_function_for_user(user_id)
        gate_name_preference = get_user_gate_preference(user_id)
        last = str(gate_function(session, cc.strip()))
        end_time = time.time()
        execution_time = end_time - start_time
        gate_name_display = gate_name_preference.upper().replace("AUTH", "AUTH").replace("STRIPE2", "2$").replace("STRIPE4", "4$")
        update_user_stats(user_id, last.split(" ")[0])
        log_check_details(user_id, cc_masked, gate_name_display, last, "single")

        check_result_message_base = get_translation('check_result_message_base', user_id)
        check_result_message = check_result_message_base.format(
            cc=cc,
            gate_name_display=gate_name_display,
            last=last,
            card_info=f"{cc[:6]}-{card_type} - {brand} - {card_level}",
            country=f"{country} - {country_flag}",
            bank=bank,
            execution_time=f"{execution_time:.1f}"
        )
        enhanced_check_result_message = f"""
<a href='https://envs.sh/smD.webp'>-</a> 💳 <b>{get_translation('check_header_checked_card', user_id)}</b>\n
<a href='https://t.me/+GdWapjhiAG05OTk1'>┏━━━━━━━━━━━⍟</a>
<a href='https://t.me/+GdWapjhiAG05OTk1'>┃</a> <b>{get_translation('check_message_cc', user_id)}:</b> <code>{cc}</code> <a href='https://t.me/+GdWapjhiAG05OTk1'>┗━━━━━━━⊛</a>\n
<a href='https://t.me/+GdWapjhiAG05OTk1'>-</a> 𝐆𝐚𝐭𝐞𝐰𝐚𝐲: ⤿ {gate_name_display} 🟢 ⤾\n
<a href='https://t.me/+GdWapjhiAG05OTk1'>-</a> 𝐑𝐞𝐬𝐩𝐨𝐧𝐬𝐞: ⤿ {last} ⤾\n\n
<a href='https://envs.sh/smD.webp'>-</a> ℹ️ <b>{get_translation('check_message_info', user_id)}:</b> <code>{card_info}</code>\n
<a href='https://t.me/+GdWapjhiAG05OTk1'>-</a> 🏳️‍🌈 <b>{get_translation('check_message_country', user_id)}:</b> <code>{country} - {country_flag}</code>\n
<a href='https://t.me/+GdWapjhiAG05OTk1'>-</a> 🏦 <b>{get_translation('check_message_bank', user_id)}:</b> <code>{bank}</code>\n\n
<a href='https://t.me/+GdWapjhiAG05OTk1'>-</a> ⏱️ <b>{get_translation('check_message_time', user_id)}:</b> <code>{execution_time}</code> {get_translation('check_message_seconds_unit', user_id)}\n
<a href='https://t.me/+GdWapjhiAG05OTk1'>-</a> 🤖 <b>{get_translation('check_message_bot_about', user_id)}:</b> <a href='https://t.me/+GdWapjhiAG05OTk1'>Crimson </a>
"""
        bot.edit_message_text(chat_id=message.chat.id, message_id=ko_msg, text=apply_theme(enhanced_check_result_message, get_user_theme(user_id)), parse_mode="HTML", disable_web_page_preview=True,
                             reply_markup=build_quick_gate_markup(cc, user_id))

        credits_remaining_message = get_translation('credits_remaining_message', user_id).format(credits=get_user_credits(user_id))
        bot.send_message(chat_id=message.chat.id, text=apply_theme(credits_remaining_message, get_user_theme(user_id)), parse_mode="HTML")

    except IndexError:
        return bot.reply_to(message, apply_theme(get_translation('provide_cc_details_message', user_id), get_user_theme(user_id)), parse_mode="HTML")
    except Exception as e:
        logging.error(f"Error in single card check: {e}")
        return bot.reply_to(message, apply_theme(get_translation('check_error_message', user_id), get_user_theme(user_id)), parse_mode="HTML")

@bot.callback_query_handler(func=lambda call: call.data.startswith('reqchk_gate:'))
def quick_check_gate_callback(call): # (quick_check_gate_callback function - same as before) ...
    user_id = call.message.chat.id

    gate_name = call.data.split(':')[1].split('|')[0]
    cc = call.data.split('cc:')[1]

    if is_rate_limited(user_id):
        return bot.answer_callback_query(call.id, text=get_translation('rate_limit_callback_answer', user_id))

    credits = get_user_credits(user_id) # (quick_check_gate_callback function - credits check - same as before) ...
    if credits != "Unlimited" and credits <= 0:
        return bot.answer_callback_query(call.id, text=get_translation('insufficient_credits_callback_answer', user_id))

    if not deduct_credits(user_id): # (quick_check_gate_callback function - deduct credits - same as before) ...
        return bot.answer_callback_query(call.id, text=get_translation('deduct_credits_callback_answer', user_id))

    session = manage_session_file() # (quick_check_gate_callback function - session - same as before) ...
    if not session:
        return bot.answer_callback_query(call.id, text=get_translation('session_error_callback_answer', user_id))

    gate_function = get_gate_function_for_user(user_id) # (quick_check_gate_callback function - card check logic - same as before) ...
    start_time = time.time()
    last = str(gate_function(session, cc.strip()))
    end_time = time.time()
    execution_time = end_time - start_time
    update_user_stats(user_id, last.split(" ")[0])
    gate_name_display = gate_name.upper().replace("AUTH", "AUTH").replace("STRIPE2", "2$").replace("STRIPE4", "4$")
    cc_masked = cc[:6] + "xxxxxx" + cc[-4:]
    log_check_details(user_id, cc_masked, gate_name_display, last, "quick_check")

    quick_check_result_message = get_translation('quick_check_result_message', user_id).format(
        gate_name_display=gate_name_display,
        last=last,
        execution_time=f"{execution_time:.1f}"
    )
    enhanced_quick_check_result_message = f"""
✅ <b>{get_translation('quick_check_header_result', user_id)}</b> {get_translation('emoji_check_mark_button', user_id)}\n\n
{get_translation('quick_check_message_gateway_used', user_id)}: <code>{gate_name_display}</code>\n
{get_translation('quick_check_message_response_is', user_id)}: <code>{last}</code>\n\n
⏱️ <b>{get_translation('check_message_time', user_id)}:</b> <code>{execution_time:.1f}</code> {get_translation('check_message_seconds_unit', user_id)}
"""
    bot.answer_callback_query(call.id, get_translation('check_processing_callback_answer', user_id))
    bot.edit_message_text(chat_id=user_id, message_id=call.message.message_id, text=apply_theme(enhanced_quick_check_result_message, get_user_theme(user_id)), parse_mode="HTML", reply_markup=build_quick_gate_markup(cc, user_id))

@bot.message_handler(commands=['note'])
def note_command(message): # (note_command function - same as before) ...
    if not ensure_registered(message): return
    user_id = message.chat.id

    try:
        args = message.text.split(maxsplit=2)
        if len(args) < 3:
            raise ValueError("Insufficient arguments")
        cc_to_note = args[1].strip()
        note_text = args[2].strip()

        global user_notes
        if str(user_id) not in user_notes:
            user_notes[str(user_id)] = {}
        user_notes[str(user_id)][cc_to_note] = note_text
        save_user_notes(user_notes)

        note_added_message = get_translation('note_added_message', user_id).format(cc_to_note=cc_to_note)
        enhanced_note_added_message = f"""
✅ 📝 <b>{get_translation('note_header_added', user_id)}</b> {get_translation('emoji_success', user_id)}\n\n
{get_translation('note_message_note_added_to_cc', user_id)}: <code>{cc_to_note}</code>
"""
        bot.reply_to(message, apply_theme(enhanced_note_added_message, get_user_theme(user_id)), parse_mode="HTML")

    except ValueError:
        bot.reply_to(message, apply_theme(get_translation('note_usage_error_message', user_id), get_user_theme(user_id)), parse_mode="HTML")
    except Exception as e:
        logging.error(f"Error adding note: {e}")
        bot.reply_to(message, apply_theme(get_translation('note_add_error_message', user_id), get_user_theme(user_id)), parse_mode="HTML")

@bot.message_handler(commands=['getnote'])
def getnote_command(message): # (getnote_command function - same as before) ...
    if not ensure_registered(message): return
    user_id = message.chat.id

    try:
        cc_to_get_note = message.text.split(maxsplit=1)[1].strip()

        note = user_notes.get(str(user_id), {}).get(cc_to_get_note)

        if note:
            note_found_message = get_translation('note_found_message', user_id).format(cc_to_get_note=cc_to_get_note, note=note)
            enhanced_note_found_message = f"""
📝 <b>{get_translation('getnote_header_note_for_cc', user_id)}</b> <code>{cc_to_get_note}</code>:\n\n
<code>{note}</code>
"""
            bot.reply_to(message, apply_theme(enhanced_note_found_message, get_user_theme(user_id)), parse_mode="HTML")
        else:
            note_not_found_message = get_translation('note_not_found_message', user_id).format(cc_to_get_note=cc_to_get_note)
            enhanced_note_not_found_message = f"""
ℹ️ 📝 <b>{get_translation('getnote_header_no_note', user_id)}</b> {get_translation('emoji_info', user_id)}\n\n
{get_translation('getnote_message_no_note_found', user_id)}: <code>{cc_to_get_note}</code>
"""
            bot.reply_to(message, apply_theme(enhanced_note_not_found_message, get_user_theme(user_id)), parse_mode="HTML")

    except IndexError:
        bot.reply_to(message, apply_theme(get_translation('getnote_usage_error_message', user_id), get_user_theme(user_id)), parse_mode="HTML")
    except Exception as e:
        logging.error(f"Error getting note: {e}")
        bot.reply_to(message, apply_theme(get_translation('note_get_error_message', user_id), get_user_theme(user_id)), parse_mode="HTML")

@bot.message_handler(commands=['delnote'])
def delnote_command(message): # (delnote_command function - same as before) ...
    if not ensure_registered(message): return
    user_id = message.chat.id

    try:
        cc_to_delete_note = message.text.split(maxsplit=1)[1].strip()

        global user_notes
        if str(user_id) in user_notes and cc_to_delete_note in user_notes[str(user_id)]:
            del user_notes[str(user_id)][cc_to_delete_note]
            save_user_notes(user_notes)
            note_deleted_message = get_translation('note_deleted_message', user_id).format(cc_to_delete_note=cc_to_delete_note)
            enhanced_note_deleted_message = f"""
✅ 📝 <b>{get_translation('delnote_header_deleted', user_id)}</b> {get_translation('emoji_success', user_id)}\n\n
{get_translation('delnote_message_note_deleted_for_cc', user_id)}: <code>{cc_to_delete_note}</code>
"""
            bot.reply_to(message, apply_theme(enhanced_note_deleted_message, get_user_theme(user_id)), parse_mode="HTML")
        else:
            note_delete_not_found_message = get_translation('note_delete_not_found_message', user_id).format(cc_to_delete_note=cc_to_delete_note)
            enhanced_note_not_found_message = f"""
ℹ️ 📝 <b>{get_translation('delnote_header_no_note', user_id)}</b> {get_translation('emoji_info', user_id)}\n\n
{get_translation('delnote_message_no_note_found', user_id)}: <code>{cc_to_delete_note}</code>
"""
            bot.reply_to(message, apply_theme(enhanced_note_not_found_message, get_user_theme(user_id)), parse_mode="HTML")

    except IndexError:
        bot.reply_to(message, apply_theme(get_translation('delnote_usage_error_message', user_id), get_user_theme(user_id)), parse_mode="HTML")
    except Exception as e:
        logging.error(f"Error deleting note: {e}")
        bot.reply_to(message, apply_theme(get_translation('note_delete_error_message', user_id), get_user_theme(user_id)), parse_mode="HTML")

@bot.message_handler(commands=['transfer'])
def transfer_credits_command(message): # (transfer_credits_command function - same as before) ...
    if not ensure_registered(message): return
    user_id = message.chat.id

    try:
        args = message.text.split()
        if len(args) != 3:
            raise ValueError("Invalid number of arguments")

        recipient_identifier = args[1].strip()
        credits_to_transfer = int(args[2])

        if credits_to_transfer <= 0:
            raise ValueError("Credits to transfer must be positive")

        sender_credits = get_user_credits(user_id)
        if sender_credits != "Unlimited" and sender_credits < credits_to_transfer:
            insufficient_transfer_credits_message = get_translation('insufficient_transfer_credits_message', user_id).format(sender_credits=sender_credits)
            enhanced_transfer_insufficient_credits_message = f"""
🚫 💰 <b>{get_translation('transfer_header_insufficient_credits', user_id)}</b> {get_translation('emoji_warning', user_id)}\n\n
{get_translation('transfer_message_insufficient_credits', user_id)}: <code>{sender_credits}</code> {get_translation('credits_unit', user_id)}
"""
            return bot.reply_to(message, apply_theme(enhanced_transfer_insufficient_credits_message, get_user_theme(user_id)), parse_mode="HTML")

        recipient_user_id = None # (transfer_credits_command function - recipient lookup - same as before) ...
        if recipient_identifier.startswith('@'):
            recipient_username = recipient_identifier[1:]
            recipient_user_id = get_user_id_from_username(recipient_username)
            if not recipient_user_id:
                user_not_found_message = get_translation('user_not_found_message', user_id).format(recipient_identifier=recipient_identifier)
                enhanced_transfer_user_not_found_message = f"""
❌ 👤 <b>{get_translation('transfer_header_user_not_found', user_id)}</b> {get_translation('emoji_error', user_id)}\n\n
{get_translation('transfer_message_user_not_found', user_id)}: <code>{recipient_identifier}</code>
"""
                return bot.reply_to(message, apply_theme(enhanced_transfer_user_not_found_message, get_user_theme(user_id)), parse_mode="HTML")
        elif recipient_identifier.isdigit():
            recipient_user_id = int(recipient_identifier)
            if not is_registered(recipient_user_id):
                user_not_registered_message = get_translation('user_not_registered_message', user_id).format(recipient_identifier=recipient_identifier)
                enhanced_transfer_user_not_registered_message = f"""
❌ 👤 <b>{get_translation('transfer_header_user_not_registered', user_id)}</b> {get_translation('emoji_error', user_id)}\n\n
{get_translation('transfer_message_user_not_registered', user_id)}: <code>{recipient_identifier}</code>
"""
                return bot.reply_to(message, apply_theme(enhanced_transfer_user_not_registered_message, get_user_theme(user_id)), parse_mode="HTML")
        else:
            raise ValueError("Invalid recipient identifier")

        if user_id == recipient_user_id: # (transfer_credits_command function - self transfer error - same as before) ...
            transfer_self_error_message = get_translation('transfer_self_error_message', user_id)
            enhanced_transfer_self_error_message = f"""
❌ ♻️ <b>{get_translation('transfer_header_self_transfer', user_id)}</b> {get_translation('emoji_error', user_id)}\n\n
{get_translation('transfer_message_self_transfer_error', user_id)}
"""
            return bot.reply_to(message, apply_theme(enhanced_transfer_self_error_message, get_user_theme(user_id)), parse_mode="HTML")

        if deduct_credits(user_id, credits=credits_to_transfer): # (transfer_credits_command function - transfer success - same as before) ...
            add_credits_to_user(recipient_user_id, credits_to_transfer)
            transfer_success_message = get_translation('transfer_success_message', user_id).format(credits_to_transfer=credits_to_transfer, recipient_identifier=recipient_identifier)
            enhanced_transfer_success_message = f"""
✅ 💰 <b>{get_translation('transfer_header_success', user_id)}</b> {get_translation('emoji_success', user_id)}\n\n
{get_translation('transfer_message_credits_transferred', user_id).format(credits_to_transfer=credits_to_transfer, recipient_identifier=recipient_identifier)}
"""
            bot.reply_to(message, apply_theme(enhanced_transfer_success_message, get_user_theme(user_id)), parse_mode="HTML")
            try: # (transfer_credits_command function - recipient notification - same as before) ...
                sender_name = message.from_user.first_name or str(user_id)
                transfer_received_notification = get_translation('transfer_received_notification', recipient_user_id).format(credits_to_transfer=credits_to_transfer, sender_name=sender_name)
                bot.send_message(recipient_user_id, apply_theme(transfer_received_notification, get_user_theme(recipient_user_id)), parse_mode="HTML")
            except Exception as e:
                logging.error(f"Error sending credit transfer notification to recipient {recipient_user_id}: {e}")
        else: # (transfer_credits_command function - general error - same as before) ...
            transfer_error_message = get_translation('transfer_error_message', user_id)
            enhanced_transfer_error_message = f"""
❌ 💰 <b>{get_translation('transfer_header_general_error', user_id)}</b> {get_translation('emoji_error', user_id)}\n\n
{get_translation('transfer_message_general_error', user_id)}
"""
            bot.reply_to(message, apply_theme(enhanced_transfer_error_message, get_user_theme(user_id)), parse_mode="HTML")

    except ValueError as e: # (transfer_credits_command function - value error - same as before) ...
        bot.reply_to(message, apply_theme(get_translation('transfer_usage_error_message', user_id).format(error=e), get_user_theme(user_id)), parse_mode="HTML")
    except Exception as e: # (transfer_credits_command function - exception error - same as before) ...
        logging.error(f"Error processing credit transfer: {e}")
        bot.reply_to(message, apply_theme(get_translation('transfer_processing_error_message', user_id), get_user_theme(user_id)), parse_mode="HTML")

@bot.message_handler(content_types=["document"])
def main(message): # (main function - same as before) ...
    if not ensure_registered(message): return
    user_id = message.chat.id

    if is_rate_limited(user_id):
        rate_limit_message = get_translation('rate_limit_message', user_id).format(rate_limit_time=RATE_LIMIT_TIME)
        return bot.reply_to(message, apply_theme(rate_limit_message, get_user_theme(user_id)), parse_mode="HTML")

    credits = get_user_credits(user_id) # (main function - credits check - same as before) ...
    if credits != "Unlimited" and credits <= 0:
        insufficient_credits_message = get_translation('insufficient_credits_message', user_id).format(credits=credits)
        return bot.reply_to(message, apply_theme(insufficient_credits_message, get_user_theme(user_id)), parse_mode="HTML")

    dd = 0 # (main function - bulk check logic - same as before) ...
    live = 0
    incorrect = 0
    ch = 0
    checked_count = 0
    ko = bot.reply_to(message, apply_theme(get_translation('bulk_check_processing_message', user_id), get_user_theme(user_id))).message_id
    ccs_results = []

    try: # (main function - file download - same as before) ...
        ee = bot.download_file(bot.get_file(message.document.file_id).file_path).decode('utf-8')
    except Exception as e:
        bot.edit_message_text(chat_id=message.chat.id, message_id=ko, text=apply_theme(get_translation('bulk_file_download_error_message', user_id), get_user_theme(user_id)))
        return

    ccs_to_check = extract_ccs_from_line(ee) # (main function - CC extraction - same as before) ...
    total = 0

    session = manage_session_file() # (main function - session and gate - same as before) ...
    if not session:
        session_error_message = get_translation('session_error_message', user_id)
        return bot.reply_to(message, apply_theme(session_error_message, get_user_theme(user_id)))
    gate_function = get_gate_function_for_user(user_id)
    gate_name_preference = get_user_gate_preference(user_id)
    gate_name_display = gate_name_preference.upper().replace("AUTH", "AUTH").replace("STRIPE2", "2$").replace("STRIPE4", "4$")

    for cc in ccs_to_check: # (main function - card loop - same as before) ...
        if handle_stop_signal(message.chat.id, ko):
            return

        if credits != "Unlimited": # (main function - credits deduction - same as before) ...
            if not deduct_credits(user_id):
                credits_exhausted_bulk_message = get_translation('credits_exhausted_bulk_message', user_id).format(checked_count=checked_count, credits=get_user_credits(user_id))
                bot.edit_message_text(chat_id=message.chat.id, message_id=ko, text=apply_theme(credits_exhausted_bulk_message, get_user_theme(user_id)), parse_mode="HTML")
                return

        total += 1 # (main function - card check - same as before) ...
        checked_count += 1
        cc_masked = cc[:6] + "xxxxxx" + cc[-4:]

        try:
            import requests
            data = requests.get('https://bins.antipublic.cc/bins/' + cc[:6]).json()
        except:
            data = {}
        brand = data.get('brand', get_translation('unknown', user_id))
        card_type = data.get('type', get_translation('unknown', user_id))
        country = data.get('country_name', get_translation('unknown', user_id))
        country_flag = data.get('country_flag', get_translation('unknown', user_id))
        bank = data.get('bank', get_translation('unknown', user_id))

        start_time = time.time()
        last = str(gate_function(session, cc.strip()))
        update_user_stats(user_id, last.split(" ")[0])
        log_check_details(user_id, cc_masked, gate_name_display, last, "bulk")

        mes = types.InlineKeyboardMarkup(row_width=1) # (main function - inline keyboard - same as before) ...
        cm1 = types.InlineKeyboardButton(f"• {cc} •", callback_data='u8')
        status = types.InlineKeyboardButton(f"• 𝐒𝐓𝐀𝐓𝐔𝐒  : {last} ", callback_data='u8')
        cm3 = types.InlineKeyboardButton(f"• 𝐀𝐏𝐏𝐑𝐎𝐕𝐄𝐃 ✅ : [ {live} ] •", callback_data='x')
        cm4 = types.InlineKeyboardButton(f"• 𝐅𝐀𝐊𝐄 𝐂𝐀𝐑𝐃 ⚠️ : [ {incorrect} ] •", callback_data='x')
        cm5 = types.InlineKeyboardButton(f"• 𝐃𝐄𝐂𝐋𝐈𝐍𝐄𝐃 ❌ : [ {dd} ] •", callback_data='x')
        cm6 = types.InlineKeyboardButton(f"• 𝐓𝐎𝐓𝐀𝐋 🎉       :  [ {total} ] •", callback_data='x')
        stop = types.InlineKeyboardButton(f"[ 𝐒𝐓𝐎𝐏 🚫 ]", callback_data='stop')
        mes.add(cm1, status, cm3, cm4, cm5, cm6, stop)
        end_time = time.time()
        execution_time = end_time - start_time
        bot.edit_message_text(chat_id=message.chat.id, message_id=ko, text=apply_theme(get_translation('bulk_wait_message', user_id), get_user_theme(user_id)), reply_markup=mes, parse_mode="HTML", disable_web_page_preview=True)

        bulk_check_card_result_message_base = get_translation('bulk_check_card_result_message_base', user_id) # (main function - output message - same as before) ...
        msg_output = bulk_check_card_result_message_base.format(
            cc=cc,
            gate_name_display=gate_name_display,
            last=last,
            card_info=f"{cc[:6]}-{card_type} - {brand}",
            country=f"{country} - {country_flag}",
            bank=bank,
            execution_time=f"{execution_time:.1f}"
        )

        result_type = "" # (main function - result type handling - same as before) ...
        if 'APPROVED ✅' in last or 'CVV ✅' in last:
            live += 1
            result_type = "✅ Approved"
            bot.reply_to(message, apply_theme(msg_output, get_user_theme(user_id)), parse_mode="HTML", disable_web_page_preview=True)
        elif 'CCN ✅' in last:
            incorrect+=1
            result_type = "⚠️ CCN"
        elif 'DECLINED ❌' in last or 'EXPIRED ❌' in last or 'Error' in last:
            dd += 1
            result_type = "❌ Declined"
        else:
            result_type = "❓ Unknown"

        ccs_results.append((cc, result_type, last))
        time.sleep(1)

    bulk_summary_text_base = get_translation('bulk_summary_message_base', user_id) # (main function - summary message - same as before) ...
    bulk_summary_text = bulk_summary_text_base.format(
        total=total,
        live=live,
        incorrect=incorrect,
        dd=dd,
        credits=get_user_credits(user_id)
    )
    bot.send_message(chat_id=message.chat.id, text=apply_theme(bulk_summary_text, get_user_theme(user_id)), parse_mode="HTML")

    try: # (main function - completion message - same as before) ...
        bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=ko,
            text=apply_theme(get_translation('bulk_check_completed_message', user_id), get_user_theme(user_id)), parse_mode="HTML", disable_web_page_preview=True
        )
    except Exception as e:
        logging.error(f"Error editing completion message: {e}")

@bot.callback_query_handler(func=lambda call: call.data == 'stop')
def stop_callback(call): # (stop_callback function - same as before) ...
    user_id = call.message.chat.id
    file_path = os.path.join(os.getcwd(), 'stop.stop')
    open(file_path, 'a').close()
    bot.answer_callback_query(call.id, get_translation('stopping_process_callback_answer', call.message.chat.id))

@bot.inline_handler(lambda query: query.query.startswith('/chk '))
def inline_check_query(inline_query): # (inline_check_query function - same as before) ...
    query_text = inline_query.query[len('/chk '):].strip()
    user_id = inline_query.from_user.id


    if is_rate_limited(user_id): # (inline_check_query function - rate limit - same as before) ...
        results = [types.InlineQueryResultArticle('2', get_translation('inline_rate_limited_title', user_id), types.InputTextMessageContent(get_translation('rate_limit_message', user_id).format(rate_limit_time=RATE_LIMIT_TIME), parse_mode="HTML"))]
        bot.answer_inline_query(inline_query.id, results)
        return

    credits = get_user_credits(user_id) # (inline_check_query function - credits check - same as before) ...
    if credits != "Unlimited" and credits <= 0:
        results = [types.InlineQueryResultArticle('3', get_translation('inline_insufficient_credits_title', user_id), types.InputTextMessageContent(get_translation('insufficient_credits_message', user_id).format(credits=credits), parse_mode="HTML"))]
        bot.answer_inline_query(inline_query.id, results)
        return

    if not re.match(r'\d{13,19}\|\d{1,2}\|\d{2,4}\|\d{3,4}', query_text): # (inline_check_query function - format check - same as before) ...
        results = [types.InlineQueryResultArticle('4', get_translation('inline_invalid_cc_format_title', user_id), types.InputTextMessageContent(get_translation('invalid_cc_format_message', user_id), parse_mode="HTML"))]
        bot.answer_inline_query(inline_query.id, results)
        return

    if not deduct_credits(user_id): # (inline_check_query function - deduct credits - same as before) ...
        results = [types.InlineQueryResultArticle('5', get_translation('inline_deduct_credits_error_title', user_id), types.InputTextMessageContent(get_translation('deduct_credits_error_message', user_id), parse_mode="HTML"))]
        bot.answer_inline_query(inline_query.id, results)
        return

    session = manage_session_file() # (inline_check_query function - session - same as before) ...
    if not session:
        results = [types.InlineQueryResultArticle('6', get_translation('inline_session_error_title', user_id), types.InputTextMessageContent(get_translation('session_error_message', user_id), parse_mode="HTML"))]
        bot.answer_inline_query(inline_query.id, results)
        return

    gate_function = get_gate_function_for_user(user_id) # (inline_check_query function - card check logic - same as before) ...
    last = str(gate_function(session, query_text.strip()))
    update_user_stats(user_id, last.split(" ")[0])
    gate_name_preference = get_user_gate_preference(user_id)
    gate_name_display = gate_name_preference.upper().replace("AUTH", "AUTH").replace("STRIPE2", "2$").replace("STRIPE4", "4$")
    cc_masked = query_text[:6] + "xxxxxx" + query_text[-4:]
    log_check_details(user_id, cc_masked, gate_name_display, last, "inline_check")

    inline_check_result_message_base = get_translation('inline_check_result_message_base', user_id) # (inline_check_query function - inline result message - same as before) ...
    inline_check_result_message = inline_check_result_message_base.format(
        last=last,
        gate_name_display=gate_name_display,
        cc=query_text
    )

    results = [types.InlineQueryResultArticle('7', get_translation('inline_check_result_title', user_id), types.InputTextMessageContent(apply_theme(inline_check_result_message, get_user_theme(user_id)), parse_mode="HTML"))]
    bot.answer_inline_query(inline_query.id, results, cache_time=1)

# --- Scheduled Downtime Check Middleware ---
@bot.message_handler(func=lambda message: True, content_types=['text', 'document', 'photo', 'sticker', 'video', 'video_note', 'voice', 'location', 'contact'])
def check_downtime_and_process_message(message): # (check_downtime_and_process_message function - same as before) ...
    is_downtime, downtime_message = check_scheduled_downtime()
    if is_downtime:
        bot.reply_to(message, apply_theme(f"🛠️ <b>Scheduled Downtime</b> 🛠️\n\n{downtime_message}", get_user_theme(message.chat.id)), parse_mode="HTML")
    else:
        bot.process_new_messages([message])

if __name__ == '__main__': # (start polling - same as before) ...
    logop = f'''━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━bot by @CrImSon_WoLf777 started sucessfully ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━'''
    print(logop)
    bot.infinity_polling()
#--- END OF FILE bot_core.py ---