<?php
  include("preguntas.php");
?>

<HTML>
<TITLE>
Formulario preguntas
</TITLE>
<HEAD>
</HEAD>
<BODY>

<H1>FORMULARIO PARA AGREGAR PREGUNTAS</H1>
<BR>
<FORM action="preguntas.php" method="post">
  <p>pregunta <input type="text" name="pregunta" size="40"></p>
<BR>
  <p>respuesta <input type="text" name="respuesta" size="40"></p>
<BR>
<p>Etapa a la que pertenece
<select name="etapa">
  <option value ="1">Inicial</option>
  <option value ="2">Media</option>
  <option value ="3">Final</option>
</select>
</p>
<BR>
<BR>
  <button type="submit" name="insertar">Insertar</button>
</FORM>

<table>

  <tr>

    <th>ID</th>
    <th>PREGUNTAS</th>
    <th>RESPUESTAS</th>
    <th>ETAPAS</th>

  </tr>
  <tr>
    <?php mostrar($Conexion); ?>
  </tr>

</table>

</BODY>
</HTML>