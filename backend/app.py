from flask import Flask, jsonify
from flask_cors import CORS

from routes.auth import auth_bp
from routes.resume import resume_bp


def create_app():

    app = Flask(__name__)

    CORS(app)

    app.register_blueprint(auth_bp)

    app.register_blueprint(resume_bp)

    @app.route("/")
    def home():

        return jsonify({
            "success": True,
            "message": "Resume Analyzer Backend Running"
        })

    @app.route("/health")
    def health():

        return jsonify({
            "status": "healthy"
        })

    return app


app = create_app()


if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )