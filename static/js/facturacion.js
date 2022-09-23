$(document).ready(function() {
    var $select1 = $('.select1'),
        $select2 = $('.select2'),
        $options = $select2.find('option');
    $select1.on('change', function() {
        $select2.html($options.filter('[data-index-number="' + this.value + '"]'));
    }).tigger('change');
});

// En la carga de la página o al cambiar de tema, es mejor agregar en línea en `head` para evitar FOUC
if (localStorage.theme === 'dark' || (!('theme' in localStorage) && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
    document.documentElement.classList.add('dark')
  } else {
    document.documentElement.classList.remove('dark')
  }
  
  // Siempre que el usuario elija explícitamente el modo de luz
  localStorage.theme = 'light'
  
  // Siempre que el usuario elija explícitamente el modo oscuro
  localStorage.theme = 'dark'
  
  // Siempre que el usuario elija explícitamente respetar la preferencia del sistema operativo
  localStorage.removeItem('theme')