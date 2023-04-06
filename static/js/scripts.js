/*!
* Start Bootstrap - Scrolling Nav v5.0.5 (https://startbootstrap.com/template/scrolling-nav)
* Copyright 2013-2022 Start Bootstrap
* Licensed under MIT (https://github.com/StartBootstrap/startbootstrap-scrolling-nav/blob/master/LICENSE)
*/
//
// Scripts
// 

window.addEventListener('DOMContentLoaded', event => {

    // Activate Bootstrap scrollspy on the main nav element
    const mainNav = document.body.querySelector('#mainNav');
    if (mainNav) {
        new bootstrap.ScrollSpy(document.body, {
            target: '#mainNav',
            offset: 74,
        });
    };

    // Collapse responsive navbar when toggler is visible
    const navbarToggler = document.body.querySelector('.navbar-toggler');
    const responsiveNavItems = [].slice.call(
        document.querySelectorAll('#navbarResponsive .nav-link')
    );
    responsiveNavItems.map(function (responsiveNavItem) {
        responsiveNavItem.addEventListener('click', () => {
            if (window.getComputedStyle(navbarToggler).display !== 'none') {
                navbarToggler.click();
            }
        });
    });

    $(document).ready(function() {
      // Esconder todas as perguntas, exceto a primeira
      $('.pergunta:not(:first)').hide();

      // Quando um botão de opção for clicado, mostrar a próxima pergunta
      $('input[type=radio]').click(function() {
        $(this).parents('.pergunta').hide().next('.pergunta').fadeIn(500);
      });

      // Quando o botão de envio for clicado, enviar o formulário
      $('form').submit(function(e) {
        e.preventDefault();
        // Aqui você pode adicionar código para enviar os dados do formulário para o servidor
        alert('Formulário enviado com sucesso!');
      });
    });

});
