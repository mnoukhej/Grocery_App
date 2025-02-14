var productPrices = {};

$(function () {
    //Json data by api call for order table
    $.get(productListApiUrl, function (response) {
        productPrices = {}
        if(response) {
            var options = '<option value="">--Select--</option>';
            $.each(response, function(index, product) {
                options += '<option value="'+ product.product_id +'">'+ product.name +'</option>';
                productPrices[product.product_id] = product.price_per_unit;
            });
            $(".product-box").find("select").empty().html(options);
        }
    });
});

$("#addMoreButton").click(function () {
    var row = $(".product-box").html();
    $(".product-box-extra").append(row);
    $(".product-box-extra .remove-row").last().removeClass('hideit');
    $(".product-box-extra .product-price").last().text('0.0');
    $(".product-box-extra .product-qty").last().val('1');
    $(".product-box-extra .product-total").last().text('0.0');
});

$(document).on("click", ".remove-row", function (){
    $(this).closest('.row').remove();
    calculateValue();
});

$(document).on("change", ".cart-product", function (){
    var product_id = $(this).val();
    var price = productPrices[product_id];

    $(this).closest('.row').find('#product_price').val(price);
    calculateValue();
});

$(document).on("change", ".product-qty", function (e){
    calculateValue();
});

$("#saveOrder").on("click", function(){
    var customerName = $("input[name='customerName']").val();
    var grandTotal = $("input[name='product_grand_total']").val();

    // Add validation for customer name and total
    if (!customerName) {
        alert("Please enter customer name");
        return;
    }

    if (!grandTotal || isNaN(parseFloat(grandTotal))) {
        alert("Invalid total value");
        return;
    }

    var formData = $("form").serializeArray();
    var requestPayload = {
        customer_name: customerName,
        grand_total: grandTotal,
        order_details: []
    };

    // Add validation to check if there are any order details
    if (formData.filter(item => item.name === 'product').length === 0) {
        alert("Please add at least one product");
        return;
    }

    for(var i=0; i<formData.length; ++i) {
        var element = formData[i];
        var lastElement = null;

        switch(element.name) {
            case 'product':
                requestPayload.order_details.push({
                    product_id: element.value,
                    quantity: null,
                    total_price: null
                });
                break;
            case 'qty':
                lastElement = requestPayload.order_details[requestPayload.order_details.length-1];
                lastElement.quantity = element.value;
                break;
            case 'item_total':
                lastElement = requestPayload.order_details[requestPayload.order_details.length-1];
                lastElement.total_price = element.value;
                break;
        }
    }

    // Add validation to check if there are any order details
    if (requestPayload.order_details.length === 0) {
        alert("Please add at least one product");
        return;
    }

    // Perform the API call only if the validation passes
    callApi("POST", orderSaveApiUrl, {
        'data': JSON.stringify(requestPayload)
    });
});

