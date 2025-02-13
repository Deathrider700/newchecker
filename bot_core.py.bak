#--- START OF FILE bot_core (3).py ---

# Secret key validation
SECRET_KEY = "@Enrd6051"

user_input = input("Enter the secret key to start the bot: ").strip()

if user_input != SECRET_KEY:
    print("Invalid key. Exiting...")
    exit(1)

print("Key accepted. Starting the bot...")

#--- START OF FILE bot_core.py ---
import telebot
import os
import re
import time
from telebot import types
import json
import uuid
import random
import requests
from datetime import datetime

ENABLE_GROUP_CHECK = True
DETAILED_BIN_INFO = True
DISPLAY_CARD_BRAND = True
REFERRAL_SYSTEM_ENABLED = True
REDEEM_SYSTEM_ENABLED = True
CREDIT_SYSTEM_ENABLED = True
DEFAULT_GATE = "auth" # New default gate setting

ADMIN_COMMAND_LOG_FILE = "admin_logs.txt"
BANNED_USERS = []

from gates.stripe_gates import Tele, Tele_stripe2, Tele_stripe4
from user_management import get_user_credits, deduct_credits, update_user_stats, get_user_gate_preference, set_user_gate_preference, is_admin, get_user_stats, redeem_credits, generate_redeem_codes, is_premium, add_credits_to_user, is_registered, register_user, generate_referral_code, get_referrer_bonus, get_referred_bonus, set_referral_bonuses, get_user_referral_link, add_admin_user, remove_admin_user, get_admin_list
from session_manager import manage_session_file
from utils import extract_ccs_from_line, generate_random_email, generate_username, generate_password, get_card_type_from_bin, generate_address, generate_phone_number, generate_iban, generate_swift, generate_btc_address, generate_usdt_address
from config import BOT_TOKEN, ADMIN_IDS

if not BOT_TOKEN:
    print("CRITICAL ERROR: BOT_TOKEN is not loaded. Bot cannot start.")
    print("Please check config.py and your environment settings.")
    exit(1)

bot = telebot.TeleBot(BOT_TOKEN, parse_mode="HTML")
subscriber = get_admin_list()
BOT_USERNAME = "crimsonxcheckerbot" # Make sure this matches your bot's username, without the '@'
BOT_VERSION = "v3.1 Enhanced Edition" # Updated version

def log_admin_command(user_id, command, args=None):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_message = f"[{timestamp}] Admin ID: {user_id}, Command: {command}"
    if args:
        log_message += f", Args: {args}"
    with open(ADMIN_COMMAND_LOG_FILE, "a") as logfile:
        logfile.write(log_message + "\n")
    print(f"Admin Command Logged: {log_message}")

def handle_stop_signal(chat_id, message_id):
    current_dir = os.getcwd()
    if os.path.exists(os.path.join(current_dir, "stop.stop")):
        try:
            bot.edit_message_text(chat_id=chat_id, message_id=message_id, text='STOPPED ✅\nBOT BY ➜ @CrImSon_WoLf777')
        except Exception as e:
            print(f"Error editing message on stop: {e}")
        try:
            os.remove(os.path.join(current_dir, 'stop.stop'))
        except Exception as e:
            print(f"Error removing stop file: {e}")
        return True
    return False

def get_gate_function_for_user(user_id):
    gate_preference = get_user_gate_preference(user_id)
    if not gate_preference: # Use default gate if no preference is set
        gate_preference = DEFAULT_GATE
    if gate_preference == "stripe2":
        return Tele_stripe2
    elif gate_preference == "stripe4":
        return Tele_stripe4
    else:
        return Tele

def is_private_chat(message):
    return message.chat.type == 'private'

def is_bot_mentioned(bot_username, message):
    if not message.text:
        return False
    if message.chat.type in ['group', 'supergroup']:
        return f'@{bot_username}' in message.text or message.reply_to_message and message.reply_to_message.from_user.username == bot_username
    return True # In private chats, messages are always directed to the bot

def needs_registration_check(message):
    if not message.text:
        return False
    command = message.text.split()[0].lower()
    if command.startswith('/'):
        command_name = command[1:].split('@')[0] # Remove '/' and bot username if present
        no_reg_commands = ['start', 'help', 'register', 'referral', 'buy', 'price', 'menu', 'bin', 'feedback', 'terms', 'privacy', 'ping', 'cmds']
        return command_name not in no_reg_commands
    return True

def _load_user_data():
    try:
        with open('user_data.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError as e:
        print(f"Corrupted user_data.json. Creating backup. Error: {e}")
        # Backup corrupted file
        backup_name = f"user_data_corrupted_{int(time.time())}.json"
        os.rename('user_data.json', backup_name)
        return {}
    except Exception as e:
        print(f"Error loading user_data.json: {e}")
        return {}

def _save_user_data(data):
    try:
        # Write to a temporary file first
        with open('user_data.tmp', 'w') as f:
            json.dump(data, f, indent=4)
        # Replace the original file atomically
        os.replace('user_data.tmp', 'user_data.json')
    except Exception as e:
        print(f"Error saving user_data.json: {e}")


@bot.message_handler(commands=['start', 'help', 'buy', 'price', 'menu', 'cmds'])
def send_welcome(message):
    if not is_private_chat(message): # Modified condition to allow in groups
        if not is_bot_mentioned(BOT_USERNAME, message):
            return

    user_id = message.chat.id
    user_name = message.from_user.first_name or "User"
    credits = get_user_credits(user_id) if CREDIT_SYSTEM_ENABLED else "Unlimited"
    current_gate = get_user_gate_preference(user_id).capitalize() or DEFAULT_GATE.capitalize() # Show default if no preference
    premium_status = "✅ Premium" if is_premium(user_id) else "🆓 Free"
    command = message.text.split()[0].lower()
    if '@' in command:
        command = command.split('@')[0][1:]
    else:
        command = command[1:]


    if command in ['help', 'start', 'menu', 'cmds']:
        help_text = f"""
🌟 <b>Crimson Checker Bot {BOT_VERSION}</b> 🌟

👋 Welcome, <b>{user_name}</b>! ({premium_status} User)
<a href='https://t.me/+GdWapjhiAG05OTk1'>┏━━━━━━━━━━━⍟</a>
<a href='https://t.me/+GdWapjhiAG05OTk1'>┃</a>
A cutting-edge bot for card checking and more!<a href='https://t.me/+GdWapjhiAG05OTk1'>┗━━━━━━━⊛</a>
"""
        if not is_registered(user_id):
            help_text += "🔑 <b>Registration Required!</b>\n   - Use /register to unlock the bot's full potential.\n\n"

        help_text += """
💳 <b>User Commands</b> 💳
<a href='https://t.me/+GdWapjhiAG05OTk1'>┏━━━━━━━━━━━⍟</a>
<a href='https://t.me/+GdWapjhiAG05OTk1'>┃</a>
   •  /chk <code>cc|mm|yy|cvv</code> - Check single card.
   •  /mchk <code>cc|mm|yy|cvv</code> - Bulk check multiple cards.
   •  /gate - Select payment gateway.
   •  /stats - View your checking stats.
   •  /bin <code>bin</code> - Lookup BIN details.
   •  /gen <code>type</code> - Generate data.
   •  /cclookup <code>cc</code> - Get card info (brand, type etc.).
   •  /feedback <code>message</code> - Send feedback.<a href='https://t.me/+GdWapjhiAG05OTk1'>┗━━━━━━━⊛</a>
"""
        if CREDIT_SYSTEM_ENABLED:
            help_text += "   •  /credits - Check your credit balance.\n"
        if REDEEM_SYSTEM_ENABLED:
            help_text += "   •  /redeem <code>code</code> - Redeem credits or premium.\n"
        if REFERRAL_SYSTEM_ENABLED:
            help_text += "   •  /referral - Get your referral link.\n"

        help_text += """
   •  /buy or /price - Credit purchase plans.
   •  /help or /menu or /cmds - Show this menu.

🛠️ <b>Utilities</b> 🛠️
<a href='https://t.me/+GdWapjhiAG05OTk1'>┏━━━━━━━━━━━⍟</a>
<a href='https://t.me/+GdWapjhiAG05OTk1'>┃</a>
   •  /ping - Check bot status.
   •  /terms - View terms of service.
   •  /privacy - View privacy policy.<a href='https://t.me/+GdWapjhiAG05OTk1'>┗━━━━━━━⊛</a>
"""
        if is_admin(user_id):
            help_text += """

⚙️ <b>Admin Commands</b> ⚙️
<a href='https://t.me/+GdWapjhiAG05OTk1'>┏━━━━━━━━━━━⍟</a>
<a href='https://t.me/+GdWapjhiAG05OTk1'>┃</a>
   •  /broadcast <code>message</code> - Send message to all users.
   •  /code <code>amount</code> - Generate redeem code.
   •  /add_credits <code>user_id</code> <code>amount</code> - Add credits.
   •  /setcredits <code>user_id</code> <code>amount</code> - Set exact credits.
   •  /setpremium <code>user_id</code> <code>true/false</code> - Set premium status.
   •  /userinfo <code>user_id</code> - Get user info.
   •  /bonus <code>referrer_bonus</code> <code>referred_bonus</code> - Set referral bonuses.
   •  /setgate <code>gate</code> - Set default gateway for new users.
   •  /listadmins - List all admins.
   •  /ban <code>user_id</code> - Ban a user.
   •  /unban <code>user_id</code> - Unban a user.
   •  /unbanall - Unban all users.
   •  /botstats - View bot statistics.
   •  /backupdata - Backup bot data.
   •  /send <code>user_id</code> <code>message</code> - Send direct message.
   •  /forward <code>user_id</code> <code>message_id</code> - Forward message to user.
   •  /setgateprice <code>gate</code> <code>price</code> - Set gate price.
   •  /getconfig - Get bot configuration.
   •  /setconfig <code>setting</code> <code>value</code> - Set bot configuration.<a href='https://t.me/+GdWapjhiAG05OTk1'>┗━━━━━━━⊛</a>
"""
        help_text += f"""

⚙️ <b>Current Settings</b> ⚙️
<a href='https://t.me/+GdWapjhiAG05OTk1'>┏━━━━━━━━━━━⍟</a>
<a href='https://t.me/+GdWapjhiAG05OTk1'>┃</a>
   •  <b>Gate:</b> <code>{current_gate}</code>"""
        if CREDIT_SYSTEM_ENABLED:
            help_text += f"\n   •  <b>Credits:</b> <code>{credits}</code>"
        help_text += "<a href='https://t.me/+GdWapjhiAG05OTk1'>┗━━━━━━━⊛</a>"

        bot.reply_to(message, help_text, parse_mode="HTML", disable_web_page_preview=True)

    elif command in ['buy', 'price']:
        buy_text = """
💎 <b>Premium Credit Plans</b> 💎
<a href='https://t.me/+GdWapjhiAG05OTk1'>┏━━━━━━━━━━━⍟</a>
<a href='https://t.me/+GdWapjhiAG05OTk1'>┃</a>
Enhance your checking power with our flexible credit plans!

💰 <b>Starter</b>     ::  2,000 Credits  ::  <b>₹499</b> ⚡
   💳 For casual users, great for starting out.

🚀 <b>Basic</b>       ::  5,000 Credits  ::  <b>₹999</b> 🚀
   ✨ Ideal for regular use, more checks, more value.

🔥 <b>Advanced</b>    ::  10,000 Credits ::  <b>₹1,999</b> 🔥
   💎 For power users, significantly increased checking capacity.

⚡ <b>Premium</b>     ::  25,000 Credits ::  <b>₹4,499</b> ⚡
   🏆 Best value for frequent heavy use.

💎 <b>Elite</b>       ::  50,000 Credits ::  <b>₹9,999</b> 💎
   👑 For ultimate power users and resellers - maximum credits!

💳 <b>Tap 'Buy Now' to explore payment options.</b><a href='https://t.me/+GdWapjhiAG05OTk1'>┗━━━━━━━⊛</a>
        """
        markup = types.InlineKeyboardMarkup()
        buy_button = types.InlineKeyboardButton("💳 Buy Now", callback_data='show_payment_methods')
        markup.add(buy_button)
        bot.reply_to(message, buy_text, reply_markup=markup, parse_mode="HTML", disable_web_page_preview=True)


@bot.callback_query_handler(func=lambda call: call.data == 'show_payment_methods')
def payment_methods_callback(call):
    user_id = call.message.chat.id
    if not is_private_chat(call.message): # Modified condition to allow in groups
        if not is_bot_mentioned(BOT_USERNAME, call.message):
            return

    payment_text = """
💳 <b>Select Payment Method</b> 💳
<a href='https://t.me/+GdWapjhiAG05OTk1'>┏━━━━━━━━━━━⍟</a>
<a href='https://t.me/+GdWapjhiAG05OTk1'>┃</a>
🔒 Secure and streamlined payment process.

"""

    payment_methods_list = """
✅ <b>Bitcoin (BTC)</b>:
   <code>15eRTKVEEqJKBLBW4sHJPuF6ByvjK5VcDw</code>

✅ <b>USDT (Trc20)</b>:
   <code>TUQysXBFPZ6mmJg9FqwYFQcPUqSepTB96E</code>

✅ <b>UPI</b>:
   📴 Currently Unavailable<a href='https://t.me/+GdWapjhiAG05OTk1'>┗━━━━━━━⊛</a>
"""

    payment_footer = """
⚡️ <b>Instant Activation!</b> Your credits will be activated automatically after payment confirmation.

💬 <b>Important</b>: DM @CrImSon_WoLf777 with payment proof.
"""

    payment_text += payment_methods_list + payment_footer

    markup = types.InlineKeyboardMarkup()
    dm_button = types.InlineKeyboardButton("📩 Contact Admin for Support", url="https://t.me/CrImSon_WoLf777")
    markup.add(dm_button)
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=payment_text, reply_markup=markup, parse_mode="HTML", disable_web_page_preview=True)


