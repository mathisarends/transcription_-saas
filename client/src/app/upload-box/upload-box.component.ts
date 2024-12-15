import {Component, ElementRef, HostBinding, HostListener, Renderer2, signal, viewChild} from '@angular/core';
import { MatButtonModule } from '@angular/material/button';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatIconModule } from '@angular/material/icon';
import {ProgressBarComponent} from "../progress-bar/progress-bar.component";

@Component({
  selector: 'app-upload-box',
  standalone: true,
  imports: [MatFormFieldModule, MatInputModule, MatIconModule, MatButtonModule],
  templateUrl: './upload-box.component.html',
  styleUrl: './upload-box.component.scss',
})
export class UploadBoxComponent {
  fileInput = viewChild("fileInput")
  uploadValue = signal(0);

  @HostBinding('class.dragover') isDragOver = signal(false);

  openFileSelector(): void {
    if (!this.fileInput()) {
      return;
    }

    (this.fileInput() as ElementRef).nativeElement.click();
  }

  @HostListener('dragover', ['$event'])
  onDragOver(event: DragEvent): void {
    console.log("event", event);
    event.preventDefault();
    this.isDragOver.set(true);
  }

  @HostListener('dragleave', ['$event'])
  onDragLeave(event: DragEvent): void {
    event.preventDefault();
    this.isDragOver.set(false);
  }

  @HostListener('drop', ['$event'])
  onFileDrop(event: DragEvent): void {
    event.preventDefault();

    this.isDragOver.set(false);
    this.handleFiles(event.dataTransfer?.files);
  }

  onFileSelected(event: Event): void {
    const input = event.target as HTMLInputElement;
    this.handleFiles(input.files);
  }

  private handleFiles(fileList: FileList | null | undefined): void {
    if (!fileList) return;

    const allowedTypes = ['audio/mp3', 'audio/wav'];
    const files = Array.from(fileList).filter((file) =>
      allowedTypes.includes(file.type)
    );

    if (files.length > 0) {
      console.log('Ausgewählte Dateien:', files);
      this.simulateUpload();
    } else {
      console.warn('Nur MP3- und WAV-Dateien sind erlaubt.');
    }
  }

  private simulateUpload(): void {
    this.uploadValue.set(0);
    const interval = setInterval(() => {
      const currentValue = this.uploadValue();
      if (currentValue >= 100) {
        clearInterval(interval);
        console.log('Upload abgeschlossen');
      } else {
        this.uploadValue.set(currentValue + 10);
      }
    }, 500);
  }
}
