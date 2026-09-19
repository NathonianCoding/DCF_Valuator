from services.forecast import forecast
from services.data import financials
from services.assumptions import assumptions
from fastapi import *
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],
    allow_methods=["*"],
    allow_headers=["*"],
)
class AssumptionData(BaseModel):

    forecast_years:int
    revenue_growth:list[float] 
    risk_free_rate:float
    equity_risk_premium:float 
    terminal_growth_rate:float
    cost_of_debt:float

@app.post("/api/valuation")
async def calcStockValue(stock:str, assumed:AssumptionData): 
    print(assumed.forecast_years, assumed.revenue_growth, 
        assumed.risk_free_rate, assumed.equity_risk_premium, 
        assumed.terminal_growth_rate)
    try:
        fin = financials.Financials(stock)
    except:
        raise HTTPException(status_code = 404, detail = f"Failed to load data for {stock}")
    fin_report = fin.load() # stores dictionary of metrics for every year

    ebit_margin, da_portion, capex_portion, working_capital_portion = forecast.getMargins(fin_report.items())
    prev_year_data = list(fin_report.items())[0][1]

    fcff = forecast.getFutureFCFFs(assumed.forecast_years, assumed.revenue_growth, prev_year_data["Tax Rate For Calcs"], 
                                   prev_year_data["Total Revenue"], prev_year_data["Working Capital"], 
                                   ebit_margin, da_portion, capex_portion, working_capital_portion)

    wacc = forecast.getWACC(prev_year_data, assumed.risk_free_rate,fin.beta, 
                            assumed.equity_risk_premium, prev_year_data["Tax Rate For Calcs"], 
                            fin.share_price, fin.shares_outstanding, assumed.cost_of_debt)

    value = forecast.getInstrinsicValues(wacc, fcff, prev_year_data["Total Debt"], fin.shares_outstanding, assumed.terminal_growth_rate)["Value per stock"]
   
    if value == 'nan':
        raise HTTPException(status_code = 404, detail = f"Data Missing from scraper")
    return {"value":value, "price": fin.share_price}


@app.get("/api/stock_prices/{ticker}")
async def getStockPrices(ticker:str):
    try:
        fin = financials.Financials(ticker)
        return {"stock_prices": fin.stock_price_snapshot}
    except:
        raise HTTPException(status_code=404, detail=f"Failed to load data for {ticker}")





   
