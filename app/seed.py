import logging
from sqlalchemy import create_engine, text
from config import Config

# Data untuk kepribadian
personalities = {
    "P01": "Sanguinis",
    "P02": "Melankolis",
    "P03": "Koleris",
    "P04": "Plegmatis"
}

# Data untuk ciri-ciri kepribadian
traits = {
    "C001": "Senang berbicara",
    "C002": "Emosian dan terbuka",
    "C003": "Suka menolong orang lain",
    "C004": "Tidak bisa dijadikan sebagai sandaran",
    "C005": "Mudah berubah mood",
    "C006": "Sedikit pelupa",
    "C007": "Sulit berkonsentrasi",
    "C008": "Kurang disiplin waktu",
    "C009": "Disiplin waktu",
    "C010": "Introvert, pemikir dan pesimis",
    "C011": "Teratur, rapi, terjadwal, tersusun sesuai pola",
    "C012": "Menyukai fakta-fakta",
    "C013": "Mendominasi pembicaraan",
    "C014": "Cendrung menganalisa, memikirkan dan mempertimbangkan",
    "C015": "Ingin selalu sempurna",
    "C016": "Segala sesuatu ingin teratur",
    "C017": "Suka mengatur",
    "C018": "Suka memerintah",
    "C019": "Tidak punya banyak teman",
    "C020": "Tidak mau kalah",
    "C021": "Senang dengan tantangan",
    "C022": "Suka petualangan",
    "C023": "Tegas, kuat, cepat dan tangkas",
    "C024": "Tidak ada istilah tidak mungkin",
    "C025": "Mau merugi agar masalah tidak berkepanjangan",
    "C026": "Kurang bersemangat",
    "C027": "Kurang teratur dan serba dingin",
    "C028": "Cendrung diam",
    "C029": "Kalem",
    "C030": "Pendengar yang baik",
    "C031": "Suka menunda dalam mengambil keputusan",
    "C032": "Sangat memerlukan perubahan"
}

# Data untuk keputusan sistem pakar
expert_system = {
    "P01": ["C001", "C002", "C003", "C004", "C005", "C006", "C007", "C008"],
    "P02": ["C009", "C010", "C011", "C012", "C013", "C014", "C015", "C016"],
    "P03": ["C017", "C018", "C019", "C020", "C021", "C022", "C023", "C024"],
    "P04": ["C025", "C026", "C027", "C028", "C029", "C030", "C031", "C032"]
}

penyakit_data = {
    "P01" : "Ablasi Retina",
    "P02" : "Konjungtivitis",
    "P03" : "Bintit",
    "P04" : "Blefaritis",
    "P05" : "Dakriosistitis",
    "P06" : "Dermatokalasis",
    "P07" : "Endoftalmitis",
    "P08" : "Entropion",
    "P09" : "Pengembara",
    "P10" : "Glaukoma",
    "P11" : "Iritasi",
    "P12" : "Katarak",
    "P13" : "Keratitis",
    "P14" : "Minus",
    "P15" : "Plus"
}

gejala_data = {
    "G01" : "Penglihatan kabur",
    "G02" : "Pengalaman floater",
    "G03" : "Fotopsia (sensasi kilatan cahaya",
    "G04" : "Mata memerah",
    "G05" : "Keluar kotoran",
    "G06" : "Kesulitan membuka kelopak mata",
    "G07" : "Mata yang menyakitkan",
    "G08" : "Mata terasa panas",
    "G09" : "Mata berair",
    "G10" : "Mata gatal",
    "G11" : "Kemerahan kecil pada kelopak mata dan nyeri",
    "G12" : "Kelopak mata terasa sakit dan nyeri",
    "G13" : "Fotofobia kepekaan terhadap cahaya)",
    "G14" : "Sakit mata",
    "G15" : "Kehilangan bulu mata",
    "G16" : "Bulu mata berkerak saat bangun tidur",
    "G17" : "Kelopak mata merah",
    "G18" : "Mata terasa tegang",
    "G19" : "Pengelupasan kulit di sekitar mata",
    "G20" : "Adanya selaput tipis di mata",
    "G21" : "Sudut mata gatal",
    "G22" : "Pembengkakan di kantong air mata",
    "G23" : "Sakit di kantong air mata",
    "G24" : "Demam",
    "G25" : "Lelah",
    "G26" : "Ketika kantong air mata ditekan, keluar seperti nanah",
    "G27" : "Kesulitan menjaga mata tetap terbuka",
    "G28" : "Bulu mata bagian atas menutupi pandangan",
    "G29" : "Mata menjadi tegang dan nyeri",
    "G30" : "Terlihat lelah dan mengantuk",
    "G31" : "Sakit kepala",
    "G32" : "Mata sering merintih",
    "G33" : "Ketika kantong air mata ditekan, keluar seperti nanah",
    "G34" : "Gangguan saraf mata",
    "G35" : "Pupil kecil",
    "G36" : "Sulit untuk melihat jarak dekat",
    "G37" : "Keterlibatan ganda di satu mata",
    "G38" : "Pembengkakan lensa",
    "G39" : "Perubahan warna putih pada bagian mata yang hitam",
    "G40" : "Lesi putih pada kornea",
    "G41" : "Cepat mengantuk",
    "G42" : "Penglihatan kabur saat melihat objek yang jauh",
    "G43" : "Mata bengkak",
    "G44" : "Kaku pada bola mata",
    "G45" : "Penglihatan kabur saat benda-benda di sekitar",
    "G46" : "Penglihatan tidak nyaman ketika difokuskan pada jarak tertentu dalam waktu yang lama",
    "G47" : "Kaku pada bola mata"
}

