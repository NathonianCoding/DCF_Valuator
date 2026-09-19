import { AfterViewInit, Component, signal, viewChild } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { StockData, DCF_failure, DCF_success } from './services/stock-data';
import {Assumptions, AssumptionValues} from './Assumptions/assumptions/assumptions';
import { FormsModule } from '@angular/forms';


export interface AssumptionsRecord{
  forecast_years:number;
  revenue_growth:Array<number>;
  risk_free_rate:number;
  equity_risk_premium:number; 
  terminal_growth_rate:number;
  cost_of_debt:number;

  
}



@Component({
  selector: 'app-root',
  standalone: true,
  imports: [RouterOutlet, Assumptions, FormsModule],
  templateUrl: './app.html',
  styleUrl: './app.css'
})

export class App{

 
  assumption= viewChild.required(Assumptions);

 

  protected readonly title = signal('client-side');
  dcf_result: DCF_success |DCF_failure | null = null;
  error_message: string | null = null;
  loading = false;

  
  constructor(private stockDataService:StockData){}
  onSearch(ticker:string){
    console.log("test");
    this.dcf_result = null;
    this.error_message = null;
    this.loading=true;
    if (ticker == null){return;}
    let assumptions:AssumptionValues = this.assumption().getValues();
   
 
    this.stockDataService.getDcfValuation(ticker, assumptions).subscribe({
      next: (result) => {
        this.dcf_result = result;
        this.loading = false;
      },
      error: (err: Error) => {
        this.error_message = err.message;
        this.loading = false;
      }
    });
    console.log(this.dcf_result, this.error_message);


  }
}