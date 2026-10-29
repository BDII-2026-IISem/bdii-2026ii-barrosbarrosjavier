import { Component, inject, OnInit, signal } from '@angular/core';
import { DecimalPipe } from '@angular/common';
import { HttpErrorResponse } from '@angular/common/http';
import { RouterLink } from '@angular/router';
import { ConfirmationService, MessageService } from 'primeng/api';
import { ButtonModule } from 'primeng/button';
import { ConfirmDialogModule } from 'primeng/confirmdialog';
import { TableModule } from 'primeng/table';
import { TagModule } from 'primeng/tag';
import { TooltipModule } from 'primeng/tooltip';
import { SupplyI } from '../../../models/supply';
import { SupplyService } from '../../../services/supply';
import { apiErrorMessage } from '../shared/supply-form';

@Component({
  selector: 'app-getall',
  standalone: true,
  imports: [RouterLink, DecimalPipe, ButtonModule, ConfirmDialogModule, TableModule, TagModule, TooltipModule],
  templateUrl: './getall.html',
  styleUrl: './getall.css',
})
export class Getall implements OnInit {
  private readonly supplyService = inject(SupplyService);
  private readonly messageService = inject(MessageService);
  private readonly confirmationService = inject(ConfirmationService);

  protected readonly supplies = signal<SupplyI[]>([]);
  protected readonly loading = signal(false);

  ngOnInit(): void {
    this.loadSupplies();
  }

  loadSupplies(): void {
    this.loading.set(true);
    this.supplyService.getAllSupplies().subscribe({
      next: (supplies) => {
        this.supplies.set(supplies);
        this.loading.set(false);
      },
      error: (err: HttpErrorResponse) => {
        this.loading.set(false);
        this.messageService.add({
          severity: 'error',
          summary: 'Error al cargar los insumos',
          detail: apiErrorMessage(err),
        });
      },
    });
  }

  deactivateSupply(supply: SupplyI): void {
    this.confirmationService.confirm({
      header: 'Desactivar insumo',
      message: `¿Desactivar el insumo "${supply.name}"? Seguirá en la lista como Inactivo.`,
      icon: 'pi pi-exclamation-triangle',
      acceptLabel: 'Desactivar',
      rejectLabel: 'Cancelar',
      acceptButtonProps: { severity: 'danger' },
      rejectButtonProps: { severity: 'secondary', outlined: true },
      accept: () => {
        this.supplyService.deleteSupplyLogic(supply.id!).subscribe({
          next: () => {
            this.messageService.add({
              severity: 'success',
              summary: 'Insumo desactivado',
              detail: `"${supply.name}" quedó Inactivo.`,
            });
            this.loadSupplies();
          },
          error: (err: HttpErrorResponse) =>
            this.messageService.add({ severity: 'error', summary: 'No se pudo desactivar', detail: apiErrorMessage(err) }),
        });
      },
    });
  }
}
