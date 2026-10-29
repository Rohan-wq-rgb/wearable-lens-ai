"""
Main Flask Application for WearableLens AI

Full-stack backend for device identification with AI integration and manual search fallback.
"""

import hashlib
import logging
import os
import re
import secrets
from datetime import datetime, timedelta
from io import BytesIO

import PIL.Image
from dotenv import load_dotenv
from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    session,
    flash,
    jsonify,
    send_from_directory,
    abort,
)
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage

from ai_service import create_provider, AnalysisResult, generate_manual_search_guidance
from ai_service.device_data import (
    search_devices,
    get_device_by_id,
    get_all_categories,
    get_all_manufacturers,
    get_price_range,
    get_comparison_data,
)

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", secrets.token_hex(32))

# Configuration from environment
DEBUG = os.getenv("FLASK_DEBUG", "False").lower() == "true"
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", 5000))
MAX_CONTENT_LENGTH = int(os.getenv("MAX_CONTENT_LENGTH", 10485760))  # 10MB

# AI Configuration
AI_PROVIDER = os.getenv("AI_PROVIDER", "")
AI_CONFIG = {
    "provider": AI_PROVIDER,
    "api_key": os.getenv(f"{AI_PROVIDER.upper()}_API_KEY", "") if AI_PROVIDER else "",
    "model": os.getenv(f"OPENAI_MODEL", "gpt-4-vision-preview"),
}

# Rate limiting
limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=[os.getenv("RATE_LIMIT_DEFAULT", "200 per day;50 per hour")],
)

app.config["rate_limit"] = os.getenv("RATE_LIMIT_DEFAULT", "200 per day;50 per hour")

# Register rate limiter
limiter.init_app(app)

