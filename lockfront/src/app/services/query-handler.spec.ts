import { TestBed } from '@angular/core/testing';

import { QueryHandler } from './query-handler';

describe('QueryHandler', () => {
  let service: QueryHandler;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(QueryHandler);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
