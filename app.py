from flask import Flask, render_template, request
import requests
import json

app = Flask(__name__)

# Địa chỉ endpoint của Prompt Flow (sửa lại theo URL của bạn)
ENDPOINT_URL = "https://pdg-ml-endpoint.southeastasia.inference.ml.azure.com/score"

# API Key từ Azure Machine Learning Endpoint (đảm bảo bảo mật)
API_KEY = "Fc8MxW3MxVCDFYvWhfbflL4qfaeUO9sAbiQfbAcPYPtEreZnvtkBJQQJ99BCAAAAAAAAAAAAINFRAZML2LYk"

HEADERS = {
    "Content-Type": "application/json",
    "Accept": "application/json",
    "Authorization": "Bearer " + API_KEY
}

@app.route("/", methods=["GET", "POST"])
def index():
    answer = ""
    question = ""
    if request.method == "POST":
        question = request.form.get("question", "")
        # Tạo payload gửi tới endpoint Prompt Flow
        payload = {
            "question": question,
            "chat_history": []  # Nếu có lịch sử chat, cập nhật ở đây
        }
        try:
            response = requests.post(ENDPOINT_URL, json=payload, headers=HEADERS)
            if response.status_code == 200:
                result = response.json()
                answer = result.get("answer", "Không có kết quả trả về.")
            else:
                answer = f"Lỗi: {response.status_code} - {response.text}"
        except Exception as e:
            answer = f"Lỗi: {str(e)}"
    return render_template("index.html", question=question, answer=answer)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)