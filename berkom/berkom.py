# Library yang dipakai: random (nomor tiket acak), flet (tampilan), flet_audio (suara)
import random

import flet as ft
import flet_audio as fta

# Warna-warna tampilan (format hex)
green = "#33ff66"
dimGreen = "#1f8a3d"
black = "#0a0a0a"
red = "#ff5555"
# Nama font yang didaftarkan di page.fonts
mono = "Mono"
jp = "JP"
brailleFont = "Braille"
# Warna kertas dan tinta untuk tiket JR
paper = "#fcd9a8"
paperDark = "#f4b877"
ink = "#3b2f27"
# Sudut putaran dalam radian (satu putaran penuh dan seperempat putaran)
fullTurn = 6.283185307179586
quarterTurn = 1.5707963267948966
# Ukuran huruf standar dan lebar satu karakter (dibanding ukuran huruf)
size = 16
charWidth = 0.602
# Lebar kotak tiket ASCII dan batas panjang nama
l = 56
maxName = 20
# Garis tepi kotak tiket, contoh: +------+
line = "+" + "-" * l + "+"

# Daftar lagu: (judul, lokasi file di folder assets)
playlist = [
    ("Quiet Town of Tokyo", "music/quiet_town_of_tokyo.mp3"),
    ("Yokaze", "music/yokaze.mp3"),
]

# Dictionary data kereta: daftar stasiun dan harga tiap jalur
trains = {
    "MRT": {
        "station": ["Lebak Bulus", "Fatmawati", "Cipete Raya", "Haji Nawi", "Blok A",
                    "Blok M", "ASEAN", "Senayan", "Istora", "Bendungan Hilir",
                    "Setiabudi", "Dukuh Atas", "Bundaran HI"],
        "initPrice": 10000,  # harga untuk 2 stasiun pertama
        "nextPrice": 10000,  # harga untuk stasiun berikutnya
    },
    "KRL": {
        "station": ["Jakarta Kota", "Jayakarta", "Mangga Besar", "Sawah Besar", "Juanda",
                    "Gondangdia", "Cikini", "Manggarai", "Tebet", "Cawang",
                    "Duren Kalibata", "Pasar Minggu Baru", "Pasar Minggu"],
        "initPrice": 3000,
        "nextPrice": 5000,
    },
    "LRT": {
        "station": ["Dukuh Atas", "Setiabudi", "Rasuna Said", "Kuningan", "Pancoran",
                    "Cikoko", "Ciliwung", "Cawang", "Taman Mini", "Kampung Rambutan",
                    "Ciracas", "Harjamukti"],
        "initPrice": 5000,
        "nextPrice": 7000,
    },
    "JR": {
        "station": ["Gotanda", "Meguro", "Ebisu", "Shibuya", "Harajuku",
                    "Yoyogi", "Shinjuku", "Shin-Okubo", "Takadanobaba", "Mejiro",
                    "Ikebukuro", "Otsuka", "Sugamo", "Komagome", "Tabata",
                    "Nishi-Nippori", "Nippori", "Uguisudani", "Ueno", "Okachimachi",
                    "Akihabara", "Kanda", "Tokyo", "Yurakucho", "Shimbashi",
                    "Hamamatsucho", "Tamachi", "Shinagawa", "Osaki"],
        "initPrice": 150,
        "nextPrice": 20,
        "currency": "¥",  # mata uang yen
        "loop": True,  # jalur melingkar (Yamanote)
        "sound": True,  # punya suara pengumuman stasiun
    },
}

# Nama stasiun JR dalam huruf kanji (untuk tiket Jepang)
kanji = {
    "Gotanda": "五反田", "Meguro": "目黒", "Ebisu": "恵比寿", "Shibuya": "渋谷",
    "Harajuku": "原宿", "Yoyogi": "代々木", "Shinjuku": "新宿", "Shin-Okubo": "新大久保",
    "Takadanobaba": "高田馬場", "Mejiro": "目白", "Ikebukuro": "池袋", "Otsuka": "大塚",
    "Sugamo": "巣鴨", "Komagome": "駒込", "Tabata": "田端", "Nishi-Nippori": "西日暮里",
    "Nippori": "日暮里", "Uguisudani": "鶯谷", "Ueno": "上野", "Okachimachi": "御徒町",
    "Akihabara": "秋葉原", "Kanda": "神田", "Tokyo": "東京", "Yurakucho": "有楽町",
    "Shimbashi": "新橋", "Hamamatsucho": "浜松町", "Tamachi": "田町", "Shinagawa": "品川",
    "Osaki": "大崎",
}

# Daftar anggota kelompok (NIM - nama)
team = [
    "18226008 - Muhammad Faris Kautsar",
    "13226044 - Putu Gede Bayu Eka Pradipa",
    "18126030 - Ahmas Ghazi Izaaturahman",
    "13226008 - Rafif Firza Izzan",
    "13226036 - Radhiyya Adis Akmal",
]

# Judul 'Train Ticket' dalam bentuk ASCII art (font nscript)
titleArt = r''' ,ggggggggggggggg                                          ,ggggggggggggggg
dP""""""88"""""""                                         dP""""""88"""""""               ,dPYb,                I8
Yb,_    88                                                Yb,_    88                      IP'`Yb                I8
 `""    88                          gg                     `""    88       gg             I8  8I             88888888
        88                          ""                            88       ""             I8  8bgg,             I8
        88   ,gggggg,    ,gggg,gg   gg    ,ggg,,ggg,              88       gg     ,gggg,  I8 dP" "8   ,ggg,     I8
        88   dP""""8I   dP"  "Y8I   88   ,8" "8P" "8,             88       88    dP"  "Yb I8d8bggP"  i8" "8i    I8
  gg,   88  ,8'    8I  i8'    ,8I   88   I8   8I   8I       gg,   88       88   i8'       I8P' "Yb,  I8, ,8I   ,I8,
   "Yb,,8P ,dP     Y8,,d8,   ,d8b,_,88,_,dP   8I   Yb,       "Yb,,8P     _,88,_,d8,_    _,d8    `Yb, `YbadP'  ,d88b,
     "Y8P' 8P      `Y8P"Y8888P"`Y88P""Y88P'   8I   `Y8         "Y8P'     8P""Y8P""Y8888PP88P      Y8888P"Y88888P""Y88'''

# Gambar gerbong penumpang (disusun dari potongan string)
coachWidth = 41
coachArt = [
    "  " + "_" * coachWidth,
    " |" + ("  ____  " * 5).ljust(coachWidth) + "|",
    " |" + (" |    | " * 5).ljust(coachWidth) + "|",
    " |" + (" |____| " * 5).ljust(coachWidth) + "|",
    " |" + "_" * coachWidth + "|",
    " |" + "___|" + "_" * (coachWidth - 8) + "|___" + "|==",
]
# Roda gerbong penumpang
coachWheelArt = [
    "     /  \\  /  \\" + " " * 15 + "/  \\  /  \\",
    "    | () || () |" + " " * 13 + "| () || () |",
    "     \\__/  \\__/" + " " * 15 + "\\__/  \\__/",
]

# Gambar lokomotif uap
locoArt = r"""
                                       ____
                    ____              |    |
  ______________   |    |   ______    |    |
 |   ________   |__|____|__|______|___|____|____
 |  |  []  []|  |                               |\__
 |  |________|  |   ____________________________|   \__
 |______________|  |____________________________||_____ \
 |____|======|__|_________________________________|_____|>""".strip("\n").split("\n")

# Dua frame roda lokomotif (batang penghubung naik-turun)
wheelArts = [
    r"""
    /  \       /  \       /  \       /  \        __
   | () |=====| () |=====| () |=====| () |      (__)
    \__/       \__/       \__/       \__/""".strip("\n").split("\n"),
    r"""
    /  \       /  \       /  \       /  \        __
   | () |     | () |     | () |     | () |      (__)
    \__/=======\__/=======\__/=======\__/""".strip("\n").split("\n"),
]


# Dua frame asap dari cerobong
smokeArts = [
    r"""
  (@@)   (  )   (@@@)   (  )    (@)
                                    (    )
                                         (@@@)
                                            (  )""".strip("\n").split("\n"),
    r"""
    (  )   (@@)   ( )   (@@@)    ( )
                                     (@@)
                                         (    )
                                            (@@)""".strip("\n").split("\n"),
]


