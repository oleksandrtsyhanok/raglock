import { Component, signal } from '@angular/core';
import { DbHandler } from '../components/db-handler/db-handler';

@Component({
  selector: 'app-settings',
  imports: [DbHandler],
  templateUrl: './settings.html',
  styleUrl: './settings.css',
})
export class Settings {
  msg = signal('DbHandler');
}
