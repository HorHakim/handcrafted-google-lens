from pathlib import Path
from html import escape
from fastapi import FastAPI, File, UploadFile, HTTPException, Request
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from backend import ImageAgent

BASE_DIR = Path(__file__).parent
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 Mo
ALLOWED_TYPES = {"image/jpeg", "image/png", "image/webp", "image/gif"}

app = FastAPI(title="Handcrafted Google Lens")
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")

agent = ImageAgent()

CONFIDENCE_CLASS = {"haute": "confidence-high", "moyen": "confidence-medium", "basse": "confidence-low"}


def build_result_fragment(data: dict) -> str:
    obj = escape(str(data.get("object", "—")))
    description = escape(str(data.get("description", "—")))
    confidence_raw = str(data.get("confidence", "")).lower()
    confidence_label = escape(str(data.get("confidence", "—")))
    confidence_class = CONFIDENCE_CLASS.get(confidence_raw, "confidence-medium")

    return f"""
<div class="result-grid">
  <div class="result-row">
    <span class="result-label">Objet</span>
    <span class="result-value">{obj}</span>
  </div>
  <div class="result-row">
    <span class="result-label">Description</span>
    <span class="result-value result-description">{description}</span>
  </div>
  <div class="result-row">
    <span class="result-label">Confiance</span>
    <span class="confidence-badge {confidence_class}">{confidence_label}</span>
  </div>
</div>
"""


@app.exception_handler(HTTPException)
async def htmx_exception_handler(request: Request, exc: HTTPException):
    return HTMLResponse(
        content=f'<p class="result-error">Erreur {exc.status_code} : {exc.detail}</p>',
        status_code=exc.status_code,
    )


@app.get("/", response_class=FileResponse)
async def serve_frontend():
    return FileResponse(BASE_DIR / "static" / "index.html")


@app.post("/api/analyze", response_class=HTMLResponse)
async def analyze_image(file: UploadFile = File(...)):
    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(415, detail="Type de fichier non supporté. Veuillez envoyer une image.")

    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(415, detail=f"Format non supporté : {file.content_type}. Formats acceptés : JPEG, PNG, WEBP, GIF.")

    image_bytes = await file.read()
    if len(image_bytes) > MAX_FILE_SIZE:
        raise HTTPException(413, detail="Image trop volumineuse (maximum 10 Mo).")

    try:
        result = agent.ask_vision_model_bytes(image_bytes, media_type=file.content_type)
    except Exception as e:
        raise HTTPException(500, detail=f"Erreur du modèle : {str(e)}")

    return HTMLResponse(content=build_result_fragment(result))
