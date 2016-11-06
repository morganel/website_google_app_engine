function myFunction() {
	document.getElementById("demo").innerHTML = "Paragraph changed.";
}

document.getElementById("myBtn").addEventListener("click", displayDate);

function displayDate() {
    document.getElementById("demo2").innerHTML = Date();
}

$(document).ready(function(){
    alert('jquery is loaded')


	$("#demo3").on("click", function(){
		console.log('hahaahahhah')
	    $(this).hide(1000,myFunction);
	});

});

function displayAnotherAlert(s) {
	alert(s)
}