@bot.message_handler(commands=['register', 'start'])
def register_command(message):
    if not is_private_chat(message): # Modified condition to allow in groups
        if not is_bot_mentioned(BOT_USERNAME, message):
            return

    user_id = message.chat.id
    user_name = message.from_user.first_name or "User"

    if is_registered(user_id):
        bot.reply_to(message, f"⚠️ <b>{user_name}</b>, you are already registered!", parse_mode="HTML")
        return

    if user_id in BANNED_USERS:
        return bot.reply_to(message, "🚫 You are banned from using this bot. Contact admin.", parse_mode="HTML")

    referrer_id = None
    if message.text.startswith('/start') and len(message.text.split()) > 1:
        try:
            ref_code = message.text.split()[1]
            referrer_id = _get_user_id_from_referral_code(ref_code)
            if referrer_id == user_id:
                referrer_id = None
            elif is_admin(referrer_id):
                referrer_id = None
        except:
            referrer_id = None

    register_result = register_user(user_id, referrer_id=referrer_id)

    if register_result == "success":
        with open("user_ids.txt", "a") as f:
            f.write(str(user_id) + "\n")

        initial_credits = get_user_credits(user_id) if CREDIT_SYSTEM_ENABLED else "Unlimited"
        registration_message = f"""
🎉 <b>Registration Successful, {user_name}!</b> 🎉
<a href='https://t.me/+GdWapjhiAG05OTk1'>┏━━━━━━━━━━━⍟</a>
<a href='https://t.me/+GdWapjhiAG05OTk1'>┃</a>
🚀 Welcome aboard the Crimson Checker Bot!

"""
        if CREDIT_SYSTEM_ENABLED:
            registration_message += f"💰 <b>{initial_credits} Credits Added to Your Account</b>\n"
        else:
            registration_message += "✨ <b>Unlimited Credits - Enjoy Full Access!</b> ✨\n"

        if referrer_id:
            referrer_bonus = get_referrer_bonus()
            referred_bonus = get_referred_bonus()
            registration_message += f"\n🎁 <b>Referral Bonus Applied!</b>\n   💰 You've received a bonus of <b>{referred_bonus} credits</b> thanks to your referrer!\n"
            try:
                bot.send_message(referrer_id, f"🎉 New user <a href='tg://user?id={user_id}'><b>{user_name}</b></a> joined using your referral!\n💰 Referral bonus of <b>{referrer_bonus} credits</b> credited to your account.", parse_mode="HTML")
            except Exception as e:
                print(f"Error sending referral bonus message to referrer {referrer_id}: {e}")

        registration_message += "\n📚 Explore the bot with /menu - Your command center!<a href='https://t.me/+GdWapjhiAG05OTk1'>┗━━━━━━━⊛</a>"
        bot.reply_to(message, registration_message, parse_mode="HTML", disable_web_page_preview=True)
    elif register_result == "already_registered":
        bot.reply_to(message, f"⚠️ <b>{user_name}</b>, you are already registered!", parse_mode="HTML")
    else:
        bot.reply_to(message, "❌ <b>Registration failed.</b> Please contact support.", parse_mode="HTML")

@bot.message_handler(commands=['referral'])
def referral_command(message):
    if not is_private_chat(message): # Modified condition to allow in groups
        if not is_bot_mentioned(BOT_USERNAME, message):
            return
    if not ensure_registered(message) or not REFERRAL_SYSTEM_ENABLED: return
    user_id = message.chat.id
    referral_link = get_user_referral_link(user_id, BOT_USERNAME)
    if referral_link:
        bot.reply_to(message, f"🔗 <b>Your Exclusive Referral Link:</b>\n\n{referral_link}\n\n📣 Share your link to invite friends and earn bonus credits!", parse_mode="HTML", disable_web_page_preview=True)
    else:
        bot.reply_to(message, "❌ <b>Error generating referral link.</b> Please try again later.", parse_mode="HTML")

@bot.message_handler(commands=['bonus'])
def bonus_command(message):
    if not is_private_chat(message): # Modified condition to allow in groups
        if not is_bot_mentioned(BOT_USERNAME, message):
            return
    if not ensure_registered(message) or not REFERRAL_SYSTEM_ENABLED: return
    user_id = message.chat.id
    if not is_admin(user_id):
        bot.reply_to(message, "🚫 Admin command only. Access Denied.", parse_mode="HTML")
        return

    log_admin_command(user_id, "bonus", message.text)

    try:
        args = message.text.split()
        if len(args) != 3:
            raise ValueError("Incorrect number of arguments provided.")
        referrer_bonus = int(args[1])
        referred_bonus = int(args[2])

        if referrer_bonus < 0 or referred_bonus < 0:
            raise ValueError("Bonuses cannot be negative values.")

        set_referral_bonuses(referrer_bonus, referred_bonus)
        bot.reply_to(message, f"✅ <b>Referral Bonuses Updated!</b>\n\n🎁 Referrer Bonus: <code>{referrer_bonus} credits</code>\n👤 Referred Bonus: <code>{referred_bonus} credits</code>", parse_mode="HTML")

    except ValueError as e:
        bot.reply_to(message, f"❌ <b>Error updating referral bonuses.</b>\n\n<b>Usage:</b> <code>/bonus referrer_bonus referred_bonus</code> (bonuses must be non-negative integers). \n\n<b>Details</b>: {e}", parse_mode="HTML")
    except Exception as e:
        print(f"Error setting referral bonuses: {e}")
        bot.reply_to(message, "❌ <b>Error setting referral bonuses.</b> Please contact support.", parse_mode="HTML")

@bot.message_handler(commands=['feedback'])
def feedback_command(message):
    if not is_private_chat(message): # Modified condition to allow in groups
        if not is_bot_mentioned(BOT_USERNAME, message):
            return
    if not ensure_registered(message): return
    user_id = message.chat.id
    try:
        feedback_text = message.text.split(maxsplit=1)[1]
        forward_message = f"<b>Feedback from User ID:</b> <code>{user_id}</code>\n<b>Username:</b> @{message.from_user.username}\n<b>Name:</b> {message.from_user.first_name} {message.from_user.last_name or ''}\n\n<b>Message:</b>\n{feedback_text}"
        for admin_id in get_admin_list():
            try:
                bot.send_message(admin_id, forward_message, parse_mode="HTML")
            except Exception as e:
                print(f"Error sending feedback to admin {admin_id}: {e}")
        bot.reply_to(message, "✅ <b>Feedback Sent!</b>\n\nYour feedback has been forwarded to the bot admins. Thank you!", parse_mode="HTML")
    except IndexError:
        bot.reply_to(message, "❌ <b>Feedback Message Required</b>\n\nUsage: <code>/feedback message</code>\nPlease provide your feedback message.", parse_mode="HTML")
    except Exception as e:
        print(f"Error processing feedback: {e}")
        bot.reply_to(message, "❌ <b>Error sending feedback.</b> Please try again later.", parse_mode="HTML")

@bot.message_handler(commands=['ping'])
def ping_command(message):
    if not is_private_chat(message): # Modified condition to allow in groups
        if not is_bot_mentioned(BOT_USERNAME, message):
            return
    if not ensure_registered(message): return
    start_time = time.time()
    pong = bot.reply_to(message, "🏓 <b>Pinging...</b>", parse_mode="HTML")
    end_time = time.time()
    latency = str(round(end_time - start_time, 2))
    bot.edit_message_text(f"🏓 <b>Pong! Latency:</b> <code>{latency} seconds</code>", chat_id=message.chat.id, message_id=pong.message_id, parse_mode="HTML")

@bot.message_handler(commands=['terms'])
def terms_command(message):
    if not is_private_chat(message): # Modified condition to allow in groups
        if not is_bot_mentioned(BOT_USERNAME, message):
            return
    if not ensure_registered(message): return
    terms_text = """
📜 <b>Terms of Service</b> 📜
<a href='https://t.me/+GdWapjhiAG05OTk1'>┏━━━━━━━━━━━⍟</a>
<a href='https://t.me/+GdWapjhiAG05OTk1'>┃</a>
These Terms of Service govern your use of Crimson Checker Bot.

<b>1. Acceptance of Terms</b>
By using this bot, you agree to be bound by these Terms of Service and our Privacy Policy.

<b>2. Bot Usage</b>
- You are responsible for using the bot in compliance with all applicable laws and regulations.
- Do not use the bot for illegal activities.
- We reserve the right to modify or terminate the bot at any time.

<b>3. Credits and Payments</b> (If applicable)
- Credits are used for accessing certain bot features.
- Payments for credits are non-refundable unless explicitly stated.
- Credit balances may expire after a period, as announced.

<b>4. Disclaimer of Warranty</b>
- The bot is provided "as is" without warranty of any kind.
- We do not guarantee the accuracy or reliability of check results.

<b>5. Limitation of Liability</b>
- We are not liable for any direct, indirect, or consequential damages resulting from bot usage.

<b>6. Privacy</b>
- We collect and process your data as described in our Privacy Policy.

<b>7. Changes to Terms</b>
- We may update these Terms of Service periodically. Continued use after changes implies acceptance.

<b>8. Contact</b>
- For support or questions, contact @CrImSon_WoLf777.<a href='https://t.me/+GdWapjhiAG05OTk1'>┗━━━━━━━⊛</a>
"""
    bot.reply_to(message, terms_text, parse_mode="HTML", disable_web_page_preview=True)

@bot.message_handler(commands=['privacy'])
def privacy_command(message):
    if not is_private_chat(message): # Modified condition to allow in groups
        if not is_bot_mentioned(BOT_USERNAME, message):
            return
    if not ensure_registered(message): return
    privacy_text = """
🔒 <b>Privacy Policy</b> 🔒
<a href='https://t.me/+GdWapjhiAG05OTk1'>┏━━━━━━━━━━━⍟</a>
<a href='https://t.me/+GdWapjhiAG05OTk1'>┃</a>
Your privacy is important to us. This Privacy Policy explains how we collect, use, and protect your information.

<b>1. Information Collection</b>
- We collect your Telegram User ID to manage your bot access and credits.
- We log admin commands for security and audit purposes.
- We may store card check statistics to improve bot performance.

<b>2. Use of Information</b>
- Your User ID is used for bot functionality, credits, and stats.
- Admin logs help us monitor bot usage and prevent abuse.
- We do not share your personal information with third parties unless required by law.

<b>3. Data Security</b>
- We take reasonable measures to protect your data from unauthorized access and misuse.
- Data is stored securely, and access is restricted to authorized personnel.

<b>4. Data Retention</b>
- We retain user data as long as necessary to provide bot services and comply with legal obligations.

<b>5. Your Rights</b>
- You can request information about the data we hold about you.
- Contact @CrImSon_WoLf777 for data inquiries.

<b>6. Policy Changes</b>
- We may update this Privacy Policy. Changes will be posted in the bot or announced.

<b>7. Consent</b>
- By using Crimson Checker Bot, you consent to this Privacy Policy.<a href='https://t.me/+GdWapjhiAG05OTk1'>┗━━━━━━━⊛</a>
"""
    bot.reply_to(message, privacy_text, parse_mode="HTML", disable_web_page_preview=True)

def ensure_registered(message):
    user_id = message.chat.id
    if user_id in BANNED_USERS:
        bot.reply_to(message, "🚫 You are banned from using this bot. Contact admin.", parse_mode="HTML")
        return False
    if not is_registered(user_id) and needs_registration_check(message):
        bot.reply_to(message, "🔑 <b>Account Registration Required</b>\n\nTo proceed with this command, please register using /register first.", parse_mode="HTML")
        return False
    return True

