// Contrato de /api/catalog/supplies/ (JSON en camelCase; minStock llega como texto decimal)

export interface SupplyI {
  id?: number;
  code: string;
  name: string;
  unitOfMeasure: string;
  minStock: string | number;
  status: boolean;
}
