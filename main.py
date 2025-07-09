import os
import telebot
from flask import Flask, request
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from cevaplar import cevaplar  # cevaplar ayrı dosyada

API_TOKEN = os.environ.get("BOT_TOKEN")
bot = telebot.TeleBot(API_TOKEN, threaded=False)
app = Flask(__name__)

# Yardım başlıkları
yardim_butonlari = [
    ("📊 CP Seviyeleri", "cp"),
    ("🏰 Klan Oluşturma", "klan"),
    ("🎵 Müzik İndirme", "muzik"),
    ("📦 Şanslı Paket", "sansli"),
    ("👤 Cinsiyet Değişikliği", "cinsiyet"),
    ("📱 Doğrulama Kodu", "dogrulama"),
    ("📧 E-Posta Doğrulama", "eposta"),
    ("🖼️ Afiş Boyutu", "afis"),
    ("👥 Profil Boyutu", "profil"),
    ("🗑️ Hesap Silme", "hesap"),
    ("🎬 GIF Nasıl Yapılır?", "gifvideo"),
    ("📌 Çok Önemli", "cokonemli"),
    ("📋 Yardım Kuralları", "yardimkurallari"),
    ("⏱️ Atılma Süreleri", "atilmasure"),
    ("🌍 Panel Ülkeler", "ulkeler"),
    ("🍇 Meyve Sorunu", "meyveneden"),
    ("🍇 Meyve Ödülleri", "meyveodul"),
    ("🎓 Hesap Bağlama", "hesapbagla"),
    ("📢 Klan Şikayetleri", "klansikayet"),
    ("⭐ Aristokrasi", "aristokrasi"),
    ("📸 Özelden İfşa", "ifsa"),
    ("🌐 Yurtdışı Uygulama", "yurtdisi"),
    ("🎧 Android Müzik", "androidmuzik"),
    ("👑 Süper Adminler", "superadmin")
]

# Hazır bildirim butonları
hazir_butonlari = [
    ("🕓 Afk", "afk"),
    ("📱 Uygulama Reklamı", "reklam"),
    ("📞 Görüntülü Sohbet", "goruntulu"),
    ("📸 İfşa Bildirimi", "ifsa_bildirim"),
    ("👥 Klon Kullanıcı", "klon"),
    ("🗣️ Argo ve Küfür", "kufur"),
    ("🛡️ Klan Başvurusu", "klanbasvuru"),
    ("📷 Uygunsuz Arka Plan", "arka"),
    ("🚫 Şiddet Profil", "siddet"),
    ("🗳️ Siyasi Profil", "siyasi"),
    ("👑 Kötüye Aristokrasi", "kotu_aristo"),
    ("💢 Panel Argo", "panelargo"),
    ("📍 Panel Türkiye", "paneltr"),
    ("🔇 Yayın Sabotaj", "sabotaj"),
    ("📄 Uygunsuz Biyografi", "biyografi"),
    ("🖼️ Uygunsuz Profil Resmi", "profilresmi"),
    ("🆔 Uygunsuz Nick", "nick"),
    ("🙋 Yusuf Bey Bilgi", "yusuf"),
    ("🗯️ Panel Argo Kullanımı", "panelargo2"),
    ("💢 Oda Kaosu", "kaos"),
    ("🚫 Pornografik Görsel", "porno"),
    ("🚫 Aristo Satışı", "aristosatis"),
    ("🔞 Oyun Argo", "oyunargo"),
    ("🌑 Karartılmış Profil", "karartma"),
    ("👤 Kişisel Bilgi İfşası", "kisiselifsa"),
    ("📱 Oyun Reklamı", "oyunreklam"),
    ("🎵 Siyasi Şarkı", "sarkiprop")
]

def grup_gonder(chat_id, liste, komut_baslik, prefix):
    toplam = len(liste)
    gruplar = [liste[i:i+20] for i in range(0, toplam, 20)]
    for index, grup in enumerate(gruplar):
        markup = InlineKeyboardMarkup(row_width=2)
        markup.add(*[InlineKeyboardButton(text, callback_data=callback) for text, callback in grup])
        baslik = f"{komut_baslik} {index + 1}/{len(gruplar)}:"
        bot.send_message(chat_id, baslik, reply_markup=markup)

@bot.message_handler(commands=["yardim"])
def yardim_mesaji(message):
    grup_gonder(message.chat.id, yardim_butonlari, "📘 Yardım", "yardim")

@bot.message_handler(commands=["hazir", "hazır", "hazirbildirimler", "hazırbildirimler"])
def hazir_mesaji(message):
    grup_gonder(message.chat.id, hazir_butonlari, "📝 Hazır Bildirim", "hazir")

@bot.callback_query_handler(func=lambda call: True)
def cevapla(call):
    if call.data == "gifvideo":
        with open("gif_nasil_yapilir.mp4", "rb") as video:
            bot.send_video(call.message.chat.id, video)
    else:
        bot.send_message(call.message.chat.id, cevaplar.get(call.data, "Bu konuda bilgi bulunamadı."))
    bot.answer_callback_query(call.id)

@app.route(f"/{API_TOKEN}", methods=["POST"])
def webhook():
    if request.headers.get("content-type") == "application/json":
        json_str = request.get_data().decode("utf-8")
        update = telebot.types.Update.de_json(json_str)
        bot.process_new_updates([update])
        return "", 200
    return "OK", 200

@app.route("/", methods=["GET"])
def set_webhook():
    bot.remove_webhook()
    bot.set_webhook(url=f"https://elif7002.onrender.com/{API_TOKEN}")
    return "Webhook set successfully", 200

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
