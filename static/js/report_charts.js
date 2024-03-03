document.addEventListener('DOMContentLoaded', function () {
    var ctxIncomeExpense = document.getElementById('incomeExpenseChart').getContext('2d');
    var incomeExpenseChart = new Chart(ctxIncomeExpense, {
        type: 'bar',
        data: {
            labels: ['Income', 'Expenses'],
            datasets: [{
                label: 'Amount',
                data: [/* Income Amount */, /* Expense Amount */],
                backgroundColor: [
                    'rgba(75, 192, 192, 0.2)',
                    'rgba(255, 99, 132, 0.2)'
                ],
                borderColor: [
                    'rgba(75, 192, 192, 1)',
                    'rgba(255, 99, 132, 1)'
                ],
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });

    var ctxCategory = document.getElementById('categorySpendingChart').getContext('2d');
    var categorySpendingChart = new Chart(ctxCategory, {
        type: 'pie',
        data: {
            labels: [/* Categories */],
            datasets: [{
                label: 'Spending by Category',
                data: [/* Category Amounts */],
                backgroundColor: [/* Colors */],
                hoverOffset: 4
            }]
        }
    });
});
