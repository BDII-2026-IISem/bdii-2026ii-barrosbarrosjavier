import { Component, inject, OnInit, signal } from '@angular/core';
import { DecimalPipe } from '@angular/common';
import { HttpErrorResponse } from '@angular/common/http';
import { ActivatedRoute, Router } from '@angular/router';
import { MessageService } from 'primeng/api';
import { ButtonModule } from 'primeng/button';
import { MessageModule } from 'primeng/message';
import { TagModule } from 'primeng/tag';
import { SupplyI } from '../../../models/supply';
import { SupplyService } from '../../../services/supply';
import { apiErrorMessage } from '../shared/supply-form';

@Component({
  selector: 'app-delete',
  standalone: true,
  imports: [DecimalPipe, ButtonModule, MessageModule, TagModule],
  templateUrl: './delete.html',
  styleUrl: './delete.css',
})
export class Delete implements OnInit {
  private readonly supplyService = inject(SupplyService);
  private readonly messageService = inject(MessageService);
  private readonly router = inject(Router);
  private readonly route = inject(ActivatedRoute);

  protected readonly supply = signal<SupplyI | null>(null);
  protected readonly deleting = signal(false);
  protected readonly error = signal<string | null>(null);

  ngOnInit(): void {
    const id = Number(this.route.snapshot.paramMap.get('id'));
    this.supplyService.getSupplyById(id).subscribe({
      next: (supply) => this.supply.set(supply),
      error: (err: HttpErrorResponse) => {
        this.messageService.add({ severity: 'error', summary: 'No se pudo cargar', detail: apiErrorMessage(err) });
        this.router.navigate(['/supplies']);
      },
    });
  }

  confirmDelete(): void {
    const supply = this.supply()!;
    this.deleting.set(true);
    this.error.set(null);
    this.supplyService.deleteSupply(supply.id!).subscribe({
      next: () => {
        this.messageService.add({
          severity: 'success',
          summary: 'Insumo eliminado',
          detail: `"${supply.name}" se eliminó definitivamente.`,
        });
        this.router.navigate(['/supplies']);
      },
      error: (err: HttpErrorResponse) => {
        this.deleting.set(false);
        // Django protege los insumos usados en recetas o movimientos y responde 500
        this.error.set(
          err.status === 500
            ? 'No se puede eliminar: el insumo está en uso por recetas o movimientos. Desactívalo desde el listado.'
            : apiErrorMessage(err),
        );
      },
    });
  }

  cancelar(): void {
    this.router.navigate(['/supplies']);
  }
}
