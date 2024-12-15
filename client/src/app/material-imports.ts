import { importProvidersFrom } from '@angular/core';
import { MatButtonModule } from '@angular/material/button';
import { MatToolbarModule } from '@angular/material/toolbar';
import { MatIconModule } from '@angular/material/icon';
import { MatSidenavModule } from '@angular/material/sidenav';

export const MATERIAL_PROVIDERS = [
  importProvidersFrom(
    MatButtonModule,
    MatToolbarModule,
    MatIconModule,
    MatSidenavModule
  ),
];
