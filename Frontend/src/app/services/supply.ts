import { HttpClient } from '@angular/common/http';
import { inject, Service } from '@angular/core';
import { Observable } from 'rxjs';
import { environment } from '../../environments/environment';
import { SupplyI } from '../models/supply';

// El token lo agrega authInterceptor; aquí no se arman cabeceras
@Service()
export class SupplyService {
  private readonly http = inject(HttpClient);
  private readonly baseUrl = `${environment.apiUrl}/catalog/supplies`;

  getAllSupplies(): Observable<SupplyI[]> {
    return this.http.get<SupplyI[]>(`${this.baseUrl}/`);
  }

  getSupplyById(id: number): Observable<SupplyI> {
    return this.http.get<SupplyI>(`${this.baseUrl}/${id}/`);
  }

  createSupply(supply: SupplyI): Observable<SupplyI> {
    return this.http.post<SupplyI>(`${this.baseUrl}/`, supply);
  }

  updateSupply(id: number, supply: Partial<SupplyI>): Observable<SupplyI> {
    return this.http.patch<SupplyI>(`${this.baseUrl}/${id}/`, supply);
  }

  // Borrado físico: Django responde 500 si el insumo está en recetas o movimientos (PROTECT)
  deleteSupply(id: number): Observable<void> {
    return this.http.delete<void>(`${this.baseUrl}/${id}/`);
  }

  // Baja lógica: deja el insumo con status = false
  deleteSupplyLogic(id: number): Observable<SupplyI> {
    return this.updateSupply(id, { status: false });
  }
}
