import { ComponentFixture, TestBed } from '@angular/core/testing';
import { provideHttpClient } from '@angular/common/http';
import { HttpTestingController, provideHttpClientTesting } from '@angular/common/http/testing';
import { ActivatedRoute, convertToParamMap, provideRouter } from '@angular/router';
import { MessageService } from 'primeng/api';
import { providePrimeNG } from 'primeng/config';
import { environment } from '../../../../environments/environment';
import { Delete } from './delete';

describe('Supply Delete', () => {
  let fixture: ComponentFixture<Delete>;
  let http: HttpTestingController;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [Delete],
      providers: [
        provideRouter([]),
        provideHttpClient(),
        provideHttpClientTesting(),
        providePrimeNG(),
        MessageService,
        { provide: ActivatedRoute, useValue: { snapshot: { paramMap: convertToParamMap({ id: '1' }) } } },
      ],
    }).compileComponents();
    fixture = TestBed.createComponent(Delete);
    http = TestBed.inject(HttpTestingController);
    fixture.detectChanges();
    http
      .expectOne(`${environment.apiUrl}/catalog/supplies/1/`)
      .flush({ id: 1, code: 'INS-001', name: 'Harina', unitOfMeasure: 'kg', minStock: '10.00', status: true });
    await fixture.whenStable();
  });

  it('should explain when Django protects a supply in use (500)', async () => {
    fixture.componentInstance.confirmDelete();
    http
      .expectOne({ method: 'DELETE', url: `${environment.apiUrl}/catalog/supplies/1/` })
      .flush('ProtectedError', { status: 500, statusText: 'Server Error' });
    await fixture.whenStable();
    expect((fixture.nativeElement as HTMLElement).textContent).toContain('está en uso');
  });
});
