import { Component, inject, signal } from '@angular/core';
import { HttpErrorResponse } from '@angular/common/http';
import { FormBuilder, ReactiveFormsModule } from '@angular/forms';
import { Router } from '@angular/router';
import { MessageService } from 'primeng/api';
import { ButtonModule } from 'primeng/button';
import { InputNumberModule } from 'primeng/inputnumber';
import { InputTextModule } from 'primeng/inputtext';
import { SelectModule } from 'primeng/select';
import { SupplyService } from '../../../services/supply';
import { apiErrorMessage, buildSupplyForm, fieldError, statusOptions, SupplyForm } from '../shared/supply-form';

@Component({
  selector: 'app-create',
  standalone: true,
  imports: [ReactiveFormsModule, ButtonModule, InputNumberModule, InputTextModule, SelectModule],
  templateUrl: './create.html',
  styleUrl: './create.css',
})
export class Create {
  private readonly supplyService = inject(SupplyService);
  private readonly messageService = inject(MessageService);
  private readonly router = inject(Router);

  protected readonly form: SupplyForm = buildSupplyForm(inject(FormBuilder));
  protected readonly statusOptions = statusOptions;
  protected readonly loading = signal(false);

  submit(): void {
    if (this.form.invalid) {
      this.form.markAllAsTouched();
      this.messageService.add({
        severity: 'warn',
        summary: 'Formulario incompleto',
        detail: 'Revisa los campos marcados.',
      });
      return;
    }
    this.loading.set(true);
    this.supplyService.createSupply(this.form.getRawValue()).subscribe({
      next: (supply) => {
        this.messageService.add({
          severity: 'success',
          summary: 'Insumo creado',
          detail: `"${supply.name}" se creó correctamente.`,
        });
        this.router.navigate(['/supplies']);
      },
      error: (err: HttpErrorResponse) => {
        this.loading.set(false);
        this.messageService.add({ severity: 'error', summary: 'No se pudo crear', detail: apiErrorMessage(err) });
      },
    });
  }

  cancelar(): void {
    this.router.navigate(['/supplies']);
  }

  getFieldError(field: keyof SupplyForm['controls']): string | null {
    return fieldError(this.form, field);
  }
}
