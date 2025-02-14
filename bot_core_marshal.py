�                   ��
  � d Z  ed�      j                  �       Zee k7  r ed�        ed�        ed�       ddlZddlZddlZddl	Z	ddlm
Z
 ddlZddlZddlZddlZddlmZ d	ad	ad	ad	ad	ad	ad
adZg addlmZmZmZ ddlmZmZm Z m!Z!m"Z"m#Z#m$Z$m%Z%m&Z&m'Z'm(Z(m)Z)m*Z*m+Z+m,Z,m-Z-m.Z.m/Z/m0Z0m1Z1m2Z2 ddl3m4Z4 ddl5m6Z6m7Z7m8Z8m9Z9m:Z:m;Z;m<Z<m=Z=m>Z>m?Z?m@Z@ ddlAmBZBmCZC eBs ed�        ed�        ed�        ej�                  eBd��      ZE e2�       ZFdZGdZHd�d�ZId� ZJd� ZKd� ZLd� ZMd� ZNeEj�                  g d���      d� �       ZPeEj�                  d � �!�      d"� �       ZReEj�                  d#d$g��      d%� �       ZSeEj�                  d&g��      d'� �       ZTeEj�                  d(g��      d)� �       ZUeEj�                  d*g��      d+� �       ZVeEj�                  d,g��      d-� �       ZWeEj�                  d.g��      d/� �       ZXeEj�                  d0g��      d1� �       ZYd2� ZZeEj�                  d3g��      d4� �       Z[eEj�                  d5� �!�      d6� �       Z\eEj�                  d7g��      d8� �       Z]eEj�                  d9g��      d:� �       Z^eEj�                  d;g��      d<� �       Z_eEj�                  d=g��      d>� �       Z`eEj�                  d?g��      d@� �       ZaeEj�                  dAg��      dB� �       ZbdCdDdEdFdGdHdI�ZceEj�                  g dJ���      dK� �       ZdeEj�                  dLg��      dM� �       ZeeEj�                  dNg��      dO� �       ZfeEj�                  dPg��      dQ� �       ZgeEj�                  dRg��      dS� �       ZheEj�                  dTg��      dU� �       ZieEj�                  dVg��      dW� �       ZjeEj�                  dXg��      dY� �       ZkeEj�                  dZg��      d[� �       ZleEj�                  d\g��      d]� �       ZmeEj�                  d^g��      d_� �       ZneEj�                  d`g��      da� �       ZoeEj�                  dbg��      dc� �       ZpeEj�                  ddg��      de� �       ZqeEj�                  dfg��      dg� �       ZreEj�                  dhg��      di� �       ZseEj�                  djg��      dk� �       ZteEj�                  dlg��      dm� �       ZueEj�                  dng��      do� �       ZveEj�                  dpg��      dq� �       ZweEj�                  drg��      ds� �       ZxeEj�                  dtg��      du� �       ZyeEj�                  dvg��      dw� �       ZzeEj�                  dxg�y�      dz� �       Z{eEj�                  d{� �!�      d|� �       Z|d}� Z}d~� Z~d� Ze�d�k(  rd�Z� ee��       eE�j                  d	���       yy)�z	@Enrd6051z'Enter the secret key to start the bot: zInvalid key. Exiting...�   z!Key accepted. Starting the bot...�    N)�types)�datetimeT�authzadmin_logs.txt)�Tele�Tele_stripe2�Tele_stripe4)�get_user_credits�deduct_credits�update_user_stats�get_user_gate_preference�set_user_gate_preference�is_admin�get_user_stats�redeem_credits�generate_redeem_codes�
is_premium�add_credits_to_user�is_registered�register_user�generate_referral_code�get_referrer_bonus�get_referred_bonus�set_referral_bonuses�get_user_referral_link�add_admin_user�remove_admin_user�get_admin_list)�manage_session_file)�extract_ccs_from_line�generate_random_email�generate_username�generate_password�get_card_type_from_bin�generate_address�generate_phone_number�generate_iban�generate_swift�generate_btc_address�generate_usdt_address)�	BOT_TOKEN�	ADMIN_IDSz:CRITICAL ERROR: BOT_TOKEN is not loaded. Bot cannot start.z5Please check config.py and your environment settings.�HTML��
parse_mode�crimsonxcheckerbotzv3.1 Enhanced Editionc                 �  � t        j                  �       j                  d�      }d|� d| � d|� �}|r|d|� �z  }t        t        d�      5 }|j                  |dz   �       d d d �       t        d|� ��       y # 1 sw Y   �xY w)	Nz%Y-%m-%d %H:%M:%S�[z] Admin ID: z, Command: z, Args: �a�
zAdmin Command Logged: )r   �now�strftime�open�ADMIN_COMMAND_LOG_FILE�write�print)�user_id�command�args�	timestamp�log_message�logfiles         �bot_core.py�log_admin_commandrB   3   s�   � �����'�'�(;�<�I��i�[��W�I�[��	�J�K����$��(�(��	�$�c�	*�g����k�D�(�)� 
+�	�"�;�-�
0�1� 
+�	*�s   �	A5�5A>c                 ��  � t        j                  �       }t         j                  j                  t         j                  j	                  |d�      �      rN	 t
        j                  | |d��       	 t        j                  t         j                  j	                  |d�      �       yy# t        $ r}t        d|� ��       Y d }~�Rd }~ww xY w# t        $ r}t        d|� ��       Y d }~yd }~ww xY w)N�	stop.stopu'   STOPPED ✅
BOT BY ➜ @CrImSon_WoLf777��chat_id�
message_id�textzError editing message on stop: zError removing stop file: TF)
�os�getcwd�path�exists�join�bot�edit_message_text�	Exceptionr:   �remove)rF   rG   �current_dir�es       rA   �handle_stop_signalrT   <   s�   � ��)�)�+�K�	�w�w�~�~�b�g�g�l�l�;��<�=�	9��!�!�'�j�Oy�!�z�	4��I�I�b�g�g�l�l�;��<�=� ��� � 	9��3�A�3�7�8�8��	9�� � 	4��.�q�c�2�3�3���	4�s0   �B! �,3C �!	C�*B=�=C�	C&�C!�!C&c                 �`   � t        | �      }|st        }|dk(  rt        S |dk(  rt        S t        S )N�stripe2�stripe4)r   �DEFAULT_GATEr   r	   r   )r;   �gate_preferences     rA   �get_gate_function_for_userrZ   J   s5   � �.�w�7�O��&���)�#���	�I�	%�����    c                 �4   � | j                   j                  dk(  S )N�private)�chat�type)�messages    rA   �is_private_chatra   U   s   � ��<�<���	�)�)r[   c                 ��   � |j                   sy|j                  j                  dv rDd| � �|j                   v xs1 |j                  xr# |j                  j                  j
                  | k(  S y)NF)�group�
supergroup�@T)rH   r^   r_   �reply_to_message�	from_user�username)�bot_usernamer`   s     rA   �is_bot_mentionedrj   X   sr   � ��<�<���|�|���3�3��<�.�!�W�\�\�1�  N�W�5M�5M�  6N�RY�Rj�Rj�Rt�Rt�R}�R}�  BN�  SN�  	N�r[   c                 ��   � | j                   sy| j                   j                  �       d   j                  �       }|j                  d�      r|dd  j                  d�      d   }g d�}||vS y)NFr   �/r   re   )�start�help�register�referral�buy�price�menu�bin�feedback�terms�privacy�ping�cmdsT)rH   �split�lower�
startswith)r`   r<   �command_name�no_reg_commandss       rA   �needs_registration_checkr   _   sk   � ��<�<���l�l� � �"�1�%�+�+�-�G����#���q�r�{�(�(��-�a�0�� S���?�2�2�r[   )rm   rn   rq   rr   rs   ry   )�commandsc                 �  � t        t        | �      st        | �      sy | j                  j                  }| j
                  j                  xs d}t        rt        |�      nd}t        |�      j                  �       xs t        j                  �       }t        |�      rdnd}| j                  j                  �       d   j                  �       }d|v r|j                  d�      d   dd  }n|dd  }|dv r�d	t         � d
|� d|� d�}t#        |�      s|dz  }|dz  }t        r|dz  }t$        r|dz  }t&        r|dz  }|dz  }t)        |�      r|dz  }|d|� d�z  }t        r	|d|� d�z  }|dz  }t*        j-                  | |dd��       y |dv rYd}t/        j0                  �       }	t/        j2                  dd��      }
|	j5                  |
�       t*        j-                  | ||	dd� �       y y )!N�User�	Unlimited�   ✅ Premium�	   🆓 Freer   re   r   )rn   rm   rs   ry   u   
🌟 <b>Crimson Checker Bot u   </b> 🌟

👋 Welcome, <b>z</b>! (u   User)
<a href='https://t.me/+GdWapjhiAG05OTk1'>┏━━━━━━━━━━━⍟</a>
<a href='https://t.me/+GdWapjhiAG05OTk1'>┃</a>
A cutting-edge bot for card checking and more!<a href='https://t.me/+GdWapjhiAG05OTk1'>┗━━━━━━━⊛</a>
u[   🔑 <b>Registration Required!</b>
   - Use /register to unlock the bot's full potential.

u_  
💳 <b>User Commands</b> 💳
<a href='https://t.me/+GdWapjhiAG05OTk1'>┏━━━━━━━━━━━⍟</a>
<a href='https://t.me/+GdWapjhiAG05OTk1'>┃</a>
   •  /chk <code>cc|mm|yy|cvv</code> - Check single card.
   •  /gate - Select payment gateway.
   •  /stats - View your checking stats.
   •  /bin <code>bin</code> - Lookup BIN details.
   •  /gen <code>type</code> - Generate data.
   •  /cclookup <code>cc</code> - Get card info (brand, type etc.).
   •  /feedback <code>message</code> - Send feedback.<a href='https://t.me/+GdWapjhiAG05OTk1'>┗━━━━━━━⊛</a>
u.      •  /credits - Check your credit balance.
u?      •  /redeem <code>code</code> - Redeem credits or premium.
u,      •  /referral - Get your referral link.
u�  
   •  /buy or /price - Credit purchase plans.
   •  /help or /menu or /cmds - Show this menu.

🛠️ <b>Utilities</b> 🛠️
<a href='https://t.me/+GdWapjhiAG05OTk1'>┏━━━━━━━━━━━⍟</a>
<a href='https://t.me/+GdWapjhiAG05OTk1'>┃</a>
   •  /ping - Check bot status.
   •  /terms - View terms of service.
   •  /privacy - View privacy policy.<a href='https://t.me/+GdWapjhiAG05OTk1'>┗━━━━━━━⊛</a>
u�  

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
   •  /add <code>user_id</code> - Add admin.
   •  /remove <code>user_id</code> - Remove admin.
   •  /listadmins - List all admins.
   •  /ban <code>user_id</code> - Ban a user.
   •  /unban <code>user_id</code> - Unban a user.
   •  /unbanall - Unban all users.
   •  /botstats - View bot statistics.
   •  /adminlogs - View admin command logs.
   •  /getlog <code>lines</code> - Get last admin log lines.
   •  /clearlogs - Clear admin logs.
   •  /backupdata - Backup bot data.
   •  /send <code>user_id</code> <code>message</code> - Send direct message.
   •  /forward <code>user_id</code> <code>message_id</code> - Forward message to user.
   •  /setgateprice <code>gate</code> <code>price</code> - Set gate price.
   •  /getconfig - Get bot configuration.
   •  /setconfig <code>setting</code> <code>value</code> - Set bot configuration.<a href='https://t.me/+GdWapjhiAG05OTk1'>┗━━━━━━━⊛</a>
u�   

⚙️ <b>Current Settings</b> ⚙️
<a href='https://t.me/+GdWapjhiAG05OTk1'>┏━━━━━━━━━━━⍟</a>
<a href='https://t.me/+GdWapjhiAG05OTk1'>┃</a>
   •  <b>Gate:</b> <code>�</code>u   
   •  <b>Credits:</b> <code>�H   <a href='https://t.me/+GdWapjhiAG05OTk1'>┗━━━━━━━⊛</a>r-   T�r/   �disable_web_page_preview)rq   rr   u�  
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
        u   💳 Buy Now�show_payment_methods��callback_data)�reply_markupr/   r�   )rj   �BOT_USERNAMEra   r^   �idrg   �
first_name�CREDIT_SYSTEM_ENABLEDr
   r   �
capitalizerX   r   rH   rz   r{   �BOT_VERSIONr   �REDEEM_SYSTEM_ENABLED�REFERRAL_SYSTEM_ENABLEDr   rN   �reply_tor   �InlineKeyboardMarkup�InlineKeyboardButton�add)r`   r;   �	user_name�credits�current_gate�premium_statusr<   �	help_text�buy_text�markup�
buy_buttons              rA   �send_welcomer�   i   s   � ��L�'�2�?�7�;S���l�l�o�o�G��!�!�,�,�6��I�+@��w�'�k�G�+�G�4�?�?�A�^�\�E\�E\�E^�L�&0��&9�]�{�N��l�l� � �"�1�%�+�+�-�G�
�g�~��-�-��$�Q�'���+���!�"�+�� �3�3��(�M� *���G�N�#3� 4��	� �W�%��y�y�I�� � 	�	� !��J�J�I� ��[�[�I�"��H�H�I�� 
� 
	�	� �G��� � �I�< 	� �
 )�>��4� 	4�	� !��;�G�9�G�L�L�I��_�_�	����W�i�F�UY��Z�	�$�	$���. �+�+�-���/�/��Nd�e�
��
�
�:�����W�h�V��im��n�7 
%r[   c                 �    � | j                   dk(  S )Nr�   ��data��calls    rA   �<lambda>r�   �   s   � �d�i�i�;Q�.Qr[   )�funcc                 ��  � | j                   j                  j                  }t        t        | j                   �      st        | j                   �      sy d}d}d}|||z   z  }t        j                  �       }t        j                  dd��      }|j                  |�       t        j                  | j                   j                  j                  | j                   j                  ||dd�	�       y )
Nu�   
💳 <b>Select Payment Method</b> 💳
<a href='https://t.me/+GdWapjhiAG05OTk1'>┏━━━━━━━━━━━⍟</a>
<a href='https://t.me/+GdWapjhiAG05OTk1'>┃</a>
🔒 Secure and streamlined payment process.

u  
✅ <b>Bitcoin (BTC)</b>:
   <code>15eRTKVEEqJKBLBW4sHJPuF6ByvjK5VcDw</code>

✅ <b>USDT (Trc20)</b>:
   <code>TUQysXBFPZ6mmJg9FqwYFQcPUqSepTB96E</code>

✅ <b>UPI</b>:
   📴 Currently Unavailable<a href='https://t.me/+GdWapjhiAG05OTk1'>┗━━━━━━━⊛</a>
u�   
⚡️ <b>Instant Activation!</b> Your credits will be activated automatically after payment confirmation.

💬 <b>Important</b>: For UPI or if automatic activation fails, DM @CrImSon_WoLf777 with payment proof.
u   📩 Contact Admin for Supportzhttps://t.me/CrImSon_WoLf777)�urlr-   T)rF   rG   rH   r�   r/   r�   )r`   r^   r�   rj   r�   ra   r   r�   r�   r�   rN   rO   rG   )r�   r;   �payment_text�payment_methods_list�payment_footerr�   �	dm_buttons          rA   �payment_methods_callbackr�   �   s�   � ��l�l���"�"�G��L�$�,�,�7��PT�P\�P\�@]���L�	���N� �(�>�9�9�L��'�'�)�F��*�*�+K�Qo�p�I�
�J�J�y�����$�,�,�"3�"3�"6�"6�4�<�<�CZ�CZ�am�  }C�  PV�  qu��  vr[   ro   rm   c           
      ��  � t        t        | �      st        | �      sy | j                  j                  }| j
                  j                  xs d}t        |�      rt        j                  | d|� d�d��       y |t        v rt        j                  | dd��      S d }| j                  j                  d�      rdt        | j                  j                  �       �      dkD  r>	 | j                  j                  �       d   }t        |�      }||k(  rd }nt!        |�      rd }t#        ||�	�      }|d
k(  r�t%        dd�      5 }|j'                  t)        |�      dz   �       d d d �       t*        rt-        |�      nd}d|� d�}t*        r
|d|� d�z  }n|dz  }|r@t/        �       }	t1        �       }
|d|
� d�z  }	 t        j3                  |d|� d|� d|	� d�d��       |dz  }t        j                  | |dd��       y |dk(  rt        j                  | d|� d�d��       y t        j                  | d d��       y #  d }Y ��xY w# 1 sw Y   ��xY w# t4        $ r}t7        d|� d|� ��       Y d }~��d }~ww xY w)!Nr�   u
   ⚠️ <b>z!</b>, you are already registered!r-   r.   �7   🚫 You are banned from using this bot. Contact admin.z/startr   )�referrer_id�success�user_ids.txtr3   r4   r�   u"   
🎉 <b>Registration Successful, u�   !</b> 🎉
<a href='https://t.me/+GdWapjhiAG05OTk1'>┏━━━━━━━━━━━⍟</a>
<a href='https://t.me/+GdWapjhiAG05OTk1'>┃</a>
🚀 Welcome aboard the Crimson Checker Bot!

u   💰 <b>z# Credits Added to Your Account</b>
u6   ✨ <b>Unlimited Credits - Enjoy Full Access!</b> ✨
uK   
🎁 <b>Referral Bonus Applied!</b>
   💰 You've received a bonus of <b>z& credits</b> thanks to your referrer!
u$   🎉 New user <a href='tg://user?id=z'><b>u?   </b></a> joined using your referral!
💰 Referral bonus of <b>z& credits</b> credited to your account.z1Error sending referral bonus message to referrer �: u   
📚 Explore the bot with /menu - Your command center!<a href='https://t.me/+GdWapjhiAG05OTk1'>┗━━━━━━━⊛</a>Tr�   �already_registeredu7   ❌ <b>Registration failed.</b> Please contact support.)rj   r�   ra   r^   r�   rg   r�   r   rN   r�   �BANNED_USERSrH   r|   �lenrz   �_get_user_id_from_referral_coder   r   r7   r9   �strr�   r
   r   r   �send_messagerP   r:   )r`   r;   r�   r�   �ref_code�register_result�f�initial_credits�registration_message�referrer_bonus�referred_bonusrS   s               rA   �register_commandr�     s�  � ��L�'�2�?�7�;S���l�l�o�o�G��!�!�,�,�6��I��W�����W�
�9�+�5V�W�dj��k���,���|�|�G�%^�kq�|�r�r��K��|�|���x�(�S����1C�1C�1E�-F��-J�	��|�|�)�)�+�A�.�H�9�(�C�K��g�%�"���+�&�"�� $�G��E�O��)�#��.�#�&�!��G�G�C��L�4�'�(� '� 8M�*�7�3�R]��$"�"+�� -� �� !� �h��.?�?c�$d�d� � �$]�]� ��/�1�N�/�1�N� �&s�  uC�  tD�  Dk�  %l�  l� �^�� � ��0T�U\�T]�]b�cl�bm�  nn�  o}�  n~�  ~d�  /e�  rx� �  y� 	�  !c�  	c�����W�2�v�`d��e�	�0�	0����W�
�9�+�5V�W�dj��k����W�W�dj��k��I	��K��
 '�&��, � ^��I�+��VX�YZ�X[�\�]�]��^�s0   �=H$ �4H.�("H: �$H+�.H7�:	I�I�Irp   c                 �  � t        t        | �      st        | �      sy t        | �      rt        sy | j
                  j                  }t        |t        �      }|rt        j                  | d|� d�dd��       y t        j                  | dd��       y )Nu+   🔗 <b>Your Exclusive Referral Link:</b>

u@   

📣 Share your link to invite friends and earn bonus credits!r-   Tr�   uB   ❌ <b>Error generating referral link.</b> Please try again later.r.   )
rj   r�   ra   �ensure_registeredr�   r^   r�   r   rN   r�   )r`   r;   �referral_links      rA   �referral_commandr�   R  s�   � ��L�'�2�?�7�;S���W�%�-D�f��l�l�o�o�G�*�7�L�A�M�����W� M�m�_�  ]_�  `�  ms�  NR��  	S����W�b�ou��vr[   �bonusc                 ��  � t        t        | �      st        | �      sy t        | �      rt        sy | j
                  j                  }t        |�      st        j                  | dd��       y t        |d| j                  �       	 | j                  j                  �       }t        |�      dk7  rt        d�      �t        |d   �      }t        |d   �      }|d	k  s|d	k  rt        d
�      �t!        ||�       t        j                  | d|� d|� d�d��       y # t        $ r%}t        j                  | d|� �d��       Y d }~y d }~wt"        $ r0}t%        d|� ��       t        j                  | dd��       Y d }~y d }~ww xY w)N�'   🚫 Admin command only. Access Denied.r-   r.   r�   �   z'Incorrect number of arguments provided.r   �   r   z"Bonuses cannot be negative values.uA   ✅ <b>Referral Bonuses Updated!</b>

🎁 Referrer Bonus: <code>u+    credits</code>
👤 Referred Bonus: <code>z credits</code>u�   ❌ <b>Error updating referral bonuses.</b>

<b>Usage:</b> <code>/bonus referrer_bonus referred_bonus</code> (bonuses must be non-negative integers). 

<b>Details</b>: z Error setting referral bonuses: uB   ❌ <b>Error setting referral bonuses.</b> Please contact support.)rj   r�   ra   r�   r�   r^   r�   r   rN   r�   rB   rH   rz   r�   �
ValueError�intr   rP   r:   )r`   r;   r=   r�   r�   rS   s         rA   �bonus_commandr�   ^  s�  � ��L�'�2�?�7�;S���W�%�-D�f��l�l�o�o�G��G�����W�G�TZ��[���g�w����5�w��|�|�!�!�#���t�9��>��F�G�G��T�!�W����T�!�W����A���!�!3��A�B�B��^�^�<����W� c�dr�cs�  t`�  ao�  `p�  p�  @�  MS��  	T��� e����W�  !M�  NO�  MP�  Q�  ^d��  	e�  	e��� w��0���4�5����W�b�ou��v�v��w�s%   �BD �	E6�D:�:E6�&E1�1E6ru   c           
      ��  � t        t        | �      st        | �      sy t        | �      sy | j                  j
                  }	 | j                  j                  d��      d   }d|� d| j                  j                  � d| j                  j                  � d| j                  j                  xs d� d|� �
}t        �       D ]  }	 t        j                  ||d	�
�       � t        j#                  | dd	�
�       y # t        $ r}t!        d|� d|� ��       Y d }~�Vd }~ww xY w# t$        $ r t        j#                  | dd	�
�       Y y t        $ r0}t!        d|� ��       t        j#                  | dd	�
�       Y d }~y d }~ww xY w)Nr   ��maxsplitz$<b>Feedback from User ID:</b> <code>z</code>
<b>Username:</b> @z
<b>Name:</b> � � z

<b>Message:</b>
r-   r.   z Error sending feedback to admin r�   uY   ✅ <b>Feedback Sent!</b>

Your feedback has been forwarded to the bot admins. Thank you!uq   ❌ <b>Feedback Message Required</b>

Usage: <code>/feedback message</code>
Please provide your feedback message.zError processing feedback: u:   ❌ <b>Error sending feedback.</b> Please try again later.)rj   r�   ra   r�   r^   r�   rH   rz   rg   rh   r�   �	last_namer   rN   r�   rP   r:   r�   �
IndexError)r`   r;   �feedback_text�forward_message�admin_idrS   s         rA   �feedback_commandr�   }  s�  � ��L�'�2�?�7�;S���W�%�v��l�l�o�o�G�o����*�*�A�*�6�q�9��@��	�Id�el�ev�ev�e�e�  eA�  AP�  QX�  Qb�  Qb�  Qm�  Qm�  Pn�  no�  pw�  pA�  pA�  pK�  pK�  pQ�  OQ�  oR�  Rg�  hu�  gv�  w��&�(�H�J�� � ��?�v� �N� )�
 	���W�{�  IO��  	P�� � J��8��
�"�Q�C�H�I�I��J�� � i����W�  U�  bh��  	i�� o��+�A�3�/�0����W�Z�gm��n�n��o�sI   � A=D �>C1�D �1	D�:D�D �D�D �!E3�;E3�&E.�.E3rx   c                 �z  � t        t        | �      st        | �      sy t        | �      sy t	        j                  �       }t
        j                  | dd��      }t	        j                  �       }t        t        ||z
  d�      �      }t
        j                  d|� d�| j                  j                  |j                  d��       y )Nu   🏓 <b>Pinging...</b>r-   r.   r�   u!   🏓 <b>Pong! Latency:</b> <code>z seconds</code>)rF   rG   r/   )rj   r�   ra   r�   �timerN   r�   r�   �roundrO   r^   r�   rG   )r`   �
start_time�pong�end_time�latencys        rA   �ping_commandr�   �  s�   � ��L�'�2�?�7�;S���W�%�v�����J��<�<��!9�f�<�M�D��y�y�{�H��%��:�-�q�1�2�G����=�g�Y�o�V�`g�`l�`l�`o�`o�  }A�  }L�  }L�  Y_��  `r[   rv   c                 �   � t        t        | �      st        | �      sy t        | �      sy d}t        j                  | |dd��       y )Nu�  
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
r-   Tr�   �rj   r�   ra   r�   rN   r�   )r`   �
terms_texts     rA   �terms_commandr�   �  s?   � ��L�'�2�?�7�;S���W�%�v�"�J�F �L�L��*��RV�L�Wr[   rw   c                 �   � t        t        | �      st        | �      sy t        | �      sy d}t        j                  | |dd��       y )Nu�  
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
r-   Tr�   r�   )r`   �privacy_texts     rA   �privacy_commandr�   �  s?   � ��L�'�2�?�7�;S���W�%�v� �L�B �L�L��,�6�TX�L�Yr[   c                 ��   � | j                   j                  }|t        v rt        j	                  | dd��       yt        |�      s$t        | �      rt        j	                  | dd��       yy)Nr�   r-   r.   Fuo   🔑 <b>Account Registration Required</b>

To proceed with this command, please register using /register first.T)r^   r�   r�   rN   r�   r   r   )r`   r;   s     rA   r�   r�   �  sb   � ��l�l�o�o�G��,�����W�W�dj��k����!�&>�w�&G����W�  R�  _e��  	f��r[   �gatec                 ��  � t        t        | �      st        | �      sy t        | �      sy | j                  j
                  }t        j                  d��      }g d�}|D ]+  \  }}|j                  t        j                  ||��      �       �- t        |�      j                  �       xs t        j                  �       }t        j                  | d|� dt        j                  �       � d�|d�	�       y )
Nr�   )�	row_width))zStripe Authzset_gate:auth)z	Stripe 2$zset_gate:stripe2)z	Stripe 4$zset_gate:stripe4r�   u   ⚙️ <b>Select Payment Gateway</b>

Choose your preferred gateway for processing card checks:

<b>Current Gateway:</b> <code>z6</code>
<b>Default Gateway (for new users):</b> <code>�9</code>

<b>Cost: 1 Credit per Check for all Gateways</b>r-   )r�   r/   )rj   r�   ra   r�   r^   r�   r   r�   r�   r�   r   r�   rX   rN   r�   )r`   r;   r�   �gates�	gate_namer�   r�   s          rA   �gate_commandr�   �  s�   � ��L�'�2�?�7�;S���W�%�v��l�l�o�o�G��'�'�!�4�F��E�
 %*� �	�=��
�
�5�-�-�i�}�U�V� %*�+�G�4�?�?�A�^�\�E\�E\�E^�L��L�L��  `�  am�  `n�  ne�  fr�  f}�  f}�  f�  e@�  @{�  |�  KQ�  ^d�L�  er[   c                 �8   � | j                   j                  d�      S )Nz	set_gate:)r�   r|   r�   s    rA   r�   r�   
  s   � �d�i�i�.B�.B�;�.Or[   c                 �  � | j                   j                  j                  }t        t        | j                   �      st        | j                   �      sy | j                  j                  d�      d   }t        ||�       |j                  dd�      j                  dd�      j                  �       }t        j                  | j                  d|� ���       t        j                  || j                   j                  d	|� d
�dd ��       y )N�:r   rV   �2$rW   �4$zGateway set to )rH   u_   ✅ <b>Gateway Updated</b>

Your active payment gateway is now:

<b>Current Gateway:</b> <code>r�   r-   )rF   rG   rH   r/   r�   )r`   r^   r�   rj   r�   ra   r�   rz   r   �replacer�   rN   �answer_callback_queryrO   rG   )r�   r;   r�   �gate_display_names       rA   �set_gate_callbackr�   
  s�   � ��l�l���"�"�G��L�$�,�,�7��PT�P\�P\�@]���	�	����$�Q�'�I��W�i�0�!�)�)�)�T�:�B�B�9�d�S�^�^�`�����d�g�g�o�>O�=P�,Q��R����'�d�l�l�6M�6M�  Wz�  {L�  zM�  MH�  UI�  V\�  ko��  pr[   �statsc                 �(  � t        t        | �      st        | �      sy t        | �      sy | j                  j
                  }t        |�      }|sddddd�}t        rt        |�      nd}t        |�      j                  �       xs t        j                  �       }d}t        r	|d|� d�z  }|d|� d|j                  d	d�      � d