@bot.message_handler(commands=["gate"])
def gate_command(message):
    if not is_private_chat(message): # Modified condition to allow in groups
        if not is_bot_mentioned(BOT_USERNAME, message):
            return
    if not ensure_registered(message): return
    user_id = message.chat.id
    markup = types.InlineKeyboardMarkup(row_width=2)
    gates = [
        ("Stripe Auth", 'set_gate:auth'),
        ("Stripe 2$", 'set_gate:stripe2'),
        ("Stripe 4$", 'set_gate:stripe4')
    ]
    for gate_name, callback_data in gates:
        markup.add(types.InlineKeyboardButton(gate_name, callback_data=callback_data))
    current_gate = get_user_gate_preference(user_id).capitalize() or DEFAULT_GATE.capitalize() # Show default gate
    bot.reply_to(message, f"⚙️ <b>Select Payment Gateway</b>\n\nChoose your preferred gateway for processing card checks:\n\n<b>Current Gateway:</b> <code>{current_gate}</code>\n<b>Default Gateway (for new users):</b> <code>{DEFAULT_GATE.capitalize()}</code>\n\n<b>Cost: 1 Credit per Check for all Gateways</b>", reply_markup=markup, parse_mode="HTML")

@bot.callback_query_handler(func=lambda call: call.data.startswith('set_gate:'))
def set_gate_callback(call):
    user_id = call.message.chat.id
    if not is_private_chat(call.message): # Modified condition to allow in groups
        if not is_bot_mentioned(BOT_USERNAME, call.message):
            return
    gate_name = call.data.split(':')[1]
    set_user_gate_preference(user_id, gate_name)
    gate_display_name = gate_name.replace("stripe2", "2$").replace("stripe4", "4$").capitalize()
    bot.answer_callback_query(call.id, text=f"Gateway set to {gate_display_name}")
    bot.edit_message_text(chat_id=user_id, message_id=call.message.message_id, text=f"✅ <b>Gateway Updated</b>\n\nYour active payment gateway is now:\n\n<b>Current Gateway:</b> <code>{gate_display_name}</code>\n\n<b>Cost: 1 Credit per Check for all Gateways</b>", parse_mode="HTML", reply_markup=None)

@bot.message_handler(commands=['stats'])
def stats_command(message):
    if not is_private_chat(message): # Modified condition to allow in groups
        if not is_bot_mentioned(BOT_USERNAME, message):
            return
    if not ensure_registered(message): return
    user_id = message.chat.id
    user_stats = get_user_stats(user_id)
    if not user_stats:
        user_stats = {'approved': 0, 'declined': 0, 'ccn': 0, 'cvv': 0}
    credits = get_user_credits(user_id) if CREDIT_SYSTEM_ENABLED else "Unlimited"
    current_gate = get_user_gate_preference(user_id).capitalize() or DEFAULT_GATE.capitalize() # Show current gate in stats

    text = f"""📊 <b>Your Checker Stats</b> 📊
<a href='https://t.me/+GdWapjhiAG05OTk1'>┏━━━━━━━━━━━⍟</a>
<a href='https://t.me/+GdWapjhiAG05OTk1'>┃</a>
Performance overview of your card checking activity:\n\n"""
    if CREDIT_SYSTEM_ENABLED:
        text += f"💰 <b>Credits Available:</b> <code>{credits}</code>\n"
    text += f"""
⚙️ <b>Current Gate:</b> <code>{current_gate}</code>
✅ <b>Approved Cards:</b>   <code>{user_stats.get('approved', 0)}</code>
❌ <b>Declined Cards:</b>   <code>{user_stats.get('declined', 0)}</code>
⚠️ <b>CCN Results:</b>       <code>{user_stats.get('ccn', 0)}</code>
✅ <b>CVV Results:</b>       <code>{user_stats.get('cvv', 0)}</code><a href='https://t.me/+GdWapjhiAG05OTk1'>┗━━━━━━━⊛</a>
"""
    bot.reply_to(message, text, parse_mode="HTML")

@bot.message_handler(commands=['credits'])
def credits_command(message):
    if not is_private_chat(message): # Modified condition to allow in groups
        if not is_bot_mentioned(BOT_USERNAME, message):
            return
    if not ensure_registered(message) or not CREDIT_SYSTEM_ENABLED: return
    user_id = message.chat.id
    credits = get_user_credits(user_id)
    credits_display = credits if not isinstance(credits, str) else "Unlimited"
    bot.reply_to(message, f"💰 <b>Your Credit Balance:</b> <code>{credits_display}</code> credits", parse_mode="HTML")

@bot.message_handler(commands=['redeem'])
def redeem_command(message):
    if not is_private_chat(message): # Modified condition to allow in groups
        if not is_bot_mentioned(BOT_USERNAME, message):
            return
    if not ensure_registered(message) or not REDEEM_SYSTEM_ENABLED: return
    user_id = message.chat.id
    log_admin_command(user_id, "redeem", message.text)
    try:
        code = message.text.split()[1]
    except IndexError:
        bot.reply_to(message, "❌ <b>Redeem Code Required</b>\n\nUsage: <code>/redeem code</code>\nPlease enter the redeem code you received.", parse_mode="HTML")
        return

    if not re.match(r"^[a-zA-Z0-9]{4}-[a-zA-Z0-9]{4}-[a-zA-Z0-9]{4}$", code):
        bot.reply_to(message, "❌ <b>Invalid Code Format</b>\n\nUse the format: <code>xxxx-xxxx-xxxx</code>", parse_mode="HTML")
        return

    redeem_result = redeem_credits(user_id, code)
    if redeem_result == "success":
        user_data = _load_user_data()
        is_premium_user = user_data.get(str(user_id), {}).get('is_premium', False)
        premium_message_part = " and you've unlocked <b>Premium Access!</b> 🎉" if is_premium_user else ""
        bot.reply_to(message, f"✅ <b>Code Redeemed Successfully!</b>\n\nYour account has been credited{premium_message_part}.", parse_mode="HTML")
    elif redeem_result == "invalid":
        bot.reply_to(message, "❌ <b>Invalid Code</b>\n\nPlease verify the redeem code and try again.", parse_mode="HTML")
    elif redeem_result == "used":
        bot.reply_to(message, "⚠️ <b>Code Already Used</b>\n\nThis redeem code has already been used.", parse_mode="HTML")
    else:
        bot.reply_to(message, "❌ <b>Redeem Error</b>\n\nAn error occurred during redemption. Please contact support.", parse_mode="HTML")

@bot.message_handler(commands=['code'])
def generate_code_command(message):
    if not is_private_chat(message): # Modified condition to allow in groups
        if not is_bot_mentioned(BOT_USERNAME, message):
            return
    if not ensure_registered(message) or not REDEEM_SYSTEM_ENABLED: return
    user_id = message.chat.id
    if not is_admin(user_id):
        bot.reply_to(message, "🚫 Admin command only. Access Denied.", parse_mode="HTML")
        return

    log_admin_command(user_id, "code", message.text)

    try:
        args = message.text.split()
        if len(args) < 2:
            raise ValueError("Amount not specified")
        amount_str = args[1].lower() # Modified to lower case for premium check
        if amount_str == 'premium' or amount_str == 'p': # Check for 'premium' or 'p'
            amount = 0
            is_premium_code = True
        else:
            amount = int(amount_str)
            is_premium_code = False

        num_codes = 1
        codes = generate_redeem_codes(amount, num_codes, code_format="xxxx-xxxx-xxxx", premium=is_premium_code)
        code_list = "\n".join(codes)
        premium_note = "(Premium Code - Grants Premium Access)" if is_premium_code else f"(Credits: {amount})" # Updated note

        bot.reply_to(message, f"✅ <b>Redeem Code Generated!</b>\n\n<code>{code_list}</code>\n\n{premium_note}\n\nDistribute this code for users to redeem credits or Premium access.", parse_mode="HTML") # Updated message

    except (ValueError, IndexError):
        bot.reply_to(message, "❌ <b>Usage Error: Credit Amount/Type Required</b>\n\nUsage: <code>/code amount</code> (amount as integer for credits, or 'premium'/'p' for premium code)", parse_mode="HTML") # Updated usage message
    except Exception as e:
        print(f"Error generating redeem code: {e}")
        bot.reply_to(message, "❌ <b>Error generating code.</b> Please contact support.", parse_mode="HTML")

@bot.message_handler(commands=['gen'])
def generate_data_command(message):
    if not is_private_chat(message): # Modified condition to allow in groups
        if not is_bot_mentioned(BOT_USERNAME, message):
            return
    if not ensure_registered(message): return
    user_id = message.chat.id

    try:
        data_type = message.text.split()[1].lower()
    except IndexError:
        bot.reply_to(message, "❌ <b>Data Type Missing</b>\n\nUsage: <code>/gen [type]</code>\n\nSupported types: <code>email</code>, <code>username</code>, <code>password</code>, <code>address</code>, <code>phone</code>", parse_mode="HTML")
        return

    if data_type == 'email':
        email = generate_random_email()
        bot.reply_to(message, f"📧 <b>Generated Email:</b> <code>{email}</code>", parse_mode="HTML")
    elif data_type == 'username':
        username = generate_username()
        bot.reply_to(message, f"👤 <b>Generated Username:</b> <code>{username}</code>", parse_mode="HTML")
    elif data_type == 'password':
        password = generate_password()
        bot.reply_to(message, f"🔑 <b>Generated Password:</b> <code>{password}</code>", parse_mode="HTML")
    elif data_type == 'address':
        address = generate_address()
        bot.reply_to(message, f"🏠 <b>Generated Address:</b> <code>{address}</code>", parse_mode="HTML")
    elif data_type == 'phone':
        phone_number = generate_phone_number()
        bot.reply_to(message, f"📞 <b>Generated Phone Number:</b> <code>{phone_number}</code>", parse_mode="HTML")
    elif data_type == 'name':
        name = generate_username()
        bot.reply_to(message, f"👤 <b>Generated Name:</b> <code>{name}</code>", parse_mode="HTML")
    elif data_type == 'zip':
        zip_code = random.randint(10000, 99999)
        bot.reply_to(message, f"✉️ <b>Generated Zip Code:</b> <code>{zip_code}</code>", parse_mode="HTML")
    elif data_type == 'iban':
        iban = generate_iban()
        bot.reply_to(message, f"🏦 <b>Generated IBAN:</b> <code>{iban}</code>", parse_mode="HTML")
    elif data_type == 'swift':
        swift = generate_swift()
        bot.reply_to(message, f"🏢 <b>Generated SWIFT/BIC:</b> <code>{swift}</code>", parse_mode="HTML")
    elif data_type == 'btc_address':
        btc_address = generate_btc_address()
        bot.reply_to(message, f"₿ <b>Generated BTC Address:</b> <code>{btc_address}</code>", parse_mode="HTML")
    elif data_type == 'usdt_address':
        usdt_address = generate_usdt_address()
        bot.reply_to(message, f"₮ <b>Generated USDT Address (TRC20):</b> <code>{usdt_address}</code>", parse_mode="HTML")
    else:
        bot.reply_to(message, "❌ <b>Invalid Data Type</b>\n\nSupported types: <code>email</code>, <code>username</code>, <code>password</code>, <code>address</code>, <code>phone</code>, <code>name</code>, <code>zip</code>, <code>iban</code>, <code>swift</code>, <code>btc_address</code>, <code>usdt_address</code>", parse_mode="HTML")

@bot.message_handler(commands=['bin'])
def bin_command(message):
    if not is_private_chat(message): # Modified condition to allow in groups
        if not is_bot_mentioned(BOT_USERNAME, message):
            return
    if not ensure_registered(message): return
    try:
        bin_input = message.text.split()[1]
        if not re.match(r'^\d{6,8}$', bin_input):
            raise ValueError("Invalid BIN format")

        try:
            data = requests.get(f'https://bins.antipublic.cc/bins/{bin_input}').json()
        except:
            return bot.reply_to(message, "❌ <b>BIN Lookup Failed</b>\n\nCould not retrieve BIN information. Please try again later.", parse_mode="HTML")

        if not data:
            return bot.reply_to(message, f"ℹ️ <b>BIN Info</b> ℹ️\n\nNo detailed information found for BIN <code>{bin_input}</code>.", parse_mode="HTML")

        bin_info_text = f"""
ℹ️ <b>BIN Info for</b> <code>{bin_input}</code> ℹ️
<a href='https://t.me/+GdWapjhiAG05OTk1'>┏━━━━━━━━━━━⍟</a>
<a href='https://t.me/+GdWapjhiAG05OTk1'>┃</a>
<b>💳 Brand:</b> <code>{data.get('brand', 'N/A')}</code>
<b>🏦 Bank:</b> <code>{data.get('bank', 'N/A')}</code>
<b>🏛️ Country:</b> <code>{data.get('country_name', 'N/A')} {data.get('country_flag', '')}</code>
<b>🗺️ Country Code:</b> <code>{data.get('country_code', 'N/A')}</code>
<b>⌨️ Type:</b> <code>{data.get('type', 'N/A')}</code>
<b>🎚️ Level:</b> <code>{data.get('level', 'N/A')}</code>
<b>ℹ️ Prepaid:</b> <code>{'Yes' if data.get('prepaid') else 'No'}</code>
<b>🌐 Website:</b> <code>{data.get('bank_url', 'N/A')}</code>
<b>📞 Phone:</b> <code>{data.get('bank_phone', 'N/A')}</code><a href='https://t.me/+GdWapjhiAG05OTk1'>┗━━━━━━━⊛</a>
"""

        bot.reply_to(message, bin_info_text, parse_mode="HTML", disable_web_page_preview=True)

    except IndexError:
        bot.reply_to(message, "❌ <b>BIN Input Required</b>\n\nUsage: <code>/bin [BIN]</code>\nPlease provide a BIN (first 6-8 digits of card).", parse_mode="HTML")
    except ValueError as e:
        bot.reply_to(message, f"❌ <b>Invalid Input</b>\n\n{e}\n\nUsage: <code>/bin [BIN]</code> (BIN must be 6-8 digits).", parse_mode="HTML")
    except Exception as e:
        print(f"Error processing /bin command: {e}")
        bot.reply_to(message, "❌ <b>Error retrieving BIN information.</b> Please contact support.", parse_mode="HTML")

