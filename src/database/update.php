<?php
    include("crud.php"); 
    print_r($_POST);
    if(isset($_POST['id'])){
        header('Location: form.php?message=error');
    }
    $id = $_POST['idQues'];
    $question = $_POST['ques'];
    $answer= $_POST['answ'];
    $stage= $_POST['stag'];
    $key = $_POST['key'];
    echo $id, $question,$answer,$stage;
    $query = "UPDATE preguntas SET pregunta = '$question', respuesta = '$answer', keyword='$key', id_etapa = '$stage' WHERE id_pregunta = '$id'";
    $result = mysqli_query($connection, $query);
    if($result == TRUE){
        echo "done";
        header('Location:form.php?message=done');
    }else{
        echo "error";
        header('Location:form.php?message=error');
    }
    mysqli_close($connection);
?>