# Fungsi untuk menggabungkan asap, gerbong, lokomotif, dan roda menjadi satu gambar kereta
def makeTrain(frame):
    tw = max(len(x) for x in coachArt)  # lebar gerbong
    lw = max(len(x) for x in locoArt)  # lebar lokomotif
    rows = []
    for s in smokeArts[frame]:
        rows.append(" " * (tw - 2) + s)
    top = len(locoArt) - len(coachArt)  # selisih tinggi lokomotif dan gerbong
    for i in range(len(locoArt)):
        left = coachArt[i - top] if i >= top else ""
        rows.append(left.ljust(tw) + locoArt[i])
    wheels = wheelArts[frame]
    for i in range(len(wheels)):
        left = coachWheelArt[i] if i < len(coachWheelArt) else ""
        rows.append(left.ljust(tw) + wheels[i])
    return "\n".join(x.rstrip().ljust(tw + lw + 2) for x in rows)


# Gambar piringan hitam (disk) yang berputar
diskArt = r"""      ...   ....      
   ..'' ''''::.::..   
  .:.:.'  ':..:.:.:.  
 .::.::.'####:.::.::. 
.:..::.########.::..:.
.::..::==o  o==::..::.
.:..::.@@@@@@@@.::..:.
 .::.::.:@@@@'.::.::. 
  .:.:.:..:'  ' :.:.  
   ..::.:::''' ''..   
      .....  ...      """

# Gambar braille pertama untuk panel kiri
brailleArt = """⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣀⣀⣀⣀⣀⣀⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣴⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣤⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣀⠀⠀⠀⢀⣴⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠻⣿⣿⣿⣿⣦⣄⠀⠀⠠⠰⠶⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣠⣤⣤⡤⢀⣴⣿⣿⣿⠏⠀⠋⢉⣠⣿⣿⣿⣿⣿⣿⣿⣤⣄⡀⠈⠙⢿⣿⣿⣿⣧⡀⠐⠻⣶⣶⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣰⣿⠟⠁⠉⢠⣾⣿⣿⡿⠁⠀⣠⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⣄⠈⠻⣿⣿⣿⣷⡄⠀⢀⠙⢿⡆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢰⠟⢁⡔⠀⣠⣿⣿⣿⡿⠁⣠⣾⣿⣿⠛⣻⣿⣿⡿⠁⠹⣿⣿⣿⣿⣿⣿⣿⣦⡀⠹⣿⣿⣿⣿⡀⠈⢧⡈⢳⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡟⢠⡿⠀⢰⣿⣿⣿⡿⠁⣼⣿⣿⡿⠃⣼⣿⠏⠀⠁⣴⣆⠈⠉⠙⢿⣿⣿⣿⣿⣷⡄⢹⣿⣿⣿⣷⠀⠀⢷⡈⣧⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠐⢠⣿⠃⠀⣿⣿⣿⣿⠃⣸⣿⣿⠟⢀⣾⠿⠋⠀⢠⣾⣿⣿⣷⣄⠀⠀⠙⢿⣿⣿⣿⣷⠀⣿⣿⣿⣿⡄⢣⠘⣇⠘⡆⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣼⡟⠀⢰⣿⣿⣿⡟⢀⣿⠟⠀⠰⠛⠋⠀⢠⣾⣿⣿⣿⣿⣿⡿⠟⠂⣀⠀⠉⠙⢿⣿⡇⢸⣿⣿⣿⣇⠘⡄⢹⡀⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢰⣿⡇⠀⠸⣿⣿⣿⡇⠈⠁⠀⠀⡀⠀⢀⣀⣤⣿⣿⣿⣿⣿⣿⣷⣤⣍⣉⣁⣤⣤⣀⠙⠓⠘⣿⣿⣿⣿⠀⣇⢸⣿⣿⡆⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⢰⣾⣿⠁⠀⠀⣿⣿⣿⡇⢠⣶⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⠀⣿⠻⣿⠛⡆⢻⠸⣿⣿⣇⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⠀⡆⠀⣿⣿⠙⡇⢸⣿⣿⡿⠿⠟⠋⠙⢻⣿⣿⣿⣿⣿⣿⣿⣿⠛⠙⠛⠿⢿⣿⣿⣿⠀⡟⠀⣿⠀⡇⢈⣀⠛⠛⠻⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⡀⠀⠀⠀⠀⠀⠀⠀⣀⣀⡀⠀⠀⢻⣿⡆⢁⠘⣿⣿⣇⣀⣀⣀⣠⣼⣿⣿⣿⣿⣿⣿⣿⣿⣦⣀⣀⠀⢠⣿⣿⣿⠀⠇⢰⣿⠀⡇⢠⣌⣉⣉⠓⠒⠶⠶⠤⠤⣤⣀⠀
⠀⠈⠓⠶⢄⠐⠲⠀⡄⢾⣿⣿⣿⣧⠀⠘⣿⡇⠘⠀⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⠀⠀⢸⣿⠀⠁⢸⣿⣿⣿⠇⢰⣀⣄⠠⠒⠉⠀⠀
⠀⠀⠀⠀⠀⠀⠘⠛⠇⠀⠹⣿⣿⣿⡄⠀⠹⣷⠀⠁⠘⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠃⠀⠀⣿⡏⠀⠀⣾⡿⠟⠋⠀⠀⠉⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡀⠀⠉⣙⠛⠀⠀⠙⡆⠀⠀⢻⣿⣿⣿⣿⣿⣿⡿⠿⣿⠿⠿⣿⠿⣿⣿⣿⣿⣿⣿⣿⣇⢀⡾⠀⠇⠀⠀⢀⡠⠄⢀⣠⣶⡇⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣷⡆⠉⠀⠀⠀⠀⠀⠀⠀⢺⣿⣿⣿⣿⣿⣿⣿⣶⣶⣶⣶⣶⣶⣿⣿⣿⣿⣿⣿⣿⣿⡿⠁⠀⠀⠀⠀⠈⢠⣶⣿⣿⣿⣷⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⡄⠀⠀⠸⣿⠀⠀⠀⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠟⠀⠀⠀⣾⠁⠀⣠⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣷⠀⠘⡀⢻⡀⠀⠀⠀⠈⠙⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠟⠉⠀⠀⠀⠀⠀⠃⠀⢰⣿⣿⣿⠀⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⠸⣿⣿⡀⠀⣧⠘⡇⠀⠀⠀⠀⠀⠀⠀⠀⠉⠛⠿⠿⢿⣿⠿⠿⠛⠋⠁⠀⠀⠀⠀⣀⣀⡀⠀⠀⠀⢸⣿⣿⡿⢰⣿⣿⡿⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⣿⡀⣿⣿⣇⠀⢿⡄⠃⢸⣿⣿⠀⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣠⣤⣾⡇⠈⣿⣿⣿⠀⠀⠀⢸⣿⣿⡇⢸⣿⡟⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠘⠀⣿⡇⣿⣿⣿⡆⠸⣧⠀⠀⣿⡇⠀⠀⠀⠀⠀⠀⠀⠐⣶⣶⣶⣿⣿⣿⣿⣿⡿⠋⠁⠀⣿⣿⡇⠀⠀⠀⣼⣿⣿⡇⠈⠟⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠘⠀⣿⡇⣿⣿⣿⣷⠀⢿⡀⠀⣿⣇⠀⠱⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⠿⠛⢉⡠⠚⠀⢰⣿⣿⡇⠀⠀⠀⣿⣿⣿⡇⠀⠀⣠⡀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⢰⡆⠀⢹⡇⢹⣿⣿⣿⡇⠸⡇⠀⢸⣿⡄⠀⢄⣉⠛⠒⠒⠦⠤⠤⠤⠤⠒⠒⠉⣁⣤⠂⠀⣸⣿⣿⠇⢨⡰⢀⣿⣿⣿⡇⠀⣰⣿⣷⡀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⢠⣿⡇⠀⠸⡇⢸⣿⣿⣿⣿⠀⣿⠀⢸⣿⣷⠀⠘⣿⣿⡏⡠⠀⣴⠂⣤⠀⣶⠈⣆⠸⠃⠈⢠⣿⣿⣿⠀⣿⡇⢸⣿⣿⣿⡇⢠⣿⣿⣿⣧⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⢠⣿⣿⣿⠀⠀⣧⠸⣿⣿⣿⣿⡇⢸⡇⠀⣿⣿⣇⠀⠘⣿⡇⡇⢸⣿⢠⣿⠄⢿⠀⣿⠀⠀⣠⣿⣿⣿⡟⢠⣿⠃⣼⣿⣿⣿⡇⣾⣿⣿⣿⣿⣧⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⣼⣿⣿⣿⡇⠀⢸⠀⣿⣿⣿⣿⣿⠈⣿⠀⢿⣿⣿⣄⠁⢘⠀⡄⢸⣿⠈⢀⠀⢘⡀⢻⠀⣴⣿⣿⣿⣿⡇⢸⣿⣤⣿⣿⣿⣿⡇⣿⣿⠛⣿⣿⣿⣆⠀⠀⠀⠀
⠀⠀⠀⠀⢠⣿⣿⠃⣸⣿⠀⠸⡄⢻⣿⣿⣿⣿⡄⢻⡆⢸⣿⣿⣿⣿⣿⠀⠃⢈⡇⠀⢸⡄⠈⣇⠘⡆⢻⣿⣿⣿⣿⠁⣾⠇⣼⣿⣿⣿⣿⡇⣿⣿⡆⠘⣿⣿⣿⡆⠀⠀⠀
⠀⠀⠀⢀⣾⣿⡏⢀⣿⣿⡇⠀⡇⠸⣿⣿⣿⣿⣇⠸⣧⢸⣿⣿⣿⣿⡇⢸⠀⣿⠇⠀⠉⠉⠀⢿⡀⢳⠸⣿⣿⣿⣿⠀⡿⠀⣿⣿⣿⡏⢹⡇⣿⣿⣧⠀⠸⣿⣿⣿⡄⠀⠀
⠀⠀⠀⣼⣿⡿⠀⣼⣿⣿⣿⠀⢱⣶⣿⣿⣿⣿⣿⠀⣿⠈⣿⣿⣿⣿⡇⠈⠀⣿⠀⠀⠀⠀⠀⠸⡇⠸⡀⢿⣿⣿⡏⢰⠃⠀⣿⣿⣿⣧⢸⡇⣿⣿⣿⡆⠀⢹⣿⣿⣿⡀⠀
⠀⠀⢠⣿⣿⠁⢠⣿⣿⣿⣿⡄⢸⡇⢻⣿⣿⣿⣿⡆⠀⠃⣿⣿⣿⣿⠀⣾⢸⡿⢀⣤⣤⣤⣤⠀⢿⠀⡇⠸⣿⣿⡇⠘⢠⠀⣿⣿⣿⣿⢸⡇⢹⣿⣿⣷⡀⠀⢿⣿⣿⣧⠀
⠀⠀⣾⣿⠏⠀⣼⣿⣿⣿⣿⡇⢸⡇⢸⣿⣿⣿⣿⡇⠀⠀⢻⣿⣿⣿⠀⠉⢸⡇⢸⣿⣿⣿⣿⡇⠸⡇⢻⡀⢿⣿⡇⠀⠀⠀⣿⣿⣿⡇⢸⡇⣼⣿⣿⣿⣇⠀⠘⣿⣿⣿⣧
⠀⣸⣿⡟⠀⢠⣿⣿⣿⣿⣿⣿⠈⡇⠈⣿⣿⣿⣿⣷⡆⠀⢸⣿⣿⡏⢠⡇⣼⠃⠀⠀⠀⠀⠀⠀⠀⣷⠘⡇⠸⣿⡇⢀⠀⠀⣿⣿⣿⡇⠈⡇⣿⣿⣿⣿⣿⡄⢆⠸⣿⣿⣿
⢠⣿⣿⠁⡌⢸⣿⣿⣿⣿⣿⣿⠀⡇⠀⢿⣿⣿⣿⣿⡇⠀⢸⣿⣿⡇⢘⠇⣿⠀⠀⠀⠀⠀⠀⠀⠀⠸⡀⢻⠀⢿⣷⠈⠀⠀⣿⣿⣿⠇⠀⡇⣿⣿⣿⣿⣿⣷⠘⡄⢹⣿⣿
⣿⣿⠇⢸⠇⣿⣿⣿⣿⣿⣿⣿⠀⡇⠀⠸⣿⣿⣿⣿⡇⠀⢸⣿⣿⠇⣘⠀⡟⢠⣤⣤⣤⣤⣤⣴⣶⠀⡇⠸⡇⢸⣿⡀⠀⠀⢿⣿⣿⠀⠀⠃⣿⣿⣿⣿⣿⣿⡄⢹⡀⢿⣿
⠙⠿⢠⣿⠀⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⢻⣿⣿⣿⠀⠀⣾⣿⣿⠀⣿⠀⡇⢸⣿⣿⣿⣿⠿⠿⠿⡇⢸⠀⢻⠈⣿⣧⠀⠀⢸⣿⡏⠠⠀⢰⣿⣿⣿⣿⣿⣿⣷⠀⢷⣸⠟
⠷⠄⠈⠋⢠⣿⣿⣿⣿⣿⣿⣿⣷⠀⠀⠀⠈⢿⣿⡟⠀⠀⣿⣿⣿⠀⠋⢀⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠸⡇⠸⡇⢻⣿⣷⡄⠀⣿⠃⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣇⠈⠀⠲
⣦⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣧⠀⢰⡄⠈⢻⠇⠀⢸⣿⣿⣿⠸⡇⢸⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢿⠀⢧⠈⣿⣿⣷⡄⠘⢠⡆⢀⣿⣿⣿⣿⣿⣿⣿⣿⡟⠀⠀⠀
⠉⠀⠀⠀⠸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣇⠈⢿⣦⡈⠀⣠⣿⣿⣿⡟⢠⠇⠘⠀⣤⣤⣤⣤⣤⣤⣤⣤⣴⡆⠸⡇⢸⡄⢹⣿⣿⡷⠀⣿⣧⣼⣿⣿⣿⣿⣿⡿⠟⢉⣤⠂⠀⠀
⠀⠀⠀⠀⠲⢤⣉⠛⠻⠿⣿⣿⣿⣿⣿⣶⣼⣿⣷⣀⣹⣿⣿⣿⡇⣼⠀⣿⠀⠛⠛⠛⠛⠋⠋⠉⠉⠉⠉⠀⢿⠈⣧⠈⣿⣿⣿⣿⣿⣿⣿⣿⠿⠟⠋⣁⣤⠶⠋⣀⠴⠀⠀
⠀⠀⠀⠀⠐⠂⠌⠉⠓⠒⠦⠤⠍⠉⠉⠙⠛⠛⠛⠻⠿⠿⠿⠿⠇⠿⠀⠿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠸⠇⠹⠄⠹⠿⠿⠿⠟⠋⠉⠤⠶⠚⠋⠉⠤⠔⠊⠁⠀⠀⠀"""