# Data untuk keputusan
keputusan_data = {
    "P01": ["G01", "G02", "G03"],
    "P02": ["G04", "G05", "G06", "G07", "G08", "G09", "G10", "G11"],
    "P03": ["G10", "G12", "G13", "G14"],
    "P04": ["G04", "G05", "G06", "G10", "G11", "G12", "G15", "G16", "G19"],
    "P05": ["G01", "G04", "G05", "G06", "G10", "G21", "G22", "G23", "G24", "G25", "G26"],
    "P06": ["G27", "G28", "G29", "G30"],
    "P07": ["G01", "G04", "G08", "G14", "G24", "G31", "G32"],
    "P08": ["G01", "G05", "G06", "G10", "G14", "G33"],
    "P09": ["G02", "G03"],
    "P10": ["G01", "G31", "G34"],
    "P11": ["G04", "G08", "G14", "G35", "G36"],
    "P12": ["G01", "G08", "G10", "G11", "G14", "G37", "G38", "G39"],
    "P13": ["G01", "G04", "G06", "G08", "G40"],
    "P14": ["G31", "G41", "G42", "G43", "G44", "G45"],
    "P15": ["G31", "G46", "G47"]
}


nilai_cf_data = [
    ("Ablasi Retina", "G01", 0.6),
    ("Ablasi Retina", "G02", 0.8),
    ("Ablasi Retina", "G03", 0.4),
    ("Konjungtivitis", "G04", 0.4),
    ("Konjungtivitis", "G05", 0.6),
    ("Konjungtivitis", "G06", 0.8),
    ("Konjungtivitis", "G07", 0.9),
    ("Konjungtivitis", "G08", 0.4),
    ("Konjungtivitis", "G09", 0.4),
    ("Konjungtivitis", "G10", 0.8),
    ("Konjungtivitis", "G11", 0.8),
    ("Bintit", "G10", 0.4),
    ("Bintit", "G12", 0.8),
    ("Bintit", "G13", 0.8),
    ("Bintit", "G14", 0.2),
    ("Blefaritis", "G04", 0.6),
    ("Blefaritis", "G06", 0.4),
    ("Blefaritis", "G10", 0.4),
    ("Blefaritis", "G11", 0.8),
    ("Blefaritis", "G12", 0.4),
    ("Blefaritis", "G15", 0.4),
    ("Blefaritis", "G16", 0.6),
    ("Blefaritis", "G19", 0.2),
    ("Dakriosistitis", "G04", 0.4),
    ("Dakriosistitis", "G05", 0.4),
    ("Dakriosistitis", "G06", 0.2),
    ("Dakriosistitis", "G10", 0.4),
    ("Dakriosistitis", "G01", 0.6),
    ("Dakriosistitis", "G21", 0.4),
    ("Dakriosistitis", "G22", 0.8),
    ("Dakriosistitis", "G23", 0.8),
    ("Dakriosistitis", "G24", 0.4),
    ("Dakriosistitis", "G26", 0.8),
    ("Dermatokalasis", "G27", 0.8),
    ("Dermatokalasis", "G28", 0.6),
    ("Dermatokalasis", "G29", 0.8),
    ("Dermatokalasis", "G30", 0.8),
    ("Endoftalmitis", "G01", 0.4),
    ("Endoftalmitis", "G04", 0.9),
    ("Endoftalmitis", "G08", 0.8),
    ("Endoftalmitis", "G24", 0.4),
    ("Endoftalmitis", "G14", 0.6),
    ("Endoftalmitis", "G32", 0.8),
    ("Endoftalmitis", "G31", 0.4),
    ("Entropion", "G01", 0.2),
    ("Entropion", "G05", 0.4),
    ("Entropion", "G06", 0.8),
    ("Entropion", "G10", 0.8),
    ("Entropion", "G14", 0.4),
    ("Entropion", "G33", 0.4),
    ("Pengembara", "G02", 0.8),
    ("Pengembara", "G03", 0.4),
    ("Glaukoma", "G01", 0.8),
    ("Glaukoma", "G31", 0.4),
    ("Glaukoma", "G34", 0.6),
    ("Iritasi", "G04", 0.9),
    ("Iritasi", "G08", 0.8),
    ("Iritasi", "G14", 0.4),
    ("Iritasi", "G35", 0.6),
    ("Iritasi", "G36", 0.6),
    ("Katarak", "G01", 0.9),
    ("Katarak", "G08", 0.8),
    ("Katarak", "G10", 0.8),
    ("Katarak", "G11", 0.2),
    ("Katarak", "G14", 0.4),
    ("Katarak", "G37", 0.8),
    ("Katarak", "G38", 0.2),
    ("Katarak", "G39", 0.8),
    ("Keratitis", "G01", 0.8),
    ("Keratitis", "G04", 0.6),
    ("Keratitis", "G06", 0.4),
    ("Keratitis", "G08", 0.6),
    ("Keratitis", "G40", 0.9),
    ("Minus", "G31", 0.4),
    ("Minus", "G41", 0.2),
    ("Minus", "G42", 0.8),
    ("Minus", "G43", 0.2),
    ("Minus", "G44", 0.9),
    ("Minus", "G45", 0.8),
    ("Plus", "G31", 0.2),
    ("Plus", "G46", 0.9),
    ("Plus", "G47", 0.6),
    ("Plus", "G48", 0.6),
]

