from flask import Blueprint, request, jsonify, current_app
from flask import send_file, current_app
from app.services.face_service import FaceService
from app.services.storage_service import StorageService
import os

face_bp = Blueprint("face", __name__)
face_service = FaceService(face_dir="faces")

@face_bp.route("/upload", methods=["POST"])
def upload():
    img_data = request.data

    save_dir = "received_images"
    os.makedirs(save_dir, exist_ok=True)
    img_path = os.path.join(save_dir, "last_upload.jpg")
    with open(img_path, "wb") as f:
        f.write(img_data)

    result = face_service.recognize_face(img_data)

    return jsonify(result)

@face_bp.route("/register", methods=["POST"])
def register():
    name = request.args.get("name")
    if not name:
        return jsonify({"status": "error", "reason": "missing_name"}), 400
    
    face_dir = current_app.config.get("FACE_DIR", "faces")
    storage_service = StorageService(face_dir)
    
    img_data = request.data
    storage_service.save_image(name, img_data)
    face_service.reload_faces()
    return jsonify({"status": "registered", "name": name})

from flask import send_file

@face_bp.route("/view", methods=["GET"])
def view_image():
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    image_path = os.path.join(base_dir, 'received_images', 'last_upload.jpg')

    if not os.path.exists(image_path):
        return "Nenhuma imagem recebida ainda.", 404

    try:
        return send_file(image_path, mimetype="image/jpeg")
    except Exception as e:
        print(f"❌ Erro ao enviar imagem: {e}")
        return "Erro interno ao carregar a imagem.", 500