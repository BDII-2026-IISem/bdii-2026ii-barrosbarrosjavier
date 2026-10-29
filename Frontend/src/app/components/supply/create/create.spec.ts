import { ComponentFixture, TestBed } from '@angular/core/testing';
import { provideHttpClient } from '@angular/common/http';
import { HttpTestingController, provideHttpClientTesting } from '@angular/common/http/testing';
import { provideRouter, Router } from '@angular/router';
import { MessageService } from 'primeng/api';
import { providePrimeNG } from 'primeng/config';
import { environment } from '../../../../environments/environment';
import { Create } from './create';

describe('Supply Create', () => {
  let fixture: ComponentFixture<Create>;
  let component: Create;
  let http: HttpTestingController;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [Create],
      providers: [provideRouter([]), provideHttpClient(), provideHttpClientTesting(), providePrimeNG(), MessageService],
    }).compileComponents();
    fixture = TestBed.createComponent(Create);
    component = fixture.componentInstance;
    http = TestBed.inject(HttpTestingController);
    await fixture.whenStable();
  });

  afterEach(() => http.verify());

  it('should not call the API with an invalid form', () => {
    component.submit();
    http.expectNone(`${environment.apiUrl}/catalog/supplies/`);
    expect(component.getFieldError('code')).toBe('Este campo es obligatorio.');
  });

  it('should POST the supply and go back to the list', () => {
    const navigate = vi.spyOn(TestBed.inject(Router), 'navigate').mockResolvedValue(true);
    const value = { code: 'INS-010', name: 'Levadura', unitOfMeasure: 'g', minStock: 500, status: true };
    (component as unknown as { form: { setValue(v: object): void } }).form.setValue(value);
    component.submit();
    const req = http.expectOne(`${environment.apiUrl}/catalog/supplies/`);
    expect(req.request.method).toBe('POST');
    expect(req.request.body).toEqual(value);
    req.flush({ id: 9, ...value, minStock: '500.00' });
    expect(navigate).toHaveBeenCalledWith(['/supplies']);
  });
});
