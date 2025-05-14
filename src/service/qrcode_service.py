import qrcode
import base64
from io import BytesIO

def generate_qr_code(data: str) -> str:
    qr = qrcode.make(data)
    buffered = BytesIO()
    qr.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()
