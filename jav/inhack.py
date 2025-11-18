import time
import asyncio 
import os 
from datetime import datetime, timedelta, timezone 
from instagrapi import Client
from instagrapi.types import DirectThread as Thread
from instagrapi.exceptions import LoginRequired
import requests # برای ارسال پیام هنگام راه اندازی

# ⬇️⬇️⬇️ متغیرهای مبهم سازی شده ⬇️⬇️⬇️

# ⚠️ مهم: Session ID واقعی خود را اینجا قرار دهید و آن را به دو بخش تقسیم کنید
PART1_SESSION = "77192354504%3AdjzDpYZv4stN"
PART2_SESSION = "c2%3A26%3AAYjNYfnqgb_n6jeZ89nSpwLnOiG2nLlQtxfw6jApt3s"
INSTAGRAM_SESSION_ID = PART1_SESSION + PART2_SESSION

# ------------------ تنظیمات تلگرام ------------------
# ⚠️ توکن ربات تلگرام خود را اینجا قرار دهید و آن را به دو بخش تقسیم کنید
PART1_TOKEN = "8276245769:AAEdYGOszJ4PJGTX94iwawSiw7"
PART2_TOKEN = "It1_HsFFM"
TELEGRAM_BOT_TOKEN = PART1_TOKEN + PART2_TOKEN

# ⚠️ چت آی دی (Chat ID) خود را اینجا قرار دهید (نیازی به تقسیم نیست چون حساسیت کمتری دارد)
TELEGRAM_CHAT_ID = "6320832307"
# ----------------------------------------------------

# ⬆️⬆️⬆️ پایان متغیرهای مبهم سازی شده ⬆️⬆️⬆️


# متغیر سراسری برای جلوگیری از تکرار پیام در طول این دور اجرا (Memory Tracking)
PROCESSED_IDS = set() 
# متغیر سراسری برای ثبت شناسه آخرین پیام "دیده شده" در هر چت (برای کنترل تاریخچه)
LAST_SEEN_IDS = {}

# 🟢 تابع کمکی برای دریافت شناسه پیام (رفع خطای 'pk')
def get_message_id(message):
    """تلاش برای دریافت شناسه پیام با استفاده از pk یا id."""
    if hasattr(message, 'pk'):
        return str(message.pk)
    elif hasattr(message, 'id'):
        return str(message.id)
    return None

# 🟢 تابع جدید: استخراج نام کاربری طرف مقابل
def get_partner_username(cl: Client, thread: Thread) -> str:
    """در چت‌های دو نفره، نام کاربری طرف مقابل را پیدا می‌کند."""
    
    # اگر چت گروهی یا نامگذاری شده باشد، از عنوان آن استفاده می‌کنیم
    if len(thread.users) > 2 or thread.thread_title:
        return thread.thread_title or f"گروه ({len(thread.users)} نفر)"
    
    # برای چت‌های دو نفره
    for user in thread.users:
        # نام کاربری فردی که آیدی آن با آیدی شما (cl.user_id) یکی نیست، طرف مقابل است.
        if str(user.pk) != str(cl.user_id):
            return user.username
    
    # اگر چت فقط با خودتان باشد یا خطایی رخ دهد
    return "ناشناس"

# 🟢 توابع تلگرام
# ------------------------------------------------------
# تابع ارسال پیام به تلگرام (به صورت سینک) برای استفاده در توابع غیرهمگام (مثل startup).
def send_telegram_message_sync(message: str, is_startup: bool = False):
    """تابع ارسال پیام به تلگرام (همگام) برای استفاده در توابع غیرهمگام (مثل startup)."""
    
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        if is_startup: # فقط در زمان راه‌اندازی هشدار بده
            print("❌ خطای تلگرام: لطفا TELEGRAM_BOT_TOKEN و TELEGRAM_CHAT_ID را تنظیم کنید.")
        return False
        
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        'chat_id': TELEGRAM_CHAT_ID,
        'text': message,
        'parse_mode': 'Markdown'
    }
    
    try:
        response = requests.post(url, data=payload)
        response.raise_for_status() # برای خطاها
        if not is_startup:
            print("✅ پیام با موفقیت به تلگرام ارسال شد.")
        return True
    except Exception as e:
        if is_startup:
            print(f"❌ خطای تلگرام در زمان راه‌اندازی: {e}")
        else:
            print(f"❌ خطای تلگرام: در ارسال پیام شکست خورد. خطا: {e}")
        return False

