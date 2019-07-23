var stock_id_set = new Set();

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
        if (result != 'success' && op != 'get') {
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
                showScraper('notice', true, stock_id, 'Query: ' + query);
            } else if (op == 'remove') {
                stock_id_set.delete(stock_id);
            } else if (op == 'get') {
                result = $.parseJSON(result)
                for (var stock_id_temp in result) {
                    stock_id_set.add(stock_id_temp);
                    showScraper('notice', true, stock_id_temp, 'Query: ' + result[stock_id_temp]);
                }
            }
            console.log(result)
        },
        error: function (XMLHttpRequest, textStatus, errorThrown) {
            showTopMsg("Error: " + textStatus)
            console.log(XMLHttpRequest.status);
            console.log(XMLHttpRequest.readyState);
            console.log(textStatus);
        }
    });
}

function showScraper(type, modal, title, text) {
    PNotify.defaults.styling = 'material';
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
        title: title,
        text: text,
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
            },
            Confirm: {
                confirm: true,
                buttons: [
                    {
                        text: 'MORE',
                        primary: true,
                        click: function (notice) {
                            alert('show detail');
                            // var chart = echarts.init($("chart"), 'white', { renderer: 'canvas' });
                        }
                    },
                    {
                        text: 'Close',
                        primary: true,
                        click: function (notice) {
                            changeScrapers('remove', notice.options.data.title, "");
                            notice.close();
                        }
                    }
                ]
            },
            History: {
                history: false
            }
        }
    };

    PNotify.notice(opts);
    PNotify.defaults.styling = 'brighttheme';
};

$(
    function () {
        changeScrapers('get', '', '');
    }
);