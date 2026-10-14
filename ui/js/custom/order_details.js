// this is order_details.js file
var productModal = $("#orderDetailsModal");
$(function () {
    var urlParams = new URLSearchParams(window.location.search);
    var queryOrderId = urlParams.get('order_id');
    var fetchUrl = queryOrderId ? (orderDetailsUrl + '?order_id=' + encodeURIComponent(queryOrderId)) : orderDetailsUrl;

    if (queryOrderId) {
        $("#order_id").text(queryOrderId);
    } else if (typeof __postOrderId !== 'undefined') {
        $("#order_id").text(__postOrderId);
    }

    // JSON data by API call
    $.get(fetchUrl, function (response) {
        if (response) {
            var table = '';
            var count = 0;
            // Sort the products by name in ascending order
            response.sort(function(a, b) {
                return (a.name || '').localeCompare(b.name || '');
            });
    
            $.each(response, function (index, product) {
                count++;
                if (product.order_id && !$("#order_id").text()) {
                    $("#order_id").text(product.order_id);
                }
                table += '<tr data-name="' + product.name + '" data-price="' + product.price_per_unit + '" data-unit="' + product.uom_id + '" data-quantity="' + product.quantity + '" data-total="' + product.total_price + '">' +
                    '<td>'+ count +'</td>'+
                    '<td>'+ product.name +'</td>'+
                    '<td>' + product.price_per_unit + '</td>' +                        
                    '<td>' + product.uom_name + '</td>' +
                    '<td>' + product.quantity + '</td>' +
                    '<td>'+ product.total_price +'</td></tr>';
            });
            $("table").find('tbody').empty().html(table);
        }
    });
});