# Upload configuration
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "webp"}
MAX_FILE_SIZE = MAX_CONTENT_LENGTH
UPLOAD_DIR = os.path.join(app.static_folder, "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Initialize AI provider
ai_provider = create_provider(AI_CONFIG)

# Logging configuration
logging.basicConfig(
    level=getattr(logging, os.getenv("LOG_LEVEL", "INFO")),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


def allowed_file(filename: str) -> bool:
    """Check if uploaded file has allowed extension."""
    if not filename:
        return False
    ext = filename.rsplit(".", 1)[-1].lower() if "." in filename else ""
    return ext in ALLOWED_EXTENSIONS


def validate_image_content(file_storage: FileStorage) -> dict:
    """Validate uploaded image content and return analysis."""
    validation = {
        "is_valid": True,
        "errors": [],
        "image_format": None,
        "image_size": None,
        "recommendations": [],
    }
    
    try:
        # Check file size
        file_storage.seek(0, 2)  # Seek to end
        file_size = file_storage.tell()
        file_storage.seek(0)  # Reset to beginning
        
        if file_size > MAX_FILE_SIZE:
            validation["is_valid"] = False
            validation["errors"].append(f"File too large: {file_size / 1024:.1f}MB. Maximum: {MAX_FILE_SIZE / 1024:.1f}MB")
        
        # Try to open and validate image
        try:
            image = PIL.Image.open(file_storage)
            validation["image_format"] = image.format
            validation["image_size"] = f"{image.width}x{image.height}"
            
            # Check reasonable dimensions for device identification
            min_dim = min(image.width, image.height)
            if min_dim < 100:
                validation["recommendations"].append(
                    "Image may be too small for reliable device identification. "
                    "Use a photo where the device is clearly visible."
                )
            
            if min_dim > 4000:
                validation["recommendations"].append(
                    "Very large image - consider resizing for faster processing."
                )
            
        except Exception as e:
            validation["is_valid"] = False
            validation["errors"].append(f"Invalid image file: {str(e)[:100]}")
    
    except Exception as e:
        validation["is_valid"] = False
        validation["errors"].append(f"Validation error: {str(e)[:100]}")
    
    return validation


def analyze_image_with_ai(image_bytes: bytes, filename: str) -> AnalysisResult:
    """Analyze image using configured AI provider or return manual search guidance."""
    if ai_provider:
        try:
            result = ai_provider.analyze_image(image_bytes, filename)
            # Log the analysis
            logger.info(
                f"AI analysis completed for {filename}: "
                f"success={result.success}, confidence={result.confidence:.2f}, "
                f"product={result.product_name}"
            )
            return result
        except Exception as e:
            logger.error(f"AI provider error: {e}")
    
    # Fallback to manual search guidance
    logger.info(f"Using manual search fallback for {filename}")
    
    # Extract visible features for manual search guidance
    try:
        features = {
            "placement": _extract_placement_feature(image_bytes),
            "shape": _extract_shape_feature(image_bytes),
            "color": _extract_color_feature(image_bytes),
            "branding": _extract_branding_feature(image_bytes),
        }
    except Exception:
        features = {}
    
    manual_guidance = generate_manual_search_guidance(features)
    
    # Return structured result indicating manual analysis needed
    return AnalysisResult(
        success=False,
        product_name="Manual search recommended",
        manufacturer="User investigation required",
        category="Wearable Device",
        confidence=0.0,
        possible_matches=[],
        facts={"analysis_method": "manual_search", "image_features": features},
        requires_verification=True,
        error_message=None,
        notes="AI provider unavailable - manual search guidance provided",
    )


def _extract_placement_feature(image_bytes: bytes) -> str:
    """Extract placement feature from image (basic heuristic)."""
    try:
        img = PIL.Image.open(BytesIO(image_bytes))
        # Simple heuristic based on image metadata or dominant features
        # In production, this would use more sophisticated analysis
        return "unknown placement"
    except Exception:
        return "unknown placement"


def _extract_shape_feature(image_bytes: bytes) -> str:
    """Extract shape feature from image."""
    try:
        img = PIL.Image.open(BytesIO(image_bytes))
        return "unknown shape"
    except Exception:
        return "unknown shape"


def _extract_color_feature(image_bytes: bytes) -> str:
    """Extract color feature from image."""
    try:
        img = PIL.Image.open(BytesIO(image_bytes))
        return "unknown color"
    except Exception:
        return "unknown color"


def _extract_branding_feature(image_bytes: bytes) -> str:
    """Extract branding/logo feature from image."""
    try:
        img = PIL.Image.open(BytesIO(image_bytes))
        return "no visible branding"
    except Exception:
        return "no visible branding"


@app.route("/")
def index():
    """Home page route."""
    return render_template("index.html")


@app.route("/identify", methods=["GET", "POST"])
@limiter.limit("10 per minute;30 per hour")
def identify():
    """Device identification page route."""
    if request.method == "POST":
        return _handle_identification_post()
    
    return render_template("identify.html")


def _handle_identification_post() -> dict:
    """Handle identification form submission."""
    # Check if file was uploaded
    if "device_image" not in request.files:
        flash("No file uploaded", "error")
        return redirect(request.url)
    
    file = request.files["device_image"]
    
    # Check if filename is empty
    if file.filename == "":
        flash("No file selected", "error")
        return redirect(request.url)
    
    # Validate file type
    if not allowed_file(file.filename):
        flash("Invalid file type. Please upload PNG, JPG, JPEG, or WEBP images.", "error")
        return redirect(request.url)
    
    # Validate content
    validation = validate_image_content(file)
    if not validation["is_valid"]:
        for error in validation["errors"]:
            flash(error, "error")
        return redirect(request.url)
    
    # Read and process image
    try:
        image_bytes = file.read()
        
        # Analyze with AI or fallback to manual guidance
        analysis_result = analyze_image_with_ai(image_bytes, file.filename)
        
        # Store result in session for display
        session["last_analysis"] = {
            "success": analysis_result.success,
            "product_name": analysis_result.product_name,
            "manufacturer": analysis_result.manufacturer,
            "category": analysis_result.category,
            "confidence": analysis_result.confidence,
            "confidence_label": analysis_result.get_confidence_label(),
            "possible_matches": analysis_result.possible_matches,
            "facts": analysis_result.facts,
            "requires_verification": analysis_result.requires_verification,
            "error_message": analysis_result.error_message,
            "timestamp": datetime.utcnow().isoformat(),
        }
        
        # If there are possible matches from AI, enrich with database info
        if analysis_result.possible_matches and analysis_result.success:
            enriched_matches = []
            for match in analysis_result.possible_matches[:3]:  # Top 3 matches
                device = get_device_by_id(match.get("id", "")) if isinstance(match.get("id"), str) else None
                if device:
                    enriched_matches.append({
                        **match,
                        "database_info": {
                            "verified": device.get("verified", False),
                            "approximate_price": device.get("approximate_price", "Not verified"),
                            "main_functions": device.get("main_functions", []),
                            "typical_users": device.get("typical_users", []),
                        }
                    })
                else:
                    enriched_matches.append(match)
            analysis_result.possible_matches = enriched_matches
        
        flash("Image analysis completed", "success")
        return jsonify({
            "success": True,
            "analysis": {
                "product_name": analysis_result.product_name,
                "manufacturer": analysis_result.manufacturer,
                "category": analysis_result.category,
                "confidence": analysis_result.confidence,
                "confidence_label": analysis_result.get_confidence_label(),
                "requires_verification": analysis_result.requires_verification,
                "possible_matches": analysis_result.possible_matches,
                "facts": analysis_result.facts,
            }
        })
        
    except Exception as e:
        logger.error(f"Identification error: {e}")
        flash(f"Analysis error: {str(e)[:200]}", "error")
        return jsonify({"success": False, "error": "Analysis failed"}), 500


@app.route("/explore")
def explore():
    """Explore wearable technology page."""
    categories = get_all_categories()
    manufacturers = get_all_manufacturers()
    price_range = get_price_range()
    
    return render_template(
        "explore.html",
        categories=categories,
        manufacturers=manufacturers,
        price_range=price_range,
    )


@app.route("/compare", methods=["GET", "POST"])
def compare():
    """Device comparison page."""
    if request.method == "POST":
        device_ids = request.form.getlist("device_ids")
        if not device_ids:
            flash("Please select at least one device to compare", "error")
            return redirect(request.url)
        
        comparison_data = get_comparison_data(device_ids)
        
        if len(comparison_data) < 2:
            flash("Please select at least 2 devices for comparison", "error")
            return redirect(request.url)
        
        return render_template(
            "compare.html",
            comparison_data=comparison_data,
            selected_devices=device_ids,
        )
    
    # GET request - show available devices
    categories = get_all_categories()
    return render_template("compare.html", categories=categories)


@app.route("/privacy")
def privacy():
    """Privacy and security page."""
    return render_template("privacy.html")


@app.route("/about")
def about():
    """About page."""
    return render_template("about.html")


@app.route("/api/health")
def health_check():
    """Health check endpoint."""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "ai_provider": AI_PROVIDER or "manual_search_only",
        "upload_limit_mb": MAX_CONTENT_LENGTH / 1024 / 1024,
    })


