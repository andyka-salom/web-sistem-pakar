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

    connection.commit()
    logging.info("Data committed to the database.")
