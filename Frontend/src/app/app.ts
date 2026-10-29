import { Component, inject, signal } from '@angular/core';
import { AsyncPipe } from '@angular/common';
import { RouterOutlet } from '@angular/router';
import { ToastModule } from 'primeng/toast';
import { Aside } from './components/layout/aside/aside';
import { Footer } from './components/layout/footer/footer';
import { Header } from './components/layout/header/header';
import { AuthService } from './services/auth';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [RouterOutlet, Header, Footer, Aside, AsyncPipe, ToastModule],
  templateUrl: './app.html',
  styleUrl: './app.css',
})
export class App {
  protected readonly title = signal('HornoRaíz');
  protected readonly authState$ = inject(AuthService).authState$;
}
