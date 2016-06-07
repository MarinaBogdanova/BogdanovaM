<?php

// Динамическая загрузка классов
function __autoload($class_name) {
        $filename = strtolower($class_name).'.php';     // функция берет имя класса
        $file = site_path.'classes'.DIRSEP.$filename;   // проверяет, существует ли файл с похожим именем в дериктории с классами

        if (file_exists($file) == false) {      // если класса нет, выскочит ошибка
                return false;
        }
        include ($file);        //если класс существует он будет загружен
}

$registry = new Registry;
?>
