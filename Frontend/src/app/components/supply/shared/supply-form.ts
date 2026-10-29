import { HttpErrorResponse } from '@angular/common/http';
import { FormBuilder, Validators } from '@angular/forms';

export const statusOptions = [
  { label: 'Activo', value: true },
  { label: 'Inactivo', value: false },
];

export function buildSupplyForm(fb: FormBuilder) {
  return fb.nonNullable.group({
    code: ['', [Validators.required, Validators.maxLength(50)]],
    name: ['', [Validators.required, Validators.minLength(2), Validators.maxLength(100)]],
    unitOfMeasure: ['', [Validators.required, Validators.maxLength(30)]],
    minStock: [0, [Validators.required, Validators.min(0)]],
    status: [true, Validators.required],
  });
}

export type SupplyForm = ReturnType<typeof buildSupplyForm>;

export function fieldError(form: SupplyForm, field: keyof SupplyForm['controls']): string | null {
  const control = form.controls[field];
  if (!control.errors || !control.touched) {
    return null;
  }
  if (control.errors['required']) return 'Este campo es obligatorio.';
  if (control.errors['minlength']) return `Mínimo ${control.errors['minlength'].requiredLength} caracteres.`;
  if (control.errors['maxlength']) return `Máximo ${control.errors['maxlength'].requiredLength} caracteres.`;
  if (control.errors['min']) return 'No puede ser negativo.';
  return 'Valor no válido.';
}

// Convierte la respuesta de error de Django en un texto para el usuario
export function apiErrorMessage(err: HttpErrorResponse): string {
  if (err.status === 0) return 'No se pudo conectar con el servidor.';
  if (err.status === 403) return err.error?.detail ?? 'No tiene autorización para esta operación.';
  if (err.status === 404) return 'El insumo no existe.';
  if (err.status === 400 && err.error && typeof err.error === 'object') {
    const [field, messages] = Object.entries(err.error)[0] ?? [];
    const text = Array.isArray(messages) ? messages[0] : messages;
    return field === 'code' ? `Código: ${text}` : String(text ?? 'Datos no válidos.');
  }
  return 'Ocurrió un error en el servidor.';
}
