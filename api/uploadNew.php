<?php
    if(move_uploaded_file($_FILES['uploaded_file']['tmp_name'], "/home/marktime/MarkTimeServer/MarkTime.db")) {
        file_put_contents("status", "uploaded\n");
        echo "success";
    } else{
        echo "fail";
    }
 ?>
