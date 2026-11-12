# LLM-egokitzen

Eredu txiki bat (`Qwen/Qwen2.5-0.5B-Instruct`) LoRA bidez doitu ikastetxeko IKT-txartelak sailkatzeko (testua → JSON), ebaluatu eta Ollama-n exekutatu.

## Edukia

```
praktikak/                    Colab koadernoak (T4 GPU)
  01_oinarri_lerroa.ipynb
  02_datuak.ipynb
  03_lora_entrenamendua.ipynb
  04_ebaluazioa.ipynb
  05_hedapena.ipynb
  ebaluatu_ollama.py          Ollama-ko eredua ebaluatzeko (ordenagailu lokalean)
datuak/
  txartelak_train.jsonl       800 adibide (prompt/completion, elkarrizketa formatua)
  txartelak_test.jsonl        150 adibide: 100 "ikusia" + 50 "berria" (txantiloi/gela berriak)
  sortu_datuak.py             Datu-multzoaren sortzailea (seed=42)
```

## Prestaketa

1. Igo `datuak/*.jsonl` Google Drive-ko `MyDrive/llm-egokitzapena/` karpetara.
2. Ireki koadernoak Colab-en eta aukeratu **T4 GPU**.
3. Koadernoen emaitzak (egokitzailea, CSVak, GGUF) karpeta berean gordetzen dira.

Bertsio finkoak: `transformers==5.22.2 peft==0.21.2 trl==1.17.1 datasets==5.2.0`.