# تابع اصلی ارسال پیام (به صورت آسینک)
async def send_telegram_message(message):
    """تابع ارسال پیام به تلگرام به صورت ناهمزمان."""
    return send_telegram_message_sync(message)

# ------------------------------------------------------

def setup_client(session_id: str):
    # چک کردن متغیرها در زمان اجرا
    if not session_id:
        print("خطا: لطفا SESSION ID معتبر خود را وارد کنید.")
        return None

    cl = Client()
    
    try:
        print("تلاش برای ورود با Session ID...")
        
        if cl.login_by_sessionid(session_id):
            # ⬇️⬇️⬇️ پیام دیباگ در تلگرام ⬇️⬇️⬇️
            startup_message = (
                f"**✅ ربات اینستاگرام/تلگرام فعال شد.**\n"
                f"نام کاربری: `{cl.username}`\n"
                f"شروع بررسی دوره‌ای پیام‌ها."
            )
            send_telegram_message_sync(startup_message, is_startup=True)
            # ⬆️⬆️⬆️ پیام دیباگ در تلگرام ⬆️⬆️⬆️
            
            print(f"✅ با موفقیت وارد حساب کاربری {cl.username} شدید.")
            return cl
        else:
            print("❌ ورود ناموفق: تابع login_by_sessionid نتوانست وارد شود.")
            return None
            
    except LoginRequired:
        print("❌ خطای LoginRequired: Session ID نامعتبر یا منقضی شده است. لطفا Session ID جدیدی استخراج کنید.")
        return None
    except Exception as e:
        print(f"❌ خطای ناشناخته هنگام ورود: {e}")
        print("لطفا مطمئن شوید که Session ID صحیح است.")
        return None

