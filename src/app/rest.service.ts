import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class RestService {

  constructor(private http : HttpClient) {}

	//soUrl : string = "https://st4rsend.net/flask/predict/python%20df";
	soUrl : string = "https://st4rsend.net/flask/predict/";

	predict(str) {
		let urlStr: string;
		urlStr = this.soUrl + str;
		//urlStr = this.soUrl + 'python';
		console.log(urlStr)
		return this.http.get(urlStr);
	}
}
