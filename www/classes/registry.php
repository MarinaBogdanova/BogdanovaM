<?php


Class Registry Implements ArrayAccess {
        private $vars = array();
}

	// сохраняет значения
	function set($key, $var) {
        if (isset($this->vars[$key]) == true) {
                throw new Exception('Unable to set var `' . $key . '`. Already set.');	// сообщение об ошибке
        }
        $this->vars[$key] = $var;
        return true;

}

	// Возвращает массив переменных. В случае ошибки будет возвращен NULL.
	function get($key) {
        if (isset($this->vars[$key]) == false) {
                return null;
        }
        return $this->vars[$key];
}

	// удаление переменных
	function remove($var) {
        unset($this->vars[$key]);
}

function offsetExists($offset) {	// пределяет, существует ли заданный ключ
         return isset($this->vars[$offset]);
}

function offsetGet($offset) {	//Возвращает значение по указанному индексу
        return $this->get($offset);
}


function offsetSet($offset, $value) {	// Устанавливает новое значение по указанному индексу
        $this->set($offset, $value);
}


function offsetUnset($offset) {	// Удаляет значение по указанному индексу
        unset($this->vars[$offset]);
}
?>
