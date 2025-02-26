# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#

# OldUserBot - Vüsal

""" UserBot başlanğıc nöqtəsi """
import importlib
from importlib import import_module
from sqlite3 import connect
import os
import requests
from telethon.tl.types import InputMessagesFilterDocument
from telethon.errors.rpcerrorlist import PhoneNumberInvalidError
from telethon.tl.functions.channels import GetMessagesRequest
from . import BRAIN_CHECKER, LOGS, bot, PLUGIN_CHANNEL_ID, CMD_HELP, LANGUAGE, OldUser_VERSION
from .modules import ALL_MODULES
import userbot.modules.sql_helper.mesaj_sql as MSJ_SQL
import userbot.modules.sql_helper.galeri_sql as GALERI_SQL
from pySmartDL import SmartDL
from telethon.tl import functions

from random import choice
import chromedriver_autoinstaller
from json import loads, JSONDecodeError

DIZCILIK_STR = [
    "Stikeri oğurlayıram...",
    "Yaşasın oğurluq...",
    "Bu stiker mənim paketimə dəvət olunur...",
    "Bunu oğurlamalıyam...",
    "Hey bu gözəl bir stiker!\nHemen oğurlayıram..",
    "Stikerini oğurlayıram\nhahaha.",
    "Hey buraya bax. (☉｡☉)!→\nMən bunu oğurlayarkən...",
    "Güllər qırmızı bənövşələr mavi, bu stikerimi paketimə oğurlayaraq havalı olacağam...",
    "Stiker həbs olunur...",
    "Bay oğru bu stikerini oğurlayır... ",
]

AFKSTR = [
    "Şu an təcili işim var, daha sonra mesaj atsan olmaz mı? Zaten yine geleceğim.",
    "Aradığınız kişi şu anda telefona cevap veremiyor. Sinyal sesinden sonra kendi tarifeniz üzerinden mesajınızı bırakabilirsiniz. Mesaj ücreti 49 kuruştur. \n`biiiiiiiiiiiiiiiiiiiiiiiiiiiiip`!",
    "Birkaç dakika içinde geleceğim. Fakat gelmezsem...\ndaha fazla bekle.",
    "Şu an burada değilim, muhtemelen başka bir yerdeyim.",
    "Güllər qırmızı\nBənövşələr mavi\nBana bir mesaj bırak\nVe sana döneceğim.",
    "Bazen hayattaki en iyi şeyler beklemeye değer…\nHemen dönerim.",
    "Hemen dönerim,\nama eğer geri dönmezsem,\ndaha sonra dönerim.",
    "Henüz anlamadıysan,\nburada deyilim.",
    "Merhaba, uzak mesajıma hoş geldiniz, bugün sizi nasıl görmezden gelebilirim?",
    "7 deniz ve 7 ülkeden uzaktayım,\n7 su ve 7 kıta,\n7 dağ ve 7 tepe,\n7 ovala ve 7 höyük,\n7 havuz ve 7 göl,\n7 bahar ve 7 çayır,\n7 şehir ve 7 mahalle,\n7 blok ve 7 ev...\n\nMesajların bile bana ulaşamayacağı bir yer!",
    "Şu anda klavyeden uzaktayım, ama ekranınızda yeterince yüksek sesle çığlık atarsanız, sizi duyabilirim.",
    "Şu yönde ilerliyorum\n---->",
    "Şu yönde ilerliyorum\n<----",
    "Lütfen mesaj bırakın ve beni zaten olduğumdan daha önemli hissettirin.",
    "Sahibim burada deyil, bu yüzden bana yazmayı bırak.",
    "Burada olsaydım,\nSana nerede olduğumu söylerdim.\n\nAma ben deyilim,\ngeri döndüğümde bana sor...",
    "Uzaklardayım!\nNe zaman dönerim bilmiyorum !\nUmarım birkaç dakika sonra!",
    "Sahibim şuan da müsait deyil. Adınızı, numarınızı ve adresinizi verirseniz ona iletibilirm ve böylelikle geri döndüğü zaman.",
    "Üzgünüm, sahibim burada deyil.\nO gelene kadar benimle konuşabilirsiniz.\nSahibim size sonra döner.",
    "Bahse girerim bir mesaj bekliyordun!",
    "Hayat çok kısa, yapacak çok şey var...\nOnlardan birini yapıyorum...",
    "Şu an burada deyilim....\nama öyleysem ...\n\nbu harika olmaz mıydı?",
]

UNAPPROVED_MSG = ("`Hey! Bu bir bot. Narahat olma.\n\n`"
                  "`Sahibim sənə PM atma icazəsi verməyib. `"
                  "`Zəhmət olmasa sahibimin aktiv olmasını gözləyin, o adətən PM-ləri təsdiqləyir.\n\n`"
                  "`Bildiyim qədərilə o, dəli insanlara PM icazəsi vermir.`")

DB = connect("learning-data-root.check")
CURSOR = DB.cursor()
CURSOR.execute("""SELECT * FROM BRAIN1""")
ALL_ROWS = CURSOR.fetchall()
INVALID_PH = '\nXƏTA: Daxil edilən telefon nömrəsi yanlışdır' \
             '\n  İpucu: Ölkə kodunu istifadə edərək nömrəni daxil et' \
             '\n       Telefon nömrənizi yenidən yoxlayın'

