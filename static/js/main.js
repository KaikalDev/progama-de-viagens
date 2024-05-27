document.addEventListener('DOMContentLoaded', function() {
    const buttons = document.querySelectorAll('[data-btn]')

    for (let i = 0; i < buttons.length; i++) {
        buttons[i].addEventListener('click', function(botao) {
            const id = botao.target.getAttribute('data-btn');
            const section = document.querySelector(`[data-sec=${id}]`)
            const cla = section.classList
            const active = `${cla[0]}--is-active`;
            if (cla.contains(active)) {
                cla.remove(active);
            } else {
                escondetodasSections(id)
                cla.add(active);
            }
        })
    }
})
document.addEventListener("DOMContentLoaded", function() {
    var data_ida = document.getElementById("data_ida");
    
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

function desmaraCheckBoxTipo2(selectedCheckboxId) {
    const checkboxes = document.querySelectorAll('[data-check-tipo2]');
    checkboxes.forEach(checkbox => {
        if (checkbox.id !== selectedCheckboxId) {
            checkbox.checked = false;
        }
    });
}

function desmaraCheckBoxTipo1(selectedCheckboxId) {
    const checkboxes = document.querySelectorAll('[data-check-tipo1]');
    checkboxes.forEach(checkbox => {
        if (checkbox.id !== selectedCheckboxId) {
            checkbox.checked = false;
        }
    });
}