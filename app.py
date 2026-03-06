import os, json
from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
from pathfinder import solve_route
from database import get_db, init_db
from dotenv import load_dotenv
from google import genai
from google.genai import types
from PIL import Image
import io

load_dotenv()
app = Flask(__name__)
CORS(app)

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

@app.route('/api/save', methods=['POST'])
def save_layout():
    data = request.json
    db = get_db()
    db.execute('INSERT INTO layouts (grid_data, start_pos, target_pos) VALUES (?, ?, ?)',
               (json.dumps(data['grid']), json.dumps(data['start']), json.dumps(data['targets'])))
    db.commit()
    return jsonify({"status": "saved"})

@app.route('/api/history')
def get_history():
    db = get_db()
    rows = db.execute('SELECT * FROM layouts ORDER BY created_at DESC LIMIT 8').fetchall()
    return jsonify([dict(row) for row in rows])

@app.route('/api/solve', methods=['POST'])
def solve():
    data = request.json
    return jsonify(solve_route(data['grid'], data['start'], data['targets']))

@app.route('/api/analyze-image', methods=['POST'])
def analyze_image():
    if 'image' not in request.files:
        return jsonify({"error": "No image provided"}), 400
    
    file = request.files['image']
    img = Image.open(io.BytesIO(file.read()))
    
    prompt = """
    You are a highly precise spatial mapping AI.
    Do not generate a full matrix. Instead, list the exact coordinates of items on this 21x21 grid.
    Rows are 0 to 20. Columns are A to U.
    Map columns to numbers: A=0, B=1, C=2, D=3, E=4, F=5, G=6, H=7, I=8, J=9, K=10, L=11, M=12, N=13, O=14, P=15, Q=16, R=17, S=18, T=19, U=20.

    1. Find ALL obstacles (shelves, boxes, debris, pallets, drums, forklifts). Return a list of their [row, col] coordinates.
    2. Find the Start position (blue square). Return its [row, col].
    3. Find all Targets (T1, T2, T3, T4 in yellow text). Return a list of their [row, col] coordinates.
    Be exhaustive and systematic. Scan row by row.
    """
    
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=[prompt, img],
        config=types.GenerateContentConfig(
            temperature=0.0,
            response_mime_type="application/json",
            response_schema={
                "type": "OBJECT",
                "properties": {
                    "obstacles": {
                        "type": "ARRAY",
                        "items": {
                            "type": "ARRAY",
                            "items": {"type": "INTEGER"}
                        }
                    },
                    "start": {
                        "type": "ARRAY",
                        "items": {"type": "INTEGER"}
                    },
                    "targets": {
                        "type": "ARRAY",
                        "items": {
                            "type": "ARRAY",
                            "items": {"type": "INTEGER"}
                        }
                    }
                },
                "required": ["obstacles", "start", "targets"]
            }
        )
    )
    
    data = json.loads(response.text)
    grid = [[0 for _ in range(21)] for _ in range(21)]
    
    for r, c in data.get('obstacles', []):
        if 0 <= r < 21 and 0 <= c < 21:
            grid[r][c] = 1
            
    return jsonify({
        "size": 21,
        "grid": grid,
        "start": data.get("start", [0, 0]),
        "targets": data.get("targets", [])
    })

@app.route('/api/config')
def config(): return jsonify({"url": os.getenv("SUPABASE_URL"), "key": os.getenv("SUPABASE_ANON_KEY")})

@app.route('/')
def index(): return render_template('index.html')

@app.route('/login')
def login(): return render_template('login.html')

if __name__ == '__main__':
    with app.app_context():
        if not os.path.exists('warehouse.sqlite'): init_db()
    app.run(debug=True, port=5000)