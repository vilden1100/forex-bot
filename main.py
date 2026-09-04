import datetime
import requests

# اطلاعات خود را بین " " قرار دهید
BOT_TOKEN = "8963564577:AAE_2ajuS1UUmGlNjZWSp97eOsYnRnZO9YA"
CHAT_ID = "8298401582"


def send_news():
    url = "https://nfs.forexfactory.net/ff_calendar_thisweek.json"
    headers = {"User-Agent": "Mozilla/5.0"}

    try:
        response = requests.get(url, headers=headers, timeout=15)
        data = response.json()

        today_str = datetime.datetime.utcnow().strftime("%Y-%m-%d")
        today_events = [
            e for e in data if e.get("date", "").startswith(today_str)
        ]

        if not today_events:
            text = "📊 امروز هیچ خبر اقتصادی در فارکس فکتوری ثبت نشده است."
        else:
            text = "📅 تمام اخبار و رویدادهای امروز فارکس فکتوری:**\n\n"
            for event in today_events:
                impact = event.get("impact", "")
                title = event.get("title", "")
                country = event.get("country", "")

                date_val = event.get("date", "")
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

        telegram_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        payload = {"chat_id": CHAT_ID, "text": text, "parse_mode": "Markdown"}
        requests.post(telegram_url, json=payload)

    except Exception as e:
        print(f"Error: {e}")


if name == "main":
    send_news()
