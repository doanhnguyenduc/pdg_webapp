from flask import Flask, render_template, request
import requests
import os

app = Flask(__name__)

# Lấy API key và endpoint từ biến môi trường
API_KEY = os.getenv("API_KEY", "")
ENDPOINT_URL = os.getenv("ENDPOINT_URL", "")

# Kiểm tra xem các biến có được đặt hay không
if not API_KEY or not ENDPOINT_URL:
    raise ValueError("Vui lòng đặt biến môi trường API_KEY và ENDPOINT_URL.")

# Headers cho request
HEADERS = {
    "Content-Type": "application/json",
    "Accept": "application/json",
    "Authorization": f"Bearer {API_KEY}",
}

@app.route("/", methods=["GET", "POST"])
def index():
    answer = ""
    question = ""

    if request.method == "POST":
        question = request.form.get("question", "").strip()
        
        if not question:
            answer = "Vui lòng nhập câu hỏi."
        else:
            payload = {
                "question": question,
                "chat_history": []  # Nếu có lịch sử chat, cập nhật ở đây
            }

            try:
                response = requests.post(ENDPOINT_URL, json=payload, headers=HEADERS, timeout=10)
                response.raise_for_status()  # Tự động phát sinh lỗi nếu HTTP status >= 400
                result = response.json()
                answer = result.get("answer", "Không có kết quả trả về.")
            except requests.exceptions.RequestException as e:
                answer = f"Lỗi kết nối đến API: {str(e)}"
            except ValueError:
                answer = "Lỗi xử lý dữ liệu JSON từ API."

    return render_template("index.html", question=question, answer=answer)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)