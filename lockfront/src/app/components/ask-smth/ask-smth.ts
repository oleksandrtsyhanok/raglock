import { Component, signal } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { QueryAnswer } from '../../model/types';

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

  onAsk(): void {
    if (!this.query()) return;  
  }
}
