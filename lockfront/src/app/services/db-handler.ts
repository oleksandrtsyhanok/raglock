import { HttpClient } from '@angular/common/http';
import { inject, Injectable } from '@angular/core';
import { FolderPath, IndexingState } from '../model/types';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class DbHandlerService {
  http = inject(HttpClient);
  rewriteDb(payload: FolderPath): Observable<IndexingState> {
    const url = `http://127.0.0.1:8000//api/index`
    return this.http.post<IndexingState>(url, payload);
  }
}
