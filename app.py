"""
Flask API for Digital Wellness Analyzer
"""

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from analyzer import WellnessAnalyzer
from llm_insights import LLMInsightGenerator

app = Flask(__name__, static_folder='.')
CORS(app)

# Core components
analyzer = WellnessAnalyzer()
llm_generator = LLMInsightGenerator()


@app.route('/')
def index():
    """Serve main HTML file."""
    return send_from_directory('.', 'index.html')


@app.route('/<path:path>')
def serve_static(path):
    """Serve static assets."""
    return send_from_directory('.', path)


@app.route('/analyze', methods=['POST'])
def analyze():
    """Analyze digital wellness data and return insights."""
    try:
        data = request.get_json()

        if not data:
            return jsonify({"error": "No data provided"}), 400

        analysis_result = analyzer.analyze(data)
        llm_insight = llm_generator.generate_insight(analysis_result, data)

        response = {
            **analysis_result,
            "llm_insight": llm_insight
        }

        return jsonify(response), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/health', methods=['GET'])
def health():
    """Health status endpoint."""
    return jsonify({"status": "healthy"}), 200


if __name__ == '__main__':
    print("Digital Wellness Analyzer API running at http://localhost:5000")
    app.run(debug=True, port=5000)
