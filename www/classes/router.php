<?php


Class Router {

        private $registry;

        private $path;

        private $args = array();


        function __construct($registry) {

                $this->registry = $registry;

        }


}

function setPath($path) {

        $path = trim($path, '/\\');

        $path .= DIRSEP;


        if (is_dir($path) == false) {

                throw new Exception ('Invalid controller path: `' . $path . '`');

        }


        $this->path = $path;

}

?>