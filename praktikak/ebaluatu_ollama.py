"""Ollama-n dagoen eredu bat test multzoarekin ebaluatu.

Erabilera:
    python ebaluatu_ollama.py txartelak txartelak_test.jsonl
    python ebaluatu_ollama.py txartelak txartelak_test.jsonl --json-gabe
"""
import argparse
import json
import time

import ollama
import pandas as pd

METRIKAK = ["json_ok", "kategoria", "lehentasuna", "kokapena", "guztiz"]


def ebaluatu_bat(sortua, zuzena):
    em = {"json_ok": False, "kategoria": False, "lehentasuna": False,
          "kokapena": False, "guztiz": False}
    try:
        s = json.loads(sortua)
    except json.JSONDecodeError:
        return em
    if not isinstance(s, dict):
        return em
    em["json_ok"] = True
    for eremua in ["kategoria", "lehentasuna", "kokapena"]:
        em[eremua] = s.get(eremua) == zuzena[eremua]
    em["guztiz"] = em["kategoria"] and em["lehentasuna"] and em["kokapena"]
    return em


def main():
    p = argparse.ArgumentParser()
    p.add_argument("eredua")
    p.add_argument("test_fitxategia")
    p.add_argument("--json-gabe", action="store_true", help="format='json' erabili gabe")
    p.add_argument("-n", type=int, default=None, help="lehen N adibideak bakarrik")
    args = p.parse_args()

    with open(args.test_fitxategia, encoding="utf-8") as f:
        adibideak = [json.loads(l) for l in f if l.strip()][: args.n]

    lerroak, t0 = [], time.time()
    for i, a in enumerate(adibideak, 1):
        testua = a["prompt"][-1]["content"]          # sistema-mezua Modelfile-tik dator
        aukerak = {} if args.json_gabe else {"format": "json"}
        r = ollama.chat(model=args.eredua, messages=[{"role": "user", "content": testua}],
                        options={"temperature": 0}, **aukerak)
        sortua = r.message.content.strip()
        zuzena = json.loads(a["completion"][0]["content"])
        lerroak.append({"testua": testua, "sortua": sortua, "mota": a.get("mota", ""),
                        **ebaluatu_bat(sortua, zuzena)})
        print(f"\r{i}/{len(adibideak)}", end="", flush=True)

    dt = time.time() - t0
    df = pd.DataFrame(lerroak)
    print(f"\n\nEredua: {args.eredua}  |  {len(df)} adibide  |  {dt / len(df):.2f} s/adibide\n")
    print(df[METRIKAK].mean().round(3).to_string())
    if df["mota"].any():
        print("\nMotaren arabera (guztiz zuzena):")
        print(df.groupby("mota")["guztiz"].mean().round(3).to_string())
    df.to_csv(f"emaitzak_{args.eredua.replace(':', '_')}.csv", index=False)


if __name__ == "__main__":
    main()
