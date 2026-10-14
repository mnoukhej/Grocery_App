var allProductsCache = [];
var allUomsCache = [];
var activeFilterUnit = 'all';

function formatCurrency(amount) {
    return '₹ ' + parseFloat(amount).toLocaleString('en-IN', {
        minimumFractionDigits: 2,
        maximumFractionDigits: 2
    });
}

function renderProductTable(products) {
    var $tbody = $("#productTableBody");
    if (!products || products.length === 0) {
        $tbody.html(
            '<tr><td colspan="5" style="text-align: center; padding: 3rem; color: var(--text-muted);">' +
            '<div class="empty-state">' +
            '<div class="empty-state-icon"><i class="fa-solid fa-box-open"></i></div>' +
            '<div class="empty-state-title">No products found</div>' +
            '<div class="empty-state-text">No items match your filter criteria.</div>' +
            '</div></td></tr>'
        );
        return;
    }

    var html = '';
    $.each(products, function (index, product) {
        var prodNum = 'PROD-' + String(product.product_id).padStart(4, '0');
        var priceDisplay = formatCurrency(product.price_per_unit);

        html += '<tr data-id="' + product.product_id + '" data-name="' + product.name + '" data-unit-id="' + product.uom_id + '" data-unit-name="' + (product.uom_name || '') + '" data-price="' + product.price_per_unit + '">' +
            '<td><span class="order-badge">#' + prodNum + '</span></td>' +
            '<td><strong><i class="fa-solid fa-cube" style="color: var(--primary); margin-right: 0.5rem; font-size: 0.85rem;"></i>' + product.name + '</strong></td>' +
            '<td><span class="uom-pill">' + (product.uom_name || 'Unit') + '</span></td>' +
            '<td><span class="amount-tag">' + priceDisplay + '</span></td>' +
            '<td style="text-align: center;">' +
                '<button type="button" class="btn-modern btn-modern-info btn-modern-sm edit-product" style="margin-right: 0.35rem;">' +
                    '<i class="fa-solid fa-pen-to-square"></i> Edit' +
                '</button>' +
                '<button type="button" class="btn-modern btn-modern-danger btn-modern-sm delete-product">' +
                    '<i class="fa-solid fa-trash-can"></i>' +
                '</button>' +
            '</td>' +
            '</tr>';
    });

    $tbody.html(html);
}

function filterProducts() {
    var query = ($("#productSearchInput").val() || '').toLowerCase().trim();
    var filtered = allProductsCache.filter(function (prod) {
        var matchesUnit = (activeFilterUnit === 'all') || ((prod.uom_name || '').toLowerCase() === activeFilterUnit.toLowerCase());
        var matchesQuery = !query ||
            (prod.name || '').toLowerCase().includes(query) ||
            String(prod.product_id).includes(query) ||
            (prod.uom_name || '').toLowerCase().includes(query);
        return matchesUnit && matchesQuery;
    });

    renderProductTable(filtered);
}

function openModal(isEdit, data) {
    var $modal = $("#customProductModal");
    if (isEdit && data) {
        $("#modalTitle").text("Edit Product #" + data.id);
        $("#productId").val(data.id);
        $("#productName").val(data.name);
        $("#productUom").val(data.unit_id);
        $("#productPrice").val(data.price);
    } else {
        $("#modalTitle").text("Add New Product");
        $("#productId").val("0");
        $("#productName").val("");
        $("#productUom").val("");
        $("#productPrice").val("");
    }
    $modal.css("display", "flex");
}

function closeModal() {
    $("#customProductModal").hide();
}

$(function () {
    // 1. Fetch UOM list
    $.get(uomListApiUrl, function (uoms) {
        if (uoms) {
            allUomsCache = uoms;
            $("#statUomCount").text(uoms.length);

            // Populate modal dropdown
            var options = '<option value="">-- Select Unit --</option>';
            var pills = '<span class="filter-pill active" data-unit="all">All Items</span>';

            $.each(uoms, function (index, uom) {
                options += '<option value="' + uom.uom_id + '">' + uom.uom_name + '</option>';
                pills += '<span class="filter-pill" data-unit="' + uom.uom_name + '">' + uom.uom_name + '</span>';
            });

            $("#productUom").html(options);
            $("#uomFilterPills").html(pills);
        }
    });

    // 2. Fetch Product list
    $.get(productListApiUrl, function (response) {
        if (response) {
            // Sort ascending by name
            response.sort(function (a, b) {
                return (a.name || '').localeCompare(b.name || '');
            });
            allProductsCache = response;

            // Stats
            var count = response.length;
            var totalPrice = 0;
            $.each(response, function (i, p) {
                totalPrice += parseFloat(p.price_per_unit || 0);
            });
            var avgPrice = count > 0 ? (totalPrice / count) : 0;

            $("#statProductCount").text(count);
            $("#statAvgPrice").text(formatCurrency(avgPrice));

            renderProductTable(response);
        }
    }).fail(function () {
        $("#productTableBody").html(
            '<tr><td colspan="5" style="text-align: center; color: var(--danger); padding: 2rem;">' +
            '<i class="fa-solid fa-triangle-exclamation"></i> Error loading products. Please verify backend is running.' +
            '</td></tr>'
        );
    });

    // Search input
    $("#productSearchInput").on("keyup", filterProducts);

    // Filter pills
    $(document).on("click", ".filter-pill", function () {
        $(".filter-pill").removeClass("active");
        $(this).addClass("active");
        activeFilterUnit = $(this).data("unit");
        filterProducts();
    });

    // Open Add Modal
    $("#openAddProductModal, #openAddProductBtn2").on("click", function () {
        openModal(false);
    });

    // Close Modal
    $("#closeModalBtn, #cancelModalBtn").on("click", closeModal);
    $(window).on("click", function (e) {
        if ($(e.target).is("#customProductModal")) {
            closeModal();
        }
    });

    // Edit Product Button
    $(document).on("click", ".edit-product", function () {
        var $tr = $(this).closest("tr");
        var data = {
            id: $tr.data("id"),
            name: $tr.data("name"),
            unit_id: $tr.data("unit-id"),
            price: $tr.data("price")
        };
        openModal(true, data);
    });

    // Save Product (Insert or Edit)
    $("#saveProduct").on("click", function () {
        var id = $("#productId").val();
        var name = $("#productName").val().trim();
        var uom_id = $("#productUom").val();
        var price = $("#productPrice").val().trim();

        if (!name) {
            alert("Please enter a product name");
            return;
        }
        if (!uom_id) {
            alert("Please select a measurement unit");
            return;
        }
        if (!price || isNaN(parseFloat(price)) || parseFloat(price) < 0) {
            alert("Please enter a valid price");
            return;
        }

        if (id && id !== "0") {
            // Edit Product
            var editPayload = {
                product_id: parseInt(id),
                name: name,
                uom_id: parseInt(uom_id),
                price_per_unit: parseFloat(price)
            };
            callApi("POST", editProductUrl, {
                data: JSON.stringify(editPayload)
            });
        } else {
            // Insert Product
            var insertPayload = {
                product_name: name,
                uom_id: parseInt(uom_id),
                price_per_unit: parseFloat(price)
            };
            callApi("POST", productSaveApiUrl, {
                data: JSON.stringify(insertPayload)
            });
        }
    });

    // Delete Product
    $(document).on("click", ".delete-product", function () {
        var $tr = $(this).closest("tr");
        var id = $tr.data("id");
        var name = $tr.data("name");

        if (confirm("Are you sure you want to delete '" + name + "'?")) {
            callApi("POST", productDeleteApiUrl, {
                product_id: id
            });
        }
    });
});
