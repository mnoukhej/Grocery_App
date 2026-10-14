$(function () {
    //Json data by api call for order table
    $.get(orderListApiUrl, function (response) {
        if(response) {
            var table = '';
            var totalCost = 0;
            $.each(response, function(index, order) {
                totalCost += parseFloat(order.total);
                table += '<tr>' +
                    '<td>'+ order.datetime +'</td>'+
                    '<td>'+ order.order_id +'</td>'+
                    '<td>'+ order.customer_name +'</td>'+
                    '<td>' + order.total.toFixed(2) + ' Rs</td>' +
                    '<td><span class="btn btn-sm btn-primary pull-middle view-order-details"> View </span></td></tr>';
            });
            table += '<tr><td colspan="3" style="text-align: end"><b>Total</b></td><td><b>'+ totalCost.toFixed(2) +' Rs</b></td></tr>';
            $("table").find('tbody').empty().html(table);
        }
    });
});

$(document).on("click", ".view-order-details", function () {
    var tr = $(this).closest('tr');
    var order_id = tr.find('td:eq(1)').text().trim();

    var data = {
        order_id: order_id
    };

    $.post(POST_orderDetailsUrl, data).always(function () {
        window.location.href = "order_details.html?order_id=" + encodeURIComponent(order_id);
    });
});
