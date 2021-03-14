let apiLink = document.getElementById('api_link');
let chartContext = document.getElementById('chart').getContext('2d');
let chart = document.getElementById('chart');
let responseArea = document.getElementById('response_value');
let responseTable = document.getElementById('response_table');
let apiTypeDropdown = document.getElementById('api_type_dropdown');
let currencyDropdown = document.getElementById('currency_dropdown');
let currencyDiv = document.getElementById('currency_div');
let singleDateOnlyCheckbox = document.getElementById('single_date_only_checkbox');
let singleDate = document.getElementById('single_date');
let startDate = document.getElementById('start_date');
let endDate = document.getElementById('end_date');
let chartInstance = null;

apiTypeDropdown.onchange = function apiTypeChanged() {
    if (apiTypeDropdown.value === 'sum') {
        currencyDiv.hidden = false;
    } else {
        currencyDiv.hidden = true;
    }
}

singleDateOnlyCheckbox.onchange = function singleDateCheckboxChanged() {
    if (singleDateOnlyCheckbox.checked === true) {
        singleDate.disabled = false;
        startDate.disabled = true;
        endDate.disabled = true;
    } else {
        singleDate.disabled = true;
        startDate.disabled = false;
        endDate.disabled = false;
    }
}

function drawChart(jsonResponse) {
    let table_array = jsonResponse['result'];

    if (table_array.length > 1) {
        let labelsArray = new Array(1);
        let dataArray = new Array(1);

        let cols = Object.keys(table_array[0]);
        let valueName;
        let valueLabel;

        if (cols.length === 3) {
            valueName = 'rate';
            valueLabel = 'Exchange rate'
        } else {
            valueName = 'sum';

            if (jsonResponse['currency'] === 'PLN') {
                valueLabel = "Sum of transactions (PLN)";
            } else {
                valueLabel = "Sum of transactions (USD)";
            }
        }

        for (let i = 0; i < table_array.length; i++) {
            labelsArray.push(table_array[i]['date']);
            dataArray.push(table_array[i][valueName])
        }

        labelsArray.length++;
        dataArray.length++;

        chartInstance = new Chart(chartContext, {
            "type": "line",
            "data": {
                "labels": labelsArray,
                "datasets": [{
                    "label": valueLabel,
                    "data": dataArray,
                    "fill": false,
                    "borderColor": "rgb(75, 192, 192)",
                    "lineTension": 0.1
                }]
            },
            "options": {
                maintainAspectRatio: true,
                scales: {
                    xAxes: [{
                        ticks: {
                            beginAtZero: true
                        },
                        display: true,
                        scaleLabel: {
                            fontSize: 30,
                            display: true,
                            labelString: 'Date'
                        }
                    }],
                    yAxes: [{
                        display: true,

                        scaleLabel: {
                            fontSize: 30,
                            display: true,
                            labelString: valueLabel
                        }
                    }]
                }
            }
        });

    }
}

async function generateLink() {
    let datesPart = getDatesPart();
    let apiTypePart = getApiTypePart();

    let link = `http://127.0.0.1:5000/api/${apiTypePart}/${datesPart}`;
    apiLink.value = link;

    if (chartInstance != null) {
        chartInstance.destroy();
    }

    const response = await fetch(link);

    if (response.status === 200) {
        const jsonResponse = await response.json()
        responseArea.value = JSON.stringify(jsonResponse);

        fillTableWith(jsonResponse);
        responseTable.hidden = false;

        if (singleDateOnlyCheckbox.checked === false) {
            drawChart(jsonResponse);
        }
    } else {
        responseArea.value = response.status + " " + response.statusText + ' (make sure that dates are correctly assigned)';
        responseTable.hidden = true;
    }
}

function getDatesPart() {
    if (singleDateOnlyCheckbox.checked === true) {
        return singleDate.value;
    } else {
        return `${startDate.value}/${endDate.value}`
    }
}

function getApiTypePart() {
    if (apiTypeDropdown.value === 'sum') {
        return `${apiTypeDropdown.value}/${currencyDropdown.value}`;
    } else {
        return `${apiTypeDropdown.value}`
    }
}

function fillTableWith(jsonResponse) {
    let table_array = jsonResponse['result'];

    let cols = Object.keys(table_array[0]);

    let headerRow;

    if (cols.length === 3) {
        headerRow = '<th>Date</th><th>Exchange rate</th><th>Is interpolated?</th>'
    } else {
        headerRow = '<th>Date</th><th>Sum</th>'
    }

    let rows = table_array
        .map(row => {
            let tds = cols.map(col => `<td>${row[col]}</td>`).join("");
            return `<tr>${tds}</tr>`;
        })
        .join("");

    const table = `
	<table>
		<thead>
			<tr>${headerRow}</tr>
		<thead>
		<tbody>
			${rows}
		<tbody>
	<table>`;

    responseTable.innerHTML = table;
}