|j                  dd�      � d|j                  dd�      � d|j                  dd�      � d�z  }t        j                  | |d��       y )Nr   ��approved�declined�ccn�cvvr�   u�   📊 <b>Your Checker Stats</b> 📊
<a href='https://t.me/+GdWapjhiAG05OTk1'>┏━━━━━━━━━━━⍟</a>
<a href='https://t.me/+GdWapjhiAG05OTk1'>┃</a>
Performance overview of your card checking activity:

u%   💰 <b>Credits Available:</b> <code>�</code>
u#   
⚙️ <b>Current Gate:</b> <code>u+   </code>
✅ <b>Approved Cards:</b>   <code>r�   u+   </code>
❌ <b>Declined Cards:</b>   <code>r   u/   </code>
⚠️ <b>CCN Results:</b>       <code>r  u,   </code>
✅ <b>CVV Results:</b>       <code>r  �P   </code><a href='https://t.me/+GdWapjhiAG05OTk1'>┗━━━━━━━⊛</a>
r-   r.   )rj   r�   ra   r�   r^   r�   r   r�   r
   r   r�   rX   �getrN   r�   )r`   r;   �
user_statsr�   r�   rH   s         rA   �stats_commandr    s%  � ��L�'�2�?�7�;S���W�%�v��l�l�o�o�G���(�J��"#��1�Q�G�
�+@��w�'�k�G�+�G�4�?�?�A�^�\�E\�E\�E^�L�9�D� ��7��y�	�J�J��� #�#/�.� 1$�$.�N�N�:�q�$A�#B� C$�$.�N�N�:�q�$A�#B� C(�(2���u�a�(@�'A� B%�%/�^�^�E�1�%=�$>� ?�� �D� �L�L��$�6�L�2r[   r�   c                 �  � t        t        | �      st        | �      sy t        | �      rt        sy | j
                  j                  }t        |�      }t        |t        �      s|nd}t        j                  | d|� d�d��       y )Nr�   u'   💰 <b>Your Credit Balance:</b> <code>z</code> creditsr-   r.   )rj   r�   ra   r�   r�   r^   r�   r
   �
isinstancer�   rN   r�   )r`   r;   r�   �credits_displays       rA   �credits_commandr  0  si   � ��L�'�2�?�7�;S���W�%�-B�F��l�l�o�o�G��w�'�G�%/���%=�g�;�O��L�L��C�O�CT�Tc�d�qw�L�xr[   �redeemc                 �  � t        t        | �      st        | �      sy t        | �      rt        sy | j
                  j                  }t        |d| j                  �       	 | j                  j                  �       d   }t        j                  d|�      st        j                  | dd��       y t        ||�      }|dk(  rXt!        �       }|j#                  t%        |�      i �      j#                  d	d
�      }|rdnd}t        j                  | d|� d�d��       y |dk(  rt        j                  | dd��       y |dk(  rt        j                  | dd��       y t        j                  | dd��       y # t        $ r t        j                  | dd��       Y y w xY w)Nr  r   ul   ❌ <b>Redeem Code Required</b>

Usage: <code>/redeem code</code>
Please enter the redeem code you received.r-   r.   z.^[a-zA-Z0-9]{4}-[a-zA-Z0-9]{4}-[a-zA-Z0-9]{4}$uK   ❌ <b>Invalid Code Format</b>

Use the format: <code>xxxx-xxxx-xxxx</code>r�   r   Fu0    and you've unlocked <b>Premium Access!</b> 🎉r�   uF   ✅ <b>Code Redeemed Successfully!</b>

Your account has been credited�.�invaliduE   ❌ <b>Invalid Code</b>

Please verify the redeem code and try again.�useduH   ⚠️ <b>Code Already Used</b>

This redeem code has already been used.uU   ❌ <b>Redeem Error</b>

An error occurred during redemption. Please contact support.)rj   r�   ra   r�   r�   r^   r�   rB   rH   rz   r�   rN   r�   �re�matchr   �_load_user_datar  r�   )r`   r;   �code�redeem_result�	user_data�is_premium_user�premium_message_parts          rA   �redeem_commandr  :  s�  � ��L�'�2�?�7�;S���W�%�-B�F��l�l�o�o�G��g�x����6���|�|�!�!�#�A�&��
 �8�8�E�t�L����W�m�  {A��  	B��"�7�D�1�M��	�!�#�%�	�#�-�-��G��b�9�=�=�l�E�R��Ud�Q�jl�����W� h�i}�h~�~�  A�  NT��  	U�	�)�	#����W�g�tz��{�	�&�	 ����W�j�w}��~����W�w�  EK��  	L��' � ����W�  P�  ]c��  	d���s   �E' �'!F�
Fr  c                 �  � t        t        | �      st        | �      sy t        | �      rt        sy | j
                  j                  }t        |�      st        j                  | dd��       y t        |d| j                  �       	 | j                  j                  �       }t        |�      dk  rt        d�      �|d   }|j                  �       dk(  rd	}d
}nt!        |�      }d}d}t#        ||d|��      }dj%                  |�      }|rdnd|� d�}	t        j                  | d|� d|	� d�d��       y # t        t&        f$ r t        j                  | dd��       Y y t(        $ r0}
t+        d|
� ��       t        j                  | dd��       Y d }
~
y d }
~
ww xY w)Nr�   r-   r.   r  r�   zAmount not specifiedr   �premiumr   TFzxxxx-xxxx-xxxx)�code_formatr  r4   z)(Premium Code - Grants Unlimited Credits)z
(Credits: �)u)   ✅ <b>Redeem Code Generated!</b>

<code>z	</code>

zE

Distribute this code for users to redeem credits or Premium access.u�   ❌ <b>Usage Error: Credit Amount Required</b>

Usage: <code>/code amount</code> (amount as integer, or 'premium' for premium code)zError generating redeem code: u9   ❌ <b>Error generating code.</b> Please contact support.)rj   r�   ra   r�   r�   r^   r�   r   rN   r�   rB   rH   rz   r�   r�   r{   r�   r   rM   r�   rP   r:   )r`   r;   r=   �
amount_str�amount�is_premium_code�	num_codes�codes�	code_list�premium_noterS   s              rA   �generate_code_commandr%  X  s�  � ��L�'�2�?�7�;S���W�%�-B�F��l�l�o�o�G��G�����W�G�TZ��[���g�v�w�|�|�4�n��|�|�!�!�#���t�9�q�=��3�4�4��!�W�
������*��F�"�O���_�F�#�O��	�%�f�i�EU�_n�o���I�I�e�$�	�FU�B�]g�hn�go�op�[q�����W� K�I�;�Va�bn�ao�  pw�  x�  EK��  	L���
�#� z����W�  f�  sy��  	z�� n��.�q�c�2�3����W�Y�fl��m�m��n�s   �B(D* �*'F�F�&F�F�genc                 �6  � t        t        | �      st        | �      sy t        | �      sy | j                  j
                  }	 | j                  j                  �       d   j                  �       }|dk(  r't        �       }t        j                  | d|� d�d��       y |dk(  r't        �       }t        j                  | d	|� d�d��       y |d
k(  r't        �       }t        j                  | d|� d�d��       y |dk(  r't        �       }t        j                  | d|� d�d��       y |dk(  r't!        �       }t        j                  | d|� d�d��       y |dk(  r't        �       }t        j                  | d|� d�d��       y |dk(  r3t#        j$                  dd�      }	t        j                  | d|	� d�d��       y |dk(  r't'        �       }
t        j                  | d|
� d�d��       y |dk(  r't)        �       }t        j                  | d|� d�d��       y |dk(  r't+        �       }t        j                  | d|� d�d��       y |dk(  r't-        �       }t        j                  | d|� d�d��       y t        j                  | dd��       y # t        $ r t        j                  | dd��       Y y w xY w)Nr   u;  ❌ <b>Data Type Missing</b>

Usage: <code>/gen [type]</code>

Supported types: <code>email</code>, <code>username</code>, <code>password</code>, <code>address</code>, <code>phone</code>, <code>name</code>, <code>zip</code>, <code>iban</code>, <code>swift</code>, <code>btc_address</code>, <code>usdt_address</code>r-   r.   �emailu#   📧 <b>Generated Email:</b> <code>r�   rh   u&   👤 <b>Generated Username:</b> <code>�passwordu&   🔑 <b>Generated Password:</b> <code>�addressu%   🏠 <b>Generated Address:</b> <code>�phoneu*   📞 <b>Generated Phone Number:</b> <code>�nameu"   👤 <b>Generated Name:</b> <code>�zipi'  i�� u(   ✉️ <b>Generated Zip Code:</b> <code>�ibanu"   🏦 <b>Generated IBAN:</b> <code>�swiftu'   🏢 <b>Generated SWIFT/BIC:</b> <code>�btc_addressu(   ₿ <b>Generated BTC Address:</b> <code>�usdt_addressu1   ₮ <b>Generated USDT Address (TRC20):</b> <code>u  ❌ <b>Invalid Data Type</b>

Supported types: <code>email</code>, <code>username</code>, <code>password</code>, <code>address</code>, <code>phone</code>, <code>name</code>, <code>zip</code>, <code>iban</code>, <code>swift</code>, <code>btc_address</code>, <code>usdt_address</code>)rj   r�   ra   r�   r^   r�   rH   rz   r{   r�   rN   r�   r!   r"   r#   r%   r&   �random�randintr'   r(   r)   r*   )r`   r;   �	data_typer(  rh   r)  r*  �phone_numberr,  �zip_coder.  r/  r0  r1  s                 rA   �generate_data_commandr7  }  s�  � ��L�'�2�?�7�;S���W�%�v��l�l�o�o�G���L�L�&�&�(��+�1�1�3�	�
 �G��%�'�����W� C�E�7�'�R�_e��f�	�j�	 �$�&�����W� F�x�j�PW�X�ek��l�	�j�	 �$�&�����W� F�x�j�PW�X�ek��l�	�i�	�"�$�����W� E�g�Y�g�V�ci��j�	�g�	�,�.�����W� J�<�.�X_�`�ms��t�	�f�	� �"�����W� B�4�&��P�]c��d�	�e�	��>�>�%��/�����W� H��
�RY�Z�gm��n�	�f�	�������W� B�4�&��P�]c��d�	�g�	�� �����W� G��w�g�V�ci��j�	�m�	#�*�,�����W� H���U\�]�jp��q�	�n�	$�,�.�����W� Q�R^�Q_�_f�g�tz��{����W�  }�  JP��  	Q��M � ����W�  `�  ms��  	t���s   � +I4 �4!J�Jrt   c                 �p  � t        t        | �      st        | �      sy t        | �      sy 	 | j                  j                  �       d   }t        j                  d|�      st        d�      �	 t        j                  d|� ��      j                  �       }|st        j                  | d|� d	�d��      S d
|� d|j                  dd�      � d|j                  dd�      � d|j                  dd�      � d|j                  dd�      � d|j                  dd�      � d|j                  dd�      � d|j                  dd�      � d|j                  d�      rdnd� d|j                  d d�      � d!|j                  d"d�      � d#�}t        j                  | |dd$�%�       y #  t        j                  | dd��      cY S xY w# t        $ r t        j                  | d&d��       Y y t        $ r&}t        j                  | d'|� d(�d��       Y d }~y d }~wt        $ r0}t!        d)|� ��       t        j                  | d*d��       Y d }~y d }~ww xY w)+Nr   z	^\d{6,8}$zInvalid BIN format� https://bins.antipublic.cc/bins/uY   ❌ <b>BIN Lookup Failed</b>

Could not retrieve BIN information. Please try again later.r-   r.   uK   ℹ️ <b>BIN Info</b> ℹ️

No detailed information found for BIN <code>�</code>.u"   
ℹ️ <b>BIN Info for</b> <code>u�   </code> ℹ️
<a href='https://t.me/+GdWapjhiAG05OTk1'>┏━━━━━━━━━━━⍟</a>
<a href='https://t.me/+GdWapjhiAG05OTk1'>┃</a>
<b>💳 Brand:</b> <code>�brand�N/A�    </code>
<b>🏦 Bank:</b> <code>�bank�&   </code>
<b>🏛️ Country:</b> <code>�country_namer�   �country_flagr�   u+   </code>
<b>🗺️ Country Code:</b> <code>�country_code�"   </code>
<b>⌨️ Type:</b> <code>r_   �$   </code>
<b>🎚️ Level:</b> <code>�level�%   </code>
<b>ℹ️ Prepaid:</b> <code>�prepaid�Yes�Nou#   </code>
<b>🌐 Website:</b> <code>�bank_urlu!   </code>
<b>📞 Phone:</b> <code>�
bank_phoner  Tr�   un   ❌ <b>BIN Input Required</b>

Usage: <code>/bin [BIN]</code>
Please provide a BIN (first 6-8 digits of card).�   ❌ <b>Invalid Input</b>

z:

