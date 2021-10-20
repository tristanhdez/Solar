<?php
  include("connection.php");
  action($connection);

  function action($connection){
    if(isset($_POST['insert'])){
      insert($connection);
      header("Location: form.php");
    }
  }
   
  function show($connection){
    $url ="edit.php?id=";
    $Result = mysqli_query($connection,"SELECT preguntas.id_pregunta, preguntas.keyword, preguntas.pregunta, preguntas.respuesta, etapas.etapa FROM preguntas  JOIN etapas ON preguntas.id_etapa = etapas.id_etapa");
    while($Row = mysqli_fetch_assoc($Result)){
        $id_question=$Row['id_pregunta'];
        echo "<tr>";  
        echo "<td>".$id_question;
        echo "<td>".$Row['pregunta'];
        echo "<td>".$Row['respuesta'];
        echo "<td>".$Row['etapa'];
        echo "<td>".$Row['keyword'];
        echo "<td><a href='$url$id_question'>Edit</a>";
        echo "<tr>"; 
    }
    mysqli_close($connection);
  }

  function showSpecific($connection){
    if(isset($_GET['id'])){
      $id=$_GET['id'];
      $query = "SELECT * FROM preguntas WHERE id_pregunta=$id";
      $result = mysqli_query($connection, $query);
      if (mysqli_num_rows($result) == 1){
        $row = mysqli_fetch_array($result);
        $id = $row['id_pregunta'];
        $question = $row['pregunta'];
        $answer = $row['respuesta'];
        $stage = $row['id_etapa'];
        $key = $row['keyword'];
        echo "<input name='idQues' type='text' value='$id'>";
        echo "<input name='ques' type='text' value='$question'>";
        echo "<input name='answ' type='text' value='$answer'>";
        echo "<input name='key' type='text' value='$key'>";
        echo "<input name='stag' type='text' value='$stage'>";
      }else{
        printf("error: %s\n", mysqli_error($connection));
      }
    }
    mysqli_close($connection);
  }

  function edit($connection){
    if(isset($_POST['submit'])){
      echo "yes";
      $id = $_POST['idQues'];
      $question = $_POST['ques'];
      $answer= $_POST['answ'];
      $stage= $_POST['stag'];
      $query = "UPDATE preguntas SET pregunta = $question, respuesta = $answer, id_etapa = $stage WHERE `preguntas`.`id_pregunta` = $id";
      mysqli_query($connection, $query);
    }else{
      echo "no";
    }
    mysqli_close($connection);
  }

  function insert($connection){
     
    $Question=$_POST['pregunta'];
    $Answer=$_POST['respuesta'];
    $Stage=$_POST['etapa'];
    $key = $_POST['keyword'];
    $Insert = "INSERT INTO preguntas(pregunta,respuesta,keyword,id_etapa) VALUES('$Question','$Answer','$key','$Stage')";

    mysqli_query($connection,$Insert);
    mysqli_close($connection);
  }
 
?>