<?php include("crud.php"); ?>
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta http-equiv="X-UA-Compatible" content="IE=edge">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <link rel="icon" href="">
  <title>Formulario</title>
</head>
<body>

  <h1>Formulario</h1>
  <br>
  <form action="crud.php" method="post">
    <p>pregunta <input type="text" name="pregunta" size="40" value=""></p>
    <br>
    <p>respuesta <input type="text" name="respuesta" size="40"></p>
    <br>
    <p>palabra clave <input type="text" name="keyword" size="40"></p>
    <br>
    <p>Etapa a la que pertenece
      <select name="etapa">
        <option value ="1">Inicial</option>
        <option value ="2">Media</option>
        <option value ="3">Final</option>
      </select>
    </p>
    <br>
    <br>
    <button type="submit" name="insert">Insertar</button>
  </form>
<table>
  <tr>
    <th>#</th>
    <th>PREGUNTAS</th>
    <th>RESPUESTAS</th>
    <th>ETAPAS</th>
    <th>PALABRA CLAVE (EN MINÚSCULA, SIN TILDES Y ESPACIOS EJ: asesoriatutor)</th>
    <th>ACCIÓN</th>
  </tr>
  <tr>
    <?php show($connection);?>
  </tr>
</table>
</body>
</HTML>