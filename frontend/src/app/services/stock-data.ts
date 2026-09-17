import { HttpClient, HttpErrorResponse } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable, catchError, throwError } from 'rxjs';

export interface DCF_success{
  value: string;
  stock_snapshot: Record<string, string>;
}
export interface DCF_failure{
  details: string;
}

@Injectable({providedIn: 'root',})
export class StockData {
  private url = "http://127.0.0.1:8000/api"
  constructor(private http: HttpClient){}
  getDcfValuation(ticker: string): Observable<DCF_success> {
    return this.http.get<DCF_success>(`${this.url}/${ticker}`).pipe(
      catchError((err: HttpErrorResponse) => {
        const message = err.error?.detail ?? 'Something went wrong fetching stock data.';
        return throwError(() => new Error(message));
      })
    );
  }
}
