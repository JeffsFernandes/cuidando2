var message = 'Este campo é obrigatório.';

$(document).ready(function() {
  $("#name").validate({
    expression: "if(VAL != '') return true; else return false;",
    message: message
  });

  $("#email").validate({
    expression: "if(VAL != '') return true; else return false;",
    message: message
	});

  $("#message").validate({
    expression: "if(VAL != '') return true; else return false;",
    message: message
	});
});
