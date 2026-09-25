import { HttpClient } from '@angular/common/http';
import { inject, Injectable } from '@angular/core';
import { QueryAnswer, UserQuery } from '../model/types';
import { Observable } from 'rxjs';
import { reportUnhandledError } from 'rxjs/internal/util/reportUnhandledError';

@Injectable({
  providedIn: 'root',
})
export class QueryHandler {
  http = inject(HttpClient);
  runQuery(payload: UserQuery): Observable<QueryAnswer> {
    const url = `http://127.0.0.1:8000/api/chat`;
    return this.http.post<QueryAnswer>(url, payload);
  }
}
