import { Component, inject, signal } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { QueryAnswer } from '../../model/types';
import { QueryHandler } from '../../services/query-handler';

@Component({
  selector: 'app-ask-smth',
  imports: [FormsModule],
  templateUrl: './ask-smth.html',
  styleUrl: './ask-smth.css',
})
export class AskSmth {
  query = signal<string>('');

  res = signal<QueryAnswer | null>(null);
  isLoading = signal(false);
  errorMsg = signal<string | null>(null);

  private queryService = inject(QueryHandler);

  onAsk(): void {
    if (!this.query()) return;

    this.isLoading.set(true);
    this.errorMsg.set(null);

    this.queryService.runQuery({query: this.query()}).subscribe({
      next: (data: QueryAnswer) => {
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