Usage: <code>/bin [BIN]</code> (BIN must be 6-8 digits).zError processing /bin command: uD   ❌ <b>Error retrieving BIN information.</b> Please contact support.�rj   r�   ra   r�   rH   rz   r  r  r�   �requestsr  �jsonrN   r�   r�   rP   r:   )r`   �	bin_inputr�   �bin_info_textrS   s        rA   �bin_commandrR  �  s�  � ��L�'�2�?�7�;S���W�%�v�$y��L�L�&�&�(��+�	��x�x��i�0��1�2�2�	[��<�<�"B�9�+� N�O�T�T�V�D� ��<�<��+x�  zC�  yD�  DL�  *M�  Z`�<�  a�  a�"�"+�� -� �(�(�7�E�2�3� 4����&�%�0�1� 2�#�x�x���>�?�q����.�Z\�A]�@^� _$�$(�H�H�^�U�$C�#D� E��8�8�F�E�2�3� 4�!�X�X�g�u�5�6� 7�'+�x�x�	�':�e��E� F� �H�H�Z��7�8� 9��(�(�<��7�8� 9��� 	���W�m��Y]��^��+	[��<�<��  *G�  TZ�<�  [�  [��, � f����W�  R�  _e��  	f�� Q����W� <�Q�C�?{�|�  JP��  	Q�  	Q��� y��/��s�3�4����W�d�qw��x�x��y�sN   �>F- �)&F �F- �-C F- �F*�(F- �*F- �-!H5�H5�G9�9H5�&H0�0H5u	   💳 VisazMC Mastercardu	   🪪 Amexu   🔭 Discoveru   💴 JCBu   🇨🇳 UnionPay)�visa�
mastercard�amex�discover�jcb�unionpay)�chk�checkz.chk�validateu   驗卡�card�ccc                 �  � t        t        | �      st        | �      sy t        | �      sy | j                  j
                  }t        rt        |�      nd}t        r&|dk7  r!|dk  rt        j                  | d|� d�d��      S t        | j                  j                  �       �      dkD  r-| j                  j                  d��      d   j                  �       nd }|st        j                  | dd��      S d }g }| j                  ry d	|v r[t        rUt!        |�      }|st        j                  | d
d��      S t        j                  | dt        |�      � d�d��      j"                  }nTt%        j&                  d|�      r&|g}t        j                  | dd��      j"                  }nt        j                  | dd��      S d}d}d}d}	t)        �       }
|
st        j                  | dd��      S t+        |�      }t-        |�      }|j/                  �       j1                  dd�      j1                  dd�      j1                  dd�      }d}|D �]�  }t3        | j                  j
                  |�      r y t        rst5        |�      sh|r?t        j7                  | j                  j
                  |d|	� dt        |�      � d�d��        y t        j                  | dt        |�      � d�d��        y |	dz  }		 t8        r)t;        j<                  d|d d z   �      j?                  �       ni }|j=                  dd �      jA                  �       }|j=                  d!d �      }|j=                  d"d �      }|j=                  d#d �      }|j=                  d$d �      }tB        r$tD        j=                  ||jG                  �       �      n|jG                  �       }tI        jH                  �       }tK         ||
|j                  �       �      �      }tM        ||j                  d%�      d   �       tI        jH                  �       }||z
  }d&|� d'|� d(|� d)|d d � d*|� d+|� d,|� d+|� d-|� d.tO        |d�      � d/�}|r�d0|v sd1|v r3|dz  }t        jQ                  | j                  j
                  |dd2�3�       nd4|v r|dz  }nd5|v sd6|v sd7|v r|dz  }d8|� d9|� d:|� d;|	� d<�	}	 t        j7                  | j                  j
                  ||dd2�=�       nt        j                  | |dd2�3�       tI        jV                  d?�       ��� |rtt        jQ                  | j                  j
                  d@|	� dAt        rt        |�      nd� d�d�B�       	 t        j7                  | j                  j
                  |dCdd2�=�       y y #  i }Y ���xY w# tR        $ r}tU        d>|� ��       Y d }~��d }~ww xY w# tR        $ r}tU        dD|� ��       Y d }~y d }~ww xY w)ENr�   r   �1   🚫 <b>Insufficient Credits</b>

You have <code>zr</code> credits remaining. You need at least 1 credit to perform a check. Please redeem a code or contact support.r-   r.   r�   uc   ❌ <b>Card Details Missing</b>

Usage: <code>/chk cc|mm|yy|cvv</code> or send a document with CCs.r4   uz   ❌ <b>No Valid Cards Detected</b>

Provide card details in <code>cc|mm|yy|cvv</code> format, one per line for bulk check.u:   💳 <b>Bulk Card Check Initiated</b> ⏳

Checking <code>z</code> cards...z$\d{13,19}\|\d{1,2}\|\d{2,4}\|\d{3,4}u%   💳 <b>Checking Card Details</b> ⏳u_   ❌ <b>Invalid Card Format</b>

Use the format: <code>cc|mm|yy|cvv</code> or upload a document.r   uK   ❌ <b>Session Error</b>

Failed to create session. Please try again later.�AUTH�STRIPE2r�   �STRIPE4r�   r�   �>   🚫 <b>Credits Exhausted</b>

Bulk check stopped after <code>zF</code> cards.
Redeem credits or purchase a plan.
Credits left: <code>r�   �rF   rG   rH   r/   ue   🚫 <b>Credits Exhausted</b>

Check stopped.
Redeem credits or purchase a plan.
Credits left: <code>r9  �   r;  �Unknownr_   r@  rA  r>  r�   u
  
<a href='https://envs.sh/smD.webp'>-</a> 💳 <b>Ｃａｒｄ Ｃｈｅｃｋ Ｒｅｓｕｌｔ</b> 💳
<a href='https://t.me/+GdWapjhiAG05OTk1'>┏━━━━━━━━━━━⍟</a>
<a href='https://t.me/+GdWapjhiAG05OTk1'>┃</a><b>💳 ＣＣ:</b> <code>u�   </code><a href='https://t.me/+GdWapjhiAG05OTk1'>┗━━━━━━━⊛</a>
<a href='https://t.me/+GdWapjhiAG05OTk1'>-</a> ⚡ <b>𝐆𝐚𝐭𝐞𝐰𝐚𝐲:</b> ⤿ u[    🟢 ⤾
<a href='https://t.me/+GdWapjhiAG05OTk1'>-</a> ✅ Ｒｅｓｐｏｎｓｅ: ⤿ uQ    ⤾

<a href='https://envs.sh/smD.webp'>-</a> ℹ️ <b>Ｉｎｆｏ</b>: <code>�-� - �c   </code>
<a href='https://t.me/+GdWapjhiAG05OTk1'>-</a> 🗺️ 𝐂𝐨𝐮𝐧𝐭𝐫𝐲: <code>uP   </code>
<a href='https://t.me/+GdWapjhiAG05OTk1'>-</a> 🏦 Ｂａｎｋ: <code>uS   </code>

<a href='https://t.me/+GdWapjhiAG05OTk1'>-</a> ⏱️ Ｔｉｍｅ: <code>u�    𝐬𝐞𝐜</code>
<a href='https://t.me/+GdWapjhiAG05OTk1'>-</a> 🤖 Ｂｏｔ Ｂｙ: <a href='https://t.me/+GdWapjhiAG05OTk1'>Crimson </a>�   APPROVED ✅�   CVV ✅Tr�   �   CCN ✅�   DECLINED ❌�   EXPIRED ❌�Erroru�   📝 <b>Bulk Checking in Progress...</b> 📝
🤖 𝗕𝘆 ➜ <a href='https://t.me/+GdWapjhiAG05OTk1'>Crimson </a>

✅ 𝐀𝐏𝐏𝐑𝐎𝐕𝐄𝐃 : [ �0    ]
⚠️ 𝐅𝐀𝐊𝐄 𝐂𝐀𝐑𝐃 : [ �,    ]
❌ 𝐃𝐄𝐂𝐋𝐈𝐍𝐄𝐃 : [ �%    ]
🎉 𝐓𝐎𝐓𝐀𝐋    :  [ � ]�rF   rG   rH   r/   r�   �Error editing bulk message: �      �?�5   ✅ <b>Bulk Card Check Completed!</b>

Checked <code>z8</code> cards from text input.
Credits remaining: <code>�rF   rH   r/   ��   📝 𝗕𝗨𝗟𝗞 𝗖𝗛𝗘𝗖𝗞 𝗖𝗢𝗠𝗣𝗟𝗘𝗧𝗘𝗗 ✅
🤖 𝗕𝗢𝗧 𝗕𝗬 ➜ @CrImSon_WoLf777z"Error editing final bulk message: ),rj   r�   ra   r�   r^   r�   r�   r
   rN   r�   r�   rH   rz   �strip�document�ENABLE_GROUP_CHECKr    rG   r  r  r   rZ   r   �upperr�   rT   r   rO   �DETAILED_BIN_INFOrN  r  rO  r{   �DISPLAY_CARD_BRAND�CARD_BRANDSr�   r�   r�   r   r�   r�   rP   r:   �sleep)r`   r;   r�   �
full_input�ko_msg�ccs_to_check�dd�live�	incorrect�checked_count�session�gate_function�gate_name_preference�gate_name_display�results_textr]  r�   r;  �	card_type�countryrA  r>  �card_brand_displayr�   �lastr�   �execution_time�
msg_output�bulk_update_textrS   s                                 rA   �check_card_commandr�  �  s�  � ��L�'�2�?�7�;S���W�%�v��l�l�o�o�G�+@��w�'�k�G���K�!7�G�a�K��|�|�G�'Z�[b�Zc�  dV�  &W�  dj�|�  k�  	k�>A�'�,�,�BT�BT�BV�>W�Z[�>[����#�#�Q�#�/��2�8�8�:�ae�J���|�|�G�  &M�  Z`�|�  a�  	a��F��L�����	��	� 2�,�Z�8����<�<��  *h�  u{�<�  |�  |����g�)e�fi�jv�fw�ex�  yI�  (J�  W]��  ^�  i�  i��	���9�:�	F�"�|�����g�'N�[a��b�m�m���|�|�G�  &I�  V\�|�  ]�  	]�	
�B��D��I��M�!�#�G���|�|�G�%t�  BH�|�  I�  	I�.�w�7�M�3�G�<��,�2�2�4�<�<�V�V�L�T�T�U^�`d�e�m�m�nw�y}�~���L����g�l�l�o�o�v�6�� �!�'�*���)�)�'�,�,�/�/�f�  ^^�  _l�  ^m�  mu�  vF�  GN�  vO�  uP�  PW�  \X�  ek�)�  l� � �L�L��  -V�  Wg�  ho�  Wp�  Vq�  qx�  +y�  FL�L�  M������	�Wh�8�<�<� B�R���V� K�L�Q�Q�S�np�D� ����)�,�2�2�4���H�H�V�Y�/�	��(�(�>�9�5���x�x��	�:���x�x��	�*��K]�[�_�_�U�E�4D�4D�4F�G�ch�cs�cs�cu���Y�Y�[�
��=��"�(�(�*�5�6���'�4�:�:�c�?�1�#5�6��9�9�;��!�J�.��K� LN�$� O]�]n�\o� pR�RV�QW� XL�LN�r�PQ�F�8�ST�U^�T_�_b�cu�bv� w\�\c�[d�dg�ht�gu� vI�IM�� OK�KP�Q_�ab�Kc�Jd� e|��
� ���%��d�):���	��� � ������*��jn� �o��d�"��1��	��4�'�=�D�+@�G�t�O��a���$*� +/�� 0.�.7�[� 9*�*,�� .#�#0�/�� 7��:��%�%�g�l�l�o�o�&�Wg�tz�  VZ�%�  [� �L�L��*��Z^�L�_��
�
�3��O �R ���������9p�q~�p�  @y�  Wl�  zJ�  KR�  zS�  r}�  y~�  ~E�  8F�  SY��  	Z�	<��!�!������!� \�  io�  JN� "� � ��s	��D��^ � :��4�Q�C�8�9�9��:��" � 	<��6�q�c�:�;�;��	<�s<   �1V�0.V�.V5 �V�	V2�V-�-V2�5	W�>W�W�cclookupc                 �  � t        t        | �      st        | �      sy t        | �      sy 	 | j                  j                  �       d   }t        j                  d|�      st        d�      �|d d }	 t        j                  d|� ��      j                  �       }|st        j                  | d	|� d
�d��      S d|j                  dd�      � d|j                  dd�      � d|j                  dd�      � d|j                  dd�      � d|j                  dd�      � d|j                  dd�      � d|j                  d�      rdnd� d�}t        j                  | |dd��       y #  t        j                  | dd��      cY S xY w# t        $ r t        j                  | d d��       Y y t        $ r&}t        j                  | d!|� d"�d��       Y d }~y d }~wt        $ r0}t!        d#|� ��       t        j                  | d$d��       Y d }~y d }~ww xY w)%Nr   z^\d{6,}$zInvalid Card Number formatre  r9  u[   ❌ <b>Card Lookup Failed</b>

