import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { OnInit } from '@angular/core';
import { initFlowbite } from 'flowbite';
import { CommonModule } from '@angular/common';
import { HttpClientModule } from '@angular/common/http';
import { ApiService } from './api.service';

interface URLField {
  index: number;
  value: string;
}

@Component({
  selector: 'app-root',
  standalone: true,
  providers: [ApiService],
  imports: [RouterOutlet, CommonModule, HttpClientModule],
  templateUrl: './app.component.html',
  styleUrl: './app.component.css'
})
export class AppComponent implements OnInit {
  title = 'frontend';

  question: string = "What are our product design decisions?";
  documentUrlsValue: string = `http://test-fileserver:8081/call_log_gfsfdfd.txt
http://test-fileserver:8081/call_log_fdadweq.txt
http://test-fileserver:8081/call_log_sdfqwer.txt
  `

  loading = false;
  facts: string[] = [];

  constructor(private apiService: ApiService) {}

  getDocumentUrls() {
    return this.documentUrlsValue.split("\n").filter(s => !!s);
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
    const documentUrls = this.getDocumentUrls();
    if (!this.question || documentUrls.length === 0) {
      return;
    }
    this.apiService.extractFactsAndPollForResults(this.question, documentUrls).subscribe(data => {
        console.log(data)
        this.facts = data.facts;
        this.loading = false;
    })
  }
}