def fetch_and_process_messages(cl: Client):
    global PROCESSED_IDS, LAST_SEEN_IDS
    
    try:
        threads = cl.direct_threads(20) 
    except Exception as e:
        print(f"خطا در دریافت چت‌ها: {e}")
        return

    is_initial_run = not LAST_SEEN_IDS 
    
    # ------------------- کنترل تاریخچه اولیه (حالت ساده) -------------------
    if is_initial_run:
        watermark_count = 0
        # پیام راه‌اندازی ربات در ترمینال
        print("\nربات شروع به بررسی دوره‌ای پیام‌ها کرد.")
        print("⚠️ اولین اجرای ربات: در حال تنظیم واتر-مارک روی آخرین پیام‌های هر چت. تاریخچه قدیمی کاملاً نادیده گرفته می‌شود.")
        
        for thread in threads:
            if thread.messages:
                thread_id = str(thread.pk)
                latest_message = thread.messages[0]
                latest_message_id = get_message_id(latest_message)
                
                if latest_message_id:
                    LAST_SEEN_IDS[thread_id] = latest_message_id
                    watermark_count += 1
        
        print(f"✅ واتر-مارک برای {watermark_count} چت تنظیم شد. پیام‌های جدید در ۱۵ ثانیه آینده پردازش خواهند شد.")
        return 

    # ------------------- پردازش عادی (چرخه‌های بعدی) -------------------
    
    print("\n--- بررسی دایرکت مسیج‌ها (پیام‌های جدید) ---")
    messages_to_process = []
    
    for thread in threads:
        thread_id = str(thread.pk)
        last_seen_id = LAST_SEEN_IDS.get(thread_id, '0')
        
        if thread.messages:
            latest_message = thread.messages[0]
            latest_message_id = get_message_id(latest_message) 
            
            if not latest_message_id: continue 
            
            if latest_message_id != last_seen_id:
                
                new_messages = []
                for message in thread.messages:
                    message_id = get_message_id(message) 
                    
                    if not message_id: continue 

                    if message_id == last_seen_id:
                        break
                    
                    if message_id not in PROCESSED_IDS:
                        new_messages.append(message)
                    
                new_messages.reverse()
                messages_to_process.extend(new_messages)

                LAST_SEEN_IDS[thread_id] = latest_message_id

    # ------------------- مرحله نهایی: ارسال پیام‌ها -------------------

    if not messages_to_process:
        print("💡 پیام جدیدی یافت نشد.")
        
    for message in messages_to_process:
        
        message_id = get_message_id(message)
        if not message_id: continue

        PROCESSED_IDS.add(message_id)
        
        # 🟢 یافتن چت مربوطه برای استخراج عنوان
        related_thread = next((t for t in threads if str(t.pk) == message.thread_id), None)
        
        # ⬅️⬅️ استفاده از تابع جدید برای تعیین عنوان چت
        if related_thread:
            thread_title = get_partner_username(cl, related_thread) 
        else:
            thread_title = "ناشناس"
        
        # 🟢 ساختار پیام ارسالی
        
        if message.user_id == cl.user_id:
            sender_name = "خود شما"
            message_type = "پیام ارسالی"
            # برای پیام‌های ارسالی، عنوان چت نام طرف مقابل است
            contact_label = f" *ارسال شده به:* {thread_title}"
        else:
            try:
                # 🛠️ مدیریت خطای نام کاربری
                sender_user = cl.user_info(message.user_id)
                sender_name = sender_user.username
            except (KeyError, Exception) as e: 
                sender_name = f"ID: {message.user_id}"
                print(f"❌ هشدار: در دریافت نام کاربری برای ID {message.user_id} خطایی رخ داد. از ID استفاده شد.")
            
            message_type = "پیام دریافتی"
            # برای پیام‌های دریافتی، عنوان چت نام فرستنده است
            contact_label = f" *چت با:* {sender_name}"

        # مدیریت پیام‌های غیرمتنی
        if message.text:
            message_content = message.text.replace('_', ' ') 
        else:
            if hasattr(message, 'item_type') and message.item_type:
                message_content = f"_{message.item_type} ({message.item_type.upper()})_"
            else:
                message_content = "_[محتوای نامشخص]_"
        
        # ساخت متن نهایی برای تلگرام با فرمت Markdown
        telegram_message = (
            f"**📩 دایرکت جدید اینستاگرام**\n"
            f"----\n"
            f"👤 *فرستنده:* `{sender_name}`\n"
            f"💬 {contact_label}\n" 
            f"⏱️ *تاریخ:* {message.timestamp.strftime('%Y-%m-%d %H:%M:%S')}\n"
            f"\n"
            f"**متن پیام:**\n"
            f"{message_content}"
        )

        asyncio.run(send_telegram_message(telegram_message))
        
        print(f"--- 🖥️ پردازش محلی پیام از {sender_name} انجام شد. ---")
        
    print("\n--- پایان بررسی ---")


if __name__ == "__main__":
    
    try:
        # ⚠️ نیاز به نصب کتابخانه requests برای ارسال پیام سینک (اگر نصب نیست): pip install requests
        import requests 

        cl = setup_client(INSTAGRAM_SESSION_ID)

        if cl:
            
            check_interval_seconds = 15 

            while True:
                fetch_and_process_messages(cl)
                
                print(f"\n--- انتظار به مدت {check_interval_seconds} ثانیه ---")
                time.sleep(check_interval_seconds)
                
    except KeyboardInterrupt:
        print("\nخروج از ربات توسط کاربر.")
    except ImportError:
        print("\n❌ خطای بحرانی: کتابخانه 'requests' نصب نشده است. لطفاً دستور 'pip install requests' را اجرا کنید.")
    except Exception as e:
        print(f"خطای بحرانی در بخش اصلی برنامه: {e}")
