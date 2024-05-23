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
        trait_ids = [trait.id for trait in Trait.query.filter(Trait.code.in_(trait_codes)).all()]
        expert_system_entries = ExpertSystem.query.filter_by(personality_id=personality.id).all()
        expert_system_trait_ids = [entry.trait_id for entry in expert_system_entries]
        
        if set(trait_ids) == set(expert_system_trait_ids):
            return personality.name
    return "Kepribadian tidak ditemukan"

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
    aturan_list = Aturan.query.all()

    for kode_gejala, confidence in selected_symptoms_with_confidence:
        for aturan in aturan_list:
            if aturan.kode_gejala == kode_gejala:
                if aturan.kode_penyakit not in penyakit_cf:
                    penyakit_cf[aturan.kode_penyakit] = 0
                cf_expert = aturan.cf_value
                cf_user = confidence
                combined_cf = cf_expert * cf_user
                penyakit_cf[aturan.kode_penyakit] = combine_cf(penyakit_cf[aturan.kode_penyakit], combined_cf)
    
    hasil_diagnosa = [
        {
            'nama_penyakit': Penyakit.query.get(kode_penyakit).nama_penyakit,
            'cf_value': penyakit_cf[kode_penyakit] * 100  
        }
        for kode_penyakit in penyakit_cf
    ]

    hasil_diagnosa.sort(key=lambda x: x['cf_value'], reverse=True)
    return hasil_diagnosa

def combine_cf(cf1, cf2):
    if cf1 == 0:
        return cf2
    return cf1 + cf2 * (1 - cf1)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
