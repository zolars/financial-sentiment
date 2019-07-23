// var chart = echarts.init($("chart"), 'white', { renderer: 'canvas' });
var query_list = [];
var stock_id_set = new Set();
var isRealtime = false;
var percent = 0;

function search() {
    var temp_pair = []
    var stock_id_notice = PNotify.notice({
        title: 'Stock ID Needed',
        text: 'Please input the Stock ID : ',
        icon: 'fas fa-question-circle',
        hide: false,
        stack: {
            'dir1': 'down',
            'modal': true,
            'firstpos1': 250
        },
        modules: {
            Confirm: {
                prompt: true
            },
            Buttons: {
                closer: false,
                sticker: false
            },
            History: {
                history: false
            },
        }
    });

    stock_id_notice.on('pnotify.confirm', function (e) {
        if (e.value === "") {
            stock_id_notice.cancelClose().update({
                title: 'Sorry',
                text: 'The Stock ID cannot be null.',
                icon: true,
                type: 'info',
                hide: true,
                modules: {
                    Confirm: {
                        prompt: false,
                        confirm: false,
                    },
                    Buttons: {
                        closer: true
                    }
                }
            });
        }
        else if (e.value == null) {

            var query_notice = PNotify.notice({
                title: 'Query Needed',
                text: 'Please input the Query : ',
                icon: 'fas fa-question-circle',
                hide: false,
                stack: {
                    'dir1': 'down',
                    'modal': true,
                    'firstpos1': 250
                },
                modules: {
                    Confirm: {
                        prompt: true,
                        buttons: [{
                            text: 'OK',
                            primary: true,
                            click: function (notice, e) {
                                if (e === "") {
                                    query_notice.cancelClose().update({
                                        title: 'Sorry',
                                        text: 'The Query cannot be null.',
                                        icon: true,
                                        type: 'info',
                                        hide: true,
                                        modules: {
                                            Confirm: {
                                                prompt: false,
                                                confirm: false,
                                            },
                                            Buttons: {
                                                closer: true
                                            }
                                        }
                                    });
                                } else if (e == null) {
                                    query_notice.remove();
                                    changeScrapers("add", temp_pair[0], temp_pair[1]);
                                } else {
                                    temp_pair.push(e);
                                    query_notice.cancelClose().update({
                                        title: e,
                                        text: 'Is it the Query you wanna search for?',
                                        icon: true,
                                        type: 'success',
                                        hide: false,
                                        modules: {
                                            Confirm: {
                                                prompt: false,
                                                confirm: true
                                            },
                                            Buttons: {
                                                closer: true
                                            }
                                        }
                                    });
                                }
                            }
                        },
                        {
                            text: 'Advanced',
                            click: function (notice) {
                                window.open('templates/twitter_advance_search.html', "_blank", "scrollbars=yes,alwaysRaised=yes");
                            }
                        },
                        {
                            text: 'CANCEL',
                            click: function (notice, e) {
                                query_notice.cancelClose().update({
                                    title: 'Sorry',
                                    text: 'You need specify a Query.',
                                    icon: true,
                                    type: 'info',
                                    hide: true,
                                    modules: {
                                        Confirm: {
                                            prompt: false,
                                            confirm: false,
                                        },
                                        Buttons: {
                                            closer: true
                                        }
                                    }
                                });
                            }
                        }]
                    },
                    Buttons: {
                        closer: false,
                        sticker: false
                    },
                    History: {
                        history: false
                    },
                }
            });

        } else {
            v = e.value.toLocaleUpperCase();
            if (stock_id_set.has(v)) {
                stock_id_notice.cancelClose().update({
                    title: 'Sorry',
                    text: 'Do not add the same Stock ID.',
                    icon: true,
                    type: 'info',
                    hide: true,
                    modules: {
                        Confirm: {
                            prompt: false,
                            confirm: false,
                        },
                        Buttons: {
                            closer: true
                        }
                    }
                });
            } else {
                temp_pair.push(v);
                stock_id_notice.cancelClose().update({
                    title: v,
                    text: 'Is it the Stock ID you wanna search for?',
                    icon: true,
                    type: 'success',
                    hide: true,
                    modules: {
                        Confirm: {
                            prompt: false,
                            confirm: true
                        },
                        Buttons: {
                            closer: true
                        }
                    }
                });
            }
        }
    });

    stock_id_notice.on('pnotify.cancel', function (e) {
        stock_id_notice.cancelClose().update({
            title: 'Sorry',
            text: 'You need specify a Stock ID.',
            icon: true,
            type: 'info',
            hide: true,
            modules: {
                Confirm: {
                    prompt: false,
                    confirm: false,
                },
                Buttons: {
                    closer: true
                }
            }
        });
    });
}

function realtime() {
    if (isRealtime) {
        var notice = PNotify.notice({
            title: 'Notice!',
            text: 'Realtime Refresh has been stopped!'
        });
        setTimeout(function () {
            notice.close();
        }, 1500);
        document.getElementById("realtime_btn").className = "button button-red";
    }
    else {
        var notice = PNotify.success({
            title: 'Notice!',
            text: 'Realtime Refresh has been started!'
        });
        setTimeout(function () {
            notice.close();
        }, 1500);
        document.getElementById("realtime_btn").className = "button button-green";
    }
    isRealtime = !isRealtime;
}

