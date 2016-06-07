<?php


Class Router {
        private $registry;
        private $path;
        private $args = array();

        function __construct($registry) {       // конструктор объекта $registry
                $this->registry = $registry;
        }
}

function setPath($path) {       // установка диреткории, в которой будут храниться контроллеры
        $path = trim($path, '/\\');     // Удаляет пробелы (или другие символы) из начала и конца строки
        $path .= DIRSEP;

        if (is_dir($path) == false) {   // если имя файла не являается директорией, выскочит ошибка
                throw new Exception ('Invalid controller path: `' . $path . '`');       
        }
        $this->path = $path;
}
?>
