$title = "How to correctly use panda's slice/replace with values form another column and then explode a row into two"
$body = "I'm working with a DataFrame that looks like this: And what I'm trying to do is basically first replace the part of the string in  that's in between the values of  and , to then explode the two pieces of the string left into two different lines (probably using Panda's explode). I.e: First expected result: To then get: I'm trying to use the following code: But the column  that I'm getting is full of NaN. I suppose it has to do with how I'm using start and stop. I could use some help with this, and also with how to later divide the rows according to the gaps. I hope I was clear enough, thanks in advance!"
$json=@"
{\"model\": \"vector\", \"threshold\": 0.20, \"title\": \"$title\", \"body\": \"$body\"}
"@
curl.exe -X POST -H 'Content-Type: application/json' `
-d  $json http://127.0.0.1:5000/flask/predict/