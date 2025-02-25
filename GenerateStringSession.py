import asyncio
import os
import sys
import time
import random

from telethon import TelegramClient, events
from telethon.errors import SessionPasswordNeededError, PhoneCodeInvalidError, PasswordHashInvalidError, PhoneNumberInvalidError
from telethon.network import ConnectionTcpAbridged
from telethon.utils import get_display_name
from telethon.sessions import StringSession

try:
   import requests
   import bs4
except:
   print("[!] Requests Tapılmadı. Yüklənir...")
   print("[!] Bs4 Tapılmadı. Yüklənir...")

   if os.name == 'nt':
      os.system("python3.8 -m pip install requests")
      os.system("python3.8 -m pip install bs4")
   else:
      os.system("pip3 install requests")
      os.system("pip3 install bs4")


# Original Source https://github.com/LonamiWebs/Telethon/master/telethon_examples/interactive_telegram_client.py #
loop = asyncio.get_event_loop()

class InteractiveTelegramClient(TelegramClient):
    def __init__(self, session_user_id, api_id, api_hash,
                 telefon=None, proxy=None):
        super().__init__(
            session_user_id, api_id, api_hash,
            connection=ConnectionTcpAbridged,
            proxy=proxy
        )
        self.found_media = {}
        print('@OldUserBot String Alıcıya Xoş Gəlmisiniz')
        print('[i] Telegramın Serverlərinə Qoşulur...')
        try:
            loop.run_until_complete(self.connect())
        except IOError:
            print('[!] Qoşularkən bir xəta baş verdi. Yenidən cəhd edilir...')
            loop.run_until_complete(self.connect())

        if not loop.run_until_complete(self.is_user_authorized()):
            if telefon == None:
               user_phone = input('[?] Telefon Nömrəniz (Nümunə: +994xxxxxxxxx): ')
            else:
               user_phone = telefon
            try:
                loop.run_until_complete(self.sign_in(user_phone))
                self_user = None
            except PhoneNumberInvalidError:
                print("[!] Yanlış Nömrə Daxil Etdiniz. Nümunədəki Kimi Daxil Edin. Nümunə: +994xxxxxxxxx")
                exit(1)
            except ValueError:
               print("[!] Yanlış Nömrə Daxil Etdiniz. Nümunədəki Kimi Daxil Edin. Nümunə: +994xxxxxxxxx")
               exit(1)

            while self_user is None:
                code = input('[?] Telegramdan Gələn Beş (5) Rəqəmli Kodu Daxil Edin: ')
                try:
                    self_user =\
                        loop.run_until_complete(self.sign_in(code=code))
                except PhoneCodeInvalidError:
                    print("[!] Kodu Yanlış Yazdınız. Zəhmət Olmasa Yenidən Cəhd Edin. [Çox Cəhd Etmək Banlanmanıza Səbəb Ola Bilər]")
                except SessionPasswordNeededError:
                    pw = input('[i] İki mərhələli doğrulama aşkar edildi. '
                                 '[?] Şifrənizi Yazın: ')
                    try:
                        self_user =\
                            loop.run_until_complete(self.sign_in(password=pw))
                    except PasswordHashInvalidError:
                        print("[!] 2 Mərhələli Şifrənizi Yanlış Yazdınız. Zəhmət Olmasa Yenidən Cəhd Edin. [Çox Cəhd Etmək Banlanmanıza Səbəb Ola Bilər]")


