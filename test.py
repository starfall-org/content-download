import asyncio
from client import make_bot

app = make_bot(
    "8003796122:AAEphkB5LNJ7vEqijXF2iAQa3BZf7T3_7ug",
    "https://d4c80923-0f37-4f55-8d7f-fac8c1e4d5da.us-east-1.cloud.genez.io",
    "cockroachdb://tlc:8WEGrYP9tFN5AnLnyNH-WQ@spunky-werebat-8469.8nk.gcp-asia-southeast1.cockroachlabs.cloud:26257/defaultdb?sslmode=verify-full",
)

if __name__ == "__main__":
    asyncio.run(app.online())
