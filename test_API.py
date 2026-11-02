import requests
import json

BASE_URL = "http://127.0.0.1:8000"

def print_response(title, response):
    print(f"=== {title} (HTTP {response.status_code}) ===")
    print(json.dumps(response.json(), indent=2))
    print()

if __name__ == "__main__":
    # 1. Test GET /
    print_response("GET / (Introduction)", requests.get(f"{BASE_URL}/"))

    # 2. Test GET /health
    print_response("GET /health (Health Check)", requests.get(f"{BASE_URL}/health"))

    # 3. Test POST /predict - Input 1 (Positive financial news)
    res_pos = requests.post(
        f"{BASE_URL}/predict",
        json={"text": "Stocks rallied and the British pound gained after strong quarterly earnings."}
    )
    print_response("POST /predict (Input 1 - Positive)", res_pos)

    # 4. Test POST /predict - Input 2 (Negative financial news)
    res_neg = requests.post(
        f"{BASE_URL}/predict",
        json={"text": "Operating profit fell 25% due to rising supply chain costs and weak demand."}
    )
    print_response("POST /predict (Input 2 - Negative)", res_neg)

    # 5. Test POST /predict - Input 3 (Neutral financial statement)
    res_neu = requests.post(
        f"{BASE_URL}/predict",
        json={"text": "The company scheduled its annual shareholder meeting for next Tuesday."}
    )
    print_response("POST /predict (Input 3 - Neutral)", res_neu)

    # 6. Test Error Handling (Empty string validation)
    res_err = requests.post(
        f"{BASE_URL}/predict",
        json={"text": "   "}
    )
    print_response("POST /predict (Validation Error)", res_err)