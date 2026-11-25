import uiautomator2 as u2
import time
import telebot
import os
import threading

# --- إعدادات بوت التيليجرام ---
TELEGRAM_TOKEN = "9032675094:AAGk8zSeWv9ewfztsAATj6_8utGZedynV44"
CHAT_ID = "7306346652" # <--- ضع معرف محادثتك هنا (رقم)

# --- متغيرات لحفظ البيانات ---
user_email = None
user_password = None
waiting_for_email = False
waiting_for_password = False
ready_to_start = False

bot = telebot.TeleBot(TELEGRAM_TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    global waiting_for_email
    bot.reply_to(message, "أهلاً بك سيدي! 🧛‍♂️\nأرسل إيميل جوجل الخاص بك:")
    waiting_for_email = True

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    global waiting_for_email, waiting_for_password, user_email, user_password, ready_to_start
    
    if waiting_for_email:
        user_email = message.text.strip()
        waiting_for_email = False
        waiting_for_password = True
        bot.reply_to(message, "تم استلام الإيميل. الآن أرسل كلمة المرور:")
        
    elif waiting_for_password:
        user_password = message.text.strip()
        waiting_for_password = False
        bot.reply_to(message, "✅ تم استلام البيانات. جاري تشغيل الهاتف الوهمي...")
        ready_to_start = True
        
    elif ready_to_start:
        bot.reply_to(message, "البوت يعمل بالفعل... يرجى الانتظار.")

def take_screenshot(d, filename="screen.png"):
    try:
        d.screenshot(filename)
        with open(filename, 'rb') as photo:
            bot.send_photo(CHAT_ID, photo, caption=f"📸 الحالة الحالية")
    except Exception as e:
        print(f"فشل إرسال الصورة: {e}")

def main():
    global ready_to_start
    print("في انتظار بيانات المستخدم...")
    # الانتظار حتى يرسل المستخدم البيانات
    while not ready_to_start:
        time.sleep(1)
        
    print(f"بدء العمل باستخدام الإيميل: {user_email}")
    try:
        d = u2.connect("127.0.0.1:5555")
        bot.send_message(CHAT_ID, "✅ تم الاتصال بالهاتف الوهمي بنجاح!")
        
        # فتح المتجر
        bot.send_message(CHAT_ID, "جاري فتح Google Play Store...")
        d.app_start("com.android.vending")
        time.sleep(5)
        take_screenshot(d, "play_store.png")
        
        # البحث عن Sign In
        if d(text="SIGN IN").exists:
            d(text="SIGN IN").click()
            time.sleep(5)
            take_screenshot(d, "sign_in_clicked.png")
            
            if d(text="Google").exists:
                d(text="Google").click()
                time.sleep(5)
                take_screenshot(d, "google_login.png")
                
                if d(text="Email or phone").exists:
                    d(text="Email or phone").set_text(user_email)
                    d(text="Next").click()
                    time.sleep(5)
                    take_screenshot(d, "email_entered.png")
                    
                    if d(text="Enter your password").exists:
                        d(text="Enter your password").set_text(user_password)
                        d(text="Next").click()
                        time.sleep(10)
                        take_screenshot(d, "password_entered.png")
                        
                        bot.send_message(CHAT_ID, "📲 يرجى تأكيد الإشعار من هاتفك (انتظر 60 ثانية)...")
                        time.sleep(60)
                        take_screenshot(d, "after_verification.png")
                        bot.send_message(CHAT_ID, "🎉 انتهى تسجيل الدخول.")
                    else:
                        bot.send_message(CHAT_ID, "⚠️ لم أجد خانة كلمة المرور.")
                else:
                    bot.send_message(CHAT_ID, "⚠️ لم أجد خانة الإيميل.")
            else:
                bot.send_message(CHAT_ID, "⚠️ لم أجد خيار Google.")
        else:
            bot.send_message(CHAT_ID, "⚠️ لم أجد زر SIGN IN.")

        bot.send_message(CHAT_ID, "انتهى السكربت.")
        
    except Exception as e:
        bot.send_message(CHAT_ID, f"❌ خطأ: {e}")

if __name__ == "__main__":
    # تشغيل البوت في خلفية منفصلة
    threading.Thread(target=bot.polling, kwargs={"none_stop": True}).start()
    main()
