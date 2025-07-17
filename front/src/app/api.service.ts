import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root',
})
export class ApiService {
  constructor(private http: HttpClient) {}

  sendQuery(input: string) {
    return this.http.post('http://localhost:8000/process-user-prompt', { prompt: input });
  }
}
