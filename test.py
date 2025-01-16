import anyio
from content.client import make_bot

app = make_bot(
    "5846865945:AAFdGzRy-1-KZXZOm1je_oR-LQTsCOCHfqI",
    "https://d4c80923-0f37-4f55-8d7f-fac8c1e4d5da.us-east-1.cloud.genez.io",
    "cockroachdb://tlc:8WEGrYP9tFN5AnLnyNH-WQ@spunky-werebat-8469.8nk.gcp-asia-southeast1.cockroachlabs.cloud:26257/defaultdb?sslmode=verify-full",
)

if __name__ == "__main__":
    anyio.run(app.online)
