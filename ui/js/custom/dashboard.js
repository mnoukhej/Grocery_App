var allOrdersCache = [];

function getInitials(name) {
    if (!name) return '??';
    var parts = name.trim().split(' ');
    if (parts.length === 1) return parts[0].substring(0, 2).toUpperCase();
    return (parts[0][0] + parts[parts.length - 1][0]).toUpperCase();
}

function formatCurrency(amount) {
    return '₹ ' + parseFloat(amount).toLocaleString('en-IN', {
        minimumFractionDigits: 2,
        maximumFractionDigits: 2
    });
}

function renderOrdersTable(orders) {
    var $tbody = $("#ordersTableBody");
    if (!orders || orders.length === 0) {
        $tbody.html(
            '<tr><td colspan="5" style="text-align: center; padding: 3rem; color: var(--text-muted);">' +
            '<div class="empty-state">' +
            '<div class="empty-state-icon"><i class="fa-solid fa-receipt"></i></div>' +
            '<div class="empty-state-title">No orders found</div>' +
            '<div class="empty-state-text">No orders match your search or no transactions recorded yet.</div>' +
            '</div></td></tr>'
        );
        return;
    }

    var html = '';
    $.each(orders, function (index, order) {
        var initials = getInitials(order.customer_name);
        var orderNum = 'ORD-' + String(order.order_id).padStart(4, '0');
        var formattedTotal = formatCurrency(order.total);

        html += '<tr data-order-id="' + order.order_id + '">' +
            '<td><span class="order-badge">#' + orderNum + '</span></td>' +
            '<td>' +
                '<div class="customer-cell">' +
                    '<div class="avatar-circle">' + initials + '</div>' +
                    '<div><strong>' + (order.customer_name || 'Guest') + '</strong></div>' +
                '</div>' +
            '</td>' +
            '<td><span style="color: var(--text-muted); font-size: 0.88rem;"><i class="fa-regular fa-calendar-days" style="margin-right: 0.35rem;"></i>' + (order.datetime || 'N/A') + '</span></td>' +
            '<td><span class="amount-tag">' + formattedTotal + '</span></td>' +
            '<td style="text-align: center;">' +
                '<button type="button" class="btn-modern btn-modern-info btn-modern-sm view-order-details" data-id="' + order.order_id + '">' +
                    '<i class="fa-solid fa-receipt"></i> View Invoice' +
                '</button>' +
            '</td>' +
            '</tr>';
    });

    $tbody.html(html);
}

$(function () {
    // 1. Fetch Orders
    $.get(orderListApiUrl, function (response) {
        if (response) {
            allOrdersCache = response;
            var totalCost = 0;
            var count = response.length;

            $.each(response, function (index, order) {
                totalCost += parseFloat(order.total || 0);
            });

            // Update KPI Cards
            $("#kpiTotalRevenue").text(formatCurrency(totalCost));
            $("#kpiTotalOrders").text(count.toLocaleString());
            var avgOrder = count > 0 ? (totalCost / count) : 0;
            $("#kpiAvgOrder").text(formatCurrency(avgOrder));
            $("#ordersCountBadge").text(count + ' Orders');

            renderOrdersTable(response);
        }
    }).fail(function () {
        $("#ordersTableBody").html(
            '<tr><td colspan="5" style="text-align: center; color: var(--danger); padding: 2rem;">' +
            '<i class="fa-solid fa-triangle-exclamation" style="margin-right: 0.5rem;"></i> Failed to load orders. Please verify MySQL is running.' +
            '</td></tr>'
        );
    });

    // 2. Fetch Products Count for 4th KPI Card
    $.get(productListApiUrl, function (products) {
        if (products && products.length !== undefined) {
            $("#kpiTotalProducts").text(products.length);
        }
    });

    // 3. Live Search Filter
    $("#orderSearchInput").on("keyup", function () {
        var query = $(this).val().toLowerCase().trim();
        if (!query) {
            renderOrdersTable(allOrdersCache);
            return;
        }

        var filtered = allOrdersCache.filter(function (order) {
            var name = (order.customer_name || '').toLowerCase();
            var id = String(order.order_id);
            var date = (order.datetime || '').toLowerCase();
            return name.includes(query) || id.includes(query) || date.includes(query);
        });

        renderOrdersTable(filtered);
    });
});

// View Order Details
$(document).on("click", ".view-order-details", function () {
    var order_id = $(this).data('id') || $(this).closest('tr').data('order-id');

    var data = {
        order_id: order_id
    };

    $.post(POST_orderDetailsUrl, data).always(function () {
        window.location.href = "order_details.html?order_id=" + encodeURIComponent(order_id);
    });
});