@app.route("/api/devices")
def api_devices():
    """API endpoint for device search."""
    query = request.args.get("q", "")
    devices = search_devices(query)
    return jsonify({
        "devices": [
            {
                "id": device["id"],
                "name": device["name"],
                "manufacturer": device["manufacturer"],
                "category": device["category"],
                "approximate_price": device.get("approximate_price", "Not verified"),
            }
            for device in devices
        ]
    })


@app.route("/api/device/<device_id>")
def api_device_detail(device_id):
    """API endpoint for detailed device information."""
    device = get_device_by_id(device_id)
    if device is None:
        abort(404, description="Device not found")
    
    return jsonify(device)


@app.route("/api/search-guidance", methods=["POST"])
def api_search_guidance():
    """API endpoint for manual search guidance."""
    if "device_image" not in request.files:
        return jsonify({"error": "No image uploaded"}), 400
    
    file = request.files["device_image"]
    if file.filename == "":
        return jsonify({"error": "No file selected"}), 400
    
    if not allowed_file(file.filename):
        return jsonify({"error": "Invalid file type"}), 400
    
    try:
        image_bytes = file.read()
        
        # Extract features for guidance
        features = {
            "placement": _extract_placement_feature(image_bytes),
            "shape": _extract_shape_feature(image_bytes),
            "color": _extract_color_feature(image_bytes),
            "branding": _extract_branding_feature(image_bytes),
        }
        
        guidance = generate_manual_search_guidance(features)
        
        return jsonify({
            "success": True,
            "guidance": guidance,
            "message": "Manual search guidance generated - verify findings with legitimate sources",
        })
        
    except Exception as e:
        logger.error(f"Search guidance error: {e}")
        return jsonify({"error": "Failed to generate guidance"}), 500


@app.errorhandler(404)
def not_found_error(error):
    """404 error handler."""
    return render_template("404.html", error=error), 404


@app.errorhandler(500)
def internal_error(error):
    """500 error handler."""
    return render_template("500.html", error=error), 500


# Cleanup - remove old uploads (run periodically or on startup)
def cleanup_old_uploads():
    """Remove uploads older than retention period."""
    retention_hours = int(os.getenv("UPLOAD_RETENTION_HOURS", 1))
    cutoff = datetime.utcnow() - timedelta(hours=retention_hours)
    
    if not os.path.exists(UPLOAD_DIR):
        return
    
    for filename in os.listdir(UPLOAD_DIR):
        filepath = os.path.join(UPLOAD_DIR, filename)
        try:
            file_mtime = datetime.fromtimestamp(os.path.getmtime(filepath))
            if file_mtime < cutoff:
                os.remove(filepath)
                logger.info(f"Removed old upload: {filename}")
        except Exception as e:
            logger.warning(f"Could not remove {filename}: {e}")


# Run cleanup on startup
with app.app_context():
    cleanup_old_uploads()


if __name__ == "__main__":
    app.run(host=HOST, port=PORT, debug=DEBUG)