from fastapi import FastAPI, HTTPException, Query
from .calculate import calculate_profit

app = FastAPI()

@app.get("/profit")
def get_profit(
    scheme_code: str = Query(..., title="Scheme Code"),
    start_date: str = Query(..., title="Start Date"),
    end_date: str = Query(..., title="End Date"),
    capital: float = Query(1000000.0, title="Capital")
):
    try:
        profit = calculate_profit(scheme_code, start_date, end_date, capital)
        return {"net_profit": profit}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