Could not retrieve card information. Please try again later.r-   r.   u[   ℹ️ <b>Card Info</b> ℹ️

No detailed information found for card starting with <code>r:  u�   
ℹ️ <b>Card Info Lookup</b> ℹ️
<a href='https://t.me/+GdWapjhiAG05OTk1'>┏━━━━━━━━━━━⍟</a>
<a href='https://t.me/+GdWapjhiAG05OTk1'>┃</a>
<b>💳 Brand:</b> <code>r;  r<  r=  r>  r?  r@  r�   rA  r�   rC  r_   rD  rE  rF  rG  rH  rI  r  Tr�   u{   ❌ <b>Card Number Required</b>

Usage: <code>/cclookup [cc]</code>
Please provide a card number (at least first 6 digits).rL  zM

Usage: <code>/cclookup [cc]</code> (Card number must be at least 6 digits).z$Error processing /cclookup command: uE   ❌ <b>Error retrieving card information.</b> Please contact support.rM  )r`   �	cc_numberrP  r�   �card_info_textrS   s         rA   �cclookup_commandr�  e  sT  � ��L�'�2�?�7�;S���W�%�v�#z��L�L�&�&�(��+�	��x�x��Y�/��9�:�:��b�q�M�	�	]��<�<�"B�9�+� N�O�T�T�V�D� ��<�<��  ,I�  JS�  IT�  T\�  *]�  jp�<�  q�  q�� �(�(�7�E�2�3� 4����&�%�0�1� 2�#�x�x���>�?�q����.�Z\�A]�@^� _��8�8�F�E�2�3� 4�!�X�X�g�u�5�6� 7�'+�x�x�	�':�e��E� F�
�� 	���W�n��Z^��_��%	]��<�<��  *I�  V\�<�  ]�  ]��& � s����W�  _�  lr��  	s�� d����W� <�Q�C�  @O�  P�  ]c��  	d�  	d��� z��4�Q�C�8�9����W�e�rx��y�y��z�sO   �AE6 �.&E �E6 �2B$E6 �E3�1E6 �3E6 �6!G>�G>�!G�G>�&G9�9G>�setgatec                 ��  � t        t        | �      st        | �      sy | j                  j                  }t        |�      st        j                  | dd��      S t        |d| j                  �       	 | j                  j                  �       d   j                  �       }|dvrt        d�      �|at        j                  | d|j                  �       � d	�d��       y # t        $ r t        j                  | d
d��       Y y t        $ r&}t        j                  | d|� d�d��       Y d }~y d }~wt         $ r0}t#        d|� ��       t        j                  | dd��       Y d }~y d }~ww xY w)Nr�   r-   r.   r�  r   )r   rV   rW   zInvalid gate nameuP   ✅ <b>Default Gateway Updated</b>

Default gateway for new users set to: <code>r:  u�   ❌ <b>Gate Name Required</b>

Usage: <code>/setgate [gate]</code>
Available gates: <code>auth</code>, <code>stripe2</code>, <code>stripe4</code>rL  zt

Usage: <code>/setgate [gate]</code>
Available gates: <code>auth</code>, <code>stripe2</code>, <code>stripe4</code>zError setting default gate: uA   ❌ <b>Error setting default gateway.</b> Please contact support.)rj   r�   ra   r^   r�   r   rN   r�   rB   rH   rz   r{   r�   rX   r�   r�   rP   r:   )r`   �admin_user_idr�   rS   s       rA   �setgate_commandr�  �  su  � ��L�'�2�?�7�;S���L�L�O�O�M��M�"��|�|�G�%N�[a�|�b�b��m�Y����=�v��L�L�&�&�(��+�1�1�3�	��:�:��0�1�1� �����W� r�s|�  tH�  tH�  tJ�  sK�  KS�  T�  ag��  	h��� I����W�  u�  BH��  	I�� L����W� <�Q�C�  @w�  x�  EK��  	L�  	L��� v��,�Q�C�0�1����W�a�nt��u�u��v�s+   �.A&C �!E�8E� D!�!E�-&E�E�	broadcastc                 �  � t        t        | �      st        | �      sy t        | �      sy | j                  j
                  }t        |�      st        j                  | dd��      S t        |d| j                  �       	 | j                  j                  d��      d   }t        �       }d}d}|D ]?  }|t        v r�	 t        j                  ||dd	�
�       |dz  }t!        j"                  d�       �A t        j                  | d|� d|� d�d��       y # t        $ r t        j                  | dd��      cY S w xY w# t$        $ r }t'        d|� d|� ��       |dz  }Y d }~��d }~ww xY w)Nr�   r-   r.   r�  r   r�   u~   ❌ <b>Broadcast Message Required</b>

Usage: <code>/broadcast message</code>
Please provide the message content to broadcast.r   Tr�   g�������?zFailed to send message to user r�   u5   ✅ <b>Broadcast Completed</b>

Message broadcast to z users.
z users could not be reached.)rj   r�   ra   r�   r^   r�   r   rN   r�   rB   rH   rz   r�   �get_all_user_idsr�   r�   r�   r�  rP   r:   )r`   r;   rH   �all_user_ids�success_count�failure_countrS   s          rA   �broadcast_commandr�  �  sz  � ��L�'�2�?�7�;S���W�%�v��l�l�o�o�G��G���|�|�G�%N�[a�|�b�b��g�{�G�L�L�9�}��|�|�!�!�1�!�-�a�0�� $�%�L��M��M����l�"��	����W�d�v�X\��]��Q��M��J�J�s�O�  � �L�L��S�Ta�Sb�bk�ly�kz�  {W�  X�  ek�L�  l��' � }��|�|�G�  &i�  v|�|�  }�  	}�}�� � 	��3�G�9�B�q�c�B�C��Q��M��	�s*   �:D �63D2�!D/�.D/�2	E�;E�E�add_creditsc                 ��  � t        t        | �      st        | �      sy t        | �      rt        sy | j
                  j                  }t        |�      st        j                  | dd��      S t        |d| j                  �       	 | j                  j                  �       }t        |�      dk7  rt        d�      �t        |d   �      }t        |d   �      }|d	k  rt        d
�      �t!        ||�       t        j                  | d|� d|� d�d��       y # t        $ r%}t        j                  | d|� �d��      cY d }~S d }~wt"        $ r0}t%        d|� ��       t        j                  | dd��      cY d }~S d }~ww xY w)Nr�   r-   r.   r�  r�   zInvalid number of argumentsr   r�   r   z)Credits to add must be a positive number.u3   ✅ <b>Credits Added</b>

Successfully added <code>z!</code> credits to user ID <code>r:  u}   ❌ <b>Usage Error</b>

Usage: <code>/add_credits user_id amount</code> (user_id and amount must be integers > 0).

Details: zError adding credits: u8   ❌ <b>Error adding credits.</b> Please contact support.)rj   r�   ra   r�   r�   r^   r�   r   rN   r�   rB   rH   rz   r�   r�   r�   r   rP   r:   )r`   r;   r=   �target_user_id�credits_to_addrS   s         rA   �add_credits_commandr�  �  s�  � ��L�'�2�?�7�;S���W�%�-B�F��l�l�o�o�G��G���|�|�G�%N�[a�|�b�b� �g�}�g�l�l�;�t��|�|�!�!�#���t�9��>��:�;�;��T�!�W����T�!�W����Q���H�I�I��N�N�;����W� U�Vd�Ue�  fG�  HV�  GW�  W_�  `�  ms��  	t��� A��|�|�G�  (i�  jk�  il�  &m�  z@�|�  A�  	A��� t��&�q�c�*�+��|�|�G�%_�lr�|�s�s��t�s1   � B
D �	E0�D4�.E0�4E0� %E+�%E0�+E0�
setcreditsc                 �^  � t        t        | �      st        | �      sy t        | �      rt        sy | j
                  j                  }t        |�      st        j                  | dd��      S t        |d| j                  �       	 | j                  j                  �       }t        |�      dk7  rt        d�      �t        |d   �      }t        |d   �      }|d	k  rt        d
�      �t!        �       }t#        |�      }||vrt        j                  | d|� d�d��      S |||   d<   t%        |�       t        j                  | d|� d|� d�d��       y # t        $ r%}t        j                  | d|� �d��      cY d }~S d }~wt&        $ r0}t)        d|� ��       t        j                  | dd��      cY d }~S d }~ww xY w)Nr�   r-   r.   r�  r�   z#User ID and credit amount required.r   r�   r   z&Credits must be a non-negative number.�)   ❌ <b>User Not Found</b>

User ID <code>�</code> is not registered.r�   u#   ✅ <b>Credits Set</b>

User <code>z</code> credits set to <code>r:  uz   ❌ <b>Usage Error</b>

Usage: <code>/setcredits user_id credits</code> (credits must be non-negative integer).

Details: zError setting credits: u9   ❌ <b>Error setting credits.</b> Please contact support.)rj   r�   ra   r�   r�   r^   r�   r   rN   r�   rB   rH   rz   r�   r�   r�   r  r�   �_save_user_datarP   r:   )r`   r�  r=   r�  �credits_to_setr  �user_id_strrS   s           rA   �set_credits_commandr�  �  s�  � ��L�'�2�?�7�;S���W�%�-B�F��L�L�O�O�M��M�"��|�|�G�%N�[a�|�b�b��m�\�7�<�<�@�u��|�|�!�!�#���t�9��>��B�C�C��T�!�W����T�!�W����A���E�F�F�#�%�	��.�)���i�'��<�<��+V�We�Vf�  gA�  *B�  OU�<�  V�  V�,:�	�+��y�)��	�"����W� E�n�EU�Ur�  tB�  sC�  CK�  L�  Y_��  	`��� ~��|�|�G�  (f�  gh�  fi�  &j�  w}�|�  ~�  	~��� u��'��s�+�,��|�|�G�%`�ms�|�t�t��u�s7   � BE �2E �	F,�E0�*F,�0F,�<%F'�!F,�'F,�
setpremiumc                 �p  � t        t        | �      st        | �      sy t        | �      sy | j                  j
                  }t        |�      st        j                  | dd��      S t        |d| j                  �       	 | j                  j                  �       }t        |�      dk7  rt        d�      �t        |d   �      }|d   j                  �       }|d	vrt        d
�      �|dk(  }t!        �       }t#        |�      }||vrt        j                  | d|� d�d��      S |||   d<   t%        |�       |rdnd}t        j                  | d|� d|� d�d��       y # t        $ r%}	t        j                  | d|	� �d��      cY d }	~	S d }	~	wt&        $ r0}	t)        d|	� ��       t        j                  | dd��      cY d }	~	S d }	~	ww xY w)Nr�   r-   r.   r�  r�   z1User ID and premium status (true/false) required.r   r�   )�true�falsez)Premium status must be 'true' or 'false'.r�  r�  r�  r   zPremium EnabledzPremium Disabledu.   ✅ <b>Premium Status Updated</b>

User <code>z
</code> - r  ut   ❌ <b>Usage Error</b>

Usage: <code>/setpremium user_id true/false</code> (status as 'true' or 'false').

Details: zError setting premium status: u@   ❌ <b>Error setting premium status.</b> Please contact support.)rj   r�   ra   r�   r^   r�   r   rN   r�   rB   rH   rz   r�   r�   r�   r{   r  r�   r�  rP   r:   )
r`   r�  r=   r�  �premium_status_strr�   r  r�  �status_displayrS   s
             rA   �set_premium_commandr�    s�  � ��L�'�2�?�7�;S���W�%�v��L�L�O�O�M��M�"��|�|�G�%N�[a�|�b�b��m�\�7�<�<�@�|��|�|�!�!�#���t�9��>��P�Q�Q��T�!�W���!�!�W�]�]�_���%6�6��H�I�I�+�v�5��#�%�	��.�)���i�'��<�<��+V�We�Vf�  gA�  *B�  OU�<�  V�  V�/=�	�+��|�,��	�"�.<�*�BT�����W� P�Q_�P`�`j�ky�jz�z{�|�  JP��  	Q��� x��|�|�G�  (`�  ab�  `c�  &d�  qw�|�  x�  	x��� |��.�q�c�2�3��|�|�G�%g�tz�|�{�{��|�s7   �:BE �8E �	F5�E9�3F5�9F5�%F0�*F5�0F5�userinfoc                 �>  � t        t        | �      st        | �      sy t        | �      sy | j                  j
                  }t        |�      st        j                  | dd��      S t        |d| j                  �       	 | j                  j                  �       }t        |�      dk7  rt        d�      �t        |d   �      }t        rt!        |�      nd}t#        |�      xs d	d	d	d	d
�}t%        |�      j'                  �       xs t(        j'                  �       }t+        |�      }|rdnd}t-        t.        t0        �      s|nd}	d|� d|� d�}
t        r	|
d|	� d�z  }
|
d|� d|j3                  dd	�      � d|j3                  dd	�      � d|j3                  dd	�      � d|j3                  dd	�      � d�z  }
t        j                  | |
dd��       y # t        $ r t        j                  | dd��      cY S t4        $ r0}t7        d|� ��       t        j                  | dd��      cY d }~S d }~ww xY w) Nr�   r-   r.   r�  r�   zUser ID not specifiedr   r�   r   r�   r�   r�   u�   
👤 <b>User Information Panel</b> 👤
<a href='https://t.me/+GdWapjhiAG05OTk1'>┏━━━━━━━━━━━⍟</a>
<a href='https://t.me/+GdWapjhiAG05OTk1'>┃</a><b>👤 User ID</b>: <code>u�   </code><a href='https://t.me/+GdWapjhiAG05OTk1'>┗━━━━━━━⊛</a>
<a href='https://t.me/+GdWapjhiAG05OTk1'>-</a> ⭐ <b>𝗣𝗿𝗲𝗺𝗶𝘂𝗺</b>: <code>r�   u`   
<a href='https://t.me/+GdWapjhiAG05OTk1'>-</a> 💰 <b>𝐂𝐫𝐞𝐝𝐢𝐭𝐬</b>: <code>uV   
<a href='https://t.me/+GdWapjhiAG05OTk1'>-</a> ⚙️ <b>𝐆𝐚𝐭𝐞</b>: <code>u�   </code>

📊 <b>Ｃｈｅｃｋ Ｓｔａｔｓ</b>:
<a href='https://t.me/+GdWapjhiAG05OTk1'>-</a> ✅ <b>𝐀𝐩𝐩𝐫𝐨𝐯𝐞𝐝</b>: <code>r�   uj   </code>
<a href='https://t.me/+GdWapjhiAG05OTk1'>-</a> ❌ <b>𝐃𝐞𝐜𝐥𝐢𝐧𝐞𝐝</b>: <code>r   uY   </code>
<a href='https://t.me/+GdWapjhiAG05OTk1'>-</a> ⚠️ <b>𝐂𝐂𝐍</b>: <code>r  uV   </code>
<a href='https://t.me/+GdWapjhiAG05OTk1'>-</a> ✅ <b>𝐂𝐕𝐕</b>: <code>r  r  Tr�   ul   ❌ <b>Usage Error: User ID Required</b>

