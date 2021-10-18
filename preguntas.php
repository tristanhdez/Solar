<?php

   $Conexion = mysqli_connect   ('localhost','root','','tutorias') or die("No se    conecto con la BD");
   mysqli_set_charset($Conexion,"utf8");
   
   accion($Conexion);

   function accion($Conexion){
     if(isset($_POST['insertar'])){
       insertar($Conexion);
       header("Location: formulario.php");
     }
     
   }
   
   function mostrar($Conexion){
     
     $Resultado = mysqli_query($Conexion,"SELECT preguntas.id_pregunta, preguntas.pregunta, preguntas.respuesta, etapas.etapa FROM preguntas  JOIN etapas ON preguntas.id_etapa = etapas.id_etapa");

     while($Fila = mysqli_fetch_array($Resultado)){
     echo "<tr>";  
     echo "<td>".$Fila['id_pregunta'];
     echo "<td>".$Fila['pregunta'];
     echo "<td>".$Fila['respuesta'];
     echo "<td>".$Fila['etapa'];
     echo "<tr>"; 
     }
     mysqli_close($Conexion);
   }

   function insertar($Conexion){
     
     $Pregunta=$_POST['pregunta'];
     $Respuesta=$_POST['respuesta'];
     $Etapa=$_POST['etapa'];
     
     $Insertar = "INSERT INTO preguntas     (pregunta,respuesta,id_etapa) VALUES     ('$Pregunta','$Respuesta','$Etapa')";

      mysqli_query($Conexion,$Insertar);
      mysqli_close($Conexion);
   }
   
 
?>