import { TestBed } from '@angular/core/testing';
import { provideHttpClient } from '@angular/common/http';
import { HttpTestingController, provideHttpClientTesting } from '@angular/common/http/testing';
import { environment } from '../../environments/environment';
import { SupplyService } from './supply';

describe('SupplyService', () => {
  const url = `${environment.apiUrl}/catalog/supplies`;
  let service: SupplyService;
  let http: HttpTestingController;

  beforeEach(() => {
    TestBed.configureTestingModule({ providers: [provideHttpClient(), provideHttpClientTesting()] });
    service = TestBed.inject(SupplyService);
    http = TestBed.inject(HttpTestingController);
  });

  afterEach(() => http.verify());

  it('should use the Django endpoints with trailing slash', () => {
    const supply = { code: 'INS-9', name: 'Sal', unitOfMeasure: 'kg', minStock: 1, status: true };
    service.getAllSupplies().subscribe();
    service.getSupplyById(4).subscribe();
    service.createSupply(supply).subscribe();
    service.updateSupply(4, { name: 'Sal fina' }).subscribe();
    service.deleteSupply(4).subscribe();

    expect(http.expectOne({ method: 'GET', url: `${url}/` })).toBeTruthy();
    expect(http.expectOne({ method: 'GET', url: `${url}/4/` })).toBeTruthy();
    expect(http.expectOne({ method: 'POST', url: `${url}/` }).request.body).toEqual(supply);
    expect(http.expectOne({ method: 'PATCH', url: `${url}/4/` }).request.body).toEqual({ name: 'Sal fina' });
    expect(http.expectOne({ method: 'DELETE', url: `${url}/4/` })).toBeTruthy();
  });

  it('should deactivate with PATCH status false', () => {
    service.deleteSupplyLogic(4).subscribe();
    const req = http.expectOne({ method: 'PATCH', url: `${url}/4/` });
    expect(req.request.body).toEqual({ status: false });
  });
});
