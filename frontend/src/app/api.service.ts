import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable, concat, filter, first, interval, map, of, repeat, shareReplay, startWith, switchMap, takeUntil, takeWhile, timer, withLatestFrom } from 'rxjs';
import { environment } from '../environments/environment';

interface GetFactsResponse {
  question: string;
  facts: string[];
  status: "processing" | "done";
}

interface ExtractFactsResponse {
  requestId: string;
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

  public getFactsById(requestId: string): Observable<GetFactsResponse> {
    return this.http.get<GetFactsResponse>(`${environment.apiUrl}/get_question_and_facts/${requestId}`)
  }

  public extractFactsAndPollForResults(question: string, documentUrls: string[]): Observable<GetFactsResponse> {
    // return this.extractFacts(question, documentUrls).pipe(
    //   switchMap(
    //     (results) => this.getFactsById(results.requestId).pipe(
    //         repeat({ delay: 3000 }),
    //         takeWhile((response) => response.status === "processing", true)
    //       )
    //     )
    // )
    // return this.extractFacts(question, documentUrls).pipe(
    //   switchMap((response: ExtractFactsResponse) => 
    //     interval(1000).pipe(
    //       startWith(0),
    //       switchMap(() => this.getFacts()),
    //       takeUntil(this.getFactsById(response.requestId).pipe(
    //         filter((factResponse: GetFactsResponse) => factResponse.status === "done")
    //       ))
    //     )
    //   )
    // );

    const init$ = this.extractFacts(question, documentUrls).pipe(shareReplay());
    const poll$ = timer(0, 3000).pipe(
      withLatestFrom(init$),
      switchMap(([ _, res ]) => this.getFacts()),
      takeWhile(val => val.status != "done", true)
    );
    return poll$;
  }
}
