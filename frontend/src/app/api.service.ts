import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable, concat, filter, first, interval, map, of, repeat, shareReplay, startWith, switchMap, takeUntil, takeWhile, timer, withLatestFrom } from 'rxjs';
import { environment } from '../environments/environment';

interface GetFactsResponse {
  question: string;
  facts: string[];
  errors: string[];
  status: "processing" | "done";
}

interface ExtractFactsResponse {
  request_id: string;
}

@Injectable({
  providedIn: 'root'
})
export class ApiService {

  constructor(private http: HttpClient) { }

  public extractFacts(question: string, documentUrls: string[]): Observable<ExtractFactsResponse> {
    const data = {
        "question": question,
        "documents": documentUrls,
    }
    return this.http.post<ExtractFactsResponse>(`${environment.apiUrl}/submit_question_and_documents`, data)
  }

  public getFacts(): Observable<GetFactsResponse> {
    return this.http.get<GetFactsResponse>(`${environment.apiUrl}/get_question_and_facts`)
  }

  public extractFactsAndPollForResults(question: string, documentUrls: string[]): Observable<GetFactsResponse> {
    const submitJob = this.extractFacts(question, documentUrls).pipe(shareReplay());
    const pollForJobCompletion = timer(0, 1000).pipe(
      withLatestFrom(submitJob),
      switchMap(([ _, _res ]) => this.getFacts()),
      takeWhile(val => val.status != "done", true)
    );
    return pollForJobCompletion;
  }
    

}