CARD_BRANDS = {
    "visa": "💳 Visa",
    "mastercard": "MC Mastercard",
    "amex": "🪪 Amex",
    "discover": "🔭 Discover",
    "jcb": "💴 JCB",
    "unionpay": "🇨🇳 UnionPay",
}

@bot.message_handler(commands=["chk", "check", ".chk", "validate", "驗卡", "card", "cc"])
def check_card_command(message):
    if not is_private_chat(message):
        if not is_bot_mentioned(BOT_USERNAME, message):
            return
    if not ensure_registered(message): return
    user_id = message.chat.id
    credits = get_user_credits(user_id) if CREDIT_SYSTEM_ENABLED else "Unlimited"

    if CREDIT_SYSTEM_ENABLED and credits != "Unlimited" and credits < 1:
        return bot.reply_to(message, f"🚫 <b>Insufficient Credits</b>\n\nYou have <code>{credits}</code> credits remaining. You need at least 1 credit to perform a check. Please redeem a code or contact support.", parse_mode="HTML")

    full_input = message.text.split(maxsplit=1)[1].strip() if len(message.text.split()) > 1 else None

    if not full_input:
        return bot.reply_to(message, "❌ <b>Card Details Missing</b>\n\nUsage: <code>/chk cc|mm|yy|cvv</code> or send a document with CCs.", parse_mode="HTML")

    ko_msg = None
    ccs_to_check = []
    bulk_check = False

    if message.document:
        return # Document handling is in 'main' function

    elif '\n' in full_input and ENABLE_GROUP_CHECK:
        ccs_to_check = extract_ccs_from_line(full_input)
        if not ccs_to_check:
            return bot.reply_to(message, "❌ <b>No Valid Cards Detected</b>\n\nProvide card details in <code>cc|mm|yy|cvv</code> format, one per line for bulk check.", parse_mode="HTML")
        ko_msg = bot.reply_to(message, f"💳 <b>Bulk Card Check Initiated</b> ⏳\n\nChecking <code>{len(ccs_to_check)}</code> cards...", parse_mode="HTML").message_id
        bulk_check = True

    elif re.match(r'\d{13,19}\|\d{1,2}\|\d{2,4}\|\d{3,4}', full_input):
        ccs_to_check = [full_input]
        ko_msg = bot.reply_to(message, "💳 <b>Checking Card Details</b> ⏳", parse_mode="HTML").message_id
    else:
        return bot.reply_to(message, "❌ <b>Invalid Card Format</b>\n\nUse the format: <code>cc|mm|yy|cvv</code> or upload a document.", parse_mode="HTML")

    dd = 0
    live = 0
    incorrect = 0
    checked_count = 0
    session = manage_session_file()
    if not session:
        return bot.reply_to(message, "❌ <b>Session Error</b>\n\nFailed to create session. Please try again later.", parse_mode="HTML")
    gate_function = get_gate_function_for_user(user_id)
    gate_name_preference = get_user_gate_preference(user_id)
    gate_name_display = gate_name_preference.upper().replace("AUTH", "AUTH").replace("STRIPE2", "2$").replace("STRIPE4", "4$")


    for cc in ccs_to_check:
        if handle_stop_signal(message.chat.id, ko_msg):
            return

        if CREDIT_SYSTEM_ENABLED:
            if not deduct_credits(user_id):
                if ko_msg:
                    bot.edit_message_text(chat_id=message.chat.id, message_id=ko_msg, text=f"🚫 <b>Credits Exhausted</b>\n\nBulk check stopped after <code>{checked_count}</code> cards.\nRedeem credits or purchase a plan.\nCredits left: <code>{get_user_credits(user_id)}</code>", parse_mode="HTML")
                else:
                    bot.reply_to(message, f"🚫 <b>Credits Exhausted</b>\n\nCheck stopped.\nRedeem credits or purchase a plan.\nCredits left: <code>{get_user_credits(user_id)}</code>", parse_mode="HTML")
                return

        checked_count += 1

        try:
            data = requests.get('https://bins.antipublic.cc/bins/' + cc[:6]).json() if DETAILED_BIN_INFO else {}
        except:
            data = {}
        brand = data.get('brand', 'Unknown').lower()
        card_type = data.get('type', 'Unknown')
        country = data.get('country_name', 'Unknown')
        country_flag = data.get('country_flag', 'Unknown')
        bank = data.get('bank', 'Unknown')
        card_brand_display = CARD_BRANDS.get(brand, brand.capitalize()) if DISPLAY_CARD_BRAND else brand.capitalize()

        start_time = time.time()
        last = str(gate_function(session, cc.strip()))
        update_user_stats(user_id, last.split(" ")[0])
        end_time = time.time()
        execution_time = end_time - start_time

        msg_output = f"""
<a href='https://envs.sh/smD.webp'>-</a> 💳 <b>Ｃａｒｄ Ｃｈｅｃｋ Ｒｅｓｕｌｔ</b> 💳
<a href='https://t.me/+GdWapjhiAG05OTk1'>┏━━━━━━━━━━━⍟</a>
<a href='https://t.me/+GdWapjhiAG05OTk1'>┃</a><b>💳 ＣＣ:</b> <code>{cc}</code><a href='https://t.me/+GdWapjhiAG05OTk1'>┗━━━━━━━⊛</a>
<a href='https://t.me/+GdWapjhiAG05OTk1'>-</a> ⚡ 𝐆𝐚𝐭𝐞𝐰𝐚𝐲: ⤿ {gate_name_display} 🟢 ⤾
<a href='https://t.me/+GdWapjhiAG05OTk1'>-</a> ✅ Ｒｅｓｐｏｎｓｅ: ⤿ {last} ⤾

<a href='https://envs.sh/smD.webp'>-</a> ℹ️ <b>Ｉｎｆｏ</b>: <code>{cc[:6]}-{card_type} - {card_brand_display}</code>
<a href='https://t.me/+GdWapjhiAG05OTk1'>-</a> 🗺️ 𝐂𝐨𝐮𝐧𝐭𝐫𝐲: <code>{country} - {country_flag}</code>
<a href='https://t.me/+GdWapjhiAG05OTk1'>-</a> 🏦 Ｂａｎｋ: <code>{bank}</code>

<a href='https://t.me/+GdWapjhiAG05OTk1'>-</a> ⏱️ Ｔｉｍｅ: <code>{round(execution_time, 1)} 𝐬𝐞𝐜</code>
<a href='https://t.me/+GdWapjhiAG05OTk1'>-</a> 🤖 Ｂｏｔ Ｂｙ: <a href='https://t.me/+GdWapjhiAG05OTk1'>Crimson </a>"""

        bot.send_message(message.chat.id, msg_output, parse_mode="HTML", disable_web_page_preview=True) # Send result immediately

        if bulk_check: # Bulk check counters and message update
            if 'APPROVED ✅' in last or 'CVV ✅' in last:
                live += 1
            elif 'CCN ✅' in last:
                incorrect+=1
            elif 'DECLINED ❌' in last or 'EXPIRED ❌' in last or 'Error' in last:
                dd += 1

            bulk_update_text = f'''📝 <b>Bulk Checking in Progress...</b> 📝
🤖 𝗕𝘆 ➜ <a href='https://t.me/+GdWapjhiAG05OTk1'>Crimson </a>

✅ 𝐀𝐏𝐏𝐑𝐎𝐕𝐄𝐃 : [ {live} ]
⚠️ 𝐅𝐀𝐊𝐄 𝐂𝐀𝐑𝐃 : [ {incorrect} ]
❌ 𝐃𝐄𝐂𝐋𝐈𝐍𝐄𝐃 : [ {dd} ]
🎉 𝐓𝐎𝐓𝐀𝐋    :  [ {checked_count} ]'''

            try:
                bot.edit_message_text(chat_id=message.chat.id, message_id=ko_msg, text=bulk_update_text, parse_mode="HTML", disable_web_page_preview=True)
            except Exception as e:
                print(f"Error editing bulk message: {e}")


    if bulk_check:
        try:
            bot.edit_message_text(
                chat_id=message.chat.id,
                message_id=ko_msg,
                text='📝 𝗕𝗨𝗟𝗞 𝗖𝗛𝗘𝗖𝗞 𝗖𝗢𝗠𝗣𝗟𝗘𝗧𝗘𝗗 ✅\n🤖 𝗕𝗢𝗧 𝗕𝗬 ➜ @CrImSon_WoLf777', parse_mode="HTML", disable_web_page_preview=True
            )
        except Exception as e:
            print(f"Error editing final bulk message: {e}")



