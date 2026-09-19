import { HttpClient, HttpErrorResponse } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable, catchError, throwError } from 'rxjs';
import { AssumptionValues } from '../Assumptions/assumptions/assumptions';
export interface DCF_success{
  value: string;
  stock_snapshot: Record<string, string>;
}
export interface DCF_failure{
  details: string;
}



@Injectable({providedIn: 'root',})
export class StockData {
  private url = "http://localhost:8000/api/valuation"

  constructor(private http: HttpClient){}
  

  getDcfValuation(ticker: string, assumptions:AssumptionValues): Observable<DCF_success|DCF_failure> {

    console.log("Assumptions");
    console.log(assumptions);
    return this.http.post<DCF_success>(this.url, {stock: ticker, assumed: assumptions}).pipe(
      catchError((err: HttpErrorResponse) => {
        console.log(err);
        const message = err.error?.detail ?? 'Something went wrong fetching stock data.';
        return throwError(() => new Error(message));
      })
    );
  }
}