Usage: <code>/userinfo user_id</code> (user_id must be an integer)zError getting user info: u>   ❌ <b>Error retrieving user info.</b> Please contact support.)rj   r�   ra   r�   r^   r�   r   rN   r�   rB   rH   rz   r�   r�   r�   r�   r
   r   r   r�   rX   r   r	  r�   r�   r  rP   r:   )r`   r;   r=   r�  �user_creditsr  �user_gate_preferencer  r�   r
  �user_info_textrS   s               rA   �userinfo_commandr�  5  s�  � ��L�'�2�?�7�;S���W�%�v��l�l�o�o�G��G���|�|�G�%N�[a�|�b�b��g�z�7�<�<�8�$z��|�|�!�!�#���t�9��>��4�5�5��T�!�W���;P�'��7�Va��#�N�3�i�A�ST�]^�gh�7i�
�7��G�R�R�T�q�Xd�Xo�Xo�Xq��$�^�4��*9��{��.8��#�.F�,�K��L� M[�K[� \_�_m�^n�nu�	y��
 !��  "C�  DS�  CT�  T[�   \�  \�^�� V�Vj�Uk� lc� dn�cq�cq�r|�~�  dA�  cB� Bc�cm�cq�cq�r|�~�  dA�  cB� BR�R\�R`�R`�af�hi�Rj�Qk� lO�OY�~�~�^c�ef�Og�Nh� i�� 	�� 	���W�n��Z^��_��� j��|�|�G�  &V�  ci�|�  j�  	j�� z��)�!��-�.��|�|�G�%e�rx�|�y�y��z�s%   �:EG �!H�$H�,%H�H�Hr�   c                 �  � t        t        | �      st        | �      sy t        | �      sy | j                  j
                  }t        |�      st        j                  | dd��      S t        |d| j                  �       	 | j                  j                  �       }t        |�      dk7  rt        d�      �t        |d   �      }t        |�      rt        j                  | d|� d	�d��       y t        j                  | d
|� d�d��       y # t        $ r t        j                  | dd��      cY S t         $ r0}t#        d|� ��       t        j                  | dd��      cY d }~S d }~ww xY w)Nr�   r-   r.   r�   r�   z%User ID to add as admin not specifiedr   u3   ✅ <b>Admin Privileges Granted</b>

User ID <code>z </code> added to the admin list.u+   ⚠️ <b>Already Admin</b>

User ID <code>z</code> is already an admin.ug   ❌ <b>Usage Error: User ID Required</b>

Usage: <code>/add user_id</code> (user_id must be an integer)zError adding admin: u/   ❌ <b>Error adding admin.</b> Contact support.)rj   r�   ra   r�   r^   r�   r   rN   r�   rB   rH   rz   r�   r�   r�   r   rP   r:   �r`   r�  r=   r�  rS   s        rA   �add_admin_commandr�  f  s[  � ��L�'�2�?�7�;S���W�%�v��L�L�O�O�M��M�"��|�|�G�%N�[a�|�b�b��m�U�G�L�L�9�k��|�|�!�!�#���t�9��>��D�E�E��T�!�W����.�)��L�L��$Y�Zh�Yi�  jJ�  #K�  X^�L�  _��L�L��$Q�R`�Qa�a}�"~�  LR�L�  S��� e��|�|�G�  &Q�  ^d�|�  e�  	e�� k��$�Q�C�(�)��|�|�G�%V�ci�|�j�j��k��+   �:A(D  �#D  � !E�#E�+%E�E�ErQ   c                 �  � t        t        | �      st        | �      sy t        | �      sy | j                  j
                  }t        |�      st        j                  | dd��      S t        |d| j                  �       	 | j                  j                  �       }t        |�      dk7  rt        d�      �t        |d   �      }t        |�      rt        j                  | d|� d	�d��       y t        j                  | d
|� d�d��       y # t        $ r t        j                  | dd��      cY S t         $ r0}t#        d|� ��       t        j                  | dd��      cY d }~S d }~ww xY w)Nr�   r-   r.   rQ   r�   z+User ID to remove from admins not specifiedr   u3   ✅ <b>Admin Privileges Revoked</b>

User ID <code>z$</code> removed from the admin list.u7   ⚠️ <b>Not an Admin or Bot Owner</b>

User ID <code>z9</code> is not an admin or cannot be removed (bot owner).uj   ❌ <b>Usage Error: User ID Required</b>

Usage: <code>/remove user_id</code> (user_id must be an integer)zError removing admin: u1   ❌ <b>Error removing admin.</b> Contact support.)rj   r�   ra   r�   r^   r�   r   rN   r�   rB   rH   rz   r�   r�   r�   r   rP   r:   r�  s        rA   �remove_admin_commandr�  �  sb  � ��L�'�2�?�7�;S���W�%�v��L�L�O�O�M��M�"��|�|�G�%N�[a�|�b�b��m�X�w�|�|�<�m��|�|�!�!�#���t�9��>��J�K�K��T�!�W����^�,��L�L��$Y�Zh�Yi�  jN�  #O�  \b�L�  c��L�L��$]�^l�]m�  ng�  #h�  u{�L�  |��� h��|�|�G�  &T�  ag�|�  h�  	h�� m��&�q�c�*�+��|�|�G�%X�ek�|�l�l��m�r�  �
listadminsc                 �`  � t        t        | �      st        | �      sy t        | �      sy | j                  j
                  }t        |�      st        j                  | dd��      S t        |d�       t        �       }d}|r|D ]  }|d|� d�z  }� n|dz  }|d	z  }t        j                  | |d��       y )
Nr�   r-   r.   r�  u�   🛡️ <b>Current Admins</b> 🛡️
<a href='https://t.me/+GdWapjhiAG05OTk1'>┏━━━━━━━━━━━⍟</a>
<a href='https://t.me/+GdWapjhiAG05OTk1'>┃</a>
z- <code>r  zNo admins added yet.
r�   )rj   r�   ra   r�   r^   r�   r   rN   r�   rB   r   )r`   r�  �
admin_list�
admin_textr�   s        rA   �list_admins_commandr�  �  s�   � ��L�'�2�?�7�;S���W�%�v��L�L�O�O�M��M�"��|�|�G�%N�[a�|�b�b��m�\�2��!�J� C�J��"�H��H�X�J�i�8�8�J� #� 	�.�.�
��\�\�J��L�L��*��L�8r[   �banc                 ��  � t        t        | �      st        | �      sy t        | �      sy | j                  j
                  }t        |�      st        j                  | dd��      S t        |d| j                  �       	 | j                  j                  �       }t        |�      dk7  rt        d�      �t        |d   �      }|t        �       v rt        j                  | dd��      S t         j#                  |�       t        j                  | d	|� d
�d��       y # t        $ r t        j                  | dd��      cY S t$        $ r0}t'        d|� ��       t        j                  | dd��      cY d }~S d }~ww xY w)Nr�   r-   r.   r�  r�   zUser ID to ban not specifiedr   u   🚫 Cannot ban another admin.u&   ✅ <b>User Banned</b>

User ID <code>z+</code> has been banned from using the bot.ug   ❌ <b>Usage Error: User ID Required</b>

Usage: <code>/ban user_id</code> (user_id must be an integer)zError banning user: u6   ❌ <b>Error banning user.</b> Please contact support.)rj   r�   ra   r�   r^   r�   r   rN   r�   rB   rH   rz   r�   r�   r�   r   r�   �appendrP   r:   r�  s        rA   �ban_user_commandr�  �  s[  � ��L�'�2�?�7�;S���W�%�v��L�L�O�O�M��M�"��|�|�G�%N�[a�|�b�b��m�U�G�L�L�9�r��|�|�!�!�#���t�9��>��;�<�<��T�!�W����^�-�-��<�<��)I�V\�<�]�]����N�+����W� H��HX�  YD�  E�  RX��  	Y��� e��|�|�G�  &Q�  ^d�|�  e�  	e�� r��$�Q�C�(�)��|�|�G�%]�jp�|�q�q��r�s+   �:A$D �1D �!E,�4E,�<%E'�!E,�'E,�unbanc                 ��  � t        t        | �      st        | �      sy t        | �      sy | j                  j
                  }t        |�      st        j                  | dd��      S t        |d| j                  �       	 | j                  j                  �       }t        |�      dk7  rt        d�      �t        |d   �      }|t        v r2t        j!                  |�       t        j                  | d|� d	�d��       y t        j                  | d
|� d�d��       y # t        $ r t        j                  | dd��      cY S t"        $ r0}t%        d|� ��       t        j                  | dd��      cY d }~S d }~ww xY w)Nr�   r-   r.   r�  r�   zUser ID to unban not specifiedr   u(   ✅ <b>User Unbanned</b>

User ID <code>z</code> has been unbanned.u-   ⚠️ <b>User Not Banned</b>

User ID <code>z&</code> was not found in the ban list.ui   ❌ <b>Usage Error: User ID Required</b>

Usage: <code>/unban user_id</code> (user_id must be an integer)zError unbanning user: u8   ❌ <b>Error unbanning user.</b> Please contact support.)rj   r�   ra   r�   r^   r�   r   rN   r�   rB   rH   rz   r�   r�   r�   r�   rQ   rP   r:   r�  s        rA   �unban_user_commandr�  �  sh  � ��L�'�2�?�7�;S���W�%�v��L�L�O�O�M��M�"��|�|�G�%N�[a�|�b�b��m�W�g�l�l�;�t��|�|�!�!�#���t�9��>��=�>�>��T�!�W����\�)�����/��L�L��$N�~�N^�^x�"y�  GM�L�  N��L�L��$S�Tb�Sc�  dJ�  #K�  X^�L�  _��� g��|�|�G�  &S�  `f�|�  g�  	g�� t��&�q�c�*�+��|�|�G�%_�lr�|�s�s��t�s+   �:A:D �5D �!E-�5E-�=%E(�"E-�(E-�unbanallc                 �8  � t        t        | �      st        | �      sy t        | �      sy | j                  j
                  }t        |�      st        j                  | dd��      S t        |d�       t        t        �      }g at        j                  | d|� d�d��       y )Nr�   r-   r.   r�  u;   ✅ <b>All Users Unbanned</b>

Successfully unbanned <code>z</code> users.)rj   r�   ra   r�   r^   r�   r   rN   r�   rB   r�   r�   )r`   r�  �users_unbanneds      rA   �unbanall_commandr�  �  s�   � ��L�'�2�?�7�;S���W�%�v��L�L�O�O�M��M�"��|�|�G�%N�[a�|�b�b��m�Z�0� ��&�N��L��L�L��Y�Zh�Yi�iw�x�  FL�L�  Mr[   �botstatsc                 �R  � t        t        | �      st        | �      sy t        | �      sy | j                  j
                  }t        |�      st        j                  | dd��      S t        |d�       t        �       }t        |�      }t        t        �       �      }t        t        �      }dt        � d|� d|� d|� d	t        rd
nd� dt         rd
nd� dt"        rd
nd� dt$        rd
nd� dt&        rd
nd� dt(        rd
nd� dt*        j-                  �       � d�}t        j                  | |dd��       y )Nr�   r-   r.   r�  u�   
📊 <b>Bot Statistics</b> 📊
<a href='https://t.me/+GdWapjhiAG05OTk1'>┏━━━━━━━━━━━⍟</a>
<a href='https://t.me/+GdWapjhiAG05OTk1'>┃</a><b>🤖 Bot Version</b>: <code>u�   </code><a href='https://t.me/+GdWapjhiAG05OTk1'>┗━━━━━━━⊛</a>
<a href='https://t.me/+GdWapjhiAG05OTk1'>-</a> 👥 <b>Total Users</b>: <code>uZ   </code>
<a href='https://t.me/+GdWapjhiAG05OTk1'>-</a> 🛡️ <b>Total Admins</b>: <code>uW   </code>
<a href='https://t.me/+GdWapjhiAG05OTk1'>-</a> 🚫 <b>Banned Users</b>: <code>uY   </code>
<a href='https://t.me/+GdWapjhiAG05OTk1'>-</a> ✅ <b>Referral System</b>: <code>�Enabled�DisableduX   </code>
<a href='https://t.me/+GdWapjhiAG05OTk1'>-</a> 💰 <b>Credit System</b>: <code>uW   </code>
<a href='https://t.me/+GdWapjhiAG05OTk1'>-</a> 🎁 <b>Redeem Codes</b>: <code>uV   </code>
<a href='https://t.me/+GdWapjhiAG05OTk1'>-</a> 📝 <b>Group Check</b>: <code>uZ   </code>
<a href='https://t.me/+GdWapjhiAG05OTk1'>-</a> ℹ️  <b>Detailed BIN</b>: <code>uV   </code>
<a href='https://t.me/+GdWapjhiAG05OTk1'>-</a> 💳 <b>Card Brands</b>: <code>uZ   </code>
<a href='https://t.me/+GdWapjhiAG05OTk1'>-</a> 🛡️ <b>Default Gate</b>: <code>r  Tr�   )rj   r�   ra   r�   r^   r�   r   rN   r�   rB   r�  r�   r   r�   r�   r�   r�   r�   r|  r~  r  rX   r�   )r`   r�  r�  �total_users�admin_count�banned_count�
stats_texts          rA   �botstats_commandr�  �  s}  � ��L�'�2�?�7�;S���W�%�v��L�L�O�O�M��M�"��|�|�G�%N�[a�|�b�b��m�Z�0�#�%�L��l�#�K��n�&�'�K��|�$�L�P� Q\�}� ]O�OZ�m� \S�S^�R_� `P�P\�~� ^R�_v�R[�  }G�  RH� HQ�^s�QZ�  zD�  QE� EP�]r�PY�  yC�  PD� DO�\n�y�t~�N� @S�`q�S\�  xB�  SC� CO�\n�y�t~�N� @S�S_�Sj�Sj�Sl�Rm� n��J� �L�L��*��RV�L�Wr[   �getlogc                 �  � t        t        | �      st        | �      sy t        | �      sy | j                  j
                  }t        |�      st        j                  | dd��      S t        |d| j                  �       	 | j                  j                  �       }d}t        |�      dkD  rt        |d   �      }|dk  s|dkD  rd}t        t        d	�      5 }|j!                  �       }d d d �       st        j                  | d
d��      S d|� d�}|| d  D ]  }||z  }�	 |dz  }t        j                  | |d��       y # 1 sw Y   �WxY w# t"        $ r t        j                  | dd��       Y y t$        $ r t        j                  | dd��       Y y t&        $ r0}t)        d|� ��       t        j                  | dd��       Y d }~y d }~ww xY w)Nr�   r-   r.   r�  �
   r   r   �d   �ruB   📜 <b>Admin Command Logs</b> 📜