@bot.message_handler(commands=["mchk"])
def mcheck_card_command(message):
    if not is_private_chat(message):
        if not is_bot_mentioned(BOT_USERNAME, message):
            return
    if not ensure_registered(message): return
    user_id = message.chat.id
    credits = get_user_credits(user_id) if CREDIT_SYSTEM_ENABLED else "Unlimited"

    if CREDIT_SYSTEM_ENABLED and credits != "Unlimited" and credits < 1:
        return bot.reply_to(message, f"🚫 <b>Insufficient Credits</b>\n\nYou have <code>{credits}</code> credits remaining. You need at least 1 credit to perform a check. Please redeem a code or contact support.", parse_mode="HTML")

    full_input = message.text.split(maxsplit=1)[1].strip() if len(message.text.split()) > 1 else None

    if not full_input:
        return bot.reply_to(message, "❌ <b>Card Details Missing</b>\n\nUsage: <code>/mchk cc|mm|yy|cvv</code> (multiple lines for bulk check).", parse_mode="HTML")


    ko_msg = None
    ccs_to_check = []

    if '\n' in full_input and ENABLE_GROUP_CHECK:
        ccs_to_check = extract_ccs_from_line(full_input)
        if not ccs_to_check:
            return bot.reply_to(message, "❌ <b>No Valid Cards Detected</b>\n\nProvide card details in <code>cc|mm|yy|cvv</code> format, one per line for bulk check.", parse_mode="HTML")
        ko_msg = bot.reply_to(message, f"💳 <b>Bulk Multiple Card Check Initiated</b> ⏳\n\nChecking <code>{len(ccs_to_check)}</code> cards...", parse_mode="HTML").message_id

    else:
        return bot.reply_to(message, "❌ <b>Invalid Input for Bulk Check</b>\n\nUse multiple lines with <code>cc|mm|yy|cvv</code> format for bulk checking with /mchk.", parse_mode="HTML")


    dd = 0
    live = 0
    incorrect = 0
    checked_count = 0
    session = manage_session_file()
    if not session:
        return bot.reply_to(message, "❌ <b>Session Error</b>\n\nFailed to create session. Please try again later.", parse_mode="HTML")
    gate_function = get_gate_function_for_user(user_id)
    gate_name_preference = get_user_gate_preference(user_id)
    gate_name_display = gate_name_preference.upper().replace("AUTH", "AUTH").replace("STRIPE2", "2$").replace("STRIPE4", "4$")


    for cc in ccs_to_check:
        if handle_stop_signal(message.chat.id, ko_msg):
            return

        if CREDIT_SYSTEM_ENABLED:
            if not deduct_credits(user_id):
                if ko_msg:
                    bot.edit_message_text(chat_id=message.chat.id, message_id=ko_msg, text=f"🚫 <b>Credits Exhausted</b>\n\nBulk check stopped after <code>{checked_count}</code> cards.\nRedeem credits or purchase a plan.\nCredits left: <code>{get_user_credits(user_id)}</code>", parse_mode="HTML")
                else:
                    bot.reply_to(message, f"🚫 <b>Credits Exhausted</b>\n\nCheck stopped.\nRedeem credits or purchase a plan.\nCredits left: <code>{get_user_credits(user_id)}</code>", parse_mode="HTML")
                return

        checked_count += 1

        try:
            data = requests.get('https://bins.antipublic.cc/bins/' + cc[:6]).json() if DETAILED_BIN_INFO else {}
        except:
            data = {}
        brand = data.get('brand', 'Unknown').lower()
        card_type = data.get('type', 'Unknown')
        country = data.get('country_name', 'Unknown')
        country_flag = data.get('country_flag', 'Unknown')
        bank = data.get('bank', 'Unknown')
        card_brand_display = CARD_BRANDS.get(brand, brand.capitalize()) if DISPLAY_CARD_BRAND else brand.capitalize()

        start_time = time.time()
        last = str(gate_function(session, cc.strip()))
        update_user_stats(user_id, last.split(" ")[0])
        end_time = time.time()
        execution_time = end_time - start_time

        msg_output = f"""
<a href='https://envs.sh/smD.webp'>-</a> 💳 <b>Ｃａｒｄ Ｃｈｅｃｋ Ｒｅｓｕｌｔ</b> 💳
<a href='https://t.me/+GdWapjhiAG05OTk1'>┏━━━━━━━━━━━⍟</a>
<a href='https://t.me/+GdWapjhiAG05OTk1'>┃</a><b>💳 ＣＣ:</b> <code>{cc}</code><a href='https://t.me/+GdWapjhiAG05OTk1'>┗━━━━━━━⊛</a>
<a href='https://t.me/+GdWapjhiAG05OTk1'>-</a> ⚡ 𝐆𝐚𝐭𝐞𝐰𝐚𝐲: ⤿ {gate_name_display} 🟢 ⤾
<a href='https://t.me/+GdWapjhiAG05OTk1'>-</a> ✅ Ｒｅｓｐｏｎｓｅ: ⤿ {last} ⤾

<a href='https://envs.sh/smD.webp'>-</a> ℹ️ <b>Ｉｎｆｏ</b>: <code>{cc[:6]}-{card_type} - {card_brand_display}</code>
<a href='https://t.me/+GdWapjhiAG05OTk1'>-</a> 🗺️ 𝐂𝐨𝐮𝐧𝐭𝐫𝐲: <code>{country} - {country_flag}</code>
<a href='https://t.me/+GdWapjhiAG05OTk1'>-</a> 🏦 Ｂａｎｋ: <code>{bank}</code>

<a href='https://t.me/+GdWapjhiAG05OTk1'>-</a> ⏱️ Ｔｉｍｅ: <code>{round(execution_time, 1)} 𝐬𝐞𝐜</code>
<a href='https://t.me/+GdWapjhiAG05OTk1'>-</a> 🤖 Ｂｏｔ Ｂｙ: <a href='https://t.me/+GdWapjhiAG05OTk1'>Crimson </a>"""

        bot.send_message(message.chat.id, msg_output, parse_mode="HTML", disable_web_page_preview=True) # Send result immediately

        if 'APPROVED ✅' in last or 'CVV ✅' in last:
            live += 1
        elif 'CCN ✅' in last:
            incorrect+=1
        elif 'DECLINED ❌' in last or 'EXPIRED ❌' in last or 'Error' in last:
            dd += 1

        bulk_update_text = f'''📝 <b>Bulk Checking in Progress...</b> 📝
🤖 𝗕𝘆 ➜ <a href='https://t.me/+GdWapjhiAG05OTk1'>Crimson </a>

✅ 𝐀𝐏𝐏𝐑𝐎𝐕𝐄𝐃 : [ {live} ]
⚠️ 𝐅𝐀𝐊𝐄 𝐂𝐀𝐑𝐃 : [ {incorrect} ]
❌ 𝐃𝐄𝐂𝐋𝐈𝐍𝐄𝐃 : [ {dd} ]
🎉 𝐓𝐎𝐓𝐀𝐋    :  [ {checked_count} ]'''

        try:
            bot.edit_message_text(chat_id=message.chat.id, message_id=ko_msg, text=bulk_update_text, parse_mode="HTML", disable_web_page_preview=True)
        except Exception as e:
            print(f"Error editing bulk message: {e}")


    try:
        bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=ko_msg,
            text='📝 𝗕𝗨𝗟𝗞 𝗖𝗛𝗘𝗖𝗞 𝗖𝗢𝗠𝗣𝗟𝗘𝗧𝗘𝗗 ✅\n🤖 𝗕𝗢𝗧 𝗕𝗬 ➜ @CrImSon_WoLf777', parse_mode="HTML", disable_web_page_preview=True
        )
    except Exception as e:
        print(f"Error editing final bulk message: {e}")


@bot.message_handler(commands=['cclookup'])
def cclookup_command(message):
    if not is_private_chat(message): # Modified condition to allow in groups
        if not is_bot_mentioned(BOT_USERNAME, message):
            return
    if not ensure_registered(message): return
    try:
        cc_number = message.text.split()[1]
        if not re.match(r'^\d{6,}$', cc_number): # Match at least 6 digits for BIN lookup
            raise ValueError("Invalid Card Number format")

        bin_input = cc_number[:6] # Get the first 6 digits for BIN lookup

        try:
            data = requests.get(f'https://bins.antipublic.cc/bins/{bin_input}').json()
        except:
            return bot.reply_to(message, "❌ <b>Card Lookup Failed</b>\n\nCould not retrieve card information. Please try again later.", parse_mode="HTML")

        if not data:
            return bot.reply_to(message, f"ℹ️ <b>Card Info</b> ℹ️\n\nNo detailed information found for card starting with <code>{bin_input}</code>.", parse_mode="HTML")

        card_info_text = f"""
ℹ️ <b>Card Info Lookup</b> ℹ️
<a href='https://t.me/+GdWapjhiAG05OTk1'>┏━━━━━━━━━━━⍟</a>
<a href='https://t.me/+GdWapjhiAG05OTk1'>┃</a>
<b>💳 Brand:</b> <code>{data.get('brand', 'N/A')}</code>
<b>🏦 Bank:</b> <code>{data.get('bank', 'N/A')}</code>
<b>🏛️ Country:</b> <code>{data.get('country_name', 'N/A')} {data.get('country_flag', '')}</code>
<b>⌨️ Type:</b> <code>{data.get('type', 'N/A')}</code>
<b>🎚️ Level:</b> <code>{data.get('level', 'N/A')}</code>
<b>ℹ️ Prepaid:</b> <code>{'Yes' if data.get('prepaid') else 'No'}</code><a href='https://t.me/+GdWapjhiAG05OTk1'>┗━━━━━━━⊛</a>
"""

        bot.reply_to(message, card_info_text, parse_mode="HTML", disable_web_page_preview=True)

    except IndexError:
        bot.reply_to(message, "❌ <b>Card Number Required</b>\n\nUsage: <code>/cclookup [cc]</code>\nPlease provide a card number (at least first 6 digits).", parse_mode="HTML")
    except ValueError as e:
        bot.reply_to(message, f"❌ <b>Invalid Input</b>\n\n{e}\n\nUsage: <code>/cclookup [cc]</code> (Card number must be at least 6 digits).", parse_mode="HTML")
    except Exception as e:
        print(f"Error processing /cclookup command: {e}")
        bot.reply_to(message, "❌ <b>Error retrieving card information.</b> Please contact support.", parse_mode="HTML")

@bot.message_handler(commands=['setgate'])
def setgate_command(message):
    if not is_private_chat(message): # Modified condition to allow in groups
        if not is_bot_mentioned(BOT_USERNAME, message):
            return
    admin_user_id = message.chat.id
    if not is_admin(admin_user_id):
        return bot.reply_to(message, "🚫 Admin command only. Access Denied.", parse_mode="HTML")

    log_admin_command(admin_user_id, "setgate", message.text)

    try:
        gate_name = message.text.split()[1].lower()
        if gate_name not in ["auth", "stripe2", "stripe4"]:
            raise ValueError("Invalid gate name")
        global DEFAULT_GATE
        DEFAULT_GATE = gate_name
        bot.reply_to(message, f"✅ <b>Default Gateway Updated</b>\n\nDefault gateway for new users set to: <code>{gate_name.capitalize()}</code>.", parse_mode="HTML")

    except IndexError:
        bot.reply_to(message, "❌ <b>Gate Name Required</b>\n\nUsage: <code>/setgate [gate]</code>\nAvailable gates: <code>auth</code>, <code>stripe2</code>, <code>stripe4</code>", parse_mode="HTML")
    except ValueError as e:
        bot.reply_to(message, f"❌ <b>Invalid Input</b>\n\n{e}\n\nUsage: <code>/setgate [gate]</code>\nAvailable gates: <code>auth</code>, <code>stripe2</code>, <code>stripe4</code>", parse_mode="HTML")
    except Exception as e:
        print(f"Error setting default gate: {e}")
        bot.reply_to(message, "❌ <b>Error setting default gateway.</b> Please contact support.", parse_mode="HTML")


@bot.message_handler(commands=['broadcast'])
def broadcast_command(message):
    if not is_private_chat(message): # Modified condition to allow in groups
        if not is_bot_mentioned(BOT_USERNAME, message):
            return
    if not ensure_registered(message): return
    user_id = message.chat.id
    if not is_admin(user_id):
        return bot.reply_to(message, "🚫 Admin command only. Access Denied.", parse_mode="HTML")

    log_admin_command(user_id, "broadcast", message.text)

    try:
        text = message.text.split(maxsplit=1)[1]
    except IndexError:
        return bot.reply_to(message, "❌ <b>Broadcast Message Required</b>\n\nUsage: <code>/broadcast message</code>\nPlease provide the message content to broadcast.", parse_mode="HTML")

    all_user_ids = get_all_user_ids()

    success_count = 0
    failure_count = 0

    for user_id in all_user_ids:
        if user_id in BANNED_USERS:
            continue
        try:
            bot.send_message(user_id, text, parse_mode="HTML", disable_web_page_preview=True)
            success_count += 1
            time.sleep(0.1)
        except Exception as e:
            print(f"Failed to send message to user {user_id}: {e}")
            failure_count += 1

    bot.reply_to(message, f"✅ <b>Broadcast Completed</b>\n\nMessage broadcast to {success_count} users.\n{failure_count} users could not be reached.", parse_mode="HTML")

@bot.message_handler(commands=['add_credits'])
def add_credits_command(message):
    if not is_private_chat(message): # Modified condition to allow in groups
        if not is_bot_mentioned(BOT_USERNAME, message):
            return
    if not ensure_registered(message) or not CREDIT_SYSTEM_ENABLED: return
    user_id = message.chat.id
    if not is_admin(user_id):
        return bot.reply_to(message, "🚫 Admin command only. Access Denied.", parse_mode="HTML")
        return

    log_admin_command(user_id, "add_credits", message.text)

    try:
        args = message.text.split()
        if len(args) != 3:
            raise ValueError("Invalid number of arguments")
        target_user_id = int(args[1])
        credits_to_add = int(args[2])

        if credits_to_add <= 0:
            raise ValueError("Credits to add must be a positive number.")

        add_credits_to_user(target_user_id, credits_to_add)
        bot.reply_to(message, f"✅ <b>Credits Added</b>\n\nSuccessfully added <code>{credits_to_add}</code> credits to user ID <code>{target_user_id}</code>.", parse_mode="HTML")

    except ValueError as e:
        return bot.reply_to(message, f"❌ <b>Usage Error</b>\n\nUsage: <code>/add_credits user_id amount</code> (user_id and amount must be integers > 0).\n\nDetails: {e}", parse_mode="HTML")
    except Exception as e:
        print(f"Error adding credits: {e}")
        return bot.reply_to(message, "❌ <b>Error adding credits.</b> Please contact support.", parse_mode="HTML")

@bot.message_handler(commands=['setcredits'])
def set_credits_command(message):
    if not is_private_chat(message): # Modified condition to allow in groups
        if not is_bot_mentioned(BOT_USERNAME, message):
            return
    if not ensure_registered(message) or not CREDIT_SYSTEM_ENABLED: return
    admin_user_id = message.chat.id
    if not is_admin(admin_user_id):
        return bot.reply_to(message, "🚫 Admin command only. Access Denied.", parse_mode="HTML")

    log_admin_command(admin_user_id, "setcredits", message.text)

    try:
        args = message.text.split()
        if len(args) != 3:
            raise ValueError("User ID and credit amount required.")
        target_user_id = int(args[1])
        credits_to_set = int(args[2])

        if credits_to_set < 0:
            raise ValueError("Credits must be a non-negative number.")

        user_data = _load_user_data()
        user_id_str = str(target_user_id)
        if user_id_str not in user_data:
            return bot.reply_to(message, f"❌ <b>User Not Found</b>\n\nUser ID <code>{target_user_id}</code> is not registered.", parse_mode="HTML")

        user_data[user_id_str]['credits'] = credits_to_set
        _save_user_data(user_data)
        bot.reply_to(message, f"✅ <b>Credits Set</b>\n\nUser <code>{target_user_id}</code> credits set to <code>{credits_to_set}</code>.", parse_mode="HTML")

    except ValueError as e:
        return bot.reply_to(message, f"❌ <b>Usage Error</b>\n\nUsage: <code>/setcredits user_id credits</code> (credits must be non-negative integer).\n\nDetails: {e}", parse_mode="HTML")
    except Exception as e:
        print(f"Error setting credits: {e}")
        return bot.reply_to(message, "❌ <b>Error setting credits.</b> Please contact support.", parse_mode="HTML")

