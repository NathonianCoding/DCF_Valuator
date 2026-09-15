class DCFAssumptions:
    def __init__(self, forecast_years:int, revenue_growth:list, risk_free_rate:float, equity_risk_premium:float, terminal_growth_rate:float, cost_of_debt:float):
        self.forecast_years = forecast_years 
        self.revenue_growth = revenue_growth #list of floats
       

        self.risk_free_rate = risk_free_rate
        self.equity_risk_premium = equity_risk_premium
        self.terminal_growth_rate = terminal_growth_rate
        self.cost_of_debt= cost_of_debt
     
