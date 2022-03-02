$(document).ready(function () {
    $('#donators').DataTable(
        {
         "paging":   false,
        "ordering": true,
        "info":     true
        }
    );
    $('#donations').DataTable(
        {
         "paging":   false,
        "ordering": true,
        "info":     false,
         "searching": false
        }
    );
});