@bot.message_handler(commands=['setpremium'])
def set_premium_command(message):
    if not is_private_chat(message): # Modified condition to allow in groups
        if not is_bot_mentioned(BOT_USERNAME, message):
            return
    if not ensure_registered(message): return
    admin_user_id = message.chat.id
    if not is_admin(admin_user_id):
        return bot.reply_to(message, "🚫 Admin command only. Access Denied.", parse_mode="HTML")

    log_admin_command(admin_user_id, "setpremium", message.text)

    try:
        args = message.text.split()
        if len(args) != 3:
            raise ValueError("User ID and premium status (true/false) required.")
        target_user_id = int(args[1])
        premium_status_str = args[2].lower()

        if premium_status_str not in ['true', 'false']:
            raise ValueError("Premium status must be 'true' or 'false'.")
        premium_status = premium_status_str == 'true'

        user_data = _load_user_data()
        user_id_str = str(target_user_id)
        if user_id_str not in user_data:
            return bot.reply_to(message, f"❌ <b>User Not Found</b>\n\nUser ID <code>{target_user_id}</code> is not registered.", parse_mode="HTML")

        user_data[user_id_str]['is_premium'] = premium_status
        _save_user_data(user_data)
        status_display = "Premium Enabled" if premium_status else "Premium Disabled"
        bot.reply_to(message, f"✅ <b>Premium Status Updated</b>\n\nUser <code>{target_user_id}</code> - {status_display}.", parse_mode="HTML")

    except ValueError as e:
        return bot.reply_to(message, f"❌ <b>Usage Error</b>\n\nUsage: <code>/setpremium user_id true/false</code> (status as 'true' or 'false').\n\nDetails: {e}", parse_mode="HTML")
    except Exception as e:
        print(f"Error setting premium status: {e}")
        return bot.reply_to(message, "❌ <b>Error setting premium status.</b> Please contact support.", parse_mode="HTML")

@bot.message_handler(commands=['userinfo'])
def userinfo_command(message):
    if not is_private_chat(message): # Modified condition to allow in groups
        if not is_bot_mentioned(BOT_USERNAME, message):
            return
    if not ensure_registered(message): return
    user_id = message.chat.id
    if not is_admin(user_id):
        return bot.reply_to(message, "🚫 Admin command only. Access Denied.", parse_mode="HTML")

    log_admin_command(user_id, "userinfo", message.text)

    try:
        args = message.text.split()
        if len(args) != 2:
            raise ValueError("User ID not specified")
        target_user_id = int(args[1])

        user_credits = get_user_credits(target_user_id) if CREDIT_SYSTEM_ENABLED else "Unlimited"
        user_stats = get_user_stats(target_user_id) or {'approved': 0, 'declined': 0, 'ccn': 0, 'cvv': 0}
        user_gate_preference = get_user_gate_preference(target_user_id).capitalize() or DEFAULT_GATE.capitalize() # Show default if no preference
        is_premium_user = is_premium(target_user_id)
        premium_status = "✅ Premium" if is_premium_user else "🆓 Free"
        credits_display = user_credits if not isinstance(credits, str) else "Unlimited"

        user_info_text = f"""
👤 <b>User Information Panel</b> 👤
<a href='https://t.me/+GdWapjhiAG05OTk1'>┏━━━━━━━━━━━⍟</a>
<a href='https://t.me/+GdWapjhiAG05OTk1'>┃</a><b>👤 User ID</b>: <code>{target_user_id}</code><a href='https://t.me/+GdWapjhiAG05OTk1'>┗━━━━━━━⊛</a>
<a href='https://t.me/+GdWapjhiAG05OTk1'>-</a> ⭐ <b>𝗣𝗿𝗲𝗺𝗶𝘂𝗺</b>: <code>{premium_status}</code>"""
        if CREDIT_SYSTEM_ENABLED:
             user_info_text += f"\n<a href='https://t.me/+GdWapjhiAG05OTk1'>-</a> 💰 <b>𝐂𝐫𝐞𝐝𝐢𝐭𝐬</b>: <code>{credits_display}</code>"
        user_info_text += f"""
<a href='https://t.me/+GdWapjhiAG05OTk1'>-</a> ⚙️ <b>𝐆𝐚𝐭𝐞</b>: <code>{user_gate_preference}</code>

📊 <b>Ｃｈｅｃｋ Ｓｔａｔｓ</b>:
<a href='https://t.me/+GdWapjhiAG05OTk1'>-</a> ✅ <b>𝐀𝐩𝐩𝐫𝐨𝐯𝐞𝐝</b>: <code>{user_stats.get('approved', 0)}</code>
<a href='https://t.me/+GdWapjhiAG05OTk1'>-</a> ❌ <b>𝐃𝐞𝐜𝐥𝐢𝐧𝐞𝐝</b>: <code>{user_stats.get('declined', 0)}</code>
<a href='https://t.me/+GdWapjhiAG05OTk1'>-</a> ⚠️ <b>𝐂𝐂𝐍</b>: <code>{user_stats.get('ccn', 0)}</code>
<a href='https://t.me/+GdWapjhiAG05OTk1'>-</a> ✅ <b>𝐂𝐕𝐕</b>: <code>{user_stats.get('cvv', 0)}</code>
"""

        bot.reply_to(message, user_info_text, parse_mode="HTML", disable_web_page_preview=True)

    except ValueError:
        return bot.reply_to(message, "❌ <b>Usage Error: User ID Required</b>\n\nUsage: <code>/userinfo user_id</code> (user_id must be an integer)", parse_mode="HTML")
    except Exception as e:
        print(f"Error getting user info: {e}")
        return bot.reply_to(message, "❌ <b>Error retrieving user info.</b> Please contact support.", parse_mode="HTML")

@bot.message_handler(commands=['add'])
def add_admin_command(message):
    if not is_private_chat(message): # Modified condition to allow in groups
        if not is_bot_mentioned(BOT_USERNAME, message):
            return
    if not ensure_registered(message): return
    admin_user_id = message.chat.id
    if not is_admin(admin_user_id):
        return bot.reply_to(message, "🚫 Admin command only. Access Denied.", parse_mode="HTML")

    log_admin_command(admin_user_id, "add", message.text)

    try:
        args = message.text.split()
        if len(args) != 2:
            raise ValueError("User ID to add as admin not specified")
        target_user_id = int(args[1])

        if add_admin_user(target_user_id):
            bot.reply_to(message, f"✅ <b>Admin Privileges Granted</b>\n\nUser ID <code>{target_user_id}</code> added to the admin list.", parse_mode="HTML")
        else:
            bot.reply_to(message, f"⚠️ <b>Already Admin</b>\n\nUser ID <code>{target_user_id}</code> is already an admin.", parse_mode="HTML")

    except ValueError:
        return bot.reply_to(message, "❌ <b>Usage Error: User ID Required</b>\n\nUsage: <code>/add user_id</code> (user_id must be an integer)", parse_mode="HTML")
    except Exception as e:
        print(f"Error adding admin: {e}")
        return bot.reply_to(message, "❌ <b>Error adding admin.</b> Contact support.", parse_mode="HTML")

@bot.message_handler(commands=['remove'])
def remove_admin_command(message):
    if not is_private_chat(message): # Modified condition to allow in groups
        if not is_bot_mentioned(BOT_USERNAME, message):
            return
    if not ensure_registered(message): return
    admin_user_id = message.chat.id
    if not is_admin(admin_user_id):
        return bot.reply_to(message, "🚫 Admin command only. Access Denied.", parse_mode="HTML")

    log_admin_command(admin_user_id, "remove", message.text)

    try:
        args = message.text.split()
        if len(args) != 2:
            raise ValueError("User ID to remove from admins not specified")
        target_user_id = int(args[1])

        if remove_admin_user(target_user_id):
            bot.reply_to(message, f"✅ <b>Admin Privileges Revoked</b>\n\nUser ID <code>{target_user_id}</code> removed from the admin list.", parse_mode="HTML")
        else:
            bot.reply_to(message, f"⚠️ <b>Not an Admin or Bot Owner</b>\n\nUser ID <code>{target_user_id}</code> is not an admin or cannot be removed (bot owner).", parse_mode="HTML")

    except ValueError:
        return bot.reply_to(message, "❌ <b>Usage Error: User ID Required</b>\n\nUsage: <code>/remove user_id</code> (user_id must be an integer)", parse_mode="HTML")
    except Exception as e:
        print(f"Error removing admin: {e}")
        return bot.reply_to(message, "❌ <b>Error removing admin.</b> Contact support.", parse_mode="HTML")

@bot.message_handler(commands=['listadmins'])
def list_admins_command(message):
    if not is_private_chat(message): # Modified condition to allow in groups
        if not is_bot_mentioned(BOT_USERNAME, message):
            return
    if not ensure_registered(message): return
    admin_user_id = message.chat.id
    if not is_admin(admin_user_id):
        return bot.reply_to(message, "🚫 Admin command only. Access Denied.", parse_mode="HTML")

    log_admin_command(admin_user_id, "listadmins")

    admin_list = get_admin_list()
    admin_text = "🛡️ <b>Current Admins</b> 🛡️\n<a href='https://t.me/+GdWapjhiAG05OTk1'>┏━━━━━━━━━━━⍟</a>\n<a href='https://t.me/+GdWapjhiAG05OTk1'>┃</a>\n"
    if admin_list:
        for admin_id in admin_list:
            admin_text += f"- <code>{admin_id}</code>\n"
    else:
        admin_text += "No admins added yet.\n"
    admin_text += "<a href='https://t.me/+GdWapjhiAG05OTk1'>┗━━━━━━━⊛</a>"
    bot.reply_to(message, admin_text, parse_mode="HTML")

@bot.message_handler(commands=['ban'])
def ban_user_command(message):
    if not is_private_chat(message): # Modified condition to allow in groups
        if not is_bot_mentioned(BOT_USERNAME, message):
            return
    if not ensure_registered(message): return
    admin_user_id = message.chat.id
    if not is_admin(admin_user_id):
        return bot.reply_to(message, "🚫 Admin command only. Access Denied.", parse_mode="HTML")

    log_admin_command(admin_user_id, "ban", message.text)

    try:
        args = message.text.split()
        if len(args) != 2:
            raise ValueError("User ID to ban not specified")
        target_user_id = int(args[1])

        if target_user_id in get_admin_list():
            return bot.reply_to(message, "🚫 Cannot ban another admin.", parse_mode="HTML")

        BANNED_USERS.append(target_user_id)
        bot.reply_to(message, f"✅ <b>User Banned</b>\n\nUser ID <code>{target_user_id}</code> has been banned from using the bot.", parse_mode="HTML")

    except ValueError:
        return bot.reply_to(message, "❌ <b>Usage Error: User ID Required</b>\n\nUsage: <code>/ban user_id</code> (user_id must be an integer)", parse_mode="HTML")
    except Exception as e:
        print(f"Error banning user: {e}")
        return bot.reply_to(message, "❌ <b>Error banning user.</b> Please contact support.", parse_mode="HTML")

@bot.message_handler(commands=['unban'])
def unban_user_command(message):
    if not is_private_chat(message): # Modified condition to allow in groups
        if not is_bot_mentioned(BOT_USERNAME, message):
            return
    if not ensure_registered(message): return
    admin_user_id = message.chat.id
    if not is_admin(admin_user_id):
        return bot.reply_to(message, "🚫 Admin command only. Access Denied.", parse_mode="HTML")

    log_admin_command(admin_user_id, "unban", message.text)

    try:
        args = message.text.split()
        if len(args) != 2:
            raise ValueError("User ID to unban not specified")
        target_user_id = int(args[1])

        if target_user_id in BANNED_USERS:
            BANNED_USERS.remove(target_user_id)
            bot.reply_to(message, f"✅ <b>User Unbanned</b>\n\nUser ID <code>{target_user_id}</code> has been unbanned.", parse_mode="HTML")
        else:
            bot.reply_to(message, f"⚠️ <b>User Not Banned</b>\n\nUser ID <code>{target_user_id}</code> was not found in the ban list.", parse_mode="HTML")

    except ValueError:
        return bot.reply_to(message, "❌ <b>Usage Error: User ID Required</b>\n\nUsage: <code>/unban user_id</code> (user_id must be an integer)", parse_mode="HTML")
    except Exception as e:
        print(f"Error unbanning user: {e}")
        return bot.reply_to(message, "❌ <b>Error unbanning user.</b> Please contact support.", parse_mode="HTML")

