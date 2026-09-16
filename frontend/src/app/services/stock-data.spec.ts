import { TestBed } from '@angular/core/testing';

import { StockData } from './stock-data';

describe('StockData', () => {
  let service: StockData;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(StockData);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
