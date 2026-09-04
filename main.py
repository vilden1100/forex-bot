import datetime
import requests

# اطلاعات ربات تلگرام خود را جایگزین کنید
BOT_TOKEN = "8963564577:AAE_2ajuS1UUmGlNjZWSp97eOsYnRnZO9YA"
CHAT_ID = "8298401582"


def send_news():
    # دریافت اخبار امروز از منبع پایدار
    url = "https://nfs.forexfactory.net/ff_calendar_thisweek.json"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }

    try:
        # دریافت داده از API تقویم
        response = requests.get(
            "https://api.statbureau.org/calendar", timeout=15
        )
    except Exception:
        pass

    # سورس جایگزین و مطمئن برای تقویم روزانه فارکس
    calendar_url = "https://raw.githubusercontent.com/man-c/forex_factory_scraper/main/data/calendar.json"

    try:
        res = requests.get(calendar_url, headers=headers, timeout=15)
        if res.status_code != 200:
            # در صورت عدم دسترسی به سورس اول، از سورس رزرو استفاده می‌شود
            calendar_url = "https://nfs.forexfactory.net/ff_calendar_thisweek.json"
            res = requests.get(calendar_url, headers=headers, timeout=15)

        data = res.json()
        today_str = datetime.datetime.utcnow().strftime("%Y-%m-%d")

        today_events = []
        for e in data:
            event_date = e.get("date", "") or e.get("Date", "")
            if event_date.startswith(today_str):
                today_events.append(e)

        if not today_events:
            text = "📊 امروز هیچ خبر اقتصادی مهمی در تقویم ثبت نشده است."
        else:
            text = "📅 اخبار و رویدادهای امروز فارکس فکتوری:**\n\n"
            for event in today_events:
                impact = event.get("impact", "") or event.get("Impact", "")
                title = event.get("title", "") or event.get("Title", "")
                country = (
                    event.get("country", "")
                    or event.get("Country", "")
                    or event.get("currency", "")
                )
                date_val = event.get("date", "") or event.get("Date", "")

                time_str = (
                    date_val.split("T")[-1][:5]
                    if "T" in date_val
                    else "All Day"
                )

                if impact == "High":
                    emoji = "🔴"
                elif impact == "Medium":
                    emoji = "🟠"
                elif impact == "Low":
                    emoji = "🟡"
                else:
                    emoji = "⚪️"

                text += f"{emoji} {country}** - {title}\n"
                text += f"⏰ زمان (UTC): `{time_str}`\n"
                text += "-------------------\n"

        # ارسال به تلگرام
        telegram_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        payload = {"chat_id": CHAT_ID, "text": text, "parse_mode": "Markdown"}
        response = requests.post(telegram_url, json=payload)
        print("Telegram Response Status:", response.status_code)

    except Exception as e:
        # ارسال پیام خطا به تلگرام برای آگاهی
        err_msg = f"⚠️ خطا در دریافت تقویم اقتصادی: {str(e)}"
        telegram_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        requests.post(telegram_url, json={"chat_id": CHAT_ID, "text": err_msg})


send_news()
