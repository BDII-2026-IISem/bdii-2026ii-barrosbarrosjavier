import { TestBed } from '@angular/core/testing';
import { provideRouter, Router } from '@angular/router';
import { RouterTestingHarness } from '@angular/router/testing';
import { provideHttpClient } from '@angular/common/http';
import { provideHttpClientTesting } from '@angular/common/http/testing';
import { ConfirmationService, MessageService } from 'primeng/api';
import { providePrimeNG } from 'primeng/config';
import { routes } from './app.routes';
import { validToken } from './testing/fake-jwt';

describe('routes', () => {
  beforeEach(() => {
    localStorage.clear();
    TestBed.configureTestingModule({
      providers: [
        provideRouter(routes),
        provideHttpClient(),
        provideHttpClientTesting(),
        providePrimeNG(),
        MessageService,
        ConfirmationService,
      ],
    });
  });

  it('should redirect the empty path to login', async () => {
    const harness = await RouterTestingHarness.create('/');
    expect(TestBed.inject(Router).url).toBe('/login');
    expect(harness.routeNativeElement?.textContent).toContain('Iniciar sesión');
  });

  it('should send protected routes and unknown routes to login without a session', async () => {
    const harness = await RouterTestingHarness.create();
    for (const url of ['/products', '/sales/edit/1', '/profile', '/no-existe']) {
      await harness.navigateByUrl(url);
      expect(TestBed.inject(Router).url).toBe('/login');
    }
  });

  it('should open the supplies CRUD screens with a session', async () => {
    localStorage.setItem('auth_token', validToken());
    const harness = await RouterTestingHarness.create();
    const screens: [string, string][] = [
      ['/supplies', 'Gestión de Insumos'],
      ['/supplies/new', 'Nuevo insumo'],
      ['/supplies/edit/1', 'Editar insumo #1'],
      ['/supplies/delete/1', 'Eliminar insumo'],
    ];
    for (const [url, text] of screens) {
      await harness.navigateByUrl(url);
      expect(harness.routeNativeElement?.textContent).toContain(text);
    }
  });

  for (const entity of ['products', 'sales']) {
    it(`should open the ${entity} screens with a session`, async () => {
      localStorage.setItem('auth_token', validToken());
      const harness = await RouterTestingHarness.create();
      const screens: [string, string][] = [
        [`/${entity}`, 'getall works!'],
        [`/${entity}/new`, 'create works!'],
        [`/${entity}/edit/1`, 'update works!'],
        [`/${entity}/delete/1`, 'delete works!'],
      ];
      for (const [url, text] of screens) {
        await harness.navigateByUrl(url);
        expect(harness.routeNativeElement?.textContent).toContain(text);
      }
    });
  }
});
