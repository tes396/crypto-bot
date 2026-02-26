import sqlite3
import requests
from datetime import datetime, timedelta

conn = sqlite3.connect("db.sqlite")
c = conn.cursor()

c.execute("SELECT id, address, detect_time FROM tokens")
rows = c.fetchall()

for r in rows:
    detect_time = datetime.fromisoformat(r[2])
    if datetime.utcnow() - detect_time > timedelta(hours=6):
        try:
            url = f"https://api.dexscreener.com/latest/dex/pairs/solana/{r[1]}"
            price_now = float(requests.get(url).json()["pair"]["priceUsd"])
            # 仮に holder列に価格を記録（MVP用）
            c.execute("UPDATE tokens SET holder=? WHERE id=?", (price_now, r[0]))
        except:
            pass

conn.commit()
conn.close()





























