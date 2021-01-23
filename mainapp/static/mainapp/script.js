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