No admin commands logged yet.u!   📜 <b>Admin Command Logs (Last u�    entries)</b> 📜
<a href='https://t.me/+GdWapjhiAG05OTk1'>┏━━━━━━━━━━━⍟</a>
<a href='https://t.me/+GdWapjhiAG05OTk1'>┃</a>
r�   u>   📜 <b>Admin Command Logs</b> 📜

Admin log file not found.u�   ❌ <b>Usage Error: Invalid Number of Lines</b>

Usage: <code>/getlog [lines]</code> (lines must be a positive integer, max 100).zError reading admin logs: u5   ❌ <b>Error reading admin logs.</b> Contact support.)rj   r�   ra   r�   r^   r�   r   rN   r�   rB   rH   rz   r�   r�   r7   r8   �	readlines�FileNotFoundErrorr�   rP   r:   )	r`   r�  r=   �lines_to_getr@   �logs�log_text�	log_entryrS   s	            rA   �getlog_commandr�    s�  � ��L�'�2�?�7�;S���W�%�v��L�L�O�O�M��M�"��|�|�G�%N�[a�|�b�b��m�X�w�|�|�<�j��|�|�!�!�#�����t�9�q�=��t�A�w�<�L��q� �L�3�$6�!���(�#�.�'��$�$�&�D� /���<�<��)o�  }C�<�  D�  D�6�|�n�  Ea�  b���|�m�n�-�I��	�!�H� .��^�^�����W�h�6��:� /�.�� � u����W�`�ms��t�� x����W�  d�  qw��  	x�� j��*�1�#�.�/����W�U�bh��i�i��j�sC   �:AE �D5�!E �3E �5D>�:E �!F>�$ F>�F>�&F9�9F>�	clearlogsc                 ��  � t        t        | �      st        | �      sy t        | �      sy | j                  j
                  }t        |�      st        j                  | dd��      S t        |d�       	 t        t        d�      j                  �        t        j                  | dd��       y # t        $ r0}t        d|� ��       t        j                  | dd��       Y d }~y d }~ww xY w)	Nr�   r-   r.   r�  �wub   ✅ <b>Admin Command Logs Cleared!</b> 📜

All admin command logs have been permanently deleted.zError clearing admin logs: u=   ❌ <b>Error clearing admin logs.</b> Please contact support.)rj   r�   ra   r�   r^   r�   r   rN   r�   rB   r7   r8   �closerP   r:   )r`   r�  rS   s      rA   �clearlogs_commandr�  C  s�   � ��L�'�2�?�7�;S���W�%�v��L�L�O�O�M��M�"��|�|�G�%N�[a�|�b�b��m�[�1�r��#�S�)�/�/�1����W�  E�  RX��  	Y��� r��+�A�3�/�0����W�]�jp��q�q��r�s   �/6B& �&	C�/&C�C�
backupdatac                 �.  � t        t        | �      st        | �      sy t        | �      sy | j                  j
                  }t        |�      st        j                  | dd��      S t        |d�       	 t        �       }t        �       }t        �       }dt        j                  �       j                  d�      � d�}|||t!        �       t#        �       t$        d�}t'        |d	�      5 }t)        j*                  ||d
��       d d d �       t        j-                  | j                  j
                  t'        |d�      d|� d�d��       t/        j0                  |�       y # 1 sw Y   �ZxY w# t2        $ r0}t5        d|� ��       t        j                  | dd��       Y d }~y d }~ww xY w)Nr�   r-   r.   r�  �bot_backup_z%Y%m%d_%H%M%Sz.json)r  �redeem_data�	admin_idsr�   r�   �default_gater�  �   )�indent�rbu<   ✅ <b>Bot Data Backup Created!</b>

Backup filename: <code>r�   )�captionr/   zError creating backup: u9   ❌ <b>Error creating backup.</b> Please contact support.)rj   r�   ra   r�   r^   r�   r   rN   r�   rB   r  �_load_redeem_datar   r   r5   r6   r   r   rX   r7   rO  �dump�send_documentrI   rQ   rP   r:   )	r`   r�  r  r�  r�  �backup_filename�backup_data�backup_filerS   s	            rA   �backupdata_commandr   U  sw  � ��L�'�2�?�7�;S���W�%�v��L�L�O�O�M��M�"��|�|�G�%N�[a�|�b�b��m�\�2�n�#�%�	�'�)��"�$�	�'�����(?�(?��(P�'Q�QV�W��"�&�"�0�2�0�2�(�
�� �/�3�'�;��I�I�k�;�q�9� (� 	���'�,�,�/�/�4���+F�  SQ�  Ra�  Qb�  bi�  Qj�  w}��  	~�
�	�	�/�"�	 (�'�� � n��'��s�+�,����W�Y�fl��m�m��n�s2   �/A.E �E�6AE �E�E �	F�$&F�F�sendc                 ��  � t        t        | �      st        | �      sy t        | �      sy | j                  j
                  }t        |�      st        j                  | dd��      S t        |d| j                  �       	 | j                  j                  d��      }t        |�      dk  rt        d�      �t        |d	   �      }|d   }t        j                  ||dd
��       t        j                  | d|� d�d��       y # t        $ r%}t        j                  | d|� �d��      cY d }~S d }~wt         $ r0}t#        d|� ��       t        j                  | dd��      cY d }~S d }~ww xY w)Nr�   r-   r.   r  r�   r�   r�   z"User ID and message text required.r   Tr�   u7   ✅ <b>Message Sent</b>

Message sent to user ID <code>r:  uL   ❌ <b>Usage Error</b>

Usage: <code>/send user_id message</code>

Details: zError sending message: u9   ❌ <b>Error sending message.</b> Please contact support.)rj   r�   ra   r�   r^   r�   r   rN   r�   rB   rH   rz   r�   r�   r�   r�   rP   r:   )r`   r�  r=   r�  �message_textrS   s         rA   �send_message_commandr  y  sR  � ��L�'�2�?�7�;S���W�%�v��L�L�O�O�M��M�"��|�|�G�%N�[a�|�b�b��m�V�W�\�\�:�u��|�|�!�!�1�!�-���t�9�q�=��A�B�B��T�!�W����A�w�������&�cg��h����W� Y�Zh�Yi�iq�r�  @F��  	G��� P��|�|�G�'w�xy�wz�%{�  IO�|�  P�  	P��� u��'��s�+�,��|�|�G�%`�ms�|�t�t��u�s1   �:A=C8 �8	E�D!�E�!E�-%E�E�E�forwardc                 ��  � t        t        | �      st        | �      sy t        | �      sy | j                  j
                  }t        |�      st        j                  | dd��      S t        |d| j                  �       	 | j                  j                  d��      }t        |�      dk  rt        d�      �t        |d	   �      }t        |d   �      }t        j                  || j                  j
                  |�       t        j                  | d
|� d|� d�d��       y # t        $ r%}t        j                  | d|� �d��      cY d }~S d }~wt         $ r0}t#        d|� ��       t        j                  | dd��      cY d }~S d }~ww xY w)Nr�   r-   r.   r  r�   r�   r�   z User ID and message ID required.r   u/   ✅ <b>Message Forwarded</b>

Message ID <code>z#</code> forwarded to user ID <code>r:  uR   ❌ <b>Usage Error</b>

Usage: <code>/forward user_id message_id</code>

Details: zError forwarding message: u<   ❌ <b>Error forwarding message.</b> Please contact support.)rj   r�   ra   r�   r^   r�   r   rN   r�   rB   rH   rz   r�   r�   r�   r�   rP   r:   )r`   r�  r=   r�  �message_id_to_forwardrS   s         rA   �forward_message_commandr  �  s}  � ��L�'�2�?�7�;S���W�%�v��L�L�O�O�M��M�"��|�|�G�%N�[a�|�b�b��m�Y����=�x��|�|�!�!�1�!�-���t�9�q�=��?�@�@��T�!�W��� #�D��G������N�G�L�L�O�O�=R�S����W� Q�Rg�Qh�  iL�  M[�  L\�  \d�  e�  rx��  	y��� V��|�|�G�'}�~�  ~A�  &B�  OU�|�  V�  	V��� x��*�1�#�.�/��|�|�G�%c�pv�|�w�w��x�s1   �:BD �	E;�D?�9E;�?E;�%E6�0E;�6E;�setgatepricec                 ��  � t        t        | �      st        | �      sy t        | �      sy | j                  j
                  }t        |�      st        j                  | dd��      S t        |d| j                  ��       	 | j                  j                  �       }t        |�      dk7  rt        d�      �|d   j                  �       }t        |d	   �      }|d
k  rt        d�      �t        j                  | d|� d|� d�d��       y # t        $ r%}t        j                  | d|� �d��      cY d }~S d }~wt         $ r0}t#        d|� ��       t        j                  | dd��      cY d }~S d }~ww xY w)Nr�   r-   r.   r	  �r;   r<   r=   r�   zGate name and price required.r   r�   r   zPrice must be non-negative.u0   ✅ <b>Gate Price Set</b>

Price for gate <code>�</code> set to <code>r:  uv   ❌ <b>Usage Error</b>

Usage: <code>/setgateprice gate price</code> (price must be a non-negative number).

Details: zError setting gate price: u5   ❌ <b>Error setting gate price.</b> Contact support.)rj   r�   ra   r�   r^   r�   r   rN   r�   rB   rH   rz   r�   r�   r{   �floatrP   r:   )r`   r�  r=   r�   rr   rS   s         rA   �setgateprice_commandr  �  sl  � ��L�'�2�?�7�;S���W�%�v��L�L�O�O�M��M�"��|�|�G�%N�[a�|�b�b��m�^�'�,�,�W�q��|�|�!�!�#���t�9��>��<�=�=���G�M�M�O�	��d�1�g����1�9��:�;�;����W� R�S\�R]�]r�sx�ry�  zB�  C�  PV��  	W��� z��|�|�G�  (b�  cd�  be�  &f�  sy�|�  z�  	z��� q��*�1�#�.�/��|�|�G�%\�io�|�p�p��q�s1   �;BC? �?	E$�D(�"E$�(E$�4%E�E$�E$�	getconfigc                 ��  � t        t        | �      st        | �      sy t        | �      sy | j                  j
                  }t        |�      st        j                  | dd��      S t        |d��       dt        � dt        rdnd	� d
t        rdnd	� dt        rdnd	� dt        rdnd	� dt        rdnd	� dt         rdnd	� dt#        �       � dt%        �       � dt&        j)                  �       � d�}t        j                  | |d��       y )Nr�   r-   r.   r  )r;   r<   u�   
⚙️ <b>Bot Configuration</b> ⚙️
<a href='https://t.me/+GdWapjhiAG05OTk1'>┏━━━━━━━━━━━⍟</a>
<a href='https://t.me/+GdWapjhiAG05OTk1'>┃</a>
<b>Bot Version:</b> <code>z"</code>
<b>Group Check:</b> <code>r�  r�  z(</code>
<b>Detailed BIN Info:</b> <code>z)</code>
<b>Display Card Brand:</b> <code>z&</code>
<b>Referral System:</b> <code>z$</code>
<b>Redeem System:</b> <code>z$</code>
<b>Credit System:</b> <code>z%</code>
<b>Referrer Bonus:</b> <code>z- credits</code>
<b>Referred Bonus:</b> <code>z+ credits</code>
<b>Default Gate:</b> <code>r  )rj   r�   ra   r�   r^   r�   r   rN   r�   rB   r�   r|  r~  r  r�   r�   r�   r   r   rX   r�   )r`   r�  �config_texts      rA   �getconfig_commandr  �  s  � ��L�'�2�?�7�;S���W�%�v��L�L�O�O�M��M�"��|�|�G�%N�[a�|�b�b��m�[�A�� '�-� (�(:�9�
�K� L!�.?��Z� P� Q"�/A�)�z�!R� S�,C�y��T� U�*?�Y�Z�P� Q�*?�Y�Z�P� Q�0�2�3� 4�0�2�3� 4�(�3�3�5�6� 7��K� �L�L��+�&�L�9r[   �	setconfigc                 �\  � t        t        | �      st        | �      sy t        | �      sy | j                  j
                  }t        |�      st        j                  | dd��      S t        |d| j                  ��       	 | j                  j                  d��      }t        |�      dk7  rt        d	�      �|d
   j                  �       }|d   j                  �       }|dk(  r|dk(  anE|dk(  r|dk(  an:|dk(  r|dk(  an/|dk(  r|dk(  an$|dk(  r|dk(  an|dk(  r|dk(  ant        d|� ��      �t        j                  | d|� d|� d�d��       y # t        $ r%}t        j                  | d|� �d��      cY d }~S d }~wt,        $ r0}t/        d|� ��       t        j                  | dd��      cY d }~S d }~ww xY w)Nr�   r-   r.   r  r  r�   r�   r�   z Setting name and value required.r   r|  r�  r~  r  r�   r�   r�   zInvalid setting name: u.   ✅ <b>Bot Setting Updated</b>

Setting <code>r  r:  uk   ❌ <b>Usage Error</b>

Usage: <code>/setconfig setting value</code> (value must be true/false).

Details: zError setting bot config: u<   ❌ <b>Error setting bot configuration.</b> Contact support.)rj   r�   ra   r�   r^   r�   r   rN   r�   rB   rH   rz   r�   r�   r}  r{   r|  r~  r  r�   r�   r�   rP   r:   )r`   r�  r=   �setting_name�setting_valuerS   s         rA   �setconfig_commandr  �  s�  � ��L�'�2�?�7�;S���W�%�v��L�L�O�O�M��M�"��|�|�G�%N�[a�|�b�b��m�[�w�|�|�T�x��|�|�!�!�1�!�-���t�9��>��?�@�@��A�w�}�}����Q������ �/�/�!.�&�!8���0�0� -�� 7���1�1�!.�&�!8���6�6�&3�v�&=�#��4�4�$1�V�$;�!��4�4�$1�V�$;�!��5�l�^�D�E�E����W� P�Q]�P^�^s�  uB�  tC�  CK�  L�  Y_��  	`��� o��|�|�G�  (W�  XY�  WZ�  &[�  hn�|�  o�  	o��� x��*�1�#�.�/��|�|�G�%c�pv�|�w�w��x�s1   �;C
E �	F+�E/�)F+�/F+�;%F&� F+�&F+r{  )�content_typesc                 ��  � t        t        | �      st        | �      sy t        | �      sy | j                  j
                  }t        rt        |�      nd}t        r&|dk7  r!|dk  rt        j                  | d|� d�d��      S d}d}d}d}t        j                  | d�      j                  }	 t        j                  | j                  j                  �      }t        j                  |j                  �      }	|	j!                  d	�      }
