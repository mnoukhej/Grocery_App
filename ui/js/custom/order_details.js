function formatCurrency(amount) {
    return '₹ ' + parseFloat(amount).toLocaleString('en-IN', {
        minimumFractionDigits: 2,
        maximumFractionDigits: 2
    });
}

$(function () {
    var urlParams = new URLSearchParams(window.location.search);
    var queryOrderId = urlParams.get('order_id');
    var fetchUrl = queryOrderId ? (orderDetailsUrl + '?order_id=' + encodeURIComponent(queryOrderId)) : orderDetailsUrl;

    if (queryOrderId) {
        $("#order_id").text(String(queryOrderId).padStart(4, '0'));
    } else if (typeof __postOrderId !== 'undefined') {
        $("#order_id").text(String(__postOrderId).padStart(4, '0'));
    }

    // Try to get customer name from order list
    if (queryOrderId) {
        $.get(orderListApiUrl, function (orders) {
            if (orders) {
                var found = orders.find(function (o) { return String(o.order_id) === String(queryOrderId); });
                if (found && found.customer_name) {
                    $("#customer_name").text(found.customer_name);
                }
            }
        });
    }

    // Fetch Order Line Items
    $.get(fetchUrl, function (response) {
        var $tbody = $("#orderDetailsTableBody");
        if (!response || response.length === 0) {
            $tbody.html(
                '<tr><td colspan="5" style="text-align: center; padding: 2.5rem; color: var(--text-muted);">' +
                '<i class="fa-solid fa-receipt fa-2x" style="color: var(--text-subtle); margin-bottom: 0.5rem; display: block;"></i>' +
                'No line items found for this order.' +
                '</td></tr>'
            );
            return;
        }

        var tableHtml = '';
        var count = 0;
        var grandTotal = 0;

        // Sort items by product name
        response.sort(function (a, b) {
            return (a.name || '').localeCompare(b.name || '');
        });

        $.each(response, function (index, item) {
            count++;
            var unitPrice = parseFloat(item.price_per_unit || 0);
            var qty = parseFloat(item.quantity || 0);
            var itemTotal = parseFloat(item.total_price || (unitPrice * qty));
            grandTotal += itemTotal;

            if (item.order_id && !queryOrderId) {
                $("#order_id").text(String(item.order_id).padStart(4, '0'));
            }

            tableHtml += '<tr>' +
                '<td><span class="order-badge">' + count + '</span></td>' +
                '<td><strong>' + item.name + '</strong></td>' +
                '<td>' + formatCurrency(unitPrice) + ' <span class="uom-pill" style="font-size: 0.7rem; margin-left: 0.25rem;">' + (item.uom_name || 'Unit') + '</span></td>' +
                '<td><span style="font-weight: 700; color: var(--dark);">' + qty + '</span> ' + (item.uom_name || '') + '</td>' +
                '<td style="text-align: right;"><span class="amount-tag">' + formatCurrency(itemTotal) + '</span></td>' +
                '</tr>';
        });

        $tbody.html(tableHtml);
        $("#invoiceTotalItems").text(count + (count === 1 ? ' Item' : ' Items'));
        $("#invoiceGrandTotal").text(formatCurrency(grandTotal));
    }).fail(function () {
        $("#orderDetailsTableBody").html(
            '<tr><td colspan="5" style="text-align: center; color: var(--danger); padding: 2rem;">' +
            '<i class="fa-solid fa-triangle-exclamation"></i> Error loading invoice details. Please verify backend connection.' +
            '</td></tr>'
        );
    });
});