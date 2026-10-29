import { TestBed } from '@angular/core/testing';
import { provideHttpClient } from '@angular/common/http';
import { HttpTestingController, provideHttpClientTesting } from '@angular/common/http/testing';
import { environment } from '../../environments/environment';
import { expiredToken, validToken } from '../testing/fake-jwt';
import { AuthService } from './auth';

describe('AuthService', () => {
  let service: AuthService;
  let http: HttpTestingController;

  beforeEach(() => {
    localStorage.clear();
    TestBed.configureTestingModule({ providers: [provideHttpClient(), provideHttpClientTesting()] });
    service = TestBed.inject(AuthService);
    http = TestBed.inject(HttpTestingController);
  });

  afterEach(() => http.verify());

  it('should save the tokens and emit true after login', () => {
    const states: boolean[] = [];
    service.authState$.subscribe((s) => states.push(s));
    const access = validToken();

    service.login({ username: 'demo', password: 'secreto123' }).subscribe();
    const req = http.expectOne(`${environment.apiUrl}/auth/login/`);
    expect(req.request.method).toBe('POST');
    expect(req.request.body).toEqual({ username: 'demo', password: 'secreto123' });
    req.flush({ access, refresh: 'r1', tokenType: 'Bearer', accessExpiresIn: 3600 });

    expect(localStorage.getItem('auth_token')).toBe(access);
    expect(localStorage.getItem('refresh_token')).toBe('r1');
    expect(service.isLoggedIn()).toBe(true);
    expect(states).toEqual([false, true]);
  });

  it('should send the refresh token on logout and clear the session', () => {
    localStorage.setItem('auth_token', validToken());
    localStorage.setItem('refresh_token', 'r1');

    service.logout().subscribe();
    const req = http.expectOne(`${environment.apiUrl}/auth/logout/`);
    expect(req.request.body).toEqual({ refresh: 'r1' });
    req.flush(null, { status: 204, statusText: 'No Content' });

    expect(localStorage.getItem('auth_token')).toBeNull();
    expect(localStorage.getItem('refresh_token')).toBeNull();
    expect(service.isLoggedIn()).toBe(false);
  });

  it('should treat an expired access token as logged out', () => {
    localStorage.setItem('auth_token', expiredToken());
    expect(service.isLoggedIn()).toBe(false);
  });
});
