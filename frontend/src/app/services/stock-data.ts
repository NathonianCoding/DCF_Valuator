import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root',
})

export interface DCF_success{
  value: string;
  stock_snapshot: Record<string, string>;
}
export interface DCF_failure{
  details: string;
}

export class StockData {}
