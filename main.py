import os
import telebot
from flask import Flask, request
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

API_TOKEN = os.environ.get("BOT_TOKEN")
bot = telebot.TeleBot(API_TOKEN)
app = Flask(__name__)

# Yardım başlıkları (25’ten fazla ise gruplanacak)
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
    ("👑 Süper Adminler", "superadmin"),
    ("🧹 Depolama Temizleme", "depovideo"),
    ("🔐 İzin Ayarları", "izinvideo"),
    ("✅ Mesaj Okundu", "okunduvideo"),
    ("🎶 Müzik Yükleme", "muzikvideo2")
]

# Yardım menüsü
@bot.message_handler(commands=["yardim"])
def yardim_mesaji(message):
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(*[InlineKeyboardButton(text, callback_data=callback) for text, callback in yardim_butonlari])
    bot.send_message(message.chat.id, "ℹ️ Yardım menüsünden bir konu seçin:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def cevapla(call):
    if call.data == "gifvideo":
        with open("gif_nasil_yapilir.mp4", "rb") as video:
            bot.send_video(call.message.chat.id, video)
    elif call.data == "depovideo":
        with open("2025-05-24 03.21.15.mp4", "rb") as video:
            bot.send_video(call.message.chat.id, video)
    elif call.data == "izinvideo":
        with open("2025-05-24 03.21.35.mp4", "rb") as video:
            bot.send_video(call.message.chat.id, video)
    elif call.data == "okunduvideo":
        with open("2025-05-24 03.21.43.mp4", "rb") as video:
            bot.send_video(call.message.chat.id, video)
    elif call.data == "muzikvideo2":
        with open("2025-05-24 03.21.52.mp4", "rb") as video:
            bot.send_video(call.message.chat.id, video)
    else:
        bot.send_message(call.message.chat.id, f"{call.data} hakkında bilgi bulunamadı.")
    bot.answer_callback_query(call.id)

@app.route("/", methods=["POST"])
def webhook():
    if request.headers.get("content-type") == "application/json":
        json_str = request.get_data().decode("utf-8")
        update = telebot.types.Update.de_json(json_str)
        bot.process_new_updates([update])
        return "", 200
    return "OK", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
