import io
import logging
import hashlib
from functools import lru_cache

import qrcode
from flask import Flask, jsonify, request, send_file, render_template

def create_app() -> Flask:
    app = Flask(__name__)
    app.config.update(
        QR_BOX_SIZE=10,
        QR_BORDER=4,
        QR_ERROR_CORRECTION=qrcode.constants.ERROR_CORRECT_H,
        QR_FILL_COLOR="black",
        QR_BACK_COLOR="white",
        MAX_INPUT_LENGTH=2048,
    )
    logging.basicConfig(level=logging.INFO, format="%(asctime)s  %(levelname)s  %(message)s")
    _register_routes(app)
    return app


@lru_cache(maxsize=128)
def _build_qr_png(data, box_size, border, error_correction, fill, back):
    qr = qrcode.QRCode(version=None, error_correction=error_correction, box_size=box_size, border=border)
    qr.add_data(data)
    qr.make(fit=True)
    image = qr.make_image(fill_color=fill, back_color=back)
    buf = io.BytesIO()
    image.save(buf, format="PNG")
    return buf.getvalue()


def _register_routes(app):

    @app.get("/")
    def home():
        return render_template("index.html")

    @app.post("/generate")
    def generate_qr():
        body = request.get_json(silent=True)
        if not body or not isinstance(body, dict):
            return jsonify(error="Request body must be JSON."), 400
        text = body.get("url", "").strip()
        if not text:
            return jsonify(error="Field 'url' is required and must not be empty."), 422
        max_len = app.config["MAX_INPUT_LENGTH"]
        if len(text) > max_len:
            return jsonify(error=f"Input exceeds the {max_len}-character limit."), 422
        try:
            png_bytes = _build_qr_png(
                data=text,
                box_size=app.config["QR_BOX_SIZE"],
                border=app.config["QR_BORDER"],
                error_correction=app.config["QR_ERROR_CORRECTION"],
                fill=app.config["QR_FILL_COLOR"],
                back=app.config["QR_BACK_COLOR"],
            )
        except Exception:
            logging.exception("QR generation failed for: %.80r", text)
            return jsonify(error="QR generation failed. Please try again."), 500

        etag = hashlib.md5(png_bytes).hexdigest()
        if request.headers.get("If-None-Match") == etag:
            return "", 304

        response = send_file(io.BytesIO(png_bytes), mimetype="image/png", max_age=3600)
        response.set_etag(etag)
        return response

    @app.errorhandler(404)
    def not_found(_): return jsonify(error="Not found."), 404

    @app.errorhandler(405)
    def method_not_allowed(_): return jsonify(error="Method not allowed."), 405


app = create_app()

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)