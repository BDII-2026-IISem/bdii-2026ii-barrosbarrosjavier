import { ComponentFixture, TestBed } from '@angular/core/testing';
import { provideHttpClient } from '@angular/common/http';
import { HttpTestingController, provideHttpClientTesting } from '@angular/common/http/testing';
import { ActivatedRoute, convertToParamMap, provideRouter } from '@angular/router';
import { MessageService } from 'primeng/api';
import { providePrimeNG } from 'primeng/config';
import { environment } from '../../../../environments/environment';
import { Update } from './update';

describe('Supply Update', () => {
  let fixture: ComponentFixture<Update>;
  let http: HttpTestingController;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [Update],
      providers: [
        provideRouter([]),
        provideHttpClient(),
        provideHttpClientTesting(),
        providePrimeNG(),
        MessageService,
        { provide: ActivatedRoute, useValue: { snapshot: { paramMap: convertToParamMap({ id: '4' }) } } },
      ],
    }).compileComponents();
    fixture = TestBed.createComponent(Update);
    http = TestBed.inject(HttpTestingController);
  });

  it('should load the supply and fill the form', async () => {
    fixture.detectChanges();
    http
      .expectOne(`${environment.apiUrl}/catalog/supplies/4/`)
      .flush({ id: 4, code: 'INS-003', name: 'Harina 3', unitOfMeasure: 'kg', minStock: '2.50', status: true });
    await fixture.whenStable();
    const input = (fixture.nativeElement as HTMLElement).querySelector<HTMLInputElement>('#name')!;
    expect(input.value).toBe('Harina 3');
  });
});