@bot.message_handler(commands=['unbanall'])
def unbanall_command(message):
    if not is_private_chat(message): # Modified condition to allow in groups
        if not is_bot_mentioned(BOT_USERNAME, message):
            return
    if not ensure_registered(message): return
    admin_user_id = message.chat.id
    if not is_admin(admin_user_id):
        return bot.reply_to(message, "🚫 Admin command only. Access Denied.", parse_mode="HTML")

    log_admin_command(admin_user_id, "unbanall")

    global BANNED_USERS
    users_unbanned = len(BANNED_USERS)
    BANNED_USERS = []
    bot.reply_to(message, f"✅ <b>All Users Unbanned</b>\n\nSuccessfully unbanned <code>{users_unbanned}</code> users.", parse_mode="HTML")

@bot.message_handler(commands=['botstats'])
def botstats_command(message):
    if not is_private_chat(message): # Modified condition to allow in groups
        if not is_bot_mentioned(BOT_USERNAME, message):
            return
    if not ensure_registered(message): return
    admin_user_id = message.chat.id
    if not is_admin(admin_user_id):
        return bot.reply_to(message, "🚫 Admin command only. Access Denied.", parse_mode="HTML")

    log_admin_command(admin_user_id, "botstats")

    all_user_ids = get_all_user_ids()
    total_users = len(all_user_ids)
    admin_count = len(get_admin_list())
    banned_count = len(BANNED_USERS)

    stats_text = f"""
📊 <b>Bot Statistics</b> 📊
<a href='https://t.me/+GdWapjhiAG05OTk1'>┏━━━━━━━━━━━⍟</a>
<a href='https://t.me/+GdWapjhiAG05OTk1'>┃</a><b>🤖 Bot Version</b>: <code>{BOT_VERSION}</code><a href='https://t.me/+GdWapjhiAG05OTk1'>┗━━━━━━━⊛</a>
<a href='https://t.me/+GdWapjhiAG05OTk1'>-</a> 👥 <b>Total Users</b>: <code>{total_users}</code>
<a href='https://t.me/+GdWapjhiAG05OTk1'>-</a> 🛡️ <b>Total Admins</b>: <code>{admin_count}</code>
<a href='https://t.me/+GdWapjhiAG05OTk1'>-</a> 🚫 <b>Banned Users</b>: <code>{banned_count}</code>
<a href='https://t.me/+GdWapjhiAG05OTk1'>-</a> ✅ <b>Referral System</b>: <code>{'Enabled' if REFERRAL_SYSTEM_ENABLED else 'Disabled'}</code>
<a href='https://t.me/+GdWapjhiAG05OTk1'>-</a> 💰 <b>Credit System</b>: <code>{'Enabled' if CREDIT_SYSTEM_ENABLED else 'Disabled'}</code>
<a href='https://t.me/+GdWapjhiAG05OTk1'>-</a> 🎁 <b>Redeem Codes</b>: <code>{'Enabled' if REDEEM_SYSTEM_ENABLED else 'Disabled'}</code>
<a href='https://t.me/+GdWapjhiAG05OTk1'>-</a> 📝 <b>Group Check</b>: <code>{'Enabled' if ENABLE_GROUP_CHECK else 'Disabled'}</code>
<a href='https://t.me/+GdWapjhiAG05OTk1'>-</a> ℹ️  <b>Detailed BIN</b>: <code>{'Enabled' if DETAILED_BIN_INFO else 'Disabled'}</code>
<a href='https://t.me/+GdWapjhiAG05OTk1'>-</a> 💳 <b>Card Brands</b>: <code>{'Enabled' if DISPLAY_CARD_BRAND else 'Disabled'}</code>
<a href='https://t.me/+GdWapjhiAG05OTk1'>-</a> 🛡️ <b>Default Gate</b>: <code>{DEFAULT_GATE.capitalize()}</code>
"""
    bot.reply_to(message, stats_text, parse_mode="HTML", disable_web_page_preview=True)

@bot.message_handler(commands=['getlog'])
def getlog_command(message):
    if not is_private_chat(message): # Modified condition to allow in groups
        if not is_bot_mentioned(BOT_USERNAME, message):
            return
    if not ensure_registered(message): return
    admin_user_id = message.chat.id
    if not is_admin(admin_user_id):
        return bot.reply_to(message, "🚫 Admin command only. Access Denied.", parse_mode="HTML")

    log_admin_command(admin_user_id, "getlog", message.text)

    try:
        args = message.text.split()
        lines_to_get = 10
        if len(args) > 1:
            lines_to_get = int(args[1])
            if lines_to_get <= 0 or lines_to_get > 100:
                lines_to_get = 10
        with open(ADMIN_COMMAND_LOG_FILE, "r") as logfile:
            logs = logfile.readlines()
        if not logs:
            return bot.reply_to(message, "📜 <b>Admin Command Logs</b> 📜\n\nNo admin commands logged yet.", parse_mode="HTML")

        log_text = f"📜 <b>Admin Command Logs (Last {lines_to_get} entries)</b> 📜\n<a href='https://t.me/+GdWapjhiAG05OTk1'>┏━━━━━━━━━━━⍟</a>\n<a href='https://t.me/+GdWapjhiAG05OTk1'>┃</a>\n"
        for log_entry in logs[-lines_to_get:]:
            log_text += log_entry
        log_text += "<a href='https://t.me/+GdWapjhiAG05OTk1'>┗━━━━━━━⊛</a>"
        bot.reply_to(message, log_text, parse_mode="HTML")

    except FileNotFoundError:
        bot.reply_to(message, "📜 <b>Admin Command Logs</b> 📜\n\nAdmin log file not found.", parse_mode="HTML")
    except ValueError:
        bot.reply_to(message, "❌ <b>Usage Error: Invalid Number of Lines</b>\n\nUsage: <code>/getlog [lines]</code> (lines must be a positive integer, max 100).", parse_mode="HTML")
    except Exception as e:
        print(f"Error reading admin logs: {e}")
        bot.reply_to(message, "❌ <b>Error reading admin logs.</b> Contact support.", parse_mode="HTML")

@bot.message_handler(commands=['clearlogs'])
def clearlogs_command(message):
    if not is_private_chat(message): # Modified condition to allow in groups
        if not is_bot_mentioned(BOT_USERNAME, message):
            return
    if not ensure_registered(message): return
    admin_user_id = message.chat.id
    if not is_admin(admin_user_id):
        return bot.reply_to(message, "🚫 Admin command only. Access Denied.", parse_mode="HTML")

    log_admin_command(admin_user_id, "clearlogs")

    try:
        open(ADMIN_COMMAND_LOG_FILE, 'w').close()
        bot.reply_to(message, "✅ <b>Admin Command Logs Cleared!</b> 📜\n\nAll admin command logs have been permanently deleted.", parse_mode="HTML")
    except Exception as e:
        print(f"Error clearing admin logs: {e}")
        bot.reply_to(message, "❌ <b>Error clearing admin logs.</b> Please contact support.", parse_mode="HTML")

@bot.message_handler(commands=['backupdata'])
def backupdata_command(message):
    if not is_private_chat(message): # Modified condition to allow in groups
        if not is_bot_mentioned(BOT_USERNAME, message):
            return
    if not ensure_registered(message): return
    admin_user_id = message.chat.id
    if not is_admin(admin_user_id):
        return bot.reply_to(message, "🚫 Admin command only. Access Denied.", parse_mode="HTML")

    log_admin_command(admin_user_id, "backupdata")

    try:
        user_data = _load_user_data()
        redeem_data = _load_redeem_data()
        admin_ids = get_admin_list()

        backup_filename = f"bot_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        backup_data = {
            "user_data": user_data,
            "redeem_data": redeem_data,
            "admin_ids": admin_ids,
            "referrer_bonus": get_referrer_bonus(),
            "referred_bonus": get_referred_bonus(),
            "default_gate": DEFAULT_GATE # Include default gate in backup
        }

        with open(backup_filename, 'w') as backup_file:
            json.dump(backup_data, backup_file, indent=4)

        bot.send_document(message.chat.id, open(backup_filename, 'rb'), caption=f"✅ <b>Bot Data Backup Created!</b>\n\nBackup filename: <code>{backup_filename}</code>", parse_mode="HTML")
        os.remove(backup_filename)

    except Exception as e:
        print(f"Error creating backup: {e}")
        bot.reply_to(message, "❌ <b>Error creating backup.</b> Please contact support.", parse_mode="HTML")

@bot.message_handler(commands=['send'])
def send_message_command(message):
    if not is_private_chat(message): # Modified condition to allow in groups
        if not is_bot_mentioned(BOT_USERNAME, message):
            return
    if not ensure_registered(message): return
    admin_user_id = message.chat.id
    if not is_admin(admin_user_id):
        return bot.reply_to(message, "🚫 Admin command only. Access Denied.", parse_mode="HTML")

    log_admin_command(admin_user_id, "send", message.text)

    try:
        args = message.text.split(maxsplit=2)
        if len(args) < 3:
            raise ValueError("User ID and message text required.")
        target_user_id = int(args[1])
        message_text = args[2]

        bot.send_message(target_user_id, message_text, parse_mode="HTML", disable_web_page_preview=True)
        bot.reply_to(message, f"✅ <b>Message Sent</b>\n\nMessage sent to user ID <code>{target_user_id}</code>.", parse_mode="HTML")

    except ValueError as e:
        return bot.reply_to(message, f"❌ <b>Usage Error</b>\n\nUsage: <code>/send user_id message</code>\n\nDetails: {e}", parse_mode="HTML")
    except Exception as e:
        print(f"Error sending message: {e}")
        return bot.reply_to(message, "❌ <b>Error sending message.</b> Please contact support.", parse_mode="HTML")

@bot.message_handler(commands=['forward'])
def forward_message_command(message):
    if not is_private_chat(message): # Modified condition to allow in groups
        if not is_bot_mentioned(BOT_USERNAME, message):
            return
    if not ensure_registered(message): return
    admin_user_id = message.chat.id
    if not is_admin(admin_user_id):
        return bot.reply_to(message, "🚫 Admin command only. Access Denied.", parse_mode="HTML")

    log_admin_command(admin_user_id, "forward", message.text)

    try:
        args = message.text.split(maxsplit=2)
        if len(args) < 3:
            raise ValueError("User ID and message ID required.")
        target_user_id = int(args[1])
        message_id_to_forward = int(args[2])

        bot.forward_message(target_user_id, message.chat.id, message_id_to_forward)
        bot.reply_to(message, f"✅ <b>Message Forwarded</b>\n\nMessage ID <code>{message_id_to_forward}</code> forwarded to user ID <code>{target_user_id}</code>.", parse_mode="HTML")

    except ValueError as e:
        return bot.reply_to(message, f"❌ <b>Usage Error</b>\n\nUsage: <code>/forward user_id message_id</code>\n\nDetails: {e}", parse_mode="HTML")
    except Exception as e:
        print(f"Error forwarding message: {e}")
        return bot.reply_to(message, "❌ <b>Error forwarding message.</b> Please contact support.", parse_mode="HTML")

@bot.message_handler(commands=['setgateprice'])
def setgateprice_command(message):
    if not is_private_chat(message): # Modified condition to allow in groups
        if not is_bot_mentioned(BOT_USERNAME, message):
            return
    if not ensure_registered(message): return
    admin_user_id = message.chat.id
    if not is_admin(admin_user_id):
        return bot.reply_to(message, "🚫 Admin command only. Access Denied.", parse_mode="HTML")

    log_admin_command(user_id=admin_user_id, command="setgateprice", args=message.text)

    try:
        args = message.text.split()
        if len(args) != 3:
            raise ValueError("Gate name and price required.")
        gate_name = args[1].lower()
        price = float(args[2])
        if price < 0:
            raise ValueError("Price must be non-negative.")
        bot.reply_to(message, f"✅ <b>Gate Price Set</b>\n\nPrice for gate <code>{gate_name}</code> set to <code>{price}</code>.", parse_mode="HTML")

    except ValueError as e:
        return bot.reply_to(message, f"❌ <b>Usage Error</b>\n\nUsage: <code>/setgateprice gate price</code> (price must be a non-negative number).\n\nDetails: {e}", parse_mode="HTML")
    except Exception as e:
        print(f"Error setting gate price: {e}")
        return bot.reply_to(message, "❌ <b>Error setting gate price.</b> Contact support.", parse_mode="HTML")

