from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from models import db, Trait, Personality, ExpertSystem, Penyakit, Gejala, Aturan
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

@app.route('/')
def landing_page():
    return render_template('index.html')

@app.route('/personality', methods=['GET', 'POST'])
def personality():
    if request.method == 'POST':
        selected_traits = request.form.getlist('traits')
        if selected_traits:
            # Find the personality based on the selected traits
            result = get_personality(selected_traits)
            return render_template('personality.html', traits=get_traits(), result=result)
    return render_template('personality.html', traits=get_traits())

def get_traits():
    return Trait.query.all()

def get_personality(trait_codes):
    personalities = Personality.query.all()
    for personality in personalities:
        # Kueri untuk mendapatkan semua Trait yang kodenya ada dalam trait_codes
        trait_ids = [trait.id for trait in Trait.query.filter(Trait.code.in_(trait_codes)).all()]
        # Mengambil semua entri dari tabel ExpertSystem yang personality_id-nya sama dengan id dari personality saat ini
        expert_system_entries = ExpertSystem.query.filter_by(personality_id=personality.id).all()
        # Mengumpulkan trait_id dari setiap entri ExpertSystem yang ditemukan dalam daftar expert_system_trait_idss 
        expert_system_trait_ids = [entry.trait_id for entry in expert_system_entries]
        
        if set(trait_ids) == set(expert_system_trait_ids):
            return get_personality_details(personality.name)
    return {"name": "Kepribadian tidak ditemukan", "characteristics": "", "positive_traits": "", "negative_traits": ""}

def get_personality_details(personality_name):
    personalities_details = {
        "Sanguinis": {
            "characteristics": "Ekstrovert, optimis, sosial, dan penuh energi.",
            "positive_traits": "Sanguinis sangat ramah, antusias, dan mudah bergaul. Mereka cenderung humoris, mudah beradaptasi, dan suka menjadi pusat perhatian.",
            "negative_traits": "Bisa kurang fokus, tidak teratur, dan seringkali terlalu berbicara atau berlebihan dalam bersosialisasi."
        },
        "Melankolis": {
            "characteristics": "Introvert, analitis, detail-oriented, dan perfeksionis.",
            "positive_traits": "Melankolis sangat teliti, teratur, dan setia. Mereka memiliki pemikiran mendalam dan seringkali kreatif dalam bidang seni atau intelektual.",
            "negative_traits": "Cenderung mudah cemas, pesimis, dan sering terlalu kritis baik terhadap diri sendiri maupun orang lain."
        },
        "Koleris": {
            "characteristics": "Ekstrovert, dominan, tegas, dan berorientasi pada tujuan.",
            "positive_traits": "Koleris sangat mandiri, ambisius, dan efektif dalam memimpin. Mereka fokus pada pencapaian tujuan dan seringkali menjadi motivator yang baik.",
            "negative_traits": "Bisa terlalu keras kepala, kurang peka terhadap perasaan orang lain, dan cenderung memaksakan kehendak."
        },
        "Plegmatis": {
            "characteristics": "Introvert, tenang, damai, dan mudah beradaptasi.",
            "positive_traits": "Plegmatis sangat sabar, mudah bekerja sama, dan stabil secara emosional. Mereka cenderung setia dan bisa diandalkan dalam situasi apapun.",
            "negative_traits": "Cenderung pasif, kurang bersemangat, dan bisa menghindari konfrontasi sehingga terlihat kurang tegas."
        }
    }
    return {
        "name": personality_name,
        **personalities_details.get(personality_name, {})
    }

@app.route('/diagnose', methods=['GET', 'POST'])
def diagnose():
    if request.method == 'POST':
        selected_symptoms = request.form.getlist('gejala')
        confidence_levels = request.form.getlist('confidence')

        if not selected_symptoms or not confidence_levels:
            return jsonify(error="Silakan pilih setidaknya satu gejala dan tingkat kepercayaannya."), 400

        selected_symptoms_with_confidence = list(zip(selected_symptoms, map(float, confidence_levels)))

        hasil_diagnosa = calculate_cf(selected_symptoms_with_confidence)
        return jsonify(hasil_diagnosa)
    
    gejala_list = Gejala.query.all()
    return render_template('penyakit.html', gejala_list=gejala_list)

def calculate_cf(selected_symptoms_with_confidence):
    penyakit_cf = {}
    penyakit_gejala_count = {}

    aturan_list = Aturan.query.all()

    for kode_gejala, confidence in selected_symptoms_with_confidence:
        for aturan in aturan_list:
            if aturan.kode_gejala == kode_gejala:
                if aturan.kode_penyakit not in penyakit_cf:
                    penyakit_cf[aturan.kode_penyakit] = []
                    penyakit_gejala_count[aturan.kode_penyakit] = 0

                cf_expert = aturan.cf_value
                cf_user = confidence
                combined_cf = cf_expert + cf_user * (1 - cf_expert)
                penyakit_cf[aturan.kode_penyakit].append(combined_cf)

                # Increment gejala count
                penyakit_gejala_count[aturan.kode_penyakit] += 1
    
    final_penyakit_cf = {}
    for kode_penyakit, cf_values in penyakit_cf.items():
        if penyakit_gejala_count[kode_penyakit] >= 2:  # Only consider diseases with at least 2 symptoms
            final_cf = cf_values[0]
            for cf in cf_values[1:]:
                final_cf = combine_cf(final_cf, cf)
            final_penyakit_cf[kode_penyakit] = final_cf

    hasil_diagnosa = [
        {
            'nama_penyakit': Penyakit.query.get(kode_penyakit).nama_penyakit,
            'deskripsi': Penyakit.query.get(kode_penyakit).deskripsi,
            'cf_value': final_penyakit_cf[kode_penyakit] * 100
        }
        for kode_penyakit in final_penyakit_cf
    ]

    # Sort the results by cf_value in descending order
    hasil_diagnosa.sort(key=lambda x: x['cf_value'], reverse=True)

    # Limit to top 3 results if there are more than 3
    if len(hasil_diagnosa) > 3:
        hasil_diagnosa = hasil_diagnosa[:3]

    return hasil_diagnosa

def combine_cf(cf1, cf2):
    combined_cf = cf1 + cf2 * (1 - cf1)
    return combined_cf if combined_cf <= 1 else 1


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
