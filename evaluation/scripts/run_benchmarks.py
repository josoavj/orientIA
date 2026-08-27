import json
import requests
import time
import os
from datetime import datetime

# Configuration
TEST_CASES_PATH = "../benchmarks/test_cases.json"
RESULTS_PATH = "../results/benchmark_report.json"
API_URL = "https://fastapifororientia.onrender.com/chat"  # URL réelle sur Render

def run_benchmarks():
    if not os.path.exists(TEST_CASES_PATH):
        print(f"Error: {TEST_CASES_PATH} not found.")
        return

    with open(TEST_CASES_PATH, "r", encoding="utf-8") as f:
        test_cases = json.load(f)

    results = []
    total_latency = 0
    passed_count = 0

    print(f"Lancement du benchmark ORIENT'IA sur API distante ({len(test_cases)} cas)...")

    for tc in test_cases:
        print(f"Running {tc['id']}...", end=" ", flush=True)
        
        start_time = time.time()
        status = "failed"
        answer = ""
        
        try:
            payload = {
                "message": tc.get("input", ""),
                "profil_candidat": tc.get("profile", None),
                "top_k": 5
            }
            
            response = requests.post(API_URL, json=payload, timeout=30)
            if response.status_code == 200:
                answer = response.json().get("answer", "")
            else:
                answer = f"API Error {response.status_code}: {response.text[:100]}"
                
            latency = int((time.time() - start_time) * 1000)
            total_latency += latency

            # Vérification intelligente
            expected = tc.get("expected_output_contains", [])
            if not expected and "expected_recommendation" in tc:
                expected = [tc["expected_recommendation"]]
            
            if answer and not answer.startswith("API Error"):
                matches = [word for word in expected if word.lower() in answer.lower()]
                # On valide si au moins UN mot-clé important est trouvé (plus réaliste pour du texte narratif)
                if len(matches) > 0:
                    status = "passed"
                    passed_count += 1
                else:
                    print(f"\n   [FAILED] Attendu: {expected} | Reçu: '{answer[:100]}...'")
            elif answer.startswith("API Error"):
                print(f"\n   [ERROR] {answer}")
            
            results.append({
                "id": tc["id"],
                "category": tc["category"],
                "input": tc.get("input", ""),
                "output": answer,
                "status": status,
                "latency_ms": latency
            })
            print(f"[{status.upper()}] ({latency}ms)")

        except Exception as e:
            print(f"[CONNECTION ERROR] {str(e)}")
            results.append({"id": tc["id"], "status": "error", "error": str(e)})

    # Rapport Final
    report = {
        "timestamp": datetime.now().isoformat(),
        "summary": {
            "total": len(test_cases),
            "passed": passed_count,
            "accuracy": round((passed_count / len(test_cases)) * 100, 2),
            "avg_latency_ms": round(total_latency / len(test_cases), 2)
        },
        "details": results
    }

    os.makedirs(os.path.dirname(RESULTS_PATH), exist_ok=True)
    with open(RESULTS_PATH, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)

    print(f"\nBenchmark terminé. Rapport généré dans {RESULTS_PATH}")
    print(f"Accuracy: {report['summary']['accuracy']}% | Latence Moyenne: {report['summary']['avg_latency_ms']}ms")

if __name__ == "__main__":
    run_benchmarks()
