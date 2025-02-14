// this is order_details.js file
var productModal = $("#orderDetailsModal");
    $(function () {

        //JSON data by API call
        $.get(orderDetailsUrl, function (response) {
            if (response) {
                var table = '';
                var count = 0;
                // Sort the products by name in ascending order
                response.sort(function(a, b) {
                    return a.name.localeCompare(b.name);
                });
        
                $.each(response, function (index, product) {
                    count++;
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

    // Assuming you have a variable named __postOrderId that holds the order_id value
// and __postCustomerName that holds the customer_name value

// Update the #order_id and #customer_name elements with the values
$("#order_id").text(__postOrderId);
//$("#customer_name").text(__postCustomerName);

        
    });