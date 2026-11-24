import uiautomator2 as u2
import time

def main():
    print("الاتصال بالهاتف الوهمي...")
    d = u2.connect("127.0.0.1:5555")
    print("تم الاتصال بنجاح!")
    time.sleep(2)
    print("إنهاء السكربت.")

if __name__ == "__main__":
    main()
