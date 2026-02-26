import requests
import sqlite3
import json
from datetime import datetime

# DB初期化
conn = sqlite3.connect("db.sqlite")
c = conn.cursor()
c.execute("""
CREATE TABLE IF NOT EXISTS tokens (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    address TEXT,
    detect_time TEXT,
    lp REAL,
    dev REAL,
    tx REAL,
    holder REAL,
    concentration REAL,
    score REAL
)
""")
conn.commit()

# 重み読み込み
with open("weights.json") as f:
    weights = json.load(f)

# DexScreener APIからTop20取得（MVP用）
url = "https://api.dexscreener.com/latest/dex/pairs/solana"
pairs = requests.get(url).json()["pairs"][:20]

scored = []

def normalize(x, min_v, max_v):
    return max(0, min(1, (x - min_v) / (max_v - min_v)))

for p in pairs:
    try:
        lp = float(p["liquidity"]["usd"])
        tx = float(p["txns"]["h1"]["buys"])
        holder = float(p.get("fdv",0))
        dev = 0.1           # MVPは仮値
        concentration = 0.5 # MVPは仮値

        lp_n = normalize(lp,0,100000)
        tx_n = normalize(tx,0,200)
        holder_n = normalize(holder,0,1000000)

        score = (weights["lp"]*lp_n +
                 weights["dev"]*(1-dev) +
                 weights["tx"]*tx_n +
                 weights["holder"]*holder_n +
                 weights["concentration"]*(1-concentration))

        scored.append((p["pairAddress"], lp, dev, tx, holder, concentration, score))
    except:
        continue

# 上位3だけ保存
top3 = sorted(scored, key=lambda x: x[6], reverse=True)[:3]

for t in top3:
    c.execute("INSERT INTO tokens (address, detect_time, lp, dev, tx, holder, concentration, score) VALUES (?,?,?,?,?,?,?,?)",
              (t[0], datetime.utcnow().isoformat(), t[1], t[2], t[3], t[4], t[5], t[6]))

conn.commit()
conn.close()

print("Top3 tokens saved.")















































































































































































