<?php include("crud.php");

if(!isset($_GET['id'])){
  header('Location: index.php?message=error');
}
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
</head>
<body>
  <form action='update.php' method="POST">
    <?php showSpecific($connection);?>
    <button type='submit' name='submit'>Enviar</button>
  </form>
</html>