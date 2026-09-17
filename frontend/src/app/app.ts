import { Component, signal } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { StockData, DCF_failure, DCF_success } from './services/stock-data';


@Component({
  selector: 'app-root',
  imports: [RouterOutlet],
  templateUrl: './app.html',
  styleUrl: './app.css'
})

export class App {
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

    this.stockDataService.getDcfValuation(ticker).subscribe({
      next: (result) => {
        this.dcf_result = result;
        this.loading = false;
      },
      error: (err: Error) => {
        this.error_message = err.message;
        this.loading = false;
      }
    });
    console.log(this.dcf_result);


  }
}