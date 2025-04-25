import requests
import time

def test_response_time(url, repeat=5):
    print(f"Testing response time for: {url}")
    
    for i in range(repeat):
        start = time.time()
        try:
            response = requests.get(url, timeout=10)
            elapsed = time.time() - start
            print(f"[{i+1}] Status: {response.status_code}, Response Time: {elapsed:.3f} seconds")
        except requests.exceptions.RequestException as e:
            print(f"[{i+1}] Request failed: {e}")

# 使用範例
if __name__ == "__main__":
    render_url = "https://voteweb.onrender.com/"
    pythonanywhere_url = "https://shanghuyunproductionside.pythonanywhere.com/login/?next=/"
    print("************ Render網站延遲測試 ************")
    test_response_time(render_url, repeat=5)
    print("************ Pythonanywhere網站延遲測試 ************")
    test_response_time(pythonanywhere_url, repeat=5)
