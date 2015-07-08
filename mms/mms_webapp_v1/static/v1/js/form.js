// FormGet Online Form Builder Js Code
// Creating and Adding Dynamic Form Elements.

var i=1;   // Global Variable for Name
var j=1;   // Global Variable for Email
/*
=================
Creating Text Box in the Form Fields
=================
*/

function textBoxCreate()
{
	var y = document.createElement("INPUT");
	y.setAttribute("type", "text");
	y.setAttribute("Placeholder", "Name_" + i);
	y.setAttribute("Name","Name_" + i);
	document.getElementById("myForm").appendChild(y);
	i++;
}

/*
=================
Creating Textarea in the Form Fields
=================
*/
// function emailBoxCreate()
// {
// 	var y = document.createElement("INPUT");
// 	var t = document.createTextNode("Email");
// 	y.appendChild(t);
// 	y.setAttribute("Placeholder","Email_"+j);
// 	y.setAttribute("Name","Email_"+j);
// 	document.getElementById("myForm").appendChild(y);
// 	j++;
// }
