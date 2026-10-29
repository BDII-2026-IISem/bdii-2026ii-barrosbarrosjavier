import { ComponentFixture, TestBed } from '@angular/core/testing';
import { provideHttpClient } from '@angular/common/http';
import { HttpTestingController, provideHttpClientTesting } from '@angular/common/http/testing';
import { provideRouter } from '@angular/router';
import { ConfirmationService, MessageService } from 'primeng/api';
import { providePrimeNG } from 'primeng/config';
import { environment } from '../../../../environments/environment';
import { Getall } from './getall';

describe('Supply Getall', () => {
  let fixture: ComponentFixture<Getall>;
  let http: HttpTestingController;
  let messages: MessageService;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [Getall],
      providers: [
        provideRouter([]),
        provideHttpClient(),
        provideHttpClientTesting(),
        providePrimeNG(),
        MessageService,
        ConfirmationService,
      ],
    }).compileComponents();
    fixture = TestBed.createComponent(Getall);
    http = TestBed.inject(HttpTestingController);
    messages = TestBed.inject(MessageService);
    fixture.detectChanges();
  });

  it('should list the supplies from the API', async () => {
    http.expectOne(`${environment.apiUrl}/catalog/supplies/`).flush([
      { id: 1, code: 'INS-001', name: 'Harina', unitOfMeasure: 'kg', minStock: '10.00', status: true },
      { id: 2, code: 'INS-002', name: 'Azúcar', unitOfMeasure: 'kg', minStock: '5.00', status: false },
    ]);
    await fixture.whenStable();
    const text = (fixture.nativeElement as HTMLElement).textContent;
    expect(text).toContain('Harina');
    expect(text).toContain('Inactivo');
  });

  it('should show a toast when the API answers 403', () => {
    const add = vi.spyOn(messages, 'add');
    http
      .expectOne(`${environment.apiUrl}/catalog/supplies/`)
      .flush({ detail: 'No tiene autorización para ejecutar esta operación.' }, { status: 403, statusText: 'Forbidden' });
    expect(add).toHaveBeenCalledWith(
      expect.objectContaining({ severity: 'error', detail: 'No tiene autorización para ejecutar esta operación.' }),
    );
  });
});
