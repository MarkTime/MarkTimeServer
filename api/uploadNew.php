<?php
    if(move_uploaded_file($_FILES['uploaded_file']['tmp_name'], "/home/marktime/MarkTimeServer/MarkTime.db")) {
        file_put_contents("status", "uploaded\n");
        echo "success";

        $command = escapeshellcmd("python ../main.py");
        $output = shell_exec($command);
        echo $output;

        file_put_contents("log", $output);

    } else{
        echo "fail";
    }
 ?>
