<!DOCTYPE html>
<html lang="pt-BR">
  <head>
    <meta charset="utf-8">
    <title>Cuidando do meu Bairro</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">

    <!-- Le HTML5 shim, for IE6-8 support of HTML5 elements -->
    <!--[if lt IE 9]>
      <script src="http://html5shim.googlecode.com/svn/trunk/html5.js"></script>
    <![endif]-->

		<!--favicon-->
		<link rel="shortcut icon" href="img/favicon.ico" type="image/x-icon"/>

    <!--CSS Styles-->
    <link href="css/bootstrap.min.css" rel="stylesheet">
    <link href="css/bootstrap-responsive.min.css" rel="stylesheet">
    <link href="css/docs.css" rel="stylesheet">
    <!--END OF CSS Styles-->
    
    <!--Javascript-->
		<script src="http://code.jquery.com/jquery-latest.min.js"></script>
    <script src="js/bootstrap.min.js"></script>
    <script src="js/application.js"></script>
		<script src="js/jquery.validate.js"></script>
		<script src="js/form-validator.js"></script>
  </head>

  <body>
    <?php include("header.inc.php"); ?>
    
    <div class="container">
			<div class="row">
		    <div class="span8 offset1">
		      <form method="post" class="form-horizontal well" id="contact-form" action="sendmail.php">
			      <?php
			    		$message = $_GET['message'];
			    		switch($message) {
			    			case 'emptyname':
			    				echo '<div class="alert alert-error">';
			    				echo '<strong>Erro:</strong> Por favor, preencha o campo \'Nome\'.';
			    				echo '</div>';
			    				break;
			    			case 'emptyemail':
			    				echo '<div class="alert alert-error">';
			    				echo '<strong>Erro:</strong> Por favor, preencha o campo \'E-mail\'.';
			    				echo '</div>';
			    				break;
			    			case 'emptymessage':
			    				echo '<div class="alert alert-error">';
			    				echo '<strong>Erro:</strong> Por favor, preencha o campo \'Mensagem\'.';
			    				echo '</div>';
			    				break;
			    			case 'invalidemail':
			    				echo '<div class="alert alert-error">';
			    				echo '<strong>Erro:</strong> Por favor, insira um e-mail válido.';
			    				echo '</div>';
			    				break;
			    			case 'success':
			    				echo '<div class="alert alert-success">';
			    				echo '<strong>Sucesso:</strong> O seu e-email foi enviado.';
			    				echo '</div>';
			    				break;
				   		}
			    	?>
		        <fieldset>
		          <legend>Contate-nos</legend>
		          
		          <div class="control-group">
		            <label class="control-label" for="name">Nome</label>
		            <div class="controls">
		              <input type="text" class="input-xlarge" id="name" name="name">
		              <p class="help-block">Digite o seu nome completo.</p>
		            </div>
    		      </div>
    		      
    		      <div class="control-group">
    		      	<label class="control-label" for="email">E-mail</label>
		            <div class="controls">
		              <input type="text" class="input-xlarge" id="email" name="email">
		              <p class="help-block">O e-mail deve ser válido.</p>
		            </div>
    		      </div>
    		      
    		      <div class="control-group">
    		      	<label class="control-label" for="message">Mensagem</label>
    		      	<div class="controls">
    		      		<textarea class="input-xlarge" id="message" name="message" rows="3"></textarea>
    		      	</div>
    		      </div>
    		      
    		      <div class="form-actions">
    		      	<button type="submit" class="btn btn-primary">Enviar</button>
    		      	<button type="reset" class="btn">Limpar</button>
    		      </div>
						</fieldset>
					</form>
				</div> <!--span7-->
			</div> <!--row-->
    </div> <!--Container-->

    <?php include("footer.inc.php"); ?>
  </body>
</html>
