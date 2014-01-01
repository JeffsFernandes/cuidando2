$("#address").keypress(function(event){
  if(event.keyCode == 13){
	event.preventDefault();
	codeAddress();
	return false;
}
});