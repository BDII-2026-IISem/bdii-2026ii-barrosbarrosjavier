import { Component, inject, OnInit, signal } from '@angular/core';
import { HttpErrorResponse } from '@angular/common/http';
import { FormBuilder, ReactiveFormsModule } from '@angular/forms';
import { ActivatedRoute, Router } from '@angular/router';
import { MessageService } from 'primeng/api';
import { ButtonModule } from 'primeng/button';
import { InputNumberModule } from 'primeng/inputnumber';
import { InputTextModule } from 'primeng/inputtext';
import { SelectModule } from 'primeng/select';
import { SupplyService } from '../../../services/supply';
import { apiErrorMessage, buildSupplyForm, fieldError, statusOptions, SupplyForm } from '../shared/supply-form';

@Component({
  selector: 'app-update',
  standalone: true,
  imports: [ReactiveFormsModule, ButtonModule, InputNumberModule, InputTextModule, SelectModule],
  templateUrl: './update.html',
  styleUrl: './update.css',
})
export class Update implements OnInit {
  private readonly supplyService = inject(SupplyService);
  private readonly messageService = inject(MessageService);
  private readonly router = inject(Router);
  private readonly route = inject(ActivatedRoute);

  protected readonly form: SupplyForm = buildSupplyForm(inject(FormBuilder));
  protected readonly statusOptions = statusOptions;
  protected readonly loading = signal(true);
  protected readonly saving = signal(false);
  protected supplyId = 0;

  ngOnInit(): void {
    this.supplyId = Number(this.route.snapshot.paramMap.get('id'));
    this.loadSupply();
  }

  loadSupply(): void {
    this.supplyService.getSupplyById(this.supplyId).subscribe({
      next: (supply) => {
        this.form.patchValue({ ...supply, minStock: Number(supply.minStock) });
        this.loading.set(false);
      },
      error: (err: HttpErrorResponse) => {
        this.messageService.add({ severity: 'error', summary: 'No se pudo cargar', detail: apiErrorMessage(err) });
        this.router.navigate(['/supplies']);
      },
    });
  }

  submit(): void {
    if (this.form.invalid) {
      this.form.markAllAsTouched();
      this.messageService.add({ severity: 'warn', summary: 'Formulario incompleto', detail: 'Revisa los campos marcados.' });
      return;
    }
    this.saving.set(true);
    this.supplyService.updateSupply(this.supplyId, this.form.getRawValue()).subscribe({
      next: (supply) => {
        this.messageService.add({
          severity: 'success',
          summary: 'Insumo actualizado',
          detail: `"${supply.name}" se actualizó correctamente.`,
        });
        this.router.navigate(['/supplies']);
      },
      error: (err: HttpErrorResponse) => {
        this.saving.set(false);
        this.messageService.add({ severity: 'error', summary: 'No se pudo actualizar', detail: apiErrorMessage(err) });
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
