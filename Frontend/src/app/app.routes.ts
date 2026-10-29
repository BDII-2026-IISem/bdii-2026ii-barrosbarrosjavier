import { Routes } from '@angular/router';
import { Login } from './components/auth/login/login';
import { authGuard } from './guards/auth-guard';

// Cada pantalla se carga al abrirla (loadComponent); así no viaja en el paquete inicial
export const routes: Routes = [
  {
    path: '',
    redirectTo: 'login',
    pathMatch: 'full',
  },
  {
    path: 'login',
    component: Login,
  },
  {
    path: 'profile',
    loadComponent: () => import('./components/auth/profile/profile').then((m) => m.Profile),
    canActivate: [authGuard],
  },
  {
    path: 'supplies',
    loadComponent: () => import('./components/supply/getall/getall').then((m) => m.Getall),
    canActivate: [authGuard],
  },
  {
    path: 'supplies/new',
    loadComponent: () => import('./components/supply/create/create').then((m) => m.Create),
    canActivate: [authGuard],
  },
  {
    path: 'supplies/edit/:id',
    loadComponent: () => import('./components/supply/update/update').then((m) => m.Update),
    canActivate: [authGuard],
  },
  {
    path: 'supplies/delete/:id',
    loadComponent: () => import('./components/supply/delete/delete').then((m) => m.Delete),
    canActivate: [authGuard],
  },
  {
    path: 'products',
    loadComponent: () => import('./components/product/getall/getall').then((m) => m.Getall),
    canActivate: [authGuard],
  },
  {
    path: 'products/new',
    loadComponent: () => import('./components/product/create/create').then((m) => m.Create),
    canActivate: [authGuard],
  },
  {
    path: 'products/edit/:id',
    loadComponent: () => import('./components/product/update/update').then((m) => m.Update),
    canActivate: [authGuard],
  },
  {
    path: 'products/delete/:id',
    loadComponent: () => import('./components/product/delete/delete').then((m) => m.Delete),
    canActivate: [authGuard],
  },
  {
    path: 'sales',
    loadComponent: () => import('./components/sale/getall/getall').then((m) => m.Getall),
    canActivate: [authGuard],
  },
  {
    path: 'sales/new',
    loadComponent: () => import('./components/sale/create/create').then((m) => m.Create),
    canActivate: [authGuard],
  },
  {
    path: 'sales/edit/:id',
    loadComponent: () => import('./components/sale/update/update').then((m) => m.Update),
    canActivate: [authGuard],
  },
  {
    path: 'sales/delete/:id',
    loadComponent: () => import('./components/sale/delete/delete').then((m) => m.Delete),
    canActivate: [authGuard],
  },
  {
    path: '**',
    redirectTo: 'login',
  },
];
