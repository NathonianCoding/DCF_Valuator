import { ComponentFixture, TestBed } from '@angular/core/testing';

import { Assumptions } from './assumptions';

describe('Assumptions', () => {
  let component: Assumptions;
  let fixture: ComponentFixture<Assumptions>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [Assumptions],
    }).compileComponents();

    fixture = TestBed.createComponent(Assumptions);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
