var productPrices = {};

function updateOrderSummary() {
    var count = $(".product-box-extra .product-item").length;
    $("#summaryItemCount").text(count);
    $("#itemsCountBadge").text(count + (count === 1 ? ' Item' : ' Items'));

    var cust = $("#customerName").val().trim();
    $("#summaryCustomer").text(cust || 'Guest');
}

function recalculateTotals() {
    var grandTotal = 0;
    $(".product-box-extra .product-item").each(function () {
        var $row = $(this);
        var qty = parseFloat($row.find('.product-qty').val()) || 0;
        var price = parseFloat($row.find('.product-price').val()) || 0;
        var lineTotal = qty * price;

        $row.find('.product-total').val(lineTotal.toFixed(2));
        grandTotal += lineTotal;
    });

    $("#product_grand_total").val(grandTotal.toFixed(2));
    updateOrderSummary();
}

$(function () {
    // 1. Load Products for dropdowns
    $.get(productListApiUrl, function (response) {
        productPrices = {};
        if (response) {
            response.sort(function (a, b) {
                return (a.name || '').localeCompare(b.name || '');
            });

            var options = '<option value="">-- Choose Product --</option>';
            $.each(response, function (index, product) {
                options += '<option value="' + product.product_id + '">' + product.name + ' (' + (product.uom_name || 'Unit') + ')</option>';
                productPrices[product.product_id] = parseFloat(product.price_per_unit || 0);
            });

            // Populate both template and initial row
            $(".product-box select").html(options);
            $(".product-box-extra select").html(options);
        }
    });

    // 2. Add More Button
    $("#addMoreButton, #addMoreButton2").on("click", function () {
        var rowHtml = $(".product-box").html();
        var $newRow = $(rowHtml);
        
        $newRow.find('.remove-row').removeClass('hideit');
        $newRow.find('.product-price').val('0.00');
        $newRow.find('.product-qty').val('1');
        $newRow.find('.product-total').val('0.00');
        
        $(".product-box-extra").append($newRow);
        updateOrderSummary();
    });

    // 3. Remove Row
    $(document).on("click", ".remove-row", function () {
        if ($(".product-box-extra .product-item").length <= 1) {
            alert("An order must contain at least one product item.");
            return;
        }
        $(this).closest('.product-item').remove();
        recalculateTotals();
    });

    // 4. Product Select Change
    $(document).on("change", ".cart-product", function () {
        var productId = $(this).val();
        var price = productPrices[productId] || 0;

        var $row = $(this).closest('.product-item');
        $row.find('.product-price').val(price.toFixed(2));
        recalculateTotals();
    });

    // 5. Quantity Change
    $(document).on("input change", ".product-qty", function () {
        recalculateTotals();
    });

    // 6. Live Customer Name Preview
    $("#customerName").on("input", function () {
        updateOrderSummary();
    });

    // 7. Save Order
    $("#saveOrder").on("click", function () {
        var customerName = $("#customerName").val().trim();
        var grandTotal = $("#product_grand_total").val().trim();

        if (!customerName) {
            alert("Please enter customer name before placing order.");
            $("#customerName").focus();
            return;
        }

        if (!grandTotal || parseFloat(grandTotal) <= 0) {
            alert("Please select at least one product with valid quantity.");
            return;
        }

        var orderDetails = [];
        var hasInvalidItem = false;

        $(".product-box-extra .product-item").each(function () {
            var $row = $(this);
            var prodId = $row.find('.cart-product').val();
            var qty = parseFloat($row.find('.product-qty').val());
            var total = parseFloat($row.find('.product-total').val());

            if (!prodId) {
                hasInvalidItem = true;
                return false;
            }

            orderDetails.push({
                product_id: parseInt(prodId),
                quantity: qty,
                total_price: total
            });
        });

        if (hasInvalidItem || orderDetails.length === 0) {
            alert("Please select a product for all item rows.");
            return;
        }

        var requestPayload = {
            customer_name: customerName,
            grand_total: parseFloat(grandTotal),
            order_details: orderDetails
        };

        // Disable button during submit
        $("#saveOrder").prop("disabled", true).html('<i class="fa-solid fa-spinner fa-spin"></i> Placing Order...');

        $.post(orderSaveApiUrl, {
            data: JSON.stringify(requestPayload)
        }).done(function (res) {
            alert("Order created successfully!");
            window.location.href = "index.html";
        }).fail(function () {
            alert("Failed to save order. Please check backend connection.");
            $("#saveOrder").prop("disabled", false).html('<i class="fa-solid fa-check-double"></i> Confirm & Place Order');
        });
    });
});
