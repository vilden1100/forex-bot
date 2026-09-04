import datetime
import requests

# اطلاعات ربات تلگرام
BOT_TOKEN = "8963564577:AAE_2ajuS1UUmGlNjZWSp97eOsYnRnZO9YA"
CHAT_ID = "8298401582"


def send_news():
    # دریافت اخبار امروز مستقیماً از TradingEconomics
    url = "https://api.tradingeconomics.com/calendar?importance=1,2,3&f=json"
    headers = {"User-Agent": "Mozilla/5.0"}

    try:
        response = requests.get(url, headers=headers, timeout=15)
        data = response.json()

        today_str = datetime.datetime.utcnow().strftime("%Y-%m-%d")

        # فیلتر کردن اخبار امروز
        today_events = [
            e
            for e in data
            if isinstance(e, dict)
            and str(e.get("Date", "")).startswith(today_str)
        ]

        if not today_events:
            text = "📊 امروز هیچ خبر اقتصادی مهمی در TradingEconomics ثبت نشده است."
        else:
            text = "📅 اخبار و رویدادهای امروز (Trading Economics):**\n\n"
            for event in today_events:
                importance = event.get("Importance", 1)
                title = event.get("Event", "")
                country = event.get("Country", "")
                date_val = str(event.get("Date", ""))

                time_str = (
                    date_val.split("T")[-1][:5]
                    if "T" in date_val
                    else "All Day"
                )

                # تعیین اهمیت خبر
                if importance == 3:
                    emoji = "🔴"
                elif importance == 2:
                    emoji = "🟠"
                else:
                    emoji = "🟡"

                text += f"{emoji} {country}** - {title}\n"
                text += f"⏰ زمان (UTC): `{time_str}`\n"
                text += "-------------------\n"

        telegram_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        payload = {"chat_id": CHAT_ID, "text": text, "parse_mode": "Markdown"}
        requests.post(telegram_url, json=payload)

    except Exception as e:
        telegram_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        requests.post(
            telegram_url,
            json={
                "chat_id": CHAT_ID,
                "text": f"⚠️ خطا در دریافت اخبار TradingEconomics: {str(e)}",
            },
        )


send_news()
