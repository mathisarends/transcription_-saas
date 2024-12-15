import { Component } from '@angular/core';
import { MatButtonModule } from '@angular/material/button';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatIconModule } from '@angular/material/icon';

@Component({
  selector: 'app-upload-box',
  standalone: true,
  imports: [MatFormFieldModule, MatInputModule, MatIconModule, MatButtonModule],
  templateUrl: './upload-box.component.html',
  styleUrl: './upload-box.component.scss',
})
export class UploadBoxComponent {
  openFileSelector(): void {
    const fileInput = document.getElementById('fileInput') as HTMLInputElement;
    fileInput.click();
  }

  // Wird aufgerufen, wenn Dateien per Drag & Drop fallen gelassen werden
  onFileDrop(event: DragEvent): void {
    event.preventDefault();
    this.handleFiles(event.dataTransfer?.files);
    this.removeDragClass();
  }

  // Fügt einen visuellen Hinweis beim Drag hinzu
  onDragOver(event: DragEvent): void {
    event.preventDefault();
    (event.currentTarget as HTMLElement).classList.add('dragover');
  }

  // Entfernt den visuellen Hinweis beim Verlassen
  onDragLeave(event: DragEvent): void {
    this.removeDragClass();
  }

  // Wird aufgerufen, wenn Dateien über das File-Input ausgewählt werden
  onFileSelected(event: Event): void {
    const target = event.target as HTMLInputElement;
    this.handleFiles(target.files);
  }

  // Dateien verarbeiten
  private handleFiles(fileList: FileList | null | undefined): void {
    if (!fileList) return;

    const allowedTypes = ['audio/mp3', 'audio/wav'];
    const files = Array.from(fileList).filter((file) =>
      allowedTypes.includes(file.type)
    );

    if (files.length > 0) {
      console.log('Ausgewählte Dateien:', files);
    } else {
      console.warn('Nur MP3- und WAV-Dateien sind erlaubt.');
    }
  }

  private removeDragClass(): void {
    const uploadBox = document.querySelector('.upload-box');
    uploadBox?.classList.remove('dragover');
  }
}
