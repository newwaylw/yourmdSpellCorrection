
from flask import Flask
from flask import request
from spell import SpellCorrection
import json

app = Flask(__name__)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def spell_correction(path):
  print("query=",path)
  candidate_list = spell.get_predictions(path,3)
  
  return json.dumps(candidate_list)

if __name__ == '__main__':
  spell = SpellCorrection('nhs_unigram.freq','symptom.vec')
  app.run(debug=True)
    
