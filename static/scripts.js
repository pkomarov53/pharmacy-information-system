$(document).ready(function() {
    $('#infoModal').on('show.bs.modal', function(event) {
        var button = $(event.relatedTarget); // Кнопка, которая вызвала модальное окно
        var name = button.data('name');
        var form = button.data('form');
        var dosage = button.data('dosage');
        var package = button.data('package');

        var modal = $(this);
        modal.find('.modal-title').text('Информация о лекарстве: ' + name);
        modal.find('#modal-drug-name').text(name);
        modal.find('#modal-drug-form').text(form);
        modal.find('#modal-drug-dosage').text(dosage);
        modal.find('#modal-drug-package').text(package);
    });
});