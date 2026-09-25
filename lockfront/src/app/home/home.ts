import { Component, signal } from '@angular/core';
import { DbHandler } from '../components/db-handler/db-handler';
import { SignalFormControl } from '@angular/forms/signals/compat';
import { AskSmth } from '../components/ask-smth/ask-smth';

@Component({
  selector: 'app-home',
  imports: [DbHandler, AskSmth],
  templateUrl: './home.html',
  styleUrl: './home.css',
})
export class Home {
  msg = signal('DbHandler');
}
