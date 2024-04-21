import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { OnInit } from '@angular/core';
import { initFlowbite } from 'flowbite';
import { CommonModule } from '@angular/common';
import { HttpClientModule } from '@angular/common/http';
import { NgIconComponent, provideIcons } from '@ng-icons/core';
import { faEnvelope } from '@ng-icons/font-awesome/regular'
import { faBrandGithub, faBrandLinkedin } from '@ng-icons/font-awesome/brands'

import { ApiService } from './api.service';
import { environment } from '../environments/environment';

interface URLField {
  index: number;
  value: string;
}

@Component({
  selector: 'app-root',
  standalone: true,
  providers: [ApiService, provideIcons({ faBrandGithub, faBrandLinkedin, faEnvelope })],
  imports: [
    RouterOutlet, 
    CommonModule, 
    HttpClientModule, 
    NgIconComponent
  ],
  templateUrl: './app.component.html',
  styleUrl: './app.component.css'
})
export class AppComponent implements OnInit {
  title = 'frontend';

  question: string = '';
  documentUrlsValue: string = '';

  loading = false;
  facts: string[] = [];
  errors: string[] = [];

  constructor(private apiService: ApiService) { }

  get hasErrors() {
    return this.errors.length > 0;
  }
  getDocumentUrls() {
    return this.documentUrlsValue.split('\n').filter(s => !!s.trim());
  }

  ngOnInit(): void {
    initFlowbite();
  }

  onQuestionValueChange(event: any) {
    this.question = event.srcElement.value;
  }

  onURLValueChange(event: any) {
    const value: string = (event.target as any).value;
    this.documentUrlsValue = value.trim();
  }

  extractFacts() {
    this.loading = true;
    this.errors = [];
    const documentUrls = this.getDocumentUrls();
    if (!this.question || documentUrls.length === 0) {
      this.loading = false;
      return;
    }
    this.apiService.extractFactsAndPollForResults(this.question, documentUrls).subscribe(res => {
      console.log(res)
      if (res.status === 'done') {
        this.facts = res.facts;
        this.errors = res.errors;
        this.loading = false;
      }
    });
  }

  loadExample() {
    this.facts = [];
    this.question = 'What are our product design decisions?';
    const exampleFiles = ['call_log_gfsfdfd.txt', 'call_log_fdadweq.txt', 'call_log_sdfqwer.txt'];
    this. documentUrlsValue = exampleFiles.map(f => `${environment.exampleServerUrl}/${f}`).join('\n')
  }
}
