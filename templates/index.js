var item_id_set = new Set();

function search(item_type) {
  var temp_pair = []
  var item_id_notice = PNotify.notice({
    title: item_type + ' ID Needed',
    text: 'Please input the ' + item_type + ' ID : ',
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

  item_id_notice.on('pnotify.confirm', function (e) {
    if (e.value === "") {
      item_id_notice.cancelClose().update({
        title: 'Sorry',
        text: 'The ' + item_type + ' ID cannot be null.',
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
                  changeScrapers("add", item_type, temp_pair[0], temp_pair[1]);
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
                window.open('https://twitter.com/search-advanced', "_blank", "scrollbars=yes,alwaysRaised=yes");
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
      if (item_id_set.has(v)) {
        item_id_notice.cancelClose().update({
          title: 'Sorry',
          text: 'Do not add the same ' + item_type + ' ID.',
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
        item_id_notice.cancelClose().update({
          title: v,
          text: 'Is it the ' + item_type + ' ID you wanna search for?',
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

  item_id_notice.on('pnotify.cancel', function (e) {
    item_id_notice.cancelClose().update({
      title: 'Sorry',
      text: 'You need specify a ' + item_type + ' ID.',
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

function changeScrapers(op, item_type, item_id, query) {
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
        text: '<b>ID : ' + item_id + '</b><br><b>Query : ' + query + '</b><br><b>' + result + '<b>',
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
    url: "http://127.0.0.1:5000/scrapers?op=" + op + "&item_type=" + item_type + "&item_id=" + item_id + "&&query=" + query,
    success: function (result) {
      showTopMsg(result)
      if (op == 'add') {
        item_id_set.add(item_id);
        showScraper(item_type, item_id, 'Query: ' + query);
      } else if (op == 'remove') {
        item_id_set.delete(item_id);
      } else if (op == 'get') {
        result = $.parseJSON(result)
        for (var item_id_temp in result) {
          item_id_set.add(item_id_temp);
          showScraper(item_type, item_id, 'Query: ' + result[item_id_temp]);
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

function showScraper(item_type, title, text) {
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
    title: "&nbsp;&nbsp;" + title,
    titleTrusted: true,
    hide: false,
    stack: window.stackContextModal,
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
              window.open('templates/charts.html?item_id=' + title);
            }
          },
          {
            text: 'Close',
            primary: true,
            click: function (notice) {
              changeScrapers('remove', '', notice.options.data.title, "");
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

  switch (item_type) {
    case 'Stock':
      opts.type = 'notice';
      opts.text = text;
      opts.icon = 'fas fa-chart-line fa-2x';
      break;
    case 'Crypto':
      opts.type = 'info';
      opts.text = '<p>' + text + '</p>';
      opts.textTrusted = true
      opts.icon = 'fas fa-money-bill fa-2x';
      break;
  }

  PNotify.alert(opts);
  PNotify.defaults.styling = 'brighttheme';
};

$(
  function () {
    changeScrapers('get', 'Stock', '', '');
    changeScrapers('get', 'Crypto', '', '');
  }
);