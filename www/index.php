<?php
error_reporting (E_ALL);	// Задает, какие ошибки PHP попадут в отчет
if (version_compare(phpversion(), '5.1.0', '<') == true) { die ('PHP5.1 Only'); }	// проверка версии PHP

// разделитель пути
define ('DIRSEP', DIRECTORY_SEPARATOR);

// Узнаём путь до файлов сайта
// realpath Возвращает канонизированный абсолютный путь к файлу
//dirname Возвращает имя родительского каталога из указанного пути
$site_path = realpath(dirname(__FILE__) . DIRSEP . '..' . DIRSEP) . DIRSEP;
define ('site_path', $site_path);

# Соединяемся с БД
$db = new PDO('mysql:host=localhost;dbname=demo', '[user]', '[password]');
$registry->set ('db', $db);	// глобальный доступ к переменной db

# Создаём шаблон
$template = new Template($registry);
$registry->set ('template', $template);

$router = new Router($registry);	//создание маршрутизатора
$registry->set ('router', $router);
$router->setPath (site_path . 'controllers');	// вызов функции setPath
$router->delegate();	// вызов функции delegate

function delegate() {
        // Анализируем путь
        $this->getController($file, $controller, $action, $args);
		// Файл доступен?
        if (is_readable($file) == false) {
                die ('404 Not Found');
        }
        // Подключаем файл
        include ($file);
        // Создаём экземпляр контроллера
        $class = 'Controller_'.$controller;
        $controller = new $class($this->registry);
        // Действие доступно?
        if (is_callable(array($controller, $action)) == false) {
                die ('404 Not Found');
        }
        // Выполняем действие
        $controller->$action();
}

private function getController(&$file, &$controller, &$action, &$args) {
	$route = (empty($_GET['route'])) ? '' : $_GET['route'];	// берет значение route из запроса
    if (empty($route)) { $route = 'index'; }
        // Получаем раздельные части
        $route = trim($route, '/\\');
        $parts = explode('/', $route);	// запрос преобразуется в такой массив: array(‘...’, ‘...’)
        $cmd_path = $this->path;
        // проходим по каждой части и проверяем является ли она директорией 
    foreach ($parts as $part) {
        $fullpath = $cmd_path.$part;
        if (is_dir($fullpath)) {
			$cmd_path .= $part.DIRSEP;
            array_shift($parts);	//извлекает первое значение массива array и возвращает его, сокращая размер array на один элемент
            continue;
        }
        // Если же текущая часть запроса не является директорией, 
        //но является файлом, она сохраняется в переменную $controller, 
        //и мы выходим из цикла, так как нашёлся контроллер, который нам нужен
        if (is_file($fullpath.'.php')) {
            $controller = $part;
            array_shift($parts);
            break;
        }
    }
    // После цикла мы проверяем переменную с именем контроллера. Если она пустая, то используем контроллер «index»
    if (empty($controller)) { $controller = 'index'; };
    $action = array_shift($parts);
    if (empty($action)) { $action = 'index'; }
    $file = $cmd_path.$controller.'.php';	//полный путь до файла контроллера, объединяя три переменные: путь, имя контроллера и расширение «php»
    $args = $parts;
}

// установка значений переменных, доступных в шаблонах
function set($varname, $value, $overwrite=false) {
	// Определяет, была ли установлена переменная значением отличным от NULL
        if (isset($this->vars[$varname]) == true AND $overwrite == false) {	                
                // Вызывает пользовательскую ошибку/предупреждение/уведомление
                trigger_error ('Unable to set var `' . $varname . '`. Already set, and overwrite not allowed.', E_USER_NOTICE);
                return false;
        }
        $this->vars[$varname] = $value;
        return true;
}

// удаление значений переменных, доступных в шаблонах
function remove($varname) {
        unset($this->vars[$varname]);	//Удаляет переменную
        return true;
}
?>
