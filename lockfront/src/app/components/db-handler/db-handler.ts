import { Component, inject, input, signal } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { DbHandlerService } from '../../services/db-handler';
import { IndexingState } from '../../model/types';

@Component({
  selector: 'app-db-handler',
  imports: [FormsModule],
  templateUrl: './db-handler.html',
  styleUrl: './db-handler.css',
})
export class DbHandler {
  msg = input();
  path = signal<string>('');

  res = signal<IndexingState | null>(null);
  isLoading = signal(false);
  errorMsg = signal<string | null>(null);

  private dbHandlerService = inject(DbHandlerService);

  onSubmit(): void {
    if (!this.path()) return;

    this.isLoading.set(true);
    this.errorMsg.set(null);

    this.dbHandlerService.rewriteDb({path: this.path()}).subscribe({
      next: (data: IndexingState) => {
        this.res.set(data);
        this.isLoading.set(false);
      },
      error: (err) => {
        this.errorMsg.set('Failed');
        this.isLoading.set(false);
      }
    })
  }
}
