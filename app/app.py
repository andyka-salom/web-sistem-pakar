from flask import Flask, render_template, request
from models import db, Trait, Personality, ExpertSystem  # Pastikan model diimport dengan benar
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        selected_traits = request.form.getlist('traits')
        if selected_traits:
            # Find the personality based on the selected traits
            result = get_personality(selected_traits)
            return render_template('index.html', traits=get_traits(), result=result)
    return render_template('index.html', traits=get_traits())

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

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
