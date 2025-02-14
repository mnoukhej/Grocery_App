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
    var order_id = tr.find('td:eq(1)').text(); // Assuming order_id is in the second column

    var data = {
        order_id: order_id
    };

    //var isDelete = confirm("Are you sure to view " + order_id + " item?");
    // if (isDelete) {
    callApi("POST", POST_orderDetailsUrl, data);
    // }
    window.location.href = "http://127.0.0.1:5500/ui/order_details.html";
    
});
