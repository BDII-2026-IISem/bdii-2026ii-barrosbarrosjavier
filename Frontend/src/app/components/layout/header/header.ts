import { Component, inject, OnDestroy, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { MenuItem } from 'primeng/api';
import { OverlayBadge } from 'primeng/overlaybadge';
import { TieredMenu } from 'primeng/tieredmenu';
import { Subscription } from 'rxjs';
import { environment } from '../../../../environments/environment';
import { AuthService } from '../../../services/auth';

@Component({
  selector: 'app-header',
  standalone: true,
  imports: [OverlayBadge, TieredMenu],
  templateUrl: './header.html',
  styleUrl: './header.css',
})
export class Header implements OnInit, OnDestroy {
  private readonly router = inject(Router);
  private readonly authService = inject(AuthService);
  private sub?: Subscription;

  protected readonly appName = environment.appName;
  items: MenuItem[] = [];
  isLoggedIn = false;

  ngOnInit(): void {
    this.sub = this.authService.authState$.subscribe((state) => {
      this.isLoggedIn = state;
      this.buildMenu();
    });
  }

  ngOnDestroy(): void {
    this.sub?.unsubscribe();
  }

  private buildMenu(): void {
    this.items = this.isLoggedIn
      ? [
          { label: 'Mi perfil', icon: 'pi pi-user', command: () => this.router.navigate(['/profile']) },
          { separator: true },
          { label: 'Cerrar sesión', icon: 'pi pi-sign-out', command: () => this.logout() },
        ]
      : [{ label: 'Iniciar sesión', icon: 'pi pi-sign-in', command: () => this.router.navigate(['/login']) }];
  }

  private logout(): void {
    this.authService.logout().subscribe(() => this.router.navigate(['/login']));
  }
}
