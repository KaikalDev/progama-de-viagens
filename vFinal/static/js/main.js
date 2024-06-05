document.addEventListener("DOMContentLoaded", function() {
    var data_ida = document.getElementById("data_ida");
    const buttonFiltro = document.querySelectorAll('[data-btn-fitro]')
    const formFiltro = document.querySelector('[data-btn-form]')
     
    for (let i = 0; i<buttonFiltro.length; i++) {
        buttonFiltro[i].addEventListener('click',function(e) {
            formFiltro.classList.toggle('card__header__lista__filtro--is-active')

        })
    }

    data_ida.addEventListener("focus", function() {
        this.type = 'date';
    });

    data_ida.addEventListener("blur", function() {
        if (!this.value) {
            this.type = 'text';
        }
    });
    var data_volta = document.getElementById("data_volta");
    
    data_volta.addEventListener("focus", function() {
        this.type = 'date';
    });

    data_volta.addEventListener("blur", function() {
        if (!this.value) {
            this.type = 'text';
        }
    });
});

function abreEfechaFiltro() {
    const classe = 'card__header__lista__filtro--is-active'
    formFiltro.classList.toggle(classe)
}