t1        |
�      }d}d}t3        �       }|st        j                  | dd��       y t5        |�      }t7        |�      }|j9                  �       j;                  dd�      j;                  dd�      j;                  dd�      }|D �]�  }t=        | j                  j
                  |�      r y t        rJt?        |�      s?t        j)                  | j                  j
                  |d|� dt        |�      � d�d��        y |dz  }|dz  }	 t@        r)tC        jD                  d|d d z   �      jG                  �       ni }|jE                  dd�      jI                  �       }|jE                  d d�      }|jE                  d!d�      }|jE                  d"d�      }|jE                  d#d�      }tJ        r$tL        jE                  ||jO                  �       �      n|jO                  �       }tQ        jP                  �       }tS         |||jU                  �       �      �      }tW        ||jY                  d$�      d   �       tQ        jP                  �       }||z
  }d%|� d&|� d'|� d(|d d � d)|� d*|� d+|� d*|� d,|� d-t[        |d�      � d.�}d/|v sd0|v r3|dz  }t        j]                  | j                  j
                  |dd1�2�       nd3|v r|dz  }nd4|v sd5|v sd6|v r|dz  }d7|� d8|� d9|� d:|� d;�	} 	 t        j)                  | j                  j
                  || dd1�<�       tQ        j^                  d>�       ��� t        j]                  | j                  j
                  d?|� d@t        rt        |�      nd� d�d�A�       	 t        j)                  | j                  j
                  |dBdd1�<�       y # t"        j$                  j&                  $ rG}t        j)                  | j                  j
                  |d
|� ���       t+        d|� ��       Y d }~y d }~wt,        $ rD}t        j)                  | j                  j
                  |d��       t+        d|� ��       Y d }~y d }~wt.        $ rG}t        j)                  | j                  j
                  |d|� ���       t+        d|� ��       Y d }~y d }~ww xY w#  i }Y ��bxY w# t.        $ r}t+        d=|� ��       Y d }~���d }~ww xY w# t.        $ r}t+        dC|� ��       Y d }~y d }~ww xY w)DNr�   r   r_  zS</code> credits. You need at least 1 credit to perform a check. Redeem or buy more.r-   r.   r   u'   📝 <b>Processing Card File</b>... ⌛zutf-8uR   ❌ <b>File Download Error</b>

Could not download file from Telegram API. Error: rE   z-Telegram API Exception during file download: uj   ❌ <b>File Encoding Error</b>

Could not decode file as UTF-8. Please ensure the file is in UTF-8 format.)�chatIdrG   rH   zUnicodeDecodeError: ua   ❌ <b>File Download Error</b>

Could not download file. Ensure it's valid and try again. Error: zGeneral File Download Error: uC   ❌ <b>Session Error</b>

Failed to start session. Try again later.r`  rV   r�   rW   r�   rc  z:</code> cards.
Redeem or buy more credits. Credits: <code>r�   rd  r9  re  r;  rf  r_   r@  rA  r>  r�   u  
<a href='https://envs.sh/smD.webp'>-</a> ✅ <b>𝐀𝐏𝐏𝐑𝐎𝐕𝐄𝐃 𝐂𝐀𝐑𝐃</b> ✅
<a href='https://t.me/+GdWapjhiAG05OTk1'>┏━━━━━━━━━━━⍟</a>
<a href='https://t.me/+GdWapjhiAG05OTk1'>┃</a>💳 𝐂𝐂: <code>u�   </code><a href='t.me/addlist/u2A-7na8YtdhZWVl'>┗━━━━━━━⊛</a>
<a href='https://t.me/+GdWapjhiAG05OTk1'>-</a> ⚡ 𝐆𝐚𝐭𝐞𝐰𝐚𝐲: ⤿ uc    🟢 ⤾
<a href='https://t.me/+GdWapjhiAG05OTk1'>-</a> ✅ 𝐑𝐞𝐬𝐩𝐨𝐧𝐬𝐞: ⤿ uN    ⤾

<a href='https://envs.sh/smD.webp'>-</a> ℹ️ 𝐈𝐧𝐟𝐨: <code>rg  rh  ri  uT   </code>
<a href='https://t.me/+GdWapjhiAG05OTk1'>-</a> 🏦 𝐁𝐚𝐧𝐤: <code>uW   </code>

<a href='https://t.me/+GdWapjhiAG05OTk1'>-</a> ⏱️ 𝐓𝐢𝐦𝐞: <code>u�    𝐬𝐞𝐜</code>
<a href='https://t.me/+GdWapjhiAG05OTk1'>-</a> 🤖 𝐁𝐨𝐭 𝐀𝐛𝐨𝐮𝐭: <a href='https://t.me/+GdWapjhiAG05OTk1'>Crimson </a>rj  rk  Tr�   rl  rm  rn  ro  u�   📝 <b>Processing File...</b> 📝
🤖 𝗕𝘆 ➜ <a href='https://t.me/+GdWapjhiAG05OTk1'>Crimson </a>

✅ 𝐀𝐏𝐏𝐑𝐎𝐕𝐄𝐃 : [ rp  rq  rr  rs  rt  ru  rv  rw  z;</code> cards from document file.
Credits remaining: <code>rx  ry  zAn error occurred: )0rj   r�   ra   r�   r^   r�   r�   r
   rN   r�   rG   �get_filer{  �file_id�download_file�	file_path�decode�telebot�	apihelper�ApiExceptionrO   r:   �UnicodeDecodeErrorrP   r    r   rZ   r   r}  r�   rT   r   r~  rN  r  rO  r{   r  r�  r�   r�   r�   rz  r   rz   r�   r�   r�  )!r`   r;   r�   r�  r�  r�  �ch�ko�	file_info�downloaded_file�eerS   r�  �totalr�  r�  r�  r�  r�  r]  r�   r;  r�  r�  rA  r>  r�  r�   r�  r�   r�  r�  r�  s!                                    rA   �mainr*    s�  � ��L�'�2�?�7�;S���W�%�v��l�l�o�o�G�+@��w�'�k�G���K�!7�G�a�K��|�|�G�'Z�[b�Zc�  dw�  &x�  EK�|�  L�  	L�	
�B��D��I�	
�B�	���g�H�	I�	T�	T�B���L�L��!1�!1�!9�!9�:�	��+�+�I�,?�,?�@���#�#�G�,�� )��,�L��E��M�!�#�G�����W�e�rx��y��.�w�7�M�3�G�<��,�2�2�4�<�<�V�V�L�T�T�U^�`d�e�m�m�nw�y}�~�����g�l�l�o�o�r�2�� �!�'�*��%�%�g�l�l�o�o�"�  VV�  Wd�  Ve�  e`�  aq�  ry�  az�  `{�  {B�  TC�  PV�%�  W����
������	�Wh�8�<�<� B�R���V� K�L�Q�Q�S�np�D� ����)�,�2�2�4���H�H�V�Y�/�	��(�(�>�9�5���x�x��	�:���x�x��	�*��K]�[�_�_�U�E�4D�4D�4F�G�ch�cs�cs�cu���Y�Y�[�
��=��"�(�(�*�5�6���'�4�:�:�c�?�1�#5�6��9�9�;��!�J�.��F� GI�T� JV�Vg�Uh� iZ�Z^�Y_� `I�IK�B�Q���PQ�R[�Q\�\_�`r�_s� t\�\c�[d�dg�ht�gu� vM�MQ�F� SO�OT�Uc�ef�Og�Nh� iM�P�
� �T�!�Y�$�%6��A�I�D����W�\�\�_�_�j�V�fj��k��$���q�L�I��t�#�}��'<��4���!�G�B� *� +/�� 0.�.7�[� 9*�*,�� .#�#(�'��/��	6��!�!�'�,�,�/�/�b�O_�lr�  NR�!�  S� 	�
�
�3�� �B ���W�\�\�_�_�5l�mz�l{�  |x�  Vk�  yI�  JQ�  yR�  q|�  x}�  }D�  4E�  RX��  Y�)�����L�L�O�O�� X�  ek�  FJ� 	� 	
��{ ���)�)� ����g�l�l�o�o�"�  Nb�  cd�  be�  Lf��  	g��=�a�S�A�B���� ����W�\�\�_�_��  My��  	{��$�Q�C�(�)���� ����g�l�l�o�o�"�  Nq�  rs�  qt�  Lu��  	v��-�a�S�1�2�����<	��D��\ � 	6��0���4�5�5��	6�� � )��#�A�3�'�(�(��)�sm   �'AR �1V�.V#�*.W �V�6=S8�8V�:U�V�=V�V�V �#	W�,W � W�	W)�W$�$W)c                 �    � | j                   dk(  S )N�stopr�   r�   s    rA   r�   r�   �  s   � �d�i�i�6�.Ar[   c                 �|  � | j                   j                  j                  }t        t        | j                   �      st        | j                   �      sy t        j                  j                  t        j                  �       d�      }t        |d�      j                  �        t        j                  | j                  d�       y )NrD   r3   zStopping process...)r`   r^   r�   rj   r�   ra   rI   rK   rM   rJ   r7   r�  rN   r�   )r�   r;   r  s      rA   �stop_callbackr.  �  sx   � ��l�l���"�"�G��L�$�,�,�7��PT�P\�P\�@]�������R�Y�Y�[�+�6�I���C���� ����d�g�g�'<�=r[   c                  ��   � g } 	 t        dd�      5 }|D ]/  }|j                  �       }|s�| j                  t        |�      �       �1 	 d d d �       | S # 1 sw Y   | S xY w# t        $ r t        d�       g cY S w xY w)Nr�   r�  zUser ID file not found.)r7   rz  r�  r�   r�  r:   )�user_idsr�   �liner;   s       rA   r�  r�  �  sw   � ��H���.�#�&�!����*�*�,����O�O�C��L�1� � '� �O� '� �O�� � ��'�(��	��s3   �A �A�A�A �A�A �A �A6�5A6c                  ��   � 	 t        dd�      5 } t        j                  | �      cd d d �       S # 1 sw Y   y xY w# t        $ r i cY S t        j                  $ r t        d�       i cY S w xY w)Nzuser_data.jsonr�  zJSONDecodeError: user_data.json)r7   rO  �loadr�  �JSONDecodeErrorr:   )r�   s    rA   r  r  �  sZ   � ���"�C�(�A��9�9�Q�<� )�(�(��� ��	���� ��/�0��	��s)   �9 �-�	9 �6�9 �9 �A(�A(�'A(c                 �   � t        �       }|j                  �       D ]&  \  }}|j                  d�      | k(  s�t        |�      c S  y )N�referral_code)r  �itemsr  r�   )r6  r  r�  �	user_infos       rA   r�   r�   �  sA   � ��!�I�"+�/�/�"3���Y��=�=��)�]�:��{�#�#� #4� r[   �__main__u�   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━bot by @CrImSon_WoLf777 started sucessfully ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━)�non_stop)N)��
SECRET_KEY�inputrz  �
user_inputr:   �exitr   rI   r  r�   r   rO  �uuidr2  rN  r   r|  r~  r  r�   r�   r�   rX   r8   r�   �gates.stripe_gatesr   r   r	   �user_managementr
   r   r   r   r   r   r   r   r   r   r   r   r   r   r   r   r   r   r   r   r   �session_managerr   �utilsr    r!   r"   r#   r$   r%   r&   r'   r(   r)   r*   �configr+   r,   �TeleBotrN   �
subscriberr�   r�   rB   rT   rZ   ra   rj   r   �message_handlerr�   �callback_query_handlerr�   r�   r�   r�   r�   r�   r�   r�   r�   r�   r�   r  r  r  r%  r7  rR  r�  r�  r�  r�  r�  r�  r�  r�  r�  r�  r�  r�  r�  r�  r�  r�  r�  r�  r   r  r  r  r  r  r*  r.  r�  r  r�   �__name__�logop�polling� r[   rA   �<module>rM     s�  ���
��<�=�C�C�E�
����	�
#�$���G� �)� *� � 	� 	� � � � � � � �� �� �� �� �� �� ���)� ��� ?� ?� e�  e�  e�  e�  e�  e� /� r�  r�  r�  r� '��	�
F�G�	�
A�B���G��g�o�o�i�F�3����
�#��%��2��	�*��� ���O��P�@o� Q�@o�F ���!Q��R�#v� S�#v�L ���z�7�3��4�;l� 5�;l�z ���z�l��+�	w� ,�	w� ���w�i��(�w� )�w�< ���z�l��+�o� ,�o�( ���v�h��'�`� (�`� ���w�i��(�'X� )�'X�R ���y�k��*�%Z� +�%Z�N� ���v�h��'�e� (�e�  ���!O��P�p� Q�p� ���w�i��(�3� )�3�4 ���y�k��*�y� +�y� ���x�j��)�L� *�L�: ���v�h��'�"n� (�"n�H ���u�g��&�.Q� '�.Q�` ���u�g��&�(y� '�(y�V �!����#��� ���Z��[�@<� \�@<�D ���z�l��+�'z� ,�'z�R ���y�k��*�v� +�v�4 ���{�m��,�l� -�l�B ���}�o��.�t� /�t�< ���|�n��-�!u� .�!u�F ���|�n��-�#|� .�#|�J ���z�l��+�.z� ,�.z�` ���u�g��&�k� '�k�6 ���x�j��)�m� *�m�6 ���|�n��-�9� .�9�( ���u�g��&�r� '�r�8 ���w�i��(�t� )�t�8 ���z�l��+�M� ,�M� ���z�l��+�X� ,�X�@ ���x�j��)�"j� *�"j�H ���{�m��,�r� -�r�" ���|�n��-�!n� .�!n�F ���v�h��'�u� (�u�4 ���y�k��*�x� +�x�4 ���~�.��/�q� 0�q�4 ���{�m��,�:� -�:�6 ���{�m��,�(x� -�(x�T ���J�<��0�w)� 1�w)�r ���!A��B�>� C�>���� �z�� q�E�	�%�L��K�K��K�� r[   