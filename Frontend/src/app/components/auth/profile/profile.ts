import { Component, inject, OnInit, signal } from '@angular/core';
import { TagModule } from 'primeng/tag';
import { UserI } from '../../../models/auth';
import { AuthService } from '../../../services/auth';

@Component({
  selector: 'app-profile',
  standalone: true,
  imports: [TagModule],
  templateUrl: './profile.html',
  styleUrl: './profile.css',
})
export class Profile implements OnInit {
  private readonly authService = inject(AuthService);

  protected readonly user = signal<UserI | null>(null);
  protected readonly error = signal<string | null>(null);

  ngOnInit(): void {
    this.authService.getProfile().subscribe({
      next: (user) => this.user.set(user),
      error: () => this.error.set('No se pudo cargar el perfil.'),
    });
  }
}
