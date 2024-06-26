import logging
from sqlalchemy import create_engine, text
from config import Config

# Data penyakit
diseases = {
    "P01": {"name": "Ablasi Retina", "description": "Ablasi retina adalah kondisi di mana retina terlepas dari jaringan di sekitarnya yang menyediakan oksigen dan nutrisi."},
    "P02": {"name": "Konjungtivitis", "description": "Konjungtivitis adalah peradangan atau infeksi pada konjungtiva, lapisan tipis yang melapisi bagian putih mata dan bagian dalam kelopak mata."},
    "P03": {"name": "Bintit", "description": "Bintit adalah benjolan merah yang menyakitkan di dekat tepi kelopak mata yang biasanya disebabkan oleh infeksi bakteri."},
    "P04": {"name": "Blefaritis", "description": "Blefaritis adalah peradangan pada kelopak mata, sering kali melibatkan bagian di mana bulu mata tumbuh."},
    "P05": {"name": "Dakriosistitis", "description": "Dakriosistitis adalah infeksi pada kantung air mata (kantung lakrimalis), biasanya disebabkan oleh penyumbatan pada saluran air mata."},
    "P06": {"name": "Dermatokalasis", "description": "Dermatokalasis adalah kondisi di mana kulit kelopak mata menjadi berlebih dan kendur, sering kali disebabkan oleh penuaan."},
    "P07": {"name": "Endoftalmitis", "description": "Endoftalmitis adalah infeksi serius pada bagian dalam mata, biasanya akibat komplikasi dari operasi mata atau cedera mata."},
    "P08": {"name": "Entropion", "description": "Entropion adalah kondisi di mana kelopak mata melipat ke dalam sehingga bulu mata dan kulit menggosok permukaan mata."},
    "P09": {"name": "Pengembara", "description": "Pengembara adalah peradangan berat pada sklera, lapisan putih mata."},
    "P10": {"name": "Glaukoma", "description": "Glaukoma adalah sekelompok kondisi mata yang merusak saraf optik, seringkali karena tekanan tinggi dalam mata."},
    "P11": {"name": "Iritasi", "description": "Iritasi adalah peradangan pada iris, bagian berwarna mata."},
    "P12": {"name": "Katarak", "description": "Katarak adalah kekeruhan pada lensa mata yang menyebabkan penurunan penglihatan."},
    "P13": {"name": "Keratitis", "description": "Keratitis adalah peradangan pada kornea, lapisan depan mata."},
    "P14": {"name": "Minus", "description": "Minus atau miopia adalah kondisi di mana mata dapat melihat objek dekat dengan jelas tetapi sulit melihat objek yang jauh."},
    "P15": {"name": "Plus", "description": "Plus atau hipermetropia adalah kondisi di mana mata dapat melihat objek yang jauh dengan jelas tetapi sulit melihat objek yang dekat."}
}


# Data gejala
symptoms = {
    "G01": "Penglihatan kabur",
    "G02": "Pengalaman floater",
    "G03": "Fotopsia (sensasi kilatan cahaya)",
    "G04": "Mata memerah",
    "G05": "Keluar Kotoran",
    "G06": "Dapatkan sesuatu di mata seseorang",
    "G07": "Bangun lebih awal atau lama tutup mata",
    "G08": "Mata yang menyakitkan",
    "G09": "Mata Terasa Panas",
    "G10": "Mata Berair",
    "G11": "Mata Gatal",
    "G12": "Kemerahan kecil pada kelopak mata dan nyeri",
    "G13": "Kelopak mata terasa sakit dan nyeri",
    "G14": "Fotofobia (Kepekaan terhadap cahaya)",
    "G15": "Sakit mata",
    "G16": "Kehilangan bulu mata",
    "G17": "Bulu mata berkerak saat bangun tidur",
    "G18": "Kelopak Mata Merah",
    "G19": "Pengelupasan kulit di sekitar mata",
    "G20": "Adanya selaput tipis di mata",
    "G21": "Sudut Mata Gatal",
    "G22": "Pembengkakan di kantong air mata",
    "G23": "Sakit di kantong air mata",
    "G24": "Demam",
    "G25": "Lelah",
    "G26": "Ketika kantong air mata ditekan, itu akan keluar seperti nanah",
    "G27": "Kesulitan menjaga mata tetap terbuka",
    "G28": "Bulu mata bagian atas menutupi Pemandangan",
    "G29": "Mata menjadi tegang dan nyeri karena mengangkat kelopak mata",
    "G30": "Terlihat lelah dan mengantuk",
    "G31": "Sakit Kepala",
    "G32": "Mata bengkak",
    "G33": "Kerak kelopak mata",
    "G34": "Gangguan saraf mata Pupil kecil",
    "G35": "Pupil Kecil",
    "G36": "Sulit Untuk Melihat Jarak Dekat",
    "G37": "Keterlibatan ganda di satu mata (Ketika mata lainnya tertutup)",
    "G38": "Pembengkakan Lensa",
    "G39": "Mengalami perubahan warna yang lebih putih pada bagian mata yang hitam",
    "G40": "Terdapat lesi putih pada kornea",
    "G41": "Mata sering merintih",
    "G42": "Cepat mengantuk",
    "G43": "Penglihatan kabur saat melihat objek yang jauh",
    "G44": "Kaku pada bola mata",
    "G45": "Kaku pada bola mata",
    "G46": "Penglihantan kabur saat benda benda di sekitar",
    "G47": "Penglihatan tidak nyaman ketika pandangan difokuskan pada jarak tertentu dalam waktu yang lama",
}

