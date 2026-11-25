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
        
        # فتح إعدادات الحساب
        bot.send_message(CHAT_ID, "جاري فتح إعدادات الحساب...")
        d.app_start("com.android.settings")
        time.sleep(3)
        
        # الضغط على "الحسابات" (Accounts) أو ما يشابهها
        # (ملاحظة: الإحداثيات قد تختلف حسب نسخة الأندرويد، سنستخدم نصوص)
        if d(text="Passwords & accounts").exists:
            d(text="Passwords & accounts").click()
        elif d(text="Accounts").exists:
            d(text="Accounts").click()
        time.sleep(3)
        take_screenshot(d, "accounts.png")
        
        # الضغط على "Add account"
        if d(text="Add account").exists:
            d(text="Add account").click()
        time.sleep(2)
        take_screenshot(d, "add_account.png")
        
        # الضغط على Google
        if d(text="Google").exists:
            d(text="Google").click()
        time.sleep(5)
        take_screenshot(d, "google_login.png")
        
        # هنا ستظهر شاشة تسجيل الدخول (قد تكون في المتصفح أو تطبيق GMS)
        # بما أننا لا نستطيع التفاعل بدقة مع كل شاشة، سنكتفي بالتقاط الصور
        # لترى بنفسك ماذا يحدث، ثم نعدل السكربت بناءً عليها.
        
        bot.send_message(CHAT_ID, "📸 راجع الصور. هل تحتاج للتفاعل مع شاشة التحقق بخطوتين؟")
        bot.send_message(CHAT_ID, "أرسل أي رسالة لبدء الانتظار (60 ثانية)...")
        
        waiting_for_user = True
        time.sleep(60) # انتظار رد المستخدم
        
        take_screenshot(d, "after_wait.png")
        bot.send_message(CHAT_ID, "انتهى السكربت.")
        
    except Exception as e:
        bot.send_message(CHAT_ID, f"❌ خطأ: {e}")

if __name__ == "__main__":
    # تشغيل البوت في خلفية منفصلة
    threading.Thread(target=bot.polling, kwargs={"none_stop": True}).start()
    main()
