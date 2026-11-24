import uiautomator2 as u2
import time

def main():
    print("الاتصال بالهاتف الوهمي...")
    d = u2.connect("127.0.0.1:5555")
    
    # فتح متجر بلاي
    print("فتح متجر Play...")
    d.app_start("com.android.vending")
    time.sleep(10)
    
    # خطوات تصفح (تقريبية، قد تحتاج لتعديل لاحقاً)
    print("محاولة الانتقال إلى Play Points...")
    d.click(1000, 150) # النقر على أيقونة الحساب
    time.sleep(3)
    if d(text="Play Points").exists:
        d(text="Play Points").click()
        time.sleep(5)
    
    print("Done")

if __name__ == "__main__":
    main()
