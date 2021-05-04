import { Component, OnInit } from '@angular/core';
import { RestService } from './rest.service';
import { FormControl, FormGroup } from '@angular/forms';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent implements OnInit {
  title = 'St4rsend Machine Learning (ML) corner';
	response: ['a','b'];
	getForm= new FormGroup({
		inputTitle: new FormControl(''),
		inputText: new FormControl('')
	})

	public models: string;


	constructor(private rs: RestService){}

	ngOnInit() {
	//	this.getForm = this.formBuilder.group({
	//		input_text: new FormControl('')
	//	});
	}

	onSubmit(){
		//var model = "baseline";
		var model = "vector";
		var threshold = .20;
		var json = {
			"model": model,
 			"threshold": threshold,
 			"title": this.getForm.get('inputTitle').value,
 			"body": this.getForm.get('inputText').value
		};
		this.rs.predict(
						json
					).subscribe(
			(response) => {
				this.response = response["tags"];
				//console.log(response['tags']);
			},
			(error) => {
				console.log("Error");
			}
		)
	}

	getModels(){
		this.rs.getModels().subscribe(
			(models) => {
				//this.models = models;
				console.log(models);
			},
			(error) => {
				console.log("Error");
			}

		)
	}
}
