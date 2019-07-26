$(document).ready(function()
{
    // global object
    var today = new Date();
    var home = {
        state: {
            keyword: '',
            crawlingStatus: null,
            data: null,
            taskIdPak: null,
            taskIdOlx: null,
            // taskIdGari: null,
            uniqueIdPak: null,
            // uniqueIdGari: null,
            uniqueIdOlx: null,
            filters: {
                min_price : 0,
                max_price : 1000000000,
                min_model : 0,
                max_model : today.getFullYear(),
                max_mileage : 1000000000
            }
        },
        statusInterval: 1
    };

    function displayAds(data)
    {
        data = JSON.parse(data);
        
        min_price = home.state.filters.min_price;
        max_price = home.state.filters.max_price;
        min_model = home.state.filters.min_model;
        max_model = home.state.filters.max_model;
        max_mileage = home.state.filters.max_mileage;

        $("#main-content").empty(); // empty out the previous content (if any or not)

        // if no results were found
        if (data.length == 0)
        {
            $(".row").append
            (
                '<div class="display-4 text-primary">' +
                    'No Results' +
                '<div>'
            );
            return;
        }

        for (var i = 0; i < data.length; i++)
        {
            image = JSON.parse(data[i].image); // get image url
            // if images are not available
            if (image[0] == "")
                image[0] = imgSrc; // defined in index.html
            
            if((min_price <= data[i].price) &&
                (data[i].price <= max_price) && 
                (min_model <= data[i].model) && 
                (data[i].model <= max_model) &&
                (data[i].mileage <= max_mileage)
                )
            {
                $(".row").append('<div class="col-sm-4 m-auto">' +
                                    '<div class="card" style="width: 20rem;">' +
                                        '<img src="' + image[0] + '" class="card-img-top" alt="' + data[i].title + '" />' +
                                        '<div class="card-body">' +
                                            '<a href="https://' + data[i].url + '">' +
                                                '<h5 class="card-title">' + data[i].title + '</h5>' +
                                            '</a>' +
                                        '</div>' +
                                        '<ul class="list-group list-group-flush">' +
                                            '<li class="list-group-item">' + data[i].price + '</li>' +
                                            '<li class="list-group-item">' + data[i].location + '</li>' +
                                            '<li class="list-group-item">' + data[i].model + '</li>' +
                                            '<li class="list-group-item">' + data[i].mileage + '</li>' +
                                            '<li class="list-group-item">' + data[i].fuel + '</li>' +
                                            '<li class="list-group-item">' + data[i].engine + '</li>' +
                                            '<li class="list-group-item">' + data[i].transmission + '</li>' +
                                        '</ul>' +
                                    '</div>' +
                                '</div>');
            }
        }
    }

    // this method does only one thing
    // making a request to server to ask status of crawling job
    function checkCrawlStatus()
    {
        $.ajax({
            type: 'GET',
            url: '/api/crawl/',
            data: {
                task_id_pak: home.state.taskIdPak,
                task_id_olx: home.state.taskIdOlx,
                // task_id_gari: home.state.taskIdGari,
                unique_id_pak: home.state.uniqueIdPak,
                unique_id_olx: home.state.uniqueIdOlx,
                // unique_id_gari: home.state.uniqueIdGari
            },
            success: function(response) {
                /* Crawling Ended */
                // show results
                if (response.data)
                {
                    // if response contains a data array
                    // that means crawling completed and we have results
                    // no need to make more requests, just clear interval
                    removeLoadScreen();
                    home.state.data = response.data;
                    displayAds(home.state.data);
                    clearInterval(home.statusInterval);
                }
                /* Crawling In Progress */
                // show status
                else if (response.status)
                {
                    // if response contains a `status` key and no data or error
                    // that means crawling process is still active, running or pending
                    // don't clear the interval
                    home.state.crawlingStatus = response.status;
                    console.log(response.status);
                }
            },
            error: function(response) {
                response = response.responseText;
                console.log(response);
                // if there is an error, no need to keep requesting & clear interval
                clearInterval(home.statusInterval);
            }
        });
    }

    // launch crawler
    function launchCrawler()
    {
        $.ajax({
            type: 'POST',
            url: '/api/crawl/',
            data: { keyword: home.state.keyword },
            success: function(response) {
                /* Keyword Found */
                // show results
                if (response.data)
                {
                    home.state.data = response.data;
                    displayAds(response.data);
                }
                /* Keyword Not Found */
                // show task_id, unique_id & status
                else
                {
                    // update the state with new task and unique id
                    home.state.taskIdPak = response.task_id_pak;
                    home.state.taskIdOlx = response.task_id_olx;
                    // home.state.taskIdOlx = response.task_id_gari;
                    home.state.uniqueIdPak = response.unique_id_pak;
                    home.state.uniqueIdOlx = response.unique_id_olx;
                    // home.state.uniqueIdOlx = response.unique_id_gari;
                    home.state.crawlingStatus = response.status;
                    // ####################### HERE ########################
                    // after updating state
                    // start to execute checkCrawlStatus method for every 2 seconds
                    // ####################### HERE ########################
                    displayLoadScreen();
                    home.statusInterval = setInterval(
                        checkCrawlStatus,
                        2000
                    );
                }
            },
            error: function(response) {
                response = response.responseText;
                console.log(response);
            }
        });
    }

    // Search Form Submission
    $('#search_form').submit(function(event)
    {
        event.preventDefault();
        home.state.keyword = $('#search_input').val();
        launchCrawler();
    });

    // Apply Filter
    $('#filterData').submit(function(event)
    {
        console.log("Inside Filter!");
        var today = new Date();
        event.preventDefault();
        var minPrice = $('#minPrice').val();
        var maxPrice = $('#maxPrice').val();
        var minModel = $('#minModel').val();
        var maxModel = $('#maxModel').val();
        var maxMileage = $('#maxMileage').val();

        if (isNaN(minPrice) || minPrice == '')
        {
            minPrice = 0;
        }
        if (isNaN(maxPrice) || maxPrice == '')
        {
            maxPrice = 1000000000;
        }
        if (isNaN(minModel) || minModel == '')
        {
            minModel = 0;
        }
        if (isNaN(maxModel) || maxModel == '')
        {
            maxModel = today.getFullYear();
        }
        if (isNaN(maxMileage) || maxMileage == '')
        {
            maxMileage = 1000000000;
        }

        home.state.filters = {
            min_price : minPrice,
            max_price : maxPrice,
            min_model : minModel,
            max_model : maxModel,
            max_mileage : maxMileage
        }
        displayAds(home.state.data);        
    }
)});