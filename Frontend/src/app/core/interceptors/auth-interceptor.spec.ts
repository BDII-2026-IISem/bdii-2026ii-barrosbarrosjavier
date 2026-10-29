import { TestBed } from '@angular/core/testing';
import { HttpClient, provideHttpClient, withInterceptors } from '@angular/common/http';
import { HttpTestingController, provideHttpClientTesting } from '@angular/common/http/testing';
import { environment } from '../../../environments/environment';
import { authInterceptor } from './auth-interceptor';

describe('authInterceptor', () => {
  let http: HttpClient;
  let controller: HttpTestingController;

  beforeEach(() => {
    localStorage.clear();
    TestBed.configureTestingModule({
      providers: [provideHttpClient(withInterceptors([authInterceptor])), provideHttpClientTesting()],
    });
    http = TestBed.inject(HttpClient);
    controller = TestBed.inject(HttpTestingController);
  });

  afterEach(() => controller.verify());

  it('should add the Bearer token to API requests', () => {
    localStorage.setItem('auth_token', 'abc');
    http.get(`${environment.apiUrl}/auth/profile/`).subscribe();
    const req = controller.expectOne(`${environment.apiUrl}/auth/profile/`);
    expect(req.request.headers.get('Authorization')).toBe('Bearer abc');
    req.flush({});
  });

  it('should not add the token to the login request', () => {
    localStorage.setItem('auth_token', 'abc');
    http.post(`${environment.apiUrl}/auth/login/`, {}).subscribe();
    const req = controller.expectOne(`${environment.apiUrl}/auth/login/`);
    expect(req.request.headers.has('Authorization')).toBe(false);
    req.flush({});
  });
});
