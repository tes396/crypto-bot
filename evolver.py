import sqlite3
import json

alpha = 0.1
SUCCESS_THRESHOLD = 1.8  # +80%

conn = sqlite3.connect("db.sqlite")
c = conn.cursor()

c.execute("SELECT lp, dev, tx, holder, concentration FROM tokens")
rows = c.fetchall()

success = [r for r in rows if r[3]>SUCCESS_THRESHOLD]
fail = [r for r in rows if r[3]<=SUCCESS_THRESHOLD]

if len(success)<5:
    conn.close()
    exit()

features = ["lp","dev","tx","holder","concentration"]
success_mean = [sum(x[i] for x in success)/len(success) for i in range(5)]
fail_mean = [sum(x[i] for x in fail)/len(fail)/1 for i in range(5)]

with open("weights.json") as f:
    weights = json.load(f)

for i, f_name in enumerate(features):
    diff = success_mean[i]-fail_mean[i]
    weights[f_name] += alpha*diff

total = sum(weights.values())
for k in weights:
    weights[k]/=total

with open("weights.json","w") as f:
    json.dump(weights,f,indent=2)

conn.close()
print("Weights updated.")















































































































