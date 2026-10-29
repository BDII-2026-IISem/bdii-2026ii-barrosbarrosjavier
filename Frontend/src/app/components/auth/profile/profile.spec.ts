import { ComponentFixture, TestBed } from '@angular/core/testing';
import { provideHttpClient } from '@angular/common/http';
import { HttpTestingController, provideHttpClientTesting } from '@angular/common/http/testing';
import { providePrimeNG } from 'primeng/config';
import { environment } from '../../../../environments/environment';
import { Profile } from './profile';

describe('Profile', () => {
  let fixture: ComponentFixture<Profile>;
  let http: HttpTestingController;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [Profile],
      providers: [provideHttpClient(), provideHttpClientTesting(), providePrimeNG()],
    }).compileComponents();
    fixture = TestBed.createComponent(Profile);
    http = TestBed.inject(HttpTestingController);
  });

  it('should load and show the profile', async () => {
    fixture.detectChanges();
    http.expectOne(`${environment.apiUrl}/auth/profile/`).flush({
      id: 2, username: 'demo', email: 'demo@hornoraiz.co', firstName: 'Demo', lastName: 'Frontend', status: 'active',
    });
    await fixture.whenStable();
    const text = (fixture.nativeElement as HTMLElement).textContent;
    expect(text).toContain('demo@hornoraiz.co');
    expect(text).toContain('Activo');
  });
});
