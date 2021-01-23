function toggle_more() {
    var sidebar = document.querySelector('.sidebar');
    var sidebarBackground = document.querySelector('.sidebar-background');
    var moreButton = document.querySelector('div.more');

    if (sidebar.style.display == 'block') {
        sidebar.style.display = '';
        sidebarBackground.style.display = '';
        moreButton.style.backgroundColor = '';
    } else {
        sidebar.style.display = 'block';
        sidebarBackground.style.display = 'block';
        moreButton.style.backgroundColor = '#a7a7aa';
    }
}

function lineChart(ctx,
                   labelName,
                   labelList,
                   dataList,
                   bdcolor = '#094480',
                   bgcolor = '#d9e2ec') {
    Chart.defaults.global.defaultFontFamily = "Oxygen";
    Chart.defaults.global.defaultFontColor = "black";

    var chart = new Chart(ctx, {
        // The type of chart we want to create
        type: 'line',

        // The data for our dataset
        data: {
            labels: labelList,
            datasets: [{
                label: labelName,
                backgroundColor: bgcolor,
                borderColor: bdcolor,
                data: dataList
            }]
        },

        // Configuration options go here
        options: {}
    });
}

function barChart(ctx,
                   labelName,
                   labelList,
                   dataList,
                   bdcolor = '#094480',
                   bgcolor = '#d9e2ec') {
    Chart.defaults.global.defaultFontFamily = "Oxygen";
    Chart.defaults.global.defaultFontColor = "black";

    var chart = new Chart(ctx, {
        // The type of chart we want to create
        type: 'bar',

        // The data for our dataset
        data: {
            labels: labelList,
            datasets: [{
                label: labelName,
                backgroundColor: bgcolor,
                borderColor: bdcolor,
                data: dataList
            }]
        },

        // Configuration options go here
        options: {
            scales: {
                yAxes: [{
                    ticks: {
                        beginAtZero: true
                    }
                }]
            }
        }
    });
}

function stackedChart(ctx, labelName, datasetlist) {
    
    var chart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labelName, // responsible for how many bars are gonna show on the chart
            // create 12 datasets, since we have 12 items
            // data[0] = labels[0] (data for first bar - 'Standing costs') | data[1] = labels[1] (data for second bar - 'Running costs')
            // put 0, if there is no data for the particular bar
            datasets: datasetlist
        },
        options: {
            responsive: false,
            legend: {
                position: 'right' // place legend on the right side of chart
            },
            scales: {
                xAxes: [{
                    stacked: true // this should be set to make the bars stacked
                }],
                yAxes: [{
                    stacked: true // this also..
                }]
            }
        }
    });
}

window.addEventListener('resize', () => {
    if (window.innerWidth > 850) {
        var sidebar = document.querySelector('.sidebar');
        var sidebarBackground = document.querySelector('.sidebar-background');
        var moreButton = document.querySelector('div.more');

        sidebar.style.display = '';
        sidebarBackground.style.display = '';
        moreButton.style.backgroundColor = '';
    }
});

function highlightCurrentPage(pageName) {
    let current = document.querySelector(`#${pageName}`);
    current.className = 'current';
}