logging.basicConfig(level=logging.INFO)
engine = create_engine(Config.SQLALCHEMY_DATABASE_URI)

with engine.connect() as connection:
    # Insert personalities
    logging.info("Inserting personalities...")
    for code, name in personalities.items():
        connection.execute(text("INSERT INTO personalities (code, name) VALUES (:code, :name)"), {"code": code, "name": name})
        logging.info(f"Inserted personality {code} - {name}")

    # Insert traits
    logging.info("Inserting traits...")
    for code, description in traits.items():
        connection.execute(text("INSERT INTO traits (code, description) VALUES (:code, :description)"), {"code": code, "description": description})
        logging.info(f"Inserted trait {code} - {description}")

    # Insert expert system data
    logging.info("Inserting expert system data...")
    for personality_code, trait_codes in expert_system.items():
        for trait_code in trait_codes:
            personality_id = connection.execute(text("SELECT id FROM personalities WHERE code=:code"), {"code": personality_code}).fetchone()[0]
            trait_id = connection.execute(text("SELECT id FROM traits WHERE code=:code"), {"code": trait_code}).fetchone()[0]
            connection.execute(text("INSERT INTO expert_system (personality_id, trait_id) VALUES (:personality_id, :trait_id)"), {"personality_id": personality_id, "trait_id": trait_id})
            logging.info(f"Linked personality {personality_code} with trait {trait_code}")

            logging.info("Inserting data for penyakit...")
        for kode, nama in penyakit_data.items():
            connection.execute(text("INSERT INTO penyakit (kode, nama) VALUES (:kode, :nama)"), {"kode": kode, "nama": nama})
            logging.info(f"Inserted data for penyakit: {kode} - {nama}")

        logging.info("Inserting data for gejala...")
        for kode, nama in gejala_data.items():
            connection.execute(text("INSERT INTO gejala (kode, nama) VALUES (:kode, :nama)"), {"kode": kode, "nama": nama})
            logging.info(f"Inserted data for gejala: {kode} - {nama}")

logging.info("Inserting data for keputusan...")
for kode_penyakit, kode_gejala_list in keputusan_data.items():
    for kode_gejala in kode_gejala_list:
        connection.execute(text("INSERT INTO keputusan (kode_penyakit, kode_gejala) VALUES (:kode_penyakit, :kode_gejala)"), {"kode_penyakit": kode_penyakit, "kode_gejala": kode_gejala})
        logging.info(f"Inserted data for keputusan: {kode_penyakit} - {kode_gejala}")

logging.info("Inserting data for nilai CF pada gejala...")
for nama_penyakit, kode_gejala, nilai_cf in nilai_cf_data:
    connection.execute(text("INSERT INTO nilai_cf_gejala (nama_penyakit, kode_gejala, nilai_cf) VALUES (:nama_penyakit, :kode_gejala, :nilai_cf)"), {"nama_penyakit": nama_penyakit, "kode_gejala": kode_gejala, "nilai_cf": nilai_cf})
    logging.info(f"Inserted data for nilai CF: {nama_penyakit} - {kode_gejala} - {nilai_cf}")

    connection.commit()
    logging.info("Data committed to the database.")