for i in ALL_ROWS:
    BRAIN_CHECKER.append(i[0])
connect("learning-data-root.check").close()

try:
    bot.start()

    idim = bot.get_me().id
    olduserbl = requests.get('https://gitlab.com/vusaloldd/olduserbot/-/raw/master/olduser.json').json()
    if idim in olduserbl:
        bot.disconnect()

    # ChromeDriver'ı Ayarlayalım #
    try:
        chromedriver_autoinstaller.install()
    except:
        pass
    
    # Galeri üçün dəyərlər
    GALERI = {}

    # PLUGIN MESAJLARI AYARLIYORUZ
    PLUGIN_MESAJLAR = {}
    ORJ_PLUGIN_MESAJLAR = {"alive": "`Salam Aleykum Allah Səni Qorusun. 🐺 OldUserBot çalışıyor.`", "afk": f"`{str(choice(AFKSTR))}`", "kickme": "`Güle Güle ben gidiyorum `🤠", "pm": UNAPPROVED_MSG, "dızcı": str(choice(DIZCILIK_STR)), "ban": "`Yasaklandı!`", "mute": "`Sessize alındı!`", "approve": "`Bana mesaj gönderebilirsin!`", "disapprove": "`Artık bana mesaj gönderemezsin!`", "block": "`Engellendin!`"}

    PLUGIN_MESAJLAR_TURLER = ["alive", "afk", "kickme", "pm", "dızcı", "ban", "mute", "approve", "disapprove", "block"]
    for mesaj in PLUGIN_MESAJLAR_TURLER:
        dmsj = MSJ_SQL.getir_mesaj(mesaj)
        if dmsj == False:
            PLUGIN_MESAJLAR[mesaj] = ORJ_PLUGIN_MESAJLAR[mesaj]
        else:
            if dmsj.startswith("MEDYA_"):
                medya = int(dmsj.split("MEDYA_")[1])
                medya = bot.get_messages(PLUGIN_CHANNEL_ID, ids=medya)
                print(medya)
                PLUGIN_MESAJLAR[mesaj] = medya
            else:
                PLUGIN_MESAJLAR[mesaj] = dmsj
    if PLUGIN_CHANNEL_ID != None:
        LOGS.info("Pluginlər Yüklənir")
        try:
            KanalId = bot.get_entity(PLUGIN_CHANNEL_ID)
            DOGRU = 1
        except:
            KanalId = "me"
            bot.send_message("me", f"`Plugin_Channel_Id'iniz yanlışdır. Pluginlər qalıcı olmayacaq.`")
            DOGRU = 0

        for plugin in bot.iter_messages(KanalId, filter=InputMessagesFilterDocument):
            if DOGRU == 0:
                break
            dosyaa = plugin.file.name
            dosyaismi = plugin.file.name.split(".")

            try:
                ext = plugin.file.name.split(".")[1]
            except:
                continue

            if not dosyaismi[1] == "py":
                continue
            if not os.path.exists("./userbot/modules/" + dosyaa):
                dosya = bot.download_media(plugin, "./userbot/modules/")
            else:
                LOGS.info("Bu Plugin Zaten Yüklü " + dosyaa)
                dosya = dosyaa
                continue 
            
            try:
                spec = importlib.util.spec_from_file_location("userbot.modules." + dosyaismi[0], dosya)
                mod = importlib.util.module_from_spec(spec)

                spec.loader.exec_module(mod)
            except Exception as e:
                LOGS.info(f"`Yükleme başarısız! Plugin hatalı.\n\nHata: {e}`")

                if os.path.exists("./userbot/modules/" + dosyaa):
                    os.remove("./userbot/modules/" + dosyaa)
                continue
            
            ndosya = dosyaismi[0]
            CMD_HELP[ndosya] = "Bu Plugin Dışarıdan Yüklenmiştir"
    else:
        bot.send_message("me", f"`Lütfen pluginlərin qalıcı olması üçün PLUGIN_CHANNEL_ID'i ayarlayın.`")
except PhoneNumberInvalidError:
    print(INVALID_PH)
    exit(1)

async def FotoDegistir (foto):
    FOTOURL = GALERI_SQL.TUM_GALERI[foto].foto
    r = requests.get(FOTOURL)

    with open(str(foto) + ".jpg", 'wb') as f:
        f.write(r.content)    
    file = await bot.upload_file(str(foto) + ".jpg")
    try:
        await bot(functions.photos.UploadProfilePhotoRequest(
            file
        ))
        return True
    except:
        return False

for module_name in ALL_MODULES:
    imported_module = import_module("userbot.modules." + module_name)

LOGS.info("Botunuz çalışıyor! Herhangi bir sohbete .alive yazarak Test edin."
          " Yardıma ihtiyacınız varsa, Destek grubumuza gelin https://t.me/OldUserBotSupports")
LOGS.info(f"Bot sürümünüz OldUserBot {OldUser_VERSION}")

"""
if len(argv) not in (1, 3, 4):
    bot.disconnect()
else:
"""
bot.run_until_disconnected()