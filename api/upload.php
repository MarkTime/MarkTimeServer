<?php
    $directory = '/home/marktime/MarkTimeServer';
    $filename = basename($_FILES['file']['name']);
    if(strrchr($_FILES['file']['name'], '.')=='.db') {
        if(move_uploaded_file($_FILES['file']['tmp_name'], $directory. $filename)) {

        }
    }
?>