<?php
	// parameters
	$name = $_POST['name'];
	$sender = $_POST['email'];
	$message = $_POST['message'];
	
	if(empty($name)) {
		header("location:contact.php?message=emptyname");
	} else if(empty($sender)) {
		header("location:contact.php?message=emptyemail");
	} else if(empty($message)) {
		header("location:contact.php?message=emptymessage");
	} else if(!filter_var($sender, FILTER_VALIDATE_EMAIL)) {
		header("location:contact.php?message=invalidemail");
	} else {
		$to = "cuidando@gpopai.org";
		$subject = "[CUIDANDO DO MEU BAIRRO] Mensagem de " . $name;
		mail($to, $subject, $message, 'From:'.$sender."\r\n");
		header("location:contact.php?message=success");
	}
?>
