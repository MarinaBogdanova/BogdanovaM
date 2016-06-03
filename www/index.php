<?php
error_reporting (E_ALL);
if (version_compare(phpversion(), '5.1.0', '<') == true) { die ('PHP5.1 Only'); }

// Константы:
define ('DIRSEP', DIRECTORY_SEPARATOR);

// Узнаём путь до файлов сайта
$site_path = realpath(dirname(__FILE__) . DIRSEP . '..' . DIRSEP) . DIRSEP;
define ('site_path', $site_path);

# Соединяемся с БД
$db = new PDO('mysql:host=localhost;dbname=demo', '[user]', '[password]');
$registry->set ('db', $db);

# Создаём объект шаблонов
$template = new Template($registry);
$registry->set ('template', $template);

# Загружаем router
$router = new Router($registry);
$registry->set ('router', $router);
$router->setPath (site_path . 'controllers');
$router->delegate();

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
        $class = 'Controller_' . $controller;
        $controller = new $class($this->registry);
        // Действие доступно?
        if (is_callable(array($controller, $action)) == false) {
                die ('404 Not Found');
        }
        // Выполняем действие
        $controller->$action();
}

private function getController(&$file, &$controller, &$action, &$args) {
	$route = (empty($_GET['route'])) ? '' : $_GET['route'];
    if (empty($route)) { $route = 'index'; }
        // Получаем раздельные части
        $route = trim($route, '/\\');
        $parts = explode('/', $route);
        // Находим правильный контроллер
        $cmd_path = $this->path;
    foreach ($parts as $part) {
        $fullpath = $cmd_path . $part;
        // Есть ли папка с таким путём?
        if (is_dir($fullpath)) {
			$cmd_path .= $part . DIRSEP;
            array_shift($parts);
            continue;
        }
        // Находим файл
        if (is_file($fullpath . '.php')) {
            $controller = $part;
            array_shift($parts);
            break;
        }
    }
    if (empty($controller)) { $controller = 'index'; };
    // Получаем действие
    $action = array_shift($parts);
    if (empty($action)) { $action = 'index'; }
    $file = $cmd_path . $controller . '.php';
    $args = $parts;
}

function set($varname, $value, $overwrite=false) {
        if (isset($this->vars[$varname]) == true AND $overwrite == false) {
                trigger_error ('Unable to set var `' . $varname . '`. Already set, and overwrite not allowed.', E_USER_NOTICE);
                return false;
        }
        $this->vars[$varname] = $value;
        return true;
}
function remove($varname) {
        unset($this->vars[$varname]);
        return true;
}
?>