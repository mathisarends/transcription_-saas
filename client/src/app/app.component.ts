import {Component, signal} from '@angular/core';
import { MatButtonModule } from '@angular/material/button';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { HeaderComponent } from './header/header.component';
import { MatIconModule } from '@angular/material/icon';
import { UploadBoxComponent } from './upload-box/upload-box.component';
import {ProgressBarComponent} from "./progress-bar/progress-bar.component";

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [
    MatButtonModule,
    HeaderComponent,
    MatFormFieldModule,
    MatInputModule,
    MatIconModule,
    UploadBoxComponent,
    ],
  templateUrl: './app.component.html',
  styleUrl: './app.component.scss',
})
export class AppComponent {
  value = signal(40);
}
