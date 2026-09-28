import { Component, inject, signal } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { ChatMsg, QueryAnswer } from '../../model/types';
import { QueryHandler } from '../../services/query-handler';
import { marked } from 'marked';

@Component({
  selector: 'app-ask-smth',
  imports: [FormsModule],
  templateUrl: './ask-smth.html',
  styleUrl: './ask-smth.css',
})
export class AskSmth {
  messages = signal<ChatMsg[]>([]);

  query = signal<string>('');

  isLoading = signal(false);
  errorMsg = signal<string | null>(null);
  now: Date = new Date();

  private queryService = inject(QueryHandler);

  onAsk(): void {
    if (!this.query()) return;
    if (this.isLoading()) return;

    let currentQuery = this.query();
    this.query.set('');

    const userMsg: ChatMsg = {
      id: Date.now(),
      time: this.now.toLocaleTimeString('en-GB', {
        hour: '2-digit',
        minute: '2-digit',
        hour12: false
      }),
      role: 'user',
      text: currentQuery
    };
    this.messages.update(msg => [...msg, userMsg]);

    this.isLoading.set(true);
    this.errorMsg.set(null);

    this.queryService.runQuery({query: currentQuery}).subscribe({
      next: async (data: QueryAnswer) => {
        const html = await marked.parse(data.answer || '');
        const responseMsg: ChatMsg = {
          id: Date.now(),
          time: this.now.toLocaleTimeString('en-GB', {
            hour: '2-digit',
            minute: '2-digit',
            hour12: false
          }),
          role: 'assistant',
          text: html,
          sources: data.sources
        };
        this.messages.update(msg => [...msg, responseMsg]);
        this.isLoading.set(false);
      },
      error: (err) => {
        this.errorMsg.set('Failed');
        this.isLoading.set(false);
      }
    })
  }
}
