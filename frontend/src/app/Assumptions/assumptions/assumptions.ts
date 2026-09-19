// assumptions.component.ts
import { Component, Input, Output, EventEmitter, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { AssumptionsRecord } from '../../app';


export class AssumptionValues implements AssumptionsRecord{
  forecast_years:number;
  revenue_growth:Array<number>;
  risk_free_rate:number;
  equity_risk_premium:number; 
  terminal_growth_rate:number;
  cost_of_debt:number;

  constructor(forecast_years:number,
  revenue_growth:Array<number>,
  risk_free_rate:number,
  equity_risk_premium:number, 
  terminal_growth_rate:number,
  cost_of_debt:number){
    this.forecast_years = forecast_years;
    this.revenue_growth = revenue_growth;
    this.risk_free_rate = risk_free_rate;
    this.equity_risk_premium = equity_risk_premium;
    this.terminal_growth_rate = terminal_growth_rate;
    this.cost_of_debt = cost_of_debt;

  }
  
}

@Component({
  selector: 'app-assumptions',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './assumptions.html',
})

export class Assumptions implements OnInit {
  forecastYears = 5;
  risk_free_rate = 0.02;
  equity_risk_premium = 0.03;
  terminal_growth_rate = 0.03;
  cost_of_debt = 0.012
  // @Output() assumptionsChange = new EventEmitter<number[]>();
  revenue_growth: number[] = [];
  ngOnInit() {
    this.revenue_growth = Array(this.forecastYears).fill(0.1);
  }


  get yearIndices(): number[] {
    return Array.from({length: this.forecastYears}, (_, i) => i);

  }

  
  onForecastYearsChange(){
    let num_of_years = this.revenue_growth.length
    if (this.forecastYears>num_of_years){
      for (let i=0; i<this.forecastYears; i++){
        this.revenue_growth.push(0.1);
      }
    }
    else{
      this.revenue_growth = this.revenue_growth.slice(0, num_of_years)
    }

  }

  public getValues() {
    return new AssumptionValues(this.forecastYears,this.revenue_growth, this.risk_free_rate,
    this.equity_risk_premium, this.terminal_growth_rate, this.cost_of_debt,
    );
  }
}
