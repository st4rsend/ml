import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class RestService {

  constructor(private http : HttpClient) {}

	soUrl : string = "https://st4rsend.net/flask/";

	predict(json) {
		let urlStr: string;
		urlStr = this.soUrl +'predict/';
		//console.log(json);
		return this.http.post(urlStr, json);
	}

	getModels() {
		let urlStr: string;
		urlStr = this.soUrl + 'models/';
		//console.log(urlStr);
		return this.http.get(urlStr);

	}
}
