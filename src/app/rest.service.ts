import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class RestService {

  constructor(private http : HttpClient) {}

	//soUrl : string = "https://st4rsend.net/flask/predict/";
	soUrl : string = "https://st4rsend.net/flask/";

	predict(str) {
		let urlStr: string;
		urlStr = this.soUrl + 'predict/' + str;
		//urlStr = this.soUrl + 'python';
		console.log(urlStr)
		return this.http.get(urlStr);
	}

	getModels() {
		let urlStr: string;
		urlStr = this.soUrl + 'models/';
		console.log(urlStr);
		return this.http.get(urlStr);

	}
}