# Gambar braille kedua (ditukar dengan tombol [ > ])
brailleArt2 = """⠀⠀⠀⠀⠀⠀⠀⠀⢀⢔⠾⢋⠷⢃⠠⠒⠈⠀⢀⣀⢂⢠⣲⢦⡪⠝⠀⢠⠎⠀⠀⠀⠀⠀⣠⣴⢪⡃⠜⠋⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠄⡀⠖⠁⠀⢀⠀⠀⡀⠀⠀⠀⠀⢀⣤⠦⡻⠂⠀⠀⠀⢼⡆⠀⠀⠁⡔⡀⡸⠀⢠⠃⠀⢸⣐⣷⣏⠉⠁⠉⢻⡄⠀⠀⡱⠑⢆⣨⠟⠊⠉⠀⠀⠈⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⢀⢔⠕⢁⠔⠁⠐⣁⣤⠴⠚⠉⢀⣠⠖⡫⠃⠁⠀⠀⣰⠃⠀⠀⡠⠀⢠⠞⡵⠃⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⠀⢀⠔⠈⠀⠀⠀⠔⡰⢃⠔⠁⠀⠀⠀⠼⡫⣠⠎⠀⠀⢀⠤⠀⠀⠀⠀⠀⠀⠰⢁⠃⢀⠇⠀⠀⣼⠋⣟⡆⠇⢀⠀⠸⢎⢵⠀⠱⠱⡈⢧⠄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⣠⡡⠁⢠⣁⣀⡴⡚⠅⠐⠈⢀⡴⠋⠐⠁⢀⡠⡤⠄⣰⠃⠀⠀⣰⠁⠀⣠⠊⠀⠀⠀⠀⢀⣀⣠⣤⠤⠶⠚⠋⠉⢀⡠⠀⠀⠀⠀⢠⣮⠞⣐⠅⠀⠀⠀⠀⢀⡴⠋⠁⣀⣠⠔⠁⠀⠀⢠⠃⠀⠀⠀⢦⠂⢠⠊⠀⠀⠚⠙⢰⢸⣷⢰⠈⢆⠀⠙⣮⢣⠀⠐⡔⡒⣧⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⢠⠟⣠⠖⠋⢁⠚⠃⣀⠔⠚⡷⠉⣉⡤⡲⢭⠞⢉⠃⣰⠏⠀⠀⡴⣉⡀⡚⠁⠑⠒⠀⡛⠛⢉⢁⠄⠀⣠⠗⠀⢀⡴⠋⠀⢀⠤⢠⢾⠋⢡⠞⠁⠀⡠⠒⠀⢀⣎⣠⢞⢵⠟⠁⠀⢀⠔⠠⠃⠀⡔⡐⠀⡇⠀⠁⠀⠀⠀⠀⡃⠈⠀⣿⠈⡀⡇⠣⡀⠈⢧⠡⡀⠈⢊⢜⣧⡀⠀⠀⠀⠀⠀⠀⠀⣀⡠⢤⣤⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⢸⢶⠃⠀⢀⠃⢠⡞⠁⢀⡼⡷⢋⣥⣮⠴⠁⡠⣵⢻⡟⠀⢀⡼⢋⢊⠌⠀⡠⠊⢀⠊⢀⣀⣆⠃⠀⣰⠃⢀⡴⠋⠀⢀⠔⠕⡡⠞⣠⠝⠁⠀⣠⠊⢀⣤⠖⣡⠞⣕⡡⠁⠀⣠⡞⡡⣶⡵⠀⣸⢣⠇⢸⡟⠀⠀⠀⡀⠀⢠⠁⡆⠀⡷⠀⡇⣏⡄⢻⠄⠀⠱⡷⣄⠀⠡⡹⡇⠀⢀⡀⠄⠒⠈⠁⠀⠀⠀⠀⠉⠓⢤⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠈⠙⠀⠀⡎⢠⠋⠀⣠⡮⠔⠈⣩⠞⠁⢀⢊⡾⢡⡄⠁⢠⡾⠡⠡⢂⠠⠊⢀⠔⣀⡴⢋⡏⠎⠀⣸⠃⣰⠟⠁⠀⡐⠁⡡⡊⠔⠈⡁⢐⣔⡟⢡⠞⡑⣡⠎⣡⠞⠝⠀⢀⣮⢟⠊⡸⠹⠁⢰⠃⣼⠀⣿⠂⢰⠀⢰⠃⠀⡌⢰⡗⢰⡧⠀⢫⡷⠇⠀⣎⢆⠀⡇⠏⢳⡤⠜⠓⠈⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠓⢄⡀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠑⣿⣖⡾⠋⠀⡠⠊⠁⢠⣖⣵⡭⡂⠁⠘⠄⢳⠁⡶⠓⣡⣰⣖⡥⠞⠁⣀⢼⢱⠀⣰⢃⡼⠃⠀⢠⡪⣪⠞⠋⡀⢔⣠⠦⠛⠉⣠⡳⢊⡴⢣⠞⢁⠊⠀⣠⡿⠛⢁⠎⢠⡳⢡⠏⢸⠟⢠⢟⠀⢸⠀⢸⠁⠀⢁⡿⠁⢠⠇⠀⠘⡇⠘⠀⡆⣾⠠⠓⠉⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⠦⡀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⡀⠝⠛⠀⡠⢊⣠⠾⠗⡾⠁⢳⠀⣽⡄⠀⢘⠾⣊⠴⢋⡵⢫⣷⣃⢀⠔⠁⣿⠆⠀⠀⡞⢁⠀⠴⠛⠘⣀⣔⡬⢖⠋⠁⢀⠔⣶⡟⠡⢈⡕⠛⠠⠂⠀⣰⠋⠀⡰⠁⢀⣧⢡⡎⢀⠟⠀⣸⢹⠀⢸⠀⡸⠀⠀⣾⠁⠀⡌⠀⣀⡸⠙⣄⠶⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠦⡀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠉⠀⠀⣰⣪⠖⠋⠀⢀⠜⢀⢌⠜⡆⣿⠼⣺⢗⣟⣡⡎⢡⠃⣤⠹⠘⠢⡤⢄⣛⡐⠠⠼⠍⠐⠀⣀⡤⡞⠉⠁⣤⠋⢀⠔⠁⣼⠏⠐⢠⠎⠐⠰⠃⠀⡼⠁⠀⡜⠀⡰⣻⢃⡞⠀⣸⠃⢀⡟⢰⠀⢸⠀⣷⠀⣸⠁⠀⡘⠀⣼⡿⠁⢠⢏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⢦⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⢎⣸⠃⠀⠀⡠⢃⣴⠟⣡⣴⣿⣷⠛⠛⡈⡇⢠⠗⢸⣾⠸⡇⠀⠀⠈⠑⡾⣫⢒⣴⣶⢟⠵⢡⠌⠀⠀⠔⠃⡠⠁⠀⣾⢋⠌⡰⠁⠀⠠⢁⡄⠐⠀⠀⢞⡒⡰⢠⡏⡾⢠⢧⡏⠀⢺⠯⢥⠀⢸⠀⡽⢠⠃⠀⡰⠇⣸⠗⠃⢠⢳⡆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠷⡄⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣨⣢⢔⣡⠖⢫⠽⠑⡟⠉⢸⢯⢏⠉⣵⡇⣸⠀⢘⢨⠃⡁⠓⠒⢢⢞⢜⣥⣫⣿⡧⠃⠀⡌⠀⠀⠈⠀⠊⠀⠀⣼⠃⠊⡐⠀⠀⢠⠣⡞⢠⡆⠀⡎⠀⠀⠁⣼⡝⢠⠟⡸⠀⠀⢸⢐⣸⠂⢸⠀⡇⢂⠄⡠⣧⣷⠏⠀⢠⡇⡈⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⣴⡆⠀⢰⡆⠀⢠⣾⣷⠀⢀⣾⠀⠀⣾⠆⠀⠀⠀⠀⠀⠀⠀⠀⠀⢹⡆
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠚⠿⠚⠋⠁⠌⠁⡠⠊⡐⣡⢟⡌⡈⢒⡏⢰⢸⢰⢸⢺⡄⠀⢀⡴⣷⢿⠏⢈⣿⠟⠷⢆⡤⢀⣀⠀⠀⠀⠀⠀⢀⣏⠌⡔⠀⠀⠀⣆⠾⢁⡞⡇⡜⠀⠀⠀⣀⣯⡴⣥⢷⠓⠒⠋⠉⠡⢸⠀⢸⠀⠇⠎⣠⠱⢸⠇⠀⢠⠃⢠⢁⡇⠀⠀⠀⠀⠀⠀⠀⠀⢰⣿⣷⢀⡿⢁⣴⠟⣹⣿⠀⣾⣷⣶⣾⡟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠸⡇
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⠔⠋⣀⣪⠞⡑⢁⢧⠙⠀⢇⢸⣿⢺⡞⡚⡯⢴⡙⠉⢀⡐⠂⡘⡞⠀⠅⠠⠉⠁⠚⠣⠝⣔⠶⣀⠀⠁⡰⠀⠀⠀⠀⡏⣄⡜⠀⡷⢓⣢⠿⠍⠛⠋⠠⡡⠂⠀⠀⠀⢀⠀⢀⡇⢨⠀⣶⡜⢸⠀⡟⠀⠀⢆⣠⠃⡈⡇⠀⠀⠀⠀⠀⠀⠀⢀⣿⠉⣿⣿⢃⣾⠿⠟⢻⣟⣸⡟⠁⢠⡿⠁⢀⣴⠆⠀⠀⠀⠀⠀⠀⠀⢠⡇
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⠴⠞⠧⠜⠋⢁⠂⠌⡰⢃⣾⣦⠀⢸⡀⣿⣄⢁⠇⠀⠀⢯⣝⣖⣿⣯⣿⣒⡭⠥⣐⡒⠤⢀⠀⠀⠈⠉⡛⢆⢠⠃⠀⠀⠀⠀⠑⠋⢀⣀⠻⠉⠁⠀⠀⢀⡠⠔⣒⣀⣭⣝⣛⣫⣿⣿⣧⠘⠀⣳⠀⣼⢠⠃⠀⠀⠸⣹⢀⠃⡇⠀⠀⠀⠀⠀⠀⠀⠘⠃⠀⠘⠃⠘⠃⠀⠀⠙⠋⠛⠀⠀⠙⠃⢠⠞⠁⠀⠀⠀⠀⠀⠀⠀⠀⢸⠃
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠁⠀⠀⠀⠀⢀⠂⣼⡞⠁⣾⡡⠘⡆⢸⡇⢸⡘⡈⢶⠀⠀⠀⢼⣣⠀⠀⢸⡄⠈⢽⡇⠛⠷⣦⣽⠀⠀⠀⠘⡟⡇⠀⠀⠀⠀⠀⠀⢠⣾⠆⠀⠀⠀⠀⢀⣯⡴⣾⠛⠩⠧⠄⣸⠃⠀⠀⣼⠆⢰⣇⡼⢰⣿⠄⠀⠀⠠⢿⠸⢰⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⣀⣤⡀⣤⡄⢀⣠⣤⣤⣤⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣨⡴⠋⠀⢰⣿⠁⢀⣿⣸⠁⢶⠧⠀⠘⢇⠀⠀⠘⢞⡄⠀⠀⠙⠧⣀⡂⠤⠂⠈⢿⣇⠀⠀⠀⠼⢿⠀⠀⠀⠀⠀⠀⢠⠘⠆⠀⠀⠀⠀⣼⡏⠀⠈⠢⢄⡤⠴⠋⠀⠀⡰⠸⡄⢳⣷⢇⡂⣯⠀⠀⢠⠃⠎⢀⠟⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⢻⡟⠉⣿⠋⠀⣿⠟⠉⠉⣽⡟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠀⠀⠀⣿⡏⠀⣼⢣⣿⡄⢸⡇⠀⠀⠈⠂⠀⠀⠀⠜⢄⡀⠀⠀⠀⠀⠀⠀⢀⡟⠯⡶⡶⢀⡶⠋⠀⠀⠀⠀⠀⠀⠀⠁⠀⢀⣄⡀⢰⡟⠳⡀⠀⠀⠀⠀⠀⠀⢀⠔⠣⠀⡌⡟⡆⢸⠇⠈⠁⡤⢸⡀⢠⠎⠀⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⡿⠁⠀⠀⠀⢰⡟⣀⣤⡾⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡟⢣⠜⠁⡾⠼⡆⠀⣷⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠉⠉⠁⠀⠚⠋⠀⠌⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠓⣞⣤⡀⠁⠉⠉⠉⠉⠀⠀⠀⠀⠀⠀⠀⣷⢸⡁⠈⠀⠀⢀⡇⠀⢡⢿⠁⠀⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠠⣶⡾⠿⠟⠂⠀⠀⠿⠿⠛⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠄⠊⠁⠀⡸⡷⢣⠺⣆⢸⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡰⠇⠘⡄⠀⠀⠀⢸⠀⢠⢿⢹⠀⠀⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡀⠀⠀⠀⠀⠀⠀⢀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⡵⠓⠁⠀⠈⠛⣷⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠐⠁⠀⠀⠁⠀⠀⢀⣇⣠⣟⡟⡜⡀⠀⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⣾⡆⢠⣷⡆⠀⣼⠇⣰⡇⢰⣷⠀⢀⣾⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠁⠀⠀⠀⠀⠀⠀⢹⡆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣼⠋⣿⢰⠇⢸⣱⡀⢤⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⢠⡾⣿⣇⣼⠏⢠⡿⢀⣿⢿⣧⣼⠇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⠂
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⣧⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣼⠇⠀⣿⣿⠀⠀⡏⠁⢸⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⡟⠁⢿⣿⠋⢀⣾⠁⣾⠃⠈⣿⡟⠀⣤⡦⠀⠀⠀⠀⠀⠀⠀⠀⢸⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢹⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢰⡟⠀⢰⣟⠇⠀⠈⠀⠀⡼⠗⠀⠀⠀⠀⠀⠀⠀⠈⠉⠀⠀⠈⠁⠀⠈⠃⠀⠉⠀⠀⠈⠁⠀⠉⠀⠀⠀⠀⠀⠀⠀⠀⢀⠞⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⣇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣿⠁⠀⡾⠊⠀⠀⠀⠀⠀⠹⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⠎⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢻⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣼⠇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠓⢄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⠋⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⣷⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠋⢦⡀⠀⢀⠄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣴⡟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠂⢄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣰⠃⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢻⡽⢆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠁⠀⠈⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⠞⣿⠇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠐⠢⢄⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⣠⣴⡾⠁⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⡎⢳⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⠞⠁⣼⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡀⠤⠀⠀⠀⠀⠀⠈⠉⠓⢾⠗⣀⠤⠤⠤⠄⠀⠀⠀⠀⠈⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣯⣳⠀⠹⣆⠀⠀⠀⠀⠀⠰⠦⠄⣀⣀⡀⠀⠀⠀⠀⠀⢀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⡀⠠⠴⠛⠁⠀⠀⠀⢀⡜⠁⠀⡰⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⢋⠖⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⢌⡆⠀⠈⢷⡀⠀⠀⠀⠀⠀⠀⠀⠀⠨⡙⢿⣿⣛⠛⠛⠛⠛⠛⠛⠻⣛⣩⢿⡋⠉⠀⠀⠀⠀⠀⠀⠀⢀⡴⠋⠀⢀⣴⠿⣿⠅⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⠗⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⡏⠳⣵⠀⠀⠀⠹⣦⠀⠀⠀⠀⠀⠀⠀⠀⠀⠑⠦⣤⣤⣭⣭⣭⣭⣭⢩⡭⠖⠃⠀⠀⠀⠀⠀⠀⠀⢀⡴⠋⠀⠀⠀⣲⠯⢸⡿⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠠⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⡇⠀⠈⠀⠀⠀⠀⠈⢳⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡴⠋⠀⠀⠀⠀⢰⡿⢌⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⡇⠀⠀⠀⠀⠀⠀⠀⠩⡿⣦⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⠎⠀⠀⠀⠀⠀⠀⢐⡺⢁⣿⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣼⣧⠀⢈⠢⡀⠀⠀⠀⠀⢘⣝⢿⣆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣾⠏⠀⠀⠀⠀⠀⠀⠒⠁⠀⢸⢹⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣤⣶⣿⣿⣿⣿⠀⠀⠑⢌⢲⣀⠀⠀⠀⠳⣅⡫⠳⣤⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣾⡽⠏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣠⣴⣾⣿⣿⣿⣿⣿⣿⣷⠀⠀⠀⢳⣍⠣⡀⠀⠀⠀⢻⡟⠆⠈⠹⠶⣤⣀⣀⣀⣀⡀⣀⢀⣀⣀⣠⣴⠿⣛⢝⡃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣶⣤⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣴⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣆⠀⠀⠈⢯⡫⡳⡀⠀⠀⠀⠻⣯⡀⠀⠀⠀⠀⠈⠉⠉⠙⠙⠋⠛⠙⢫⣍⡳⢎⠋⠀⠀⠀⣠⡴⠖⠀⠀⠀⠀⠀⢀⣿⣿⣿⣿⣿⣷⣤⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣠⣴⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣄⠀⠈⡟⣬⡑⠄⠀⠀⠀⠱⡷⣂⠤⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣜⣪⡍⠀⠀⠀⠀⡰⠏⠁⣀⠀⠀⠀⠀⠀⣸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣤⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣄⠸⡦⡋⡦⠀⠀⠀⠀⠈⢎⠙⠕⣓⠂⠤⢀⢠⠄⠀⠀⠜⠳⠋⠀⠀⠀⢀⡾⢋⡥⠴⣇⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣤⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⢀⣀⣤⣴⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣌⡢⡹⡄⠀⠀⠀⠀⠘⡖⠔⣒⡠⠄⡭⠃⠀⠀⠐⡺⠁⠀⠀⢀⡴⢿⡙⠃⣐⠒⠉⠁⢀⣠⣴⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣦⣄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⣀⣠⣴⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣧⣀⡀⠀⠀⠀⠻⠅⡒⠄⢹⡁⠀⠀⠀⢻⠀⠀⠀⢠⣾⣿⡋⢠⠑⢀⣃⣤⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣦⣄⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀"""

