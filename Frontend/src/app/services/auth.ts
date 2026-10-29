import { HttpClient } from '@angular/common/http';
import { inject, Service } from '@angular/core';
import { BehaviorSubject, Observable, of } from 'rxjs';
import { catchError, map, tap } from 'rxjs/operators';
import { environment } from '../../environments/environment';
import { LoginI, LoginResponseI, UserI } from '../models/auth';

const ACCESS_KEY = 'auth_token';
const REFRESH_KEY = 'refresh_token';

@Service()
export class AuthService {
  private readonly http = inject(HttpClient);
  private readonly baseUrl = `${environment.apiUrl}/auth`;

  private readonly authStateSubject = new BehaviorSubject<boolean>(this.isLoggedIn());
  readonly authState$ = this.authStateSubject.asObservable();

  login(credentials: LoginI): Observable<LoginResponseI> {
    return this.http.post<LoginResponseI>(`${this.baseUrl}/login/`, credentials).pipe(
      tap((response) => {
        this.setTokens(response.access, response.refresh);
        this.authStateSubject.next(true);
      }),
    );
  }

  logout(): Observable<void> {
    const refresh = this.storage()?.getItem(REFRESH_KEY);
    const request = refresh
      ? this.http.post<void>(`${this.baseUrl}/logout/`, { refresh }).pipe(catchError(() => of(undefined)))
      : of(undefined);
    return request.pipe(
      tap(() => {
        this.clearTokens();
        this.authStateSubject.next(false);
      }),
      map(() => undefined),
    );
  }

  getProfile(): Observable<UserI> {
    return this.http.get<UserI>(`${this.baseUrl}/profile/`);
  }

  getToken(): string | null {
    return this.storage()?.getItem(ACCESS_KEY) ?? null;
  }

  isLoggedIn(): boolean {
    const token = this.getToken();
    if (!token) {
      return false;
    }
    const expiresAt = this.tokenExpiry(token);
    return expiresAt === null || expiresAt > Date.now();
  }

  private setTokens(access: string, refresh: string): void {
    this.storage()?.setItem(ACCESS_KEY, access);
    this.storage()?.setItem(REFRESH_KEY, refresh);
  }

  private clearTokens(): void {
    this.storage()?.removeItem(ACCESS_KEY);
    this.storage()?.removeItem(REFRESH_KEY);
  }

  // Lee "exp" del payload del JWT (segundos) y lo devuelve en milisegundos
  private tokenExpiry(token: string): number | null {
    try {
      const payload = JSON.parse(atob(token.split('.')[1].replace(/-/g, '+').replace(/_/g, '/')));
      return typeof payload.exp === 'number' ? payload.exp * 1000 : null;
    } catch {
      return null;
    }
  }

  private storage(): Storage | null {
    return typeof localStorage === 'undefined' ? null : localStorage;
  }
}
