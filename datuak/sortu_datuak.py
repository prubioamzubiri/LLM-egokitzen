"""Ikastetxeko IKT-txartelen datu-multzo sintetikoa sortzen du (euskaraz)."""
import json, random, sys
random.seed(42)
out = sys.argv[1]

SYSTEM = ("Ikastetxeko IKT-laguntza zerbitzuko sailkatzailea zara. "
          "Erantzun JSON objektu bakarrarekin, beste testurik gabe. Eremuak: "
          "kategoria (sarea|hardwarea|softwarea|kontuak|inprimagailua), "
          "lehentasuna (baxua|ertaina|altua), kokapena (testua edo null).")

# (nominatiboa, inesiboa, leku-genitiboa)
LEKUAK = [("A12 gela","A12 gelan","A12 gelako"),("A21 gela","A21 gelan","A21 gelako"),
 ("liburutegia","liburutegian","liburutegiko"),("idazkaritza","idazkaritzan","idazkaritzako"),
 ("irakasle-gela","irakasle-gelan","irakasle-gelako"),("informatika-gela","informatika-gelan","informatika-gelako"),
 ("B05 laborategia","B05 laborategian","B05 laborategiko"),("zuzendaritza","zuzendaritzan","zuzendaritzako"),
 ("ekitaldi-aretoa","ekitaldi-aretoan","ekitaldi-aretoko"),("C03 tailerra","C03 tailerrean","C03 tailerreko"),
 ("B14 gela","B14 gelan","B14 gelako"),("kafetegia","kafetegian","kafetegiko")]
LEKU_TEST = [("D02 gela","D02 gelan","D02 gelako"),("orientazio-gela","orientazio-gelan","orientazio-gelako")]

GAILUAK = ["ordenagailua","proiektorea","pantaila","teklatua","sagua","eramangarria","bozgorailua"]
PLATAFORMAK = ["Moodlen","Teamsen","Classroomen","posta elektronikoan","Ikasgunean"]
PROGRAMAK = ["Moodle","Visual Studio Code","LibreOffice","Teams","Chrome","Python","Docker","Excel"]

T = {
 "sarea": ["{in} ez dago interneteko konexiorik.","Wifia oso motel dabil {in}.","{gen} sare-kablea ez dabil, ez dago konexiorik.",
           "Ezin naiz wifira konektatu {in}, pasahitza onartzen ez duela dio.","Internet etengabe eteten da {in}.",
           "Ez dago sarerik.","Wifiak ez du funtzionatzen eta ez dakit zergatik."],
 "hardwarea": ["{gen} {gailu} ez da pizten.","{gen} {gailu} hautsita dago.","{in} {gailu} ez dabil ondo, oso berotzen da.",
           "Nire {gailu} ez da pizten.","{gen} {gailu} zarata arraroak egiten ditu.","{in} {gailu} bakarrik itzaltzen da."],
 "softwarea": ["{prog} ez da irekitzen {in}.","{prog} eguneratzean errore bat agertzen da.","Ezin dut {prog} instalatu {gen} ordenagailuan.",
           "{prog} bat-batean ixten da.","{prog} programaren lizentzia iraungita dago.","{prog} oso motel doa {in}."],
 "kontuak": ["Pasahitza ahaztu dut eta ezin naiz sartu.","Nire kontua blokeatuta dago.","Ezin naiz {plat} sartu, erabiltzailea ez dela existitzen dio.",
           "Ikasle berri batek ez du konturik oraindik.","Posta elektronikoko pasahitza aldatu behar dut.","{in} ezin naiz saioa hasi nire kontuarekin."],
 "inprimagailua": ["{gen} inprimagailuak ez du inprimatzen.","Papera trabatuta dago {gen} inprimagailuan.","{gen} inprimagailuak tinta falta du.",
           "Inprimagailua ez da agertzen nire ordenagailuan.","{in} inprimatzeko ilara blokeatuta dago.","Inprimagailuak orri zuriak ateratzen ditu."],
}
T_TEST = {  # ikusi gabeko txantiloiak (orokortzea neurtzeko)
 "sarea": ["Gaur goizetik {in} sarea erorita dago."],
 "hardwarea": ["{gen} {gailu} kolpe bat jaso du eta ez dabil."],
 "softwarea": ["{prog} irekitzean pantaila beltza ikusten da {in}."],
 "kontuak": ["Bi faktoreko autentifikazioak ez dit kodea bidaltzen."],
 "inprimagailua": ["{gen} inprimagailuak argi gorria du eta ez du ezer egiten."],
}
ALTUA = [" Premiazkoa da!"," Azterketa bat dugu ordu batean."," Klase osoa geldirik dago."," Ezin dugu lanik egin."]
BAXUA = [" Ez da larria, ahal duzuenean."," Ez dago presarik."," Datorren astean begiratzea nahikoa da."]
HASIERA = ["","","Kaixo, ","Egun on, ","Arratsalde on: ","Mesedez, "]

def sortu(n, txantiloiak, lekuak, mota=None):
    rows = []
    for _ in range(n):
        kat = random.choice(list(txantiloiak))
        t = random.choice(txantiloiak[kat])
        nom, ine, gen = random.choice(lekuak)
        testua = t.replace("{in}", ine).replace("{gen}", gen).format(gailu=random.choice(GAILUAK), prog=random.choice(PROGRAMAK), plat=random.choice(PLATAFORMAK))
        kokapena = nom if ("{in}" in t or "{gen}" in t) else None
        r = random.random()
        if r < 0.3: lehen, testua = "altua", testua + random.choice(ALTUA)
        elif r < 0.55: lehen, testua = "baxua", testua + random.choice(BAXUA)
        else: lehen = "ertaina"
        h = random.choice(HASIERA)
        lehen_hitza = testua.split()[0]
        izen_berezia = lehen_hitza in PROGRAMAK or any(c.isdigit() for c in lehen_hitza)
        if h and not izen_berezia:
            testua = testua[0].lower() + testua[1:]
        testua = h + testua if h else testua[0].upper() + testua[1:]
        erantzuna = json.dumps({"kategoria": kat, "lehentasuna": lehen, "kokapena": kokapena}, ensure_ascii=False)
        rows.append({"prompt":[{"role":"system","content":SYSTEM},{"role":"user","content":testua}],
                     "completion":[{"role":"assistant","content":erantzuna}]})
        if mota: rows[-1]["mota"] = mota
    return rows

train = sortu(800, T, LEKUAK)
test = sortu(100, T, LEKUAK, "ikusia") + sortu(50, T_TEST, LEKUAK + LEKU_TEST, "berria")
random.shuffle(test)
for izena, d in [("txartelak_train.jsonl", train), ("txartelak_test.jsonl", test)]:
    with open(f"{out}/{izena}", "w", encoding="utf-8") as f:
        for r in d: f.write(json.dumps(r, ensure_ascii=False) + "\n")
print(len(train), len(test))
