document.addEventListener('DOMContentLoaded', function() {
    // Получаем данные из контекста
    const chartData = JSON.parse(document.getElementById('chart-data').textContent);
    
    // Создаем контекст для графика
    const ctx = document.getElementById('profit-chart').getContext('2d');
    
    // Создаем график
    new Chart(ctx, {
        type: 'line',
        data: {
            labels: chartData.labels,
            datasets: [
                {
                    label: 'Фактическая прибыль',
                    data: chartData.actual,
                    borderColor: 'rgb(75, 192, 192)',
                    tension: 0.1,
                    fill: false,
                    spanGaps: true
                },
                {
                    label: 'Предсказание (скользящая средняя)',
                    data: chartData.predictions,
                    borderColor: 'rgb(255, 99, 132)',
                    borderDash: [5, 5],
                    tension: 0.1,
                    fill: false,
                    spanGaps: true
                }
            ]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'Прибыль (₽)'
                    }
                },
                x: {
                    title: {
                        display: true,
                        text: 'Месяц'
                    }
                }
            },
            plugins: {
                title: {
                    display: true,
                    text: 'Динамика прибыли и предсказания на 3 месяца вперед'
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            let label = context.dataset.label || '';
                            if (label) {
                                label += ': ';
                            }
                            if (context.parsed.y !== null) {
                                label += new Intl.NumberFormat('ru-RU', {
                                    style: 'currency',
                                    currency: 'RUB'
                                }).format(context.parsed.y);
                            }
                            return label;
                        }
                    }
                }
            }
        }
    });
}); 