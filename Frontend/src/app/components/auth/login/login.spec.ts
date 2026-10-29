import { ComponentFixture, TestBed } from '@angular/core/testing';
import { provideHttpClient } from '@angular/common/http';
import { HttpTestingController, provideHttpClientTesting } from '@angular/common/http/testing';
import { provideRouter, Router } from '@angular/router';
import { providePrimeNG } from 'primeng/config';
import { environment } from '../../../../environments/environment';
import { validToken } from '../../../testing/fake-jwt';
import { Login } from './login';

describe('Login', () => {
  let fixture: ComponentFixture<Login>;
  let http: HttpTestingController;

  const fill = (user: string, password: string) => {
    const el = fixture.nativeElement as HTMLElement;
    const userInput = el.querySelector<HTMLInputElement>('#user')!;
    const passInput = el.querySelector<HTMLInputElement>('#password')!;
    userInput.value = user;
    userInput.dispatchEvent(new Event('input'));
    passInput.value = password;
    passInput.dispatchEvent(new Event('input'));
    el.querySelector<HTMLFormElement>('form')!.dispatchEvent(new Event('submit'));
  };

  beforeEach(async () => {
    localStorage.clear();
    await TestBed.configureTestingModule({
      imports: [Login],
      providers: [
        provideRouter([{ path: 'products', children: [] }]),
        provideHttpClient(),
        provideHttpClientTesting(),
        providePrimeNG(),
      ],
    }).compileComponents();
    fixture = TestBed.createComponent(Login);
    http = TestBed.inject(HttpTestingController);
    await fixture.whenStable();
  });

  afterEach(() => http.verify());

  it('should not call the API with an empty form', async () => {
    fill('', '');
    await fixture.whenStable();
    http.expectNone(`${environment.apiUrl}/auth/login/`);
    expect((fixture.nativeElement as HTMLElement).textContent).toContain('mínimo 6 caracteres');
  });

  it('should send email when the user writes an address', async () => {
    fill('demo@hornoraiz.co', 'secreto123');
    const req = http.expectOne(`${environment.apiUrl}/auth/login/`);
    expect(req.request.body).toEqual({ email: 'demo@hornoraiz.co', password: 'secreto123' });
    req.flush({ access: validToken(), refresh: 'r', tokenType: 'Bearer', accessExpiresIn: 3600 });
  });

  it('should show an error on 401', async () => {
    fill('demo', 'incorrecta');
    http
      .expectOne(`${environment.apiUrl}/auth/login/`)
      .flush({ detail: 'Credenciales inválidas.' }, { status: 401, statusText: 'Unauthorized' });
    await fixture.whenStable();
    expect((fixture.nativeElement as HTMLElement).textContent).toContain('Usuario o contraseña incorrectos.');
  });

  it('should go to /products after a successful login', async () => {
    const navigate = vi.spyOn(TestBed.inject(Router), 'navigate').mockResolvedValue(true);
    fill('demo', 'secreto123');
    http
      .expectOne(`${environment.apiUrl}/auth/login/`)
      .flush({ access: validToken(), refresh: 'r', tokenType: 'Bearer', accessExpiresIn: 3600 });
    expect(navigate).toHaveBeenCalledWith(['/products']);
  });
});