# Pasangan (gambar, ukuran huruf): ukuran dibuat agar gambar pas di kotak yang sama
arts = [(brailleArt, 3.9), (brailleArt2, 3.4)]


# Fungsi untuk membuat satu baris kotak tiket ASCII (rata kiri)
def row(text):
    return f"| {text:<{l - 2}} |"


# Fungsi untuk membuat judul di tengah kotak tiket ASCII
def title(text):
    return f"|{text:^{l}}|"


# Fungsi untuk membuat nomor tiket acak 5 digit
def tiketno():
    return str(random.randint(0, 99999)).zfill(5)


# Fungsi untuk menghitung jumlah stasiun yang dilewati
def calcDistance(data, start, end):
    distance = abs(end - start)
    if data.get("loop"):
        distance = min(distance, len(data["station"]) - distance)  # jalur melingkar: ambil arah yang lebih dekat
    return distance


# Fungsi untuk menghitung harga tiket
def calcPrice(distance, initPrice, nextPrice):
    price = 0
    for i in range(distance):
        if i < 2:  # 2 stasiun pertama
            price += initPrice
        else:
            price += nextPrice
    return price


# Fungsi untuk menulis harga beserta mata uangnya, contoh: Rp24,000
def money(data, price):
    return data.get("currency", "Rp") + f"{price:,}"


