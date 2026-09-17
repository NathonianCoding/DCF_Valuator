// assumptions.component.ts
import { Component, Input, Output, EventEmitter, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-assumptions',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './assumptions.html',
})

export class Assumptions implements OnInit {
  @Input() forecastYears = 5;
  @Input() risk_free_rate = 0.02;
  @Input() equity_risk_premium = 0.03;
  @Input() terminal_growth_rate = 0.03;
  @Input() cost_of_debt = 0.012
  @Output() assumptionsChange = new EventEmitter<number[]>();

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

  getValues() {
    return {
      forecastYears: this.forecastYears,
      revenueGrowth: this.revenue_growth,
      risk_free_rate: this.risk_free_rate,
      equity_risk_premium: this.equity_risk_premium,
      terminal_growth_rate: this.terminal_growth_rate,
      cost_of_debt: this.cost_of_debt,
    };}
}