if __name__ == '__main__':
   print("[i] OldUserBot String V3\n@OldUserBot\n\n")
   print("[1] Avtomatik API ID/HASH Alıcı")
   print("[2] String Alıcı\n")
   
   try:
      secim = int(input("[?] Seçim Edin: "))
   except:
      print("[!] Zəhmət Olmasa Yalnız Rəqəm Daxil Edin!")

   if secim == 2:
      API_ID = input('[?] API ID\'iniz [Hazır Açarları İstifadə Etmək Üçün Boş Buraxın]: ')
      if API_ID == "":
         print("[i] Hazır Açarlar İstifadə Edilir...")
         API_ID = 4
         API_HASH = "014b35b6184100b085b0d0572f9b5103"
      else:
         API_HASH = input('[?] API HASH\'iniz: ')

      client = InteractiveTelegramClient(StringSession(), API_ID, API_HASH)
      print("[i] String Açarınız Aşağıdadır!\n\n\n" + client.session.save())
   elif secim == 1:
      numara = input("[?] Telefon Nömrəniz: ")
      try:
         rastgele = requests.post("https://my.telegram.org/auth/send_password", data={"phone": numara}).json()["random_hash"]
      except:
         print("[!] Kod Göndərilə Bilmədi. Telefon Nömrənizi Yoxlayın.")
         exit(1)
      
      sifre = input("[?] Telegramdan Gələn Kodu Yazın: ")
      try:
         cookie = requests.post("https://my.telegram.org/auth/login", data={"phone": numara, "random_hash": rastgele, "password": sifre}).cookies.get_dict()
      except:
         print("[!] Yəqin Kodu Yanlış Yazdınız. Zəhmət Olmasa Skripti Yenidən Başladın.")
         exit(1)
      app = requests.post("https://my.telegram.org/apps", cookies=cookie).text
      soup = bs4.BeautifulSoup(app, features="html.parser")

      if soup.title.string == "Create new application":
         print("[i] Tətbiqiniz Yoxdur. Yaradılır...")
         hashh = soup.find("input", {"name": "hash"}).get("value")
         AppInfo = {
            "hash": hashh,
            "app_title":"OldUserBot",
            "app_shortname": "OldUser" + str(random.randint(9, 99)) + str(time.time()).replace(".", ""),
            "app_url": "",
            "app_platform": "android",
            "app_desc": ""
         }
         app = requests.post("https://my.telegram.org/apps/create", data=AppInfo, cookies=cookie).text
         print(app)
         print("[i] Tətbiq uğurla yaradıldı!")
         print("[i] API ID/HASH alınır...")
         newapp = requests.get("https://my.telegram.org/apps", cookies=cookie).text
         newsoup = bs4.BeautifulSoup(newapp, features="html.parser")

         g_inputs = newsoup.find_all("span", {"class": "form-control input-xlarge uneditable-input"})
         app_id = g_inputs[0].string
         api_hash = g_inputs[1].string
         print("[i] Məlumatlar Gətirildi! Zəhmət Olmasa Bunları Qeyd Edin.\n\n")
         print(f"[i] API ID: {app_id}")
         print(f"[i] API HASH: {api_hash}")
         try:
            stringonay = int(input("[?] String Almaq İstəyirsiniz? [Bəli üçün 1 Yazın]: "))
         except:
            print("[!] Zəhmət Olmasa Yalnız Rəqəm Yazın!")

         if stringonay == 1:
            client = InteractiveTelegramClient(StringSession(), app_id, api_hash, numara)
            print("[i] String Açarınız Aşağıdadır!\n\n\n" + client.session.save())
         else:
            print("[i] Skript Dayandırılır...")
            exit(1)
      elif  soup.title.string == "App configuration":
         print("[i] Artıq Tətbiq Yaratmısınız. API ID/HASH Çəkilir...")
         g_inputs = soup.find_all("span", {"class": "form-control input-xlarge uneditable-input"})
         app_id = g_inputs[0].string
         api_hash = g_inputs[1].string
         print("[i] Məlumatlar Gətirildi! Zəhmət Olmasa Bunları Qeyd Edin.\n\n")
         print(f"[i] API ID: {app_id}")
         print(f"[i] API HASH: {api_hash}")
         try:
            stringonay = int(input("[?] String Almaq İstəyirsiniz? [Bəli üçün 1 Yazın]: "))
         except:
            print("[!] Zəhmət Olmasa Yalnız Rəqəm Yazın!")

         if stringonay == 1:
            client = InteractiveTelegramClient(StringSession(), app_id, api_hash, numara)
            print("[i] String Açarınız Aşağıdadır!\n\n\n" + client.session.save())
         else:
            print("[i] Skript Dayandırılır...")
            exit(1)
      else:
         print("[!] Bir Xəta Baş Verdi.")
         exit(1)
   else:
      print("[!] Naməlum seçim.")