# Fungsi untuk membuat teks hijau dengan font monospace
def text(value, color=green, bold=False, fontSize=size):
    return ft.Text(value, font_family=mono, size=fontSize, color=color, no_wrap=True,
                   weight=ft.FontWeight.BOLD if bold else ft.FontWeight.NORMAL)


# Fungsi untuk membuat tombol (isi hijau atau garis tepi saja)
def button(label, onClick, filled=True):
    return ft.Container(
        content=text(label, black if filled else green, True),
        bgcolor=green if filled else black,
        border=None if filled else ft.Border.all(1, green),
        padding=ft.Padding(left=24, top=12, right=24, bottom=12),
        on_click=onClick,
    )


# Fungsi untuk membuat teks Jepang pada tiket JR
def jpText(value, size, bold=False, spacing=0):
    return ft.Text(value, font_family=jp, size=size, color=ink, no_wrap=True,
                   weight=ft.FontWeight.BOLD if bold else ft.FontWeight.NORMAL,
                   style=ft.TextStyle(letter_spacing=spacing, height=1.0))


# Fungsi untuk menaruh elemen pada posisi tertentu di dalam Stack
def place(control, left, top):
    control.left = left
    control.top = top
    return control


# Fungsi untuk membuat teks yang diputar 90 derajat (tanggal dan jam di sisi tiket)
def sideways(value, size, centreX, centreY, boxWidth):
    box = ft.Container(
        content=jpText(value, size),
        width=boxWidth, height=size * 1.3,
        alignment=ft.Alignment.CENTER,
        rotate=ft.Rotate(angle=quarterTurn, alignment=ft.Alignment.CENTER),
    )
    return place(box, centreX - boxWidth / 2, centreY - size * 0.65)


