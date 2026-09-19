
# computes and returns unleveraged free cash flow
def getFCFF(ebit, tax, depreciation_amortization, capital_expenditure, working_capital_change):
    return ebit*(1-tax)+depreciation_amortization-capital_expenditure-working_capital_change

# returns a list of predicted free cash flow for each future year
#assumes the company's margins stay constant over future years
def getFutureFCFFs(forecast_years, revenue_growth, tax, prev_total_rev, prev_working_capital, ebit_margin, da_portion, capex_portion, working_capital_portion):
    forecast = [0]*forecast_years

    for i in range(forecast_years):
        curr_total_rev = prev_total_rev*(1+revenue_growth[i])
        ebit = ebit_margin*curr_total_rev
        depreciation_amortization = da_portion*curr_total_rev
        capital_expenditure = capex_portion*curr_total_rev
        curr_working_capital = working_capital_portion*curr_total_rev
        working_capital_change = curr_working_capital-prev_working_capital
        forecast[i]=getFCFF(ebit, tax, depreciation_amortization, capital_expenditure, working_capital_change)
        prev_total_rev=curr_total_rev
        prev_working_capital = curr_working_capital
    return forecast

# returns the average ebit margin, depreciation and amortization portion, capital expenditure portion and working capital portion across financial report
#if financials is empty then
def getMargins(financials):
    if financials == {}:
        raise "No Financial Data Provided"
    total_rev=0
    total_ebit=0
    total_da=0
    total_capital_exp = 0
    total_working_capital = 0
    num_of_years=0
    for (_, value) in financials:
        num_of_years+=1
        total_rev+=value["Total Revenue"]
        total_ebit+=value["EBIT"]
        total_da+=value["Depreciation And Amortization"]
        total_capital_exp+=value["Capital Expenditure"]
        total_working_capital+=value["Working Capital"]
    
    return (total_ebit/total_rev, 
            total_da/total_rev,
            total_capital_exp/total_rev,
            total_working_capital/total_rev
            ) 

def getWACC(curr_finances, risk_free_rate, beta, equity_risk_premium, tax, price, shares, cost_of_debt):
    equity_cost = risk_free_rate+beta*equity_risk_premium
    debt_after_tax = curr_finances["Total Debt"] * (1-tax)

    market_cap = price * shares

    debt_weight = curr_finances["Total Debt"]/(market_cap+debt_after_tax)

    wacc = debt_weight*cost_of_debt*(1-tax) + (1-debt_weight)*equity_cost
 
    return wacc

# returns (enterprise value, total equity, value per stock) at year 0
# assumes terminal perpeuity growth rate is 2%
def getInstrinsicValues(wacc, FCFF_forecast, total_debt, shares_outstanding, perpetuity_growth_rate):
    
    years_forecast = len(FCFF_forecast)
    last_FCFF = FCFF_forecast[years_forecast-1]
    terminal =  last_FCFF *(1+ perpetuity_growth_rate)/(wacc-perpetuity_growth_rate)
    ev = sum([FCFF_forecast[i]/((1+wacc)**(i+1)) for i in range(years_forecast-1)]) + (FCFF_forecast[years_forecast-1]+terminal)/(1+wacc)**years_forecast
    return {"Value per stock":f"{((ev-total_debt)/shares_outstanding).item():.2f}"}

    