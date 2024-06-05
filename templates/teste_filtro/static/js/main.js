
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