# Data aturan
rules = {
    "P01": [("G01", 0.6), ("G02", 0.8), ("G03", 0.4)],
    "P02": [("G04", 0.4), ("G05", 0.6), ("G06", 0.8), ("G07", 0.9), ("G08", 0.4), ("G09", 0.4), ("G10", 0.8), ("G11", 0.8)],
    "P03": [("G10", 0.4), ("G12", 0.8), ("G13", 0.8), ("G14", 0.2)],
    "P04": [("G04", 0.6), ("G06", 0.4), ("G10", 0.4), ("G11", 0.8), ("G12", 0.4), ("G15", 0.4), ("G16", 0.6), ("G19", 0.2)],
    "P05": [("G04", 0.4), ("G05", 0.4), ("G06", 0.2), ("G10", 0.4), ("G01", 0.6), ("G21", 0.4), ("G22", 0.8), ("G23", 0.8), ("G24", 0.4), ("G26", 0.8)],
    "P06": [("G27", 0.8), ("G28", 0.6), ("G29", 0.8), ("G30", 0.8)],
    "P07": [("G01", 0.4), ("G04", 0.9), ("G08", 0.8), ("G14", 0.6), ("G24", 0.4), ("G31", 0.4), ("G32", 0.8)],
    "P08": [("G01", 0.2), ("G05", 0.4), ("G06", 0.8), ("G10", 0.8), ("G14", 0.4), ("G33", 0.4)],
    "P09": [("G02", 0.8), ("G03", 0.4)],
    "P10": [("G01", 0.8), ("G31", 0.4), ("G34", 0.6)],
    "P11": [("G04", 0.9), ("G08", 0.8), ("G14", 0.4), ("G35", 0.6), ("G36", 0.6)],
    "P12": [("G01", 0.9), ("G08", 0.8), ("G10", 0.8), ("G11", 0.2), ("G14", 0.4), ("G37", 0.8), ("G38", 0.2), ("G39", 0.8)],
    "P13": [("G01", 0.8), ("G04", 0.6), ("G06", 0.4), ("G08", 0.6), ("G40", 0.9)],
    "P14": [("G31", 0.4), ("G41", 0.2), ("G42", 0.8), ("G43", 0.2), ("G44", 0.9), ("G45", 0.8)],
    "P15": [("G31", 0.2), ("G46", 0.9), ("G47", 0.6)]
}

logging.basicConfig(level=logging.INFO)
engine = create_engine(Config.SQLALCHEMY_DATABASE_URI)

with engine.connect() as connection:
    logging.info("Inserting diseases...")
    for code, details in diseases.items():
        name = details["name"]
        description = details["description"]
        connection.execute(
            text("INSERT INTO penyakit (kode_penyakit, nama_penyakit, deskripsi) VALUES (:code, :name, :description)"),
            {"code": code, "name": name, "description": description}
        )
        logging.info(f"Inserted disease {code} - {name} - {description}")

    # Insert symptoms
    logging.info("Inserting symptoms...")
    for code, description in symptoms.items():
        connection.execute(text("INSERT INTO gejala (kode_gejala, nama_gejala) VALUES (:code, :description)"), {"code": code, "description": description})
        logging.info(f"Inserted symptom {code} - {description}")

    # Insert rules
    logging.info("Inserting rules...")
    for disease_code, symptom_data in rules.items():
        for symptom_code, cf_value in symptom_data:
            connection.execute(text("INSERT INTO aturan (kode_penyakit, kode_gejala, cf_value) VALUES (:disease_code, :symptom_code, :cf_value)"), {"disease_code": disease_code, "symptom_code": symptom_code, "cf_value": cf_value})
            logging.info(f"Linked disease {disease_code} with symptom {symptom_code} and CF {cf_value}")

    connection.commit()
    logging.info("Data committed to the database.")
