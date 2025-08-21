# generate_qr.py
import qrcode
from qrcode.constants import ERROR_CORRECT_H

URL = "https://geowise-agent-834ayjzfuzvdvinmifsg4k.streamlit.app/?embed=true"

qr = qrcode.QRCode(error_correction=ERROR_CORRECT_H, box_size=10, border=8)
qr.add_data(URL)
qr.make(fit=True)

img = qr.make_image(fill_color="black", back_color="white")  # <- solid white, no transparency
img = img.convert("RGB")
img.save("qrCode_geowise.png")            # ideally 300–600px per side
print("Saved qr_geowise.png")
