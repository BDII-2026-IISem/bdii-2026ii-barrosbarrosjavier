import { Component, OnInit } from '@angular/core';
import { MenuItem } from 'primeng/api';
import { PanelMenu } from 'primeng/panelmenu';

@Component({
  selector: 'app-aside',
  standalone: true,
  imports: [PanelMenu],
  templateUrl: './aside.html',
  styleUrl: './aside.css',
})
export class Aside implements OnInit {
  items: MenuItem[] | undefined;

  ngOnInit() {
    this.items = [
      {
        label: 'Catálogo',
        icon: 'pi pi-fw pi-book',
        items: [
          { label: 'Productos', icon: 'pi pi-fw pi-shopping-bag', routerLink: '/products' },
          { label: 'Insumos', icon: 'pi pi-fw pi-box', routerLink: '/supplies' },
          { label: 'Recetas', icon: 'pi pi-fw pi-list' },
          { label: 'Promociones', icon: 'pi pi-fw pi-tags' },
        ],
      },
      {
        label: 'Producción',
        icon: 'pi pi-fw pi-cog',
        items: [
          { label: 'Lotes de producción', icon: 'pi pi-fw pi-th-large' },
          { label: 'Movimientos de insumos', icon: 'pi pi-fw pi-arrow-right-arrow-left' },
        ],
      },
      {
        label: 'Ventas',
        icon: 'pi pi-fw pi-shopping-cart',
        items: [{ label: 'Ventas', icon: 'pi pi-fw pi-receipt', routerLink: '/sales' }],
      },
      {
        label: 'Seguridad',
        icon: 'pi pi-fw pi-shield',
        items: [
          { label: 'Usuarios', icon: 'pi pi-fw pi-users' },
          { label: 'Roles', icon: 'pi pi-fw pi-id-card' },
        ],
      },
    ];
  }
}
