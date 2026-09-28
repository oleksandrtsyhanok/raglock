import { Routes } from '@angular/router';

export const routes: Routes = [
    {
        path: '',
        pathMatch: 'full',
        loadComponent: () => {
            return import('./home/home').then(
                m => m.Home
            )
        }
    },
    {
        path: 'settings',
        pathMatch: 'full',
        loadComponent: () => {
            return import('./settings/settings').then(
                m => m.Settings
            )
        }
    },
    {
        path: 'home',
        redirectTo: '',
        pathMatch: 'full'
    }
];
