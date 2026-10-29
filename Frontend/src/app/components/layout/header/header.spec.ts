import { provideHttpClient } from '@angular/common/http';
import { ComponentFixture, TestBed } from '@angular/core/testing';
import { provideRouter } from '@angular/router';
import { providePrimeNG } from 'primeng/config';
import { validToken } from '../../../testing/fake-jwt';
import { Header } from './header';

describe('Header', () => {
  let component: Header;
  let fixture: ComponentFixture<Header>;

  beforeEach(async () => {
    localStorage.clear();
    await TestBed.configureTestingModule({
      imports: [Header],
      providers: [provideRouter([]), provideHttpClient(), providePrimeNG()],
    }).compileComponents();

    fixture = TestBed.createComponent(Header);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should offer only "Iniciar sesión" without a session', () => {
    expect(component.items.map((item) => item.label)).toEqual(['Iniciar sesión']);
  });

  it('should offer profile and logout with a session', async () => {
    localStorage.setItem('auth_token', validToken());
    TestBed.resetTestingModule();
    await TestBed.configureTestingModule({
      imports: [Header],
      providers: [provideRouter([]), provideHttpClient(), providePrimeNG()],
    }).compileComponents();
    const logged = TestBed.createComponent(Header);
    await logged.whenStable();
    const labels = logged.componentInstance.items.filter((i) => !i.separator).map((i) => i.label);
    expect(labels).toEqual(['Mi perfil', 'Cerrar sesión']);
    expect((logged.nativeElement as HTMLElement).querySelector('p-overlaybadge')).toBeTruthy();
  });
});
