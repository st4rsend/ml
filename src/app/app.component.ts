import { Component, OnInit } from '@angular/core';
import { RestService } from './rest.service';
import { FormControl, FormGroup } from '@angular/forms';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent implements OnInit {
  title = 'ml-angular';
	public response = ["initial", "string"];
	getForm= new FormGroup({
		inputText: new FormControl('')
	})


	constructor(private rs: RestService){}

	ngOnInit() {
	//	this.getForm = this.formBuilder.group({
	//		input_text: new FormControl('')
	//	});
	}

	onSubmit(){
		console.log(this.getForm.get('inputText').value);
		this.rs.predict(this.getForm.get('inputText').value).subscribe(
			(response) => {
				this.response = response["tags"];
				//console.log(response['tags']);
			},
			(error) => {
				console.log("Error");
			}
		)
	}
}
