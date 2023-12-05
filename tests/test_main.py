from fastapi.testclient import TestClient
from mutual_fund_profit_calculator.main import app

client = TestClient(app)

def test_get_profit():
    response = client.get("/profit?scheme_code=101206&start_date=26-07-2023&end_date=18-10-2023&capital=1000000")
    assert response.status_code == 200
    assert "net_profit" in response.json()
