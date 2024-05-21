from flask import Flask, render_template, request
from models import db, Trait, Personality, ExpertSystem, Penyakit, Gejala, Keputusan  # Pastikan model diimport dengan benar
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

def get_gejala():
    return Gejala.query.all()

def get_personality(trait_codes):
    personalities = Personality.query.all()
    for personality in personalities:
        trait_ids = [trait.id for trait in Trait.query.filter(Trait.code.in_(trait_codes)).all()]
        expert_system_entries = ExpertSystem.query.filter_by(personality_id=personality.id).all()
        expert_system_trait_ids = [entry.trait_id for entry in expert_system_entries]
        
        if set(trait_ids) == set(expert_system_trait_ids):
            return personality.name
    return "Kepribadian tidak ditemukan"







@app.route('/penyakit', methods=['GET', 'POST'])
def penyakit():
    if request.method == 'POST':
        selected_gejala = request.form.getlist('gejala')
        if selected_gejala:
            # Find the disease based on the selected symptoms
            result = get_penyakit(selected_gejala)
            return render_template('penyakit.html', gejala=get_gejala(), result=result)
    return render_template('penyakit.html', gejala=get_gejala())



def get_penyakit(gejala_codes):
    penyakit_list = Penyakit.query.all()
    for penyakit in penyakit_list:
        gejala_ids = [gejala.id for gejala in Gejala.query.filter(Gejala.code.in_(gejala_codes)).all()]
        keputusan_entries = Keputusan.query.filter_by(penyakit_id=penyakit.id).all()
        keputusan_gejala_ids = [entry.gejala_id for entry in keputusan_entries]

        if set(gejala_ids) == set(keputusan_gejala_ids):
            return penyakit.nama
    return "Penyakit tidak ditemukan"

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