# Fungsi untuk membuat tiket JR bergaya Jepang
def makeJrTicket(fromStation, price, ticketNo, now):
    name = kanji.get(fromStation, fromStation)
    charSize = min(56, 140 / len(name))  # ukuran kanji menyesuaikan jumlah huruf
    stationBox = ft.Container(
        content=ft.Column([jpText(c, charSize, True) for c in name],
                          spacing=2, tight=True,
                          horizontal_alignment=ft.CrossAxisAlignment.CENTER),
        width=92, height=172,
        alignment=ft.Alignment.CENTER,
        border=ft.Border.all(2.5, ink),
    )
    romaji = ft.Row([
        ft.Container(jpText("JR", 10, True), border=ft.Border.all(1.2, ink),
                     padding=ft.Padding(left=2, top=1, right=2, bottom=1)),
        jpText(fromStation.upper(), 17, spacing=1),
    ], spacing=6, tight=True)
    fare = ft.Row([
        jpText(str(price), 78),
        ft.Column([jpText("円", 22), jpText("区", 22), jpText("間", 22)], spacing=0, tight=True),
    ], spacing=4, tight=True, vertical_alignment=ft.CrossAxisAlignment.CENTER)
    child = (price // 2) // 10 * 10  # harga anak: setengah harga, dibulatkan ke bawah per 10 yen
    childFare = ft.Row([jpText("小児", 20), jpText(str(child), 26), jpText("円", 20)],
                       spacing=2, tight=True, vertical_alignment=ft.CrossAxisAlignment.END)
    footer = ft.Row([jpText(str(price), 19), jpText("発売当日限り有効", 17), jpText("下車前途無効", 17)],
                    spacing=18, tight=True)
    date = f"{now.year}.-{now.month}.-{now.day}"  # tanggal hari ini
    clock = f"{ticketNo[-4:]} {now.hour:02}:{now.minute:02}"  # nomor tiket dan jam

    return ft.Container(
        width=640, height=336,
        border_radius=6,
        gradient=ft.LinearGradient(begin=ft.Alignment.TOP_LEFT, end=ft.Alignment.BOTTOM_RIGHT,
                                   colors=[paper, paperDark]),
        clip_behavior=ft.ClipBehavior.HARD_EDGE,
        content=ft.Stack([
            sideways(date, 34, 48, 160, 240),
            place(romaji, 112, 22),
            place(stationBox, 128, 62),
            place(jpText("▶", 44), 252, 120),
            place(jpText("山手線", 21, spacing=9), 330, 74),
            place(fare, 318, 98),
            place(childFare, 334, 206),
            place(footer, 96, 270),
            sideways(clock, 34, 596, 160, 260),
        ], clip_behavior=ft.ClipBehavior.NONE),
    )


# Fungsi utama yang menjalankan seluruh aplikasi
async def main(page: ft.Page):
    page.title = "Jakarta Train Ticket System"
    page.fonts = {"Mono": "fonts/DejaVuSansMono.ttf", "JP": "fonts/NotoSansJP-Ticket.otf",
                  "Braille": "fonts/DejaVuBraille.ttf"}
    page.bgcolor = black
    page.padding = 0
    page.window.maximized = True  # jendela langsung dibuat maksimal

    # Dictionary untuk menyimpan keadaan aplikasi (kereta terpilih, musik, animasi, dll.)
    state = {"train": "MRT", "audio": None, "music": None, "musicOn": True, "track": 0,
             "spinning": False, "trainPhase": "reset", "frame": 0,
             "trainAlive": False, "diskAlive": False, "puffAlive": False, "art": 0}

    # ---------- judul ----------
    titleWidth = max(len(x) for x in titleArt.splitlines())
    titleText = text(titleArt, fontSize=12)

    # Fungsi untuk mengecilkan judul agar muat di layar
    def fitTitle():
        width = page.width or 1200
        room = width - 2 * 230
        titleText.size = max(6, min(16, room / (titleWidth * charWidth)))

    # ---------- halaman form ----------
    # Kolom isian nama
    nameField = ft.TextField(
        width=420, text_style=ft.TextStyle(font_family=mono, size=size, color=green),
        border=ft.OutlineInputBorder(side=ft.BorderSide(color=green)), cursor_color=green,
        bgcolor=black, max_length=maxName, counter_style=ft.TextStyle(color=dimGreen),
    )

    # Fungsi untuk membuat dropdown pilihan stasiun
    def dropdown():
        return ft.Dropdown(
            width=420, menu_height=420, editable=False, enable_search=False,
            text_style=ft.TextStyle(font_family=mono, size=size, color=green),
            border=ft.OutlineInputBorder(side=ft.BorderSide(color=green)), color=green,
            bgcolor=black, fill_color=black, filled=True,
            menu_style=ft.MenuStyle(bgcolor=black),
        )

    # Dropdown stasiun asal dan tujuan
    initStation = dropdown()
    finalStation = dropdown()
    # Baris pilihan kereta, teks harga, teks error, dan teks tiket ASCII
    checkRow = ft.Row(spacing=24)
    priceText = text("")
    errorText = text("", red)
    ticketText = text("", fontSize=18)

    # Fungsi untuk membuat baris berisi label dan kolom isian
    def labelled(label, control):
        return ft.Row([ft.Container(text(label), width=110), control],
                      vertical_alignment=ft.CrossAxisAlignment.CENTER)

    # Fungsi untuk mengambil data kereta dan indeks stasiun yang dipilih (-1 jika belum dipilih)
    def selected():
        data = trains[state["train"]]
        station = data["station"]
        start = station.index(initStation.value) if initStation.value in station else -1
        end = station.index(finalStation.value) if finalStation.value in station else -1
        return data, station, start, end

    # Fungsi untuk memperbarui tulisan jumlah stasiun dan harga
    def updatePrice():
        data, station, start, end = selected()
        if start == -1 or end == -1 or start == end:
            priceText.value = ""
            return
        distance = calcDistance(data, start, end)
        price = calcPrice(distance, data["initPrice"], data["nextPrice"])
        priceText.value = f"{distance} stops  |  {money(data, price)}"

    # ---------- suara ----------
    # Fungsi untuk menjalankan perintah suara tanpa membuat program error
    async def safely(call):
        try:
            await call
        except Exception:
            pass

    # Fungsi untuk menghentikan pengumuman stasiun
    async def stopAudio():
        if state["audio"] is not None:
            await safely(state["audio"].release())
            state["audio"] = None
            await duckMusic(False)

    # Fungsi untuk mengecilkan/mengembalikan volume musik saat ada pengumuman
    async def duckMusic(down):
        if state["music"] is not None:
            state["music"].volume = 0.15 if down else 0.6
            state["music"].update()

    # Dijalankan saat pengumuman selesai, volume musik dikembalikan
    async def announceDone(e):
        if e.state == fta.AudioState.COMPLETED:
            await duckMusic(False)

    # Fungsi untuk memutar pengumuman stasiun (hanya kereta JR)
    async def announce(stationName):
        await stopAudio()
        if not trains[state["train"]].get("sound"):
            return
        audio = fta.Audio(src=f"sounds/{state['train']}/{stationName}.wav",
                          on_state_change=announceDone)
        state["audio"] = audio
        await duckMusic(True)
        await safely(audio.play())

    # Fungsi untuk pindah ke lagu berikutnya
    async def changeTrack():
        old = state["music"]
        state["music"] = None
        if old is not None:
            await safely(old.release())
        state["track"] = (state["track"] + 1) % len(playlist)
        trackName.value = playlist[state["track"]][0]
        page.update()
        if state["musicOn"]:
            await startMusic()

    # Dijalankan saat lagu habis, lalu pindah ke lagu berikutnya
    async def trackEnded(e):
        if e.state == fta.AudioState.COMPLETED:
            await changeTrack()

    # Fungsi untuk memulai atau melanjutkan musik
    async def startMusic():
        if state["music"] is None:
            name, src = playlist[state["track"]]
            state["music"] = fta.Audio(src=src, volume=0.6,
                                       release_mode=fta.ReleaseMode.STOP,
                                       on_state_change=trackEnded)
            trackName.value = name
            page.update()
            await safely(state["music"].play())
        else:
            await safely(state["music"].resume())

    # Fungsi untuk menjeda musik
    async def pauseMusic():
        if state["music"] is not None:
            await safely(state["music"].pause())

    # ---------- pilihan kereta ----------
    # Fungsi untuk menggambar pilihan kereta [x] / [ ]
    def drawChecks():
        checkRow.controls = []
        for train in trains:
            chosen = train == state["train"]
            mark = "[x] " if chosen else "[ ] "
            checkRow.controls.append(ft.Container(
                content=text(mark + train, green if chosen else dimGreen, chosen),
                on_click=makeClick(train),
            ))

    # Fungsi untuk membuat aksi klik untuk tiap kereta
    def makeClick(train):
        async def click(e):
            await pickTrain(train)
        return click

    # Fungsi untuk membuat daftar pilihan stasiun pada dropdown
    def makeOptions(train):
        options = []
        for s in trains[train]["station"]:
            options.append(ft.DropdownOption(
                key=s, text=s,
                style=ft.ButtonStyle(color=green, text_style=ft.TextStyle(font_family=mono, size=size)),
            ))
        return options

    # Fungsi yang dijalankan saat kereta dipilih
    async def pickTrain(train):
        state["train"] = train
        drawChecks()
        initStation.options = makeOptions(train)
        finalStation.options = makeOptions(train)
        initStation.value = None
        finalStation.value = None
        priceText.value = ""
        await stopAudio()
        page.update()
        kick()

    # Dijalankan saat stasiun asal dipilih
    def pickStart(e):
        updatePrice()
        page.update()

    # Dijalankan saat stasiun tujuan dipilih (pengumuman diputar untuk JR)
    async def pickDestination(e):
        updatePrice()
        page.update()
        if finalStation.value:
            await announce(finalStation.value)

    # Menghubungkan dropdown dengan fungsinya
    initStation.on_select = pickStart
    finalStation.on_select = pickDestination

    # ---------- halaman ----------
    # Fungsi tombol BUY TICKET: memeriksa isian lalu membuat tiket
    async def buyTicket(e):
        kick()
        name = (nameField.value or "").strip()[:maxName]  # nama dipotong maksimal 20 huruf
        data, station, start, end = selected()

        # Memeriksa isian sebelum membuat tiket
        if name == "":
            errorText.value = "Name cannot be empty"
        elif start == -1 or end == -1:
            errorText.value = "Please choose both stations, sir " + name
        elif start == end:
            errorText.value = "Departure and destination are the same"
        else:
            errorText.value = ""
            distance = calcDistance(data, start, end)
            price = calcPrice(distance, data["initPrice"], data["nextPrice"])
            ticketNo = tiketno()
            # Kereta JR memakai tiket gaya Jepang, kereta lain memakai kotak ASCII
            if state["train"] == "JR":
                now = ft.DatePicker().current_date  # tanggal dan jam hari ini dari Flet
                ticketHolder.content = ft.Column([
                    makeJrTicket(station[start], price, ticketNo, now),
                    text(f"{name}  |  {station[start]} -> {station[end]}  |  {distance} stops", fontSize=14),
                ], spacing=14, tight=True, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
            else:
                ticketText.value = "\n".join([
                    line,
                    title("TICKET"),
                    line,
                    row("Passenger : " + name),
                    row("Train     : " + state["train"]),
                    row("From      : " + station[start]),
                    row("To        : " + station[end]),
                    row("Stops     : " + str(distance)),
                    row("Price     : " + money(data, price)),
                    row("Ticket No : " + ticketNo),
                    line,
                    title("Have a safe trip, sir " + name + "!"),
                    line,
                ])
                ticketHolder.content = ticketText
            # Pindah ke halaman tiket, lalu putar pengumuman
            switcher.content = ticketPage
            page.update()
            await announce(station[end])
            return
        page.update()

    # Fungsi tombol NEW TICKET: mengosongkan form dan kembali ke halaman form
    async def newTicket(e):
        await stopAudio()
        nameField.value = ""
        initStation.value = None
        finalStation.value = None
        priceText.value = ""
        switcher.content = formPage
        page.update()

    # Halaman form pemesanan tiket
    formPage = ft.Container(
        key="form",
        width=560,
        content=ft.Column([
            labelled("Name", nameField),
            labelled("Train", checkRow),
            labelled("From", initStation),
            labelled("To", finalStation),
            ft.Container(priceText, padding=ft.Padding(left=110, top=4, right=0, bottom=4)),
            ft.Container(button("[ BUY TICKET ]", buyTicket),
                         padding=ft.Padding(left=110, top=4, right=0, bottom=0)),
            ft.Container(errorText, padding=ft.Padding(left=110, top=8, right=0, bottom=0)),
        ], spacing=10, tight=True),
    )

    # Tempat untuk menaruh tiket (ASCII atau JR)
    ticketHolder = ft.Container(content=ticketText)

    # Halaman tiket
    ticketPage = ft.Container(
        key="ticket",
        content=ft.Column([
            ticketHolder,
            ft.Container(height=10),
            button("[ NEW TICKET ]", newTicket, filled=False),
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, tight=True),
    )

    # Wadah yang isinya diganti antara halaman form dan halaman tiket
    switcher = ft.Container(content=formPage)

    # ---------- piringan berputar ----------
    # Piringan hitam yang diputar dengan animasi
    disk = ft.Container(
        content=ft.Text(diskArt, font_family=mono, size=8, color=green, no_wrap=True,
                        style=ft.TextStyle(height=1.204)),
        rotate=ft.Rotate(angle=0, alignment=ft.Alignment.CENTER),
        animate_rotation=ft.Animation(2000, ft.AnimationCurve.LINEAR),  # satu putaran memakan waktu 2 detik
    )
    # Tulisan lagu yang sedang diputar dan tombol pause
    nowPlaying = text("now playing", dimGreen, fontSize=11)
    trackName = text(playlist[0][0], green, True, fontSize=12)
    pauseLabel = text("[ pause ]", green, fontSize=11)

    # Fungsi tombol pause/play
    async def toggleMusic(e):
        state["musicOn"] = not state["musicOn"]
        if state["musicOn"]:
            pauseLabel.value = "[ pause ]"
            if not state["spinning"]:
                spinNext()
            await startMusic()
        else:
            pauseLabel.value = "[ play ]"
            await pauseMusic()
        page.update()

    # Fungsi tombol next
    async def skipTrack(e):
        await changeTrack()

    # Baris tombol pause dan next
    controls = ft.Row([
        ft.Container(pauseLabel, on_click=toggleMusic),
        ft.Container(text("[ next >> ]", green, fontSize=11), on_click=skipTrack),
    ], spacing=10, tight=True)

    # Kotak di kanan atas berisi piringan, judul lagu, dan tombol
    diskBox = ft.Container(
        content=ft.Column([
            ft.Container(disk, on_click=toggleMusic),
            ft.Container(height=4),
            nowPlaying,
            trackName,
            controls,
        ], spacing=4, tight=True, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
        top=24, right=32,
    )

    # Fungsi untuk memutar piringan satu putaran lagi (berhenti jika musik dijeda)
    def spinNext(e=None):
        if not state["musicOn"]:
            state["spinning"] = False
            return
        state["spinning"] = True
        angle = disk.rotate.angle + fullTurn
        disk.rotate = ft.Rotate(angle=angle, alignment=ft.Alignment.CENTER)
        disk.update()

    # Dijalankan setiap kali satu putaran selesai, lalu memutar lagi
    def diskEnded(e):
        state["diskAlive"] = True
        spinNext()

    disk.on_animation_end = diskEnded

    # ---------- kereta berjalan ----------
    # Ukuran huruf kereta, dua frame gambar kereta, dan lebar kereta dalam piksel
    trainSize = 10
    trainFrames = [makeTrain(0), makeTrain(1)]
    trainWidth = max(len(x) for x in trainFrames[0].splitlines()) * charWidth * trainSize
    trainText = text(trainFrames[0], fontSize=trainSize)
    # Kereta yang digeser dari kiri ke kanan
    movingTrain = ft.Container(
        content=trainText,
        offset=ft.Offset(-1.2, 0),
        animate_offset=ft.Animation(1, ft.AnimationCurve.LINEAR),
    )
    # Rel kereta
    rail = text("=" * 400, dimGreen, fontSize=trainSize)
    # Jalur kereta di bagian bawah layar
    trainLane = ft.Container(
        content=ft.Column([movingTrain, rail], spacing=0, tight=True),
        left=0, right=0, bottom=16, clip_behavior=ft.ClipBehavior.HARD_EDGE,
    )

    # Lama perjalanan kereta dari kiri ke kanan (detik)
    trainSeconds = 16

    # Fungsi untuk menggerakkan kereta: kembali ke kiri, lalu berjalan ke kanan
    def trainNext(e=None):
        if state["trainPhase"] == "travel":
            state["trainPhase"] = "reset"
            movingTrain.animate_offset = ft.Animation(1, ft.AnimationCurve.LINEAR)
            movingTrain.offset = ft.Offset(-1.2, 0)
        else:
            state["trainPhase"] = "travel"
            target = (page.width or 1400) / trainWidth + 0.2
            movingTrain.animate_offset = ft.Animation(trainSeconds * 1000, ft.AnimationCurve.LINEAR)
            movingTrain.offset = ft.Offset(target, 0)
        movingTrain.update()

    # Dijalankan saat gerakan kereta selesai, lalu memulai gerakan berikutnya
    def trainEnded(e):
        state["trainAlive"] = True
        trainNext()

    movingTrain.on_animation_end = trainEnded

    # Fungsi untuk mengganti frame asap dan roda
    def puffNext(e=None):
        state["frame"] = 1 - state["frame"]
        trainText.value = trainFrames[state["frame"]]
        puffTicker.opacity = state["frame"]
        trainText.update()
        puffTicker.update()

    # Dijalankan setiap 0,25 detik (saat animasi penghitung waktu selesai)
    def puffEnded(e):
        state["puffAlive"] = True
        puffNext()

    # Penghitung waktu tak terlihat (ukuran 1x1) sebagai pengganti sleep
    puffTicker = ft.Container(width=1, height=1, opacity=0,
                              animate_opacity=ft.Animation(250, ft.AnimationCurve.LINEAR),
                              on_animation_end=puffEnded, left=0, top=0)

    # Fungsi untuk memulai animasi yang belum berjalan
    def kick(e=None):
        if not state["trainAlive"]:
            trainNext()
        if not state["diskAlive"] and state["musicOn"]:
            spinNext()
        if not state["puffAlive"]:
            puffNext()

    # Animasi dimulai setelah elemen muncul di layar
    movingTrain.on_size_change = kick
    disk.on_size_change = kick

    # ---------- panel kredit ----------
    # Gambar braille di panel kiri
    artText = ft.Text(arts[0][0], font_family=brailleFont, size=arts[0][1], color=green,
                      no_wrap=True, style=ft.TextStyle(height=1.464))

    # Fungsi tombol [ > ]: mengganti gambar
    def nextArt(e):
        state["art"] = (state["art"] + 1) % len(arts)
        artText.value, artText.size = arts[state["art"]]
        artText.update()

    # Tombol [ > ] di pojok kiri bawah gambar
    artButton = ft.Container(
        content=text("[ > ]", green, True, fontSize=12),
        border=ft.Border.all(1, green), bgcolor=black,
        padding=ft.Padding(left=4, top=2, right=4, bottom=2),
        on_click=nextArt, left=0, bottom=0,
    )
    # Kotak gambar beserta tombolnya
    artBox = ft.Stack([
        ft.Container(artText, width=330, height=240, alignment=ft.Alignment.CENTER),
        artButton,
    ], width=330, height=240)

    # Panel kiri: gambar, 'Arranged By', dan daftar anggota
    creditBox = ft.Container(
        width=330,
        content=ft.Column([
            artBox,
            ft.Container(height=8),
            text("Arranged By :", green, True, fontSize=13),
            ft.Container(height=2),
        ] + [text(member, green, fontSize=11) for member in team],
            spacing=3, tight=True, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
        left=24, top=280,
    )

    # ---------- keyboard dan ukuran layar ----------
    # Fungsi untuk tombol keyboard: Esc keluar layar penuh, F11 / Ctrl+F layar penuh
    async def onKey(e):
        if e.key == "Escape":
            page.window.full_screen = False
            page.update()
        elif e.key == "F11" or (e.key == "F" and e.ctrl):
            page.window.full_screen = not page.window.full_screen
            page.update()

    # Dijalankan saat ukuran jendela berubah
    def onResize(e):
        fitTitle()
        page.update()
        kick()

    # Menghubungkan event keyboard dan ukuran layar
    page.on_keyboard_event = onKey
    page.on_resize = onResize

    # ---------- tata letak ----------
    # Kolom tengah: judul dan halaman (form/tiket)
    centre = ft.Container(
        content=ft.Column([
            ft.Container(titleText, padding=ft.Padding(left=0, top=40, right=0, bottom=30)),
            switcher,
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, tight=True),
        alignment=ft.Alignment.TOP_CENTER,
        left=0, right=0, top=0,
    )

    # Menyusun semua bagian (urutan dari belakang ke depan)
    page.add(ft.Stack([trainLane, puffTicker, centre, creditBox, diskBox], expand=True))

    # Persiapan awal: judul, kereta MRT, layar penuh, animasi, dan musik
    fitTitle()
    await pickTrain("MRT")
    await page.get_device_info()
    page.window.full_screen = True
    page.update()
    kick()
    page.run_task(startMusic)

# Menjalankan aplikasi (folder assets berisi font, musik, dan suara)
ft.run(main, assets_dir="assets")
