import { ComponentFixture, TestBed } from '@angular/core/testing';

import { DbHandler } from './db-handler';

describe('DbHandler', () => {
  let component: DbHandler;
  let fixture: ComponentFixture<DbHandler>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [DbHandler],
    }).compileComponents();

    fixture = TestBed.createComponent(DbHandler);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