function changeScrapers(op, stock_id, query) {

    function showTopMsg(result) {
        if (typeof window.stackBarTop === 'undefined') {
            window.stackBarTop = {
                'dir1': 'down',
                'firstpos1': 0,
                'spacing1': 0,
                'push': 'top'
            };
        }
        if (result == 'success') {
            var opts = {
                title: 'Succeed to ' + op + ' a Scrapy as below : ',
                text: '<b>Stock ID : ' + stock_id + '</b><br><b>Query : ' + query + '</b>',
                textTrusted: true,
                type: 'success',
                addClass: 'stack-bar-top',
                cornerClass: 'ui-pnotify-sharp',
                shadow: false,
                width: '100%',
                stack: window.stackBarTop
            };
            PNotify.alert(opts);
            document.getElementById("tables").innerHTML = stock_id_set + "<br>" + query_list;
        }
        else {
            var opts = {
                title: 'Fail to ' + op + ' a Scrapy as below : ',
                text: '<b>Stock ID : ' + stock_id + '</b><br><b>Query : ' + query + '</b><br><b>' + result + '<b>',
                textTrusted: true,
                type: 'error',
                addClass: 'stack-bar-top',
                cornerClass: 'ui-pnotify-sharp',
                shadow: false,
                width: '100%',
                stack: window.stackBarTop
            };
            PNotify.alert(opts);
        }
    }

    $.ajax({
        type: "GET",
        url: "http://127.0.0.1:5000/scrapers?op=" + op + "&stock_id=" + stock_id + "&&query=" + query,
        success: function (result) {
            showTopMsg(result)
            if (op == 'add') {
                stock_id_set.add(stock_id);
                query_list.push(query);
            } else if (op == 'remove') {
                // TODO
            }
            console.log(result)
        },
        error: function (XMLHttpRequest, textStatus, errorThrown) {
            showTopMsg("Error: " + textStatus)
            console.log(XMLHttpRequest.status);
            console.log(XMLHttpRequest.readyState);
            console.log(textStatus);
        },
    });
}

function fetchQuery() {
    $.ajax({
        type: "GET",
        url: "http://127.0.0.1:5000/scrapers?op=get&stock_id=0&query=0",
        success: function (result) {
            console.log(result)
        },
        error: function (XMLHttpRequest, textStatus, errorThrown) {
            console.log(XMLHttpRequest.status);
            console.log(XMLHttpRequest.readyState);
            console.log(textStatus);
        },
    });
}

function fetchData(isClick) {
    if (isRealtime || isClick) {
        beginLoading(isClick);
        count = 0;
        for (var stock_id of stock_id_set) {
            query = query_list[count];
            count++;
            $.ajax({
                type: "GET",
                url: "http://127.0.0.1:5000/scrapers?op=add&stock_id=" + stock_id + "&&query=" + query,
                dataType: 'json',
                success: function (result) {
                    console.log(result)
                    // chart.setOption(result["chart"]);
                    endLoading(isClick);
                },
                error: function (XMLHttpRequest, textStatus, errorThrown) {
                    errorLoading(isClick);
                    console.log(XMLHttpRequest.status);
                    console.log(XMLHttpRequest.readyState);
                    console.log(textStatus);
                },
            });
        }
    }
}

function loading() {
    percent = 0;
    PNotify.defaults.icons = 'fontawesome5';
    window.loading_notice = PNotify.info({
        text: 'Please Wait',
        icon: 'fas fa-cog fa-spin',
        addClass: 'custom',
        hide: false,
        shadow: false,
        stack: {
            'modal': true,
            'overlayClose': false
        },
        modules: {
            Buttons: {
                closer: false,
                sticker: false
            }
        }
    });

    setTimeout(function () {
        window.loading_notice.update({
            title: false
        });
        var interval = setInterval(function () {
            var options = {
                text: percent + '% complete.'
            };
            if (percent < 0) {
                window.clearInterval(interval);
                options.title = 'Error!';
                options.type = 'error';
                options.text = 'Please check the data source...'
                options.hide = true;
                options.icon = 'fas fa-exclamation-triangle';
                options.shadow = true;
                options.width = PNotify.defaults.width;
                options.modules = {
                    Buttons: {
                        closer: true,
                        sticker: false
                    }
                };
            }
            if (percent >= 0 && percent < 80) {
                options.title = 'Loading...';
            }
            if (percent === 80) {
                options.title = 'Almost There...';
                percent -= 2;
            }
            if (percent >= 100) {
                window.clearInterval(interval);
                options.title = 'Done!';
                options.type = 'success';
                options.hide = true;
                options.icon = 'fas fa-check';
                options.shadow = true;
                options.width = PNotify.defaults.width;
                options.modules = {
                    Buttons: {
                        closer: true,
                        sticker: false
                    }
                };
            }
            window.loading_notice.update(options);
            percent += 2;
        }, 120);
    }, 2000);
}

function beginLoading(isClick) {
    if (isClick) {
        percent = 0;
        loading();
    }
}

function endLoading(isClick) {
    if (isClick) {
        percent = 100;
    } else {
        percent = 100;
        var notice = PNotify.success({
            title: 'Success!',
            text: 'Chart has been refreshed just now!'
        });
        setTimeout(function () {
            notice.close();
        }, 5000);
    }
}

function errorLoading(isClick) {
    if (isClick) {
        percent = -1;
    }
}

$(
    function () {
        fetchQuery();
        fetchData(false);
        setInterval(fetchData, 10000);
    }
);

window.showScraper = function showScraper(type, modal) {
    if (typeof window.stackContextModal === 'undefined') {
        window.stackContextModal = {
            'dir1': 'down',
            'firstpos1': 25,
            'context': document.getElementById('scrapers'),
            'modal': false,
            'overlayClose': false
        };
    }
    var opts = {
        title: 'Over Here',
        text: "Check me out. I'm in a different stack.",
        hide: false,
        stack: window.stackContextModal,
        type: 'info',
        width: '700px',
        modules: {
            Buttons: {
                closer: false,
                sticker: false
            },
            Mobile: {
                swipeDismiss: false
            }
        }
    };

    PNotify.notice(opts);

};