@bot.message_handler(commands=['getconfig'])
def getconfig_command(message):
    if not is_private_chat(message): # Modified condition to allow in groups
        if not is_bot_mentioned(BOT_USERNAME, message):
            return
    if not ensure_registered(message): return
    admin_user_id = message.chat.id
    if not is_admin(admin_user_id):
        return bot.reply_to(message, "🚫 Admin command only. Access Denied.", parse_mode="HTML")

    log_admin_command(user_id=admin_user_id, command="getconfig")

    config_text = f"""
⚙️ <b>Bot Configuration</b> ⚙️
<a href='https://t.me/+GdWapjhiAG05OTk1'>┏━━━━━━━━━━━⍟</a>
<a href='https://t.me/+GdWapjhiAG05OTk1'>┃</a>
<b>Bot Version:</b> <code>{BOT_VERSION}</code>
<b>Group Check:</b> <code>{'Enabled' if ENABLE_GROUP_CHECK else 'Disabled'}</code>
<b>Detailed BIN Info:</b> <code>{'Enabled' if DETAILED_BIN_INFO else 'Disabled'}</code>
<b>Display Card Brand:</b> <code>{'Enabled' if DISPLAY_CARD_BRAND else 'Disabled'}</code>
<b>Referral System:</b> <code>{'Enabled' if REFERRAL_SYSTEM_ENABLED else 'Disabled'}</code>
<b>Redeem System:</b> <code>{'Enabled' if REDEEM_SYSTEM_ENABLED else 'Disabled'}</code>
<b>Credit System:</b> <code>{'Enabled' if CREDIT_SYSTEM_ENABLED else 'Disabled'}</code>
<b>Referrer Bonus:</b> <code>{get_referrer_bonus()} credits</code>
<b>Referred Bonus:</b> <code>{get_referred_bonus()} credits</code>
<b>Default Gate:</b> <code>{DEFAULT_GATE.capitalize()}</code>
"""
    bot.reply_to(message, config_text, parse_mode="HTML")

@bot.message_handler(commands=['setconfig'])
def setconfig_command(message):
    if not is_private_chat(message): # Modified condition to allow in groups
        if not is_bot_mentioned(BOT_USERNAME, message):
            return
    if not ensure_registered(message): return
    admin_user_id = message.chat.id
    if not is_admin(admin_user_id):
        return bot.reply_to(message, "🚫 Admin command only. Access Denied.", parse_mode="HTML")

    log_admin_command(user_id=admin_user_id, command="setconfig", args=message.text)

    try:
        args = message.text.split(maxsplit=2)
        if len(args) != 3:
            raise ValueError("Setting name and value required.")
        setting_name = args[1].upper()
        setting_value = args[2].lower()

        global ENABLE_GROUP_CHECK, DETAILED_BIN_INFO, DISPLAY_CARD_BRAND, REFERRAL_SYSTEM_ENABLED, REDEEM_SYSTEM_ENABLED, CREDIT_SYSTEM_ENABLED

        if setting_name == 'ENABLE_GROUP_CHECK':
            ENABLE_GROUP_CHECK = setting_value == 'true'
        elif setting_name == 'DETAILED_BIN_INFO':
            DETAILED_BIN_INFO = setting_value == 'true'
        elif setting_name == 'DISPLAY_CARD_BRAND':
            DISPLAY_CARD_BRAND = setting_value == 'true'
        elif setting_name == 'REFERRAL_SYSTEM_ENABLED':
            REFERRAL_SYSTEM_ENABLED = setting_value == 'true'
        elif setting_name == 'REDEEM_SYSTEM_ENABLED':
            REDEEM_SYSTEM_ENABLED = setting_value == 'true'
        elif setting_name == 'CREDIT_SYSTEM_ENABLED':
            CREDIT_SYSTEM_ENABLED = setting_value == 'true'
        else:
            raise ValueError(f"Invalid setting name: {setting_name}")

        bot.reply_to(message, f"✅ <b>Bot Setting Updated</b>\n\nSetting <code>{setting_name}</code> set to <code>{setting_value}</code>.", parse_mode="HTML")

    except ValueError as e:
        return bot.reply_to(message, f"❌ <b>Usage Error</b>\n\nUsage: <code>/setconfig setting value</code> (value must be true/false).\n\nDetails: {e}", parse_mode="HTML")
    except Exception as e:
        print(f"Error setting bot config: {e}")
        return bot.reply_to(message, "❌ <b>Error setting bot configuration.</b> Contact support.", parse_mode="HTML")

@bot.message_handler(content_types=["document"])
def main(message):
    if not is_private_chat(message):
        if not is_bot_mentioned(BOT_USERNAME, message):
            return
    if not ensure_registered(message): return
    user_id = message.chat.id
    credits = get_user_credits(user_id) if CREDIT_SYSTEM_ENABLED else "Unlimited"

    if CREDIT_SYSTEM_ENABLED and credits != "Unlimited" and credits < 1:
        return bot.reply_to(message, f"🚫 <b>Insufficient Credits</b>\n\nYou have <code>{credits}</code> credits. You need at least 1 credit to perform a check. Redeem or buy more.", parse_mode="HTML")

    dd = 0
    live = 0
    incorrect = 0
    ch = 0
    ko = bot.reply_to(message, "📝 <b>Processing Card File</b>... ⌛").message_id

    try:
        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        ee = downloaded_file.decode('utf-8')
    except telebot.apihelper.ApiException as e:
        bot.edit_message_text(chat_id=message.chat.id, message_id=ko, text=f"❌ <b>File Download Error</b>\n\nCould not download file from Telegram API. Error: {e}")
        print(f"Telegram API Exception during file download: {e}")
        return
    except UnicodeDecodeError as e:
        bot.edit_message_text(chatId=message.chat.id, message_id=ko, text=f"❌ <b>File Encoding Error</b>\n\nCould not decode file as UTF-8. Please ensure the file is in UTF-8 format.")
        print(f"UnicodeDecodeError: {e}")
        return
    except Exception as e:
        bot.edit_message_text(chat_id=message.chat.id, message_id=ko, text=f"❌ <b>File Download Error</b>\n\nCould not download file. Ensure it's valid and try again. Error: {e}")
        print(f"General File Download Error: {e}")
        return


    ccs_to_check = extract_ccs_from_line(ee)
    total = 0
    checked_count = 0
    session = manage_session_file()
    if not session:
        bot.reply_to(message, "❌ <b>Session Error</b>\n\nFailed to start session. Try again later.", parse_mode="HTML")
        return
    gate_function = get_gate_function_for_user(user_id)
    gate_name_preference = get_user_gate_preference(user_id)
    gate_name_display = gate_name_preference.upper().replace("AUTH", "AUTH").replace("stripe2", "2$").replace("stripe4", "4$")


    for cc in ccs_to_check:
        if handle_stop_signal(message.chat.id, ko):
            return

        if CREDIT_SYSTEM_ENABLED:
            if not deduct_credits(user_id):
                bot.edit_message_text(chat_id=message.chat.id, message_id=ko, text=f"🚫 <b>Credits Exhausted</b>\n\nBulk check stopped after <code>{checked_count}</code> cards.\nRedeem or buy more credits. Credits: <code>{get_user_credits(user_id)}</code>", parse_mode="HTML")
                return

        total += 1
        checked_count += 1
        try:
            data = requests.get('https://bins.antipublic.cc/bins/' + cc[:6]).json() if DETAILED_BIN_INFO else {}
        except:
            data = {}
        brand = data.get('brand', 'Unknown').lower()
        card_type = data.get('type', 'Unknown')
        country = data.get('country_name', 'Unknown')
        country_flag = data.get('country_flag', 'Unknown')
        bank = data.get('bank', 'Unknown')
        card_brand_display = CARD_BRANDS.get(brand, brand.capitalize()) if DISPLAY_CARD_BRAND else brand.capitalize()

        start_time = time.time()
        last = str(gate_function(session, cc.strip()))
        update_user_stats(user_id, last.split(" ")[0])

        end_time = time.time()
        execution_time = end_time - start_time

        msg_output = f"""
<a href='https://envs.sh/smD.webp'>-</a> ✅ <b>𝐀𝐏𝐏𝐑𝐎𝐕𝐄𝐃 𝐂𝐀𝐑𝐃</b> ✅
<a href='https://t.me/+GdWapjhiAG05OTk1'>┏━━━━━━━━━━━⍟</a>
<a href='https://t.me/+GdWapjhiAG05OTk1'>┃</a>💳 𝐂𝐂: <code>{cc}</code><a href='t.me/addlist/u2A-7na8YtdhZWVl'>┗━━━━━━━⊛</a>
<a href='https://t.me/+GdWapjhiAG05OTk1'>-</a> ⚡ 𝐆𝐚𝐭𝐞𝐰𝐚𝐲: ⤿ {gate_name_display} 🟢 ⤾
<a href='https://t.me/+GdWapjhiAG05OTk1'>-</a> ✅ 𝐑𝐞𝐬𝐩𝐨𝐧𝐬𝐞: ⤿ {last} ⤾

<a href='https://envs.sh/smD.webp'>-</a> ℹ️ 𝐈𝐧𝐟𝐨: <code>{cc[:6]}-{card_type} - {card_brand_display}</code>
<a href='https://t.me/+GdWapjhiAG05OTk1'>-</a> 🗺️ 𝐂𝐨𝐮𝐧𝐭𝐫𝐲: <code>{country} - {country_flag}</code>
<a href='https://t.me/+GdWapjhiAG05OTk1'>-</a> 🏦 𝐁𝐚𝐧𝐤: <code>{bank}</code>

<a href='https://t.me/+GdWapjhiAG05OTk1'>-</a> ⏱️ 𝐓𝐢𝐦𝐞: <code>{round(execution_time, 1)} 𝐬𝐞𝐜</code>
<a href='https://t.me/+GdWapjhiAG05OTk1'>-</a> 🤖 𝐁𝐨𝐭 𝐀𝐛𝐨𝐮𝐭: <a href='https://t.me/+GdWapjhiAG05OTk1'>Crimson </a>"""

        if 'APPROVED ✅' in last or 'CVV ✅' in last: # Send only approved results
            bot.send_message(message.chat.id, msg_output, parse_mode="HTML", disable_web_page_preview=True)

        if 'APPROVED ✅' in last or 'CVV ✅' in last:
            live += 1
        elif 'CCN ✅' in last:
            incorrect+=1
        elif 'DECLINED ❌' in last or 'EXPIRED ❌' in last or 'Error' in last:
            dd += 1

        bulk_update_text = f'''📝 <b>Processing File...</b> 📝
🤖 𝗕𝘆 ➜ <a href='https://t.me/+GdWapjhiAG05OTk1'>Crimson </a>

✅ 𝐀𝐏𝐏𝐑𝐎𝐕𝐄𝐃 : [ {live} ]
⚠️ 𝐅𝐀𝐊𝐄 𝐂𝐀𝐑𝐃 : [ {incorrect} ]
❌ 𝐃𝐄𝐂𝐋𝐈𝐍𝐄𝐃 : [ {dd} ]
🎉 𝐓𝐎𝐓𝐀𝐋    :  [ {total} ]'''
        try:
            bot.edit_message_text(chat_id=message.chat.id, message_id=ko, text=bulk_update_text, parse_mode="HTML", disable_web_page_preview=True)
        except Exception as e:
            print(f"Error editing bulk message: {e}")

        time.sleep(0.5) # Reduced sleep for faster processing


    bot.send_message(chat_id=message.chat.id, text=f"✅ <b>Bulk Card Check Completed!</b>\n\nChecked <code>{checked_count}</code> cards from document file.\nCredits remaining: <code>{get_user_credits(user_id) if CREDIT_SYSTEM_ENABLED else 'Unlimited'}</code>", parse_mode="HTML")

    try:
        bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=ko,
            text='📝 𝗕𝗨𝗟𝗞 𝗖𝗛𝗘𝗖𝗞 𝗖𝗢𝗠𝗣𝗟𝗘𝗧𝗘𝗗 ✅\n🤖 𝗕𝗢𝗧 𝗕𝗬 ➜ @CrImSon_WoLf777', parse_mode="HTML", disable_web_page_preview=True
        )
    except Exception as e:
        print(f"An error occurred: {e}")

@bot.callback_query_handler(func=lambda call: call.data == 'stop')
def stop_callback(call):
    user_id = call.message.chat.id
    if not is_private_chat(message): # Modified condition to allow in groups
        if not is_bot_mentioned(BOT_USERNAME, call.message):
            return
    file_path = os.path.join(os.getcwd(), 'stop.stop')
    open(file_path, 'a').close()
    bot.answer_callback_query(call.id, "Stopping process...")

def get_all_user_ids():
    user_ids = []
    try:
        with open("user_ids.txt", "r") as f:
            for line in f:
                user_id = line.strip()
                if user_id:
                    user_ids.append(int(user_id))
    except FileNotFoundError:
        print("User ID file not found.")
        return []
    return user_ids

def _get_user_id_from_referral_code(referral_code):
    user_data = _load_user_data()
    for user_id_str, user_info in user_data.items():
        if user_info.get('referral_code') == referral_code:
            return int(user_id_str)
    return None

if __name__ == '__main__':
    logop = f'''━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━bot by @CrImSon_WoLf777 started sucessfully ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━'''
    print(logop)
    bot.polling(non_stop=True)
#--- END OF FILE bot_core.py ---