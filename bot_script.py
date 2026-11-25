import uiautomator2 as u2
import time
import telebot
import os
import threading

# --- إعدادات بوت التيليجرام ---
TELEGRAM_TOKEN = "9032675094:AAGk8zSeWv9ewfztsAATj6_8utGZedynV44"
CHAT_ID = "7306346652" # <--- ضع معرف محادثتك هنا (رقم)

# --- إعدادات الحساب ---
EMAIL = "nvhjgvjj49@gmail.com" # <--- ضع إيميلك هنا
PASSWORD = "fawazfawaz1234@" # <--- ضع كلمة المرور العادية هنا

bot = telebot.TeleBot(TELEGRAM_TOKEN)
waiting_for_user = False

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    global waiting_for_user
    if waiting_for_user:
        bot.reply_to(message, "✅ تم استلام ردك. سأكمل العملية الآن...")
        waiting_for_user = False

def take_screenshot(d, filename="screen.png"):
    try:
        d.screenshot(filename)
        with open(filename, 'rb') as photo:
            bot.send_photo(CHAT_ID, photo, caption=f"📸 الحالة الحالية")
    except Exception as e:
        print(f"فشل إرسال الصورة: {e}")

def main():
    global waiting_for_user
    print("الاتصال بالهاتف الوهمي...")
    try:
        d = u2.connect("127.0.0.1:5555")
        print("تم الاتصال!")
        bot.send_message(CHAT_ID, "✅ تم الاتصال بالهاتف الوهمي بنجاح!")
        
        # 1. فتح تطبيق متجر بلاي
        bot.send_message(CHAT_ID, "جاري فتح تطبيق Google Play Store...")
        d.app_start("com.android.vending")
        time.sleep(5)
        take_screenshot(d, "play_store.png")
        
        # 2. الضغط على أيقونة الحساب (أعلى اليمين)
        # الإحداثيات تقريبية، قد تحتاج تعديلاً حسب دقة الشاشة
        bot.send_message(CHAT_ID, "جاري الضغط على أيقونة الحساب...")
        d.click(1000, 150) 
        time.sleep(3)
        take_screenshot(d, "account_menu.png")
        
        # 3. الضغط على "Add account" (أو "إضافة حساب")
        if d(text="Add account").exists:
            d(text="Add account").click()
            bot.send_message(CHAT_ID, "✅ تم اختيار إضافة حساب.")
            time.sleep(3)
            take_screenshot(d, "add_account.png")
            
            # 4. الضغط على Google
            if d(text="Google").exists:
                d(text="Google").click()
                time.sleep(5)
                take_screenshot(d, "google_login.png")
                
                # 5. إدخال الإيميل
                if d(text="Email or phone").exists:
                    d(text="Email or phone").set_text(EMAIL)
                    d(text="Next").click()
                    time.sleep(5)
                    take_screenshot(d, "email_entered.png")
                    
                    # 6. إدخال كلمة المرور
                    if d(text="Enter your password").exists:
                        d(text="Enter your password").set_text(PASSWORD)
                        d(text="Next").click()
                        time.sleep(10)
                        take_screenshot(d, "password_entered.png")
                        
                        # 7. الانتظار (لتأكيد الإشعار)
                        bot.send_message(CHAT_ID, "📲 إذا ظهرت شاشة تحقق، يرجى تأكيدها من هاتفك. (انتظر 60 ثانية)...")
                        waiting_for_user = True
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
            bot.send_message(CHAT_ID, "⚠️ لم أجد خيار إضافة حساب.")

        bot.send_message(CHAT_ID, "انتهى السكربت.")
        
    except Exception as e:
        bot.send_message(CHAT_ID, f"❌ خطأ: {e}")

if __name__ == "__main__":
    threading.Thread(target=bot.polling, kwargs={"none_stop": True}).start()
    main()
