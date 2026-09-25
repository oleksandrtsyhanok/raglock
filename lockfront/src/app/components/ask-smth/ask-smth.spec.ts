import { ComponentFixture, TestBed } from '@angular/core/testing';

import { AskSmth } from './ask-smth';

describe('AskSmth', () => {
  let component: AskSmth;
  let fixture: ComponentFixture<AskSmth>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [AskSmth],
    }).compileComponents();

    fixture = TestBed.createComponent(AskSmth);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
