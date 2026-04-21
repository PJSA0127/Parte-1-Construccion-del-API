const API_BASE = "http://127.0.0.1:8000";

let top20Cryptos = [];
let myChart = null;

async function init() {
    await fetchTop20();
    loadMarket();
    getHistory(); 
    loadVolatility(); // Nueva función
}

function loadVolatility() {
    let highHtml = '<ul class="list-group list-group-flush">';
    let lowHtml = '<ul class="list-group list-group-flush">';

    top20Cryptos.forEach(coin => {
        const change = coin.cambio_24h || 0;
        const colorClass = change >= 0 ? 'text-success' : 'text-danger';
        const icon = change >= 0 ? 'fa-arrow-trend-up' : 'fa-arrow-trend-down';
        
        const itemHtml = `
            <li class="list-group-item d-flex justify-content-between align-items-center py-3">
                <div>
                    <strong class="d-block">${coin.nombre}</strong>
                    <small class="text-muted">${coin.simbolo.toUpperCase()}</small>
                </div>
                <div class="text-end">
                    <span class="fw-bold ${colorClass}">${change.toFixed(2)}%</span>
                    <i class="fa-solid ${icon} ms-2 ${colorClass}"></i>
                </div>
            </li>`;

        if (Math.abs(change) > 5) {
            highHtml += itemHtml;
        } else {
            lowHtml += itemHtml;
        }
    });

    $('#high-vol-list').html(highHtml + '</ul>');
    $('#low-vol-list').html(lowHtml + '</ul>');
}

async function fetchTop20() {
    try {
        const response = await fetch(`${API_BASE}/crypto`);
        const data = await response.json();
        // Ya vienen ordenadas por market_cap (prioridad) desde el servicio
        top20Cryptos = data.slice(0, 20);
        populateSelectors();
    } catch (error) {
        console.error("Error cargando criptos:", error);
    }
}

function populateSelectors() {
    const selects = ['#conv-id', '#hist-id', '#alert-id'];
    const options = top20Cryptos.map(coin => 
        `<option value="${coin.id}">${coin.nombre} (${coin.simbolo.toUpperCase()})</option>`
    ).join('');

    selects.forEach(selector => $(selector).html(options));
}

function loadMarket() {
    let html = '';
    top20Cryptos.forEach(coin => {
        html += `
        <div class="col-md-4 col-sm-6">
            <div class="crypto-card text-center">
                <div class="crypto-title">${coin.nombre} (${coin.simbolo.toUpperCase()})</div>
                <div class="crypto-price">$${coin.precio.toLocaleString()}</div>
                <div class="mt-3">
                    <button class="btn btn-sm btn-primary px-3" onclick="showDetails('${coin.id}')">
                        <i class="fa-solid fa-circle-info me-1"></i>Detalles
                    </button>
                </div>
            </div>
        </div>`;
    });
    $('#crypto-list').html(html);
}

async function showDetails(coinId) {
    const modal = new bootstrap.Modal(document.getElementById('detailsModal'));
    $('#detail-content').html('<div class="spinner-border text-primary"></div>');
    $('#detail-name').text('Cargando...');
    modal.show();

    try {
        const res = await fetch(`${API_BASE}/crypto/${coinId}`);
        const data = await res.json();
        
        $('#detail-name').text(`${data.nombre} (${data.simbolo.toUpperCase()})`);
        
        const content = `
            <div class="mb-4">
                <h2 class="fw-bold text-primary">$${data.precio_actual.toLocaleString()}</h2>
                <span class="badge bg-light text-dark border p-2">Ranking #${data.ranking}</span>
            </div>
            <div class="row text-start g-3">
                <div class="col-6">
                    <small class="text-muted d-block">Capitalización</small>
                    <strong>$${data.market_cap.toLocaleString()}</strong>
                </div>
                <div class="col-6 text-end">
                    <small class="text-muted d-block">Simbolo</small>
                    <strong>${data.simbolo.toUpperCase()}</strong>
                </div>
            </div>
            <hr class="my-4 opacity-50">
            <div class="alert alert-info py-2 small">
                <i class="fa-solid fa-circle-exclamation me-2"></i>
                Usa el ID <b>${coinId}</b> para consultas técnicas.
            </div>
        `;
        $('#detail-content').html(content);
    } catch (e) {
        $('#detail-content').html('<p class="text-danger">Error al cargar detalles.</p>');
    }
}

async function getHistory() {
    const id = $('#hist-id').val() || 'bitcoin';
    try {
        const res = await fetch(`${API_BASE}/history/${id}`);
        const data = await res.json();
        
        // CORRECCIÓN DE FECHAS: Agrupar por día
        const dailyMap = new Map();
        
        data.precios.forEach(p => {
            const dateObj = new Date(p[0]);
            const day = String(dateObj.getDate()).padStart(2, '0');
            const month = String(dateObj.getMonth() + 1).padStart(2, '0');
            const dateStr = `${day}/${month}`;
            
            // Guardamos el último precio registrado de ese día
            dailyMap.set(dateStr, p[1]);
        });

        // Convertimos el Map a arrays para Chart.js (tomando los últimos 7 días)
        const allLabels = Array.from(dailyMap.keys());
        const allPrices = Array.from(dailyMap.values());
        
        const labels = allLabels.slice(-7);
        const prices = allPrices.slice(-7);

        renderChart(labels, prices, id);
    } catch (e) {
        console.error("Error en gráfico:", e);
    }
}

function renderChart(labels, prices, coinId) {
    const ctx = document.getElementById('historyChart').getContext('2d');
    
    if (myChart) {
        myChart.destroy();
    }

    myChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: `Precio de ${coinId.toUpperCase()} (USD)`,
                data: prices,
                backgroundColor: 'rgba(108, 92, 231, 0.7)',
                borderColor: 'rgba(108, 92, 231, 1)',
                borderWidth: 1,
                borderRadius: 5,
                barPercentage: 0.5
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { display: false },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            return ' Precio: $' + context.parsed.y.toLocaleString();
                        }
                    }
                }
            },
            scales: {
                y: {
                    beginAtZero: false,
                    grid: { color: '#f0f0f0' },
                    ticks: {
                        callback: function(value) { return '$' + value.toLocaleString(); }
                    }
                },
                x: {
                    grid: { display: false }
                }
            }
        }
    });
}

async function convert() {
    const id = $('#conv-id').val();
    const amount = $('#conv-amount').val();
    const currency = $('#conv-currency').val();
    if (!amount) return alert("Ingresa una cantidad");

    try {
        const res = await fetch(`${API_BASE}/convert?coin_id=${id}&amount=${amount}&target_currency=${currency}`);
        const data = await res.json();
        $('#conv-result').html(`${data.resultado.toLocaleString()} <small>${data.moneda_destino.toUpperCase()}</small>`);
    } catch (e) { alert("Error en conversión"); }
}

async function createAlert() {
    const payload = {
        email: $('#alert-email').val(),
        coin_id: $('#alert-id').val(),
        target_price: parseFloat($('#alert-price').val())
    };
    if (!payload.email || !payload.target_price) return alert("Completa todos los campos");

    try {
        const res = await fetch(`${API_BASE}/alert`, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(payload)
        });
        const data = await res.json();
        $('#alert-res').text(data.message);
    } catch (e) { alert("Error creando alerta"); }
}

$(document).ready(init);
