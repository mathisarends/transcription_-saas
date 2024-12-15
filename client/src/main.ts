import { bootstrapApplication } from '@angular/platform-browser';
import { provideAnimations } from '@angular/platform-browser/animations';
import { MATERIAL_PROVIDERS } from './app/material-imports';
import { AppComponent } from './app/app.component';

bootstrapApplication(AppComponent, {
  providers: [
    provideAnimations(),
    ...MATERIAL_PROVIDERS, // Globale Bereitstellung der Material-Module
  ],
}).catch((err) => console.error(err));
