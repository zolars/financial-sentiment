var item_id_set = new Set();
var notice_dict = {}

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
                  updateCrypto();
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
    if (result != 'success') {
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
      if (op == 'getItems') {
        result = $.parseJSON(result)
        for (var response_item_id in result) {
          item_id_set.add(response_item_id);
          showScraper(item_type, response_item_id, 'Query: ' + result[response_item_id]);
        }
      } else if (op == 'add') {
        showTopMsg(result)
        item_id_set.add(item_id);
        showScraper(item_type, item_id, 'Query: ' + query);
      } else if (op == 'remove') {
        showTopMsg(result)
        item_id_set.delete(item_id);
        delete notice_dict[item_id];
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

function showScraper(item_type, item_id, text) {
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
    title: "&nbsp;&nbsp;" + item_id,
    titleTrusted: true,
    hide: false,
    stack: window.stackContextModal,
    width: '1000px',
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
        // buttons: [
        //   {
        //     text: 'MORE',
        //     primary: true,
        //     click: function (notice) {
        //       window.open('templates/charts.html?item_id=' + item_id);
        //     }
        //   },
        //   {
        //     text: 'Close',
        //     primary: true,
        //     click: function (notice) {
        //       var temp = notice.options.data.title.split("&nbsp;&nbsp;")[1];
        //       changeScrapers('remove', '', temp, "");
        //       notice.close();
        //     }
        //   }
        // ]
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
      opts.modules.Confirm.buttons = [
        {
          text: 'MORE',
          primary: true,
          click: function (notice) {
            window.open('templates/charts.html?item_id=' + item_id);
          }
        },
        {
          text: 'Close',
          primary: true,
          click: function (notice) {
            var temp = notice.options.data.title.split("&nbsp;&nbsp;")[1];
            changeScrapers('remove', '', temp, "");
            notice.close();
          }
        }
      ];
      break;
    case 'Crypto':
      opts.type = 'info';
      opts.text = '<p>' + text + '</p>' +
        ["<table border=\"1\">",
          "<tr>",
          "<td>Price</td>",
          "<td>Price High</td>",
          "<td>Price Low</td>",
          "<td>Volume Sold</td>",
          "<td>Coin Supply</td>",
          "<td>Market Cap</td>",
          "<td>Velocity</td>",
          "</tr>",
          "<tr>",
          "<td id='price_" + item_id + "'></td>",
          "<td id='high_" + item_id + "'></td>",
          "<td id='low_" + item_id + "'></td>",
          "<td id='volume_sold_" + item_id + "'></td>",
          "<td id='coin_supply_" + item_id + "'></td>",
          "<td id='market_cap_" + item_id + "'></td>",
          "<td id='velocity_" + item_id + "'></td>",
          "</tr>",
          "</table>"].join("") + '<br>' +
        ["<table border=\"1\">",
          "<tr>",
          "<td>Number of Twitter Posts</td>",
          "<td>Average of Twitter Posts</td>",
          "<td>Spike of Twitter Posts</td>",
          "<td>Sentiment</td>",
          "<td>Total Average Sentiment</td>",
          "<td>Sentiment Normality</td>",
          "</tr>",
          "<tr>",
          "<td id='amount_hour_" + item_id + "'></td>",
          "<td id='amount_avg_" + item_id + "'></td>",
          "<td id='amount_spike_" + item_id + "'></td>",
          "<td id='sentiment_hour_" + item_id + "'></td>",
          "<td id='sentiment_avg_" + item_id + "'></td>",
          "<td id='sentiment_spike_" + item_id + "'></td>",
          "</tr>",
          "</table>"].join("");
      opts.textTrusted = true;
      opts.icon = 'fas fa-money-bill fa-2x';
      opts.modules.Confirm.buttons = [
        {
          text: 'Close',
          primary: true,
          click: function (notice) {
            var temp = notice.options.data.title.split("&nbsp;&nbsp;")[1];
            changeScrapers('remove', '', temp, "");
            notice.close();
          }
        }
      ];
      break;
  }
  notice_dict[item_id] = PNotify.alert(opts);
  PNotify.defaults.styling = 'brighttheme';
};

function updateCrypto() {
  for (var item_id in notice_dict) {
    if (notice_dict[item_id].options.data.type == 'info') {
      console.log(item_id, notice_dict[item_id]);
      // Crypto Amount
      $.ajax({
        type: "GET",
        url: "http://127.0.0.1:5000/getCryptoData?item_id=" + item_id,
        success: function (result) {
          this.item_id = this.url.replace("http://127.0.0.1:5000/getCryptoData?item_id=", "");

          // Price
          console.log(this.item_id, "price: ", result.price.toLocaleString('en-US', { style: 'currency', currency: 'USD' }));
          $('#price_' + this.item_id).text(result.price.toLocaleString('en-US', { style: 'currency', currency: 'USD' }));
          // Price High
          console.log(this.item_id, "high: ", result.high.toLocaleString('en-US', { style: 'currency', currency: 'USD' }));
          $('#high_' + this.item_id).text(result.high.toLocaleString('en-US', { style: 'currency', currency: 'USD' }));
          // Price Low
          console.log(this.item_id, "low: ", result.low.toLocaleString('en-US', { style: 'currency', currency: 'USD' }));
          $('#low_' + this.item_id).text(result.low.toLocaleString('en-US', { style: 'currency', currency: 'USD' }));
          // Volume sold(hour)
          console.log(this.item_id, "volume_sold: ", result.volume_sold.toLocaleString('en-US', { style: 'currency', currency: 'USD' }));
          $('#volume_sold_' + this.item_id).text(result.volume_sold.toLocaleString('en-US', { style: 'currency', currency: 'USD' }));
          // Coin Supply
          console.log(this.item_id, "coin_supply: ", result.coin_supply.toLocaleString('en-US', { style: 'currency', currency: 'USD' }));
          $('#coin_supply_' + this.item_id).text(result.coin_supply.toLocaleString('en-US', { style: 'currency', currency: 'USD' }));
          // Market Cap
          console.log(this.item_id, "market_cap: ", result.market_cap.toLocaleString('en-US', { style: 'currency', currency: 'USD' }));
          $('#market_cap_' + this.item_id).text(result.market_cap.toLocaleString('en-US', { style: 'currency', currency: 'USD' }));
          // Velocity
          console.log(this.item_id, "velocity: ", result.velocity);
          $('#velocity_' + this.item_id).text(result.velocity);
          // Number of Twitter Posts
          console.log(this.item_id, "amount_hour: ", result.amount_hour);
          $('#amount_hour_' + this.item_id).text(result.amount_hour);
          // Average twitter posts per hour
          console.log(this.item_id, "amount_avg: ", result.amount_avg);
          $('#amount_avg_' + this.item_id).text(result.amount_avg.toFixed(0));
          // Spike in twitter posts  (Amount of twitter posts - average per hour)/ average per hour)
          console.log(this.item_id, "amount_spike: ", result.amount_spike);
          $('#amount_spike_' + this.item_id).text(result.amount_spike.toFixed(0));
          // Sentiment over	
          console.log(this.item_id, "sentiment_hour: ", result.sentiment_hour);
          $('#sentiment_hour_' + this.item_id).text(result.sentiment_hour.toFixed(2));
          // Total Average Sentiment
          console.log(this.item_id, "sentiment_avg: ", result.sentiment_avg);
          $('#sentiment_avg_' + this.item_id).text(result.sentiment_avg.toFixed(2));
          // Sentiment Normality  (Sentiment over - total average sentment) / total average sentment
          console.log(this.item_id, "sentiment_spike: ", result.sentiment_spike);
          $('#sentiment_spike_' + this.item_id).text(result.sentiment_spike.toFixed(2));
        }
      });
    }
  }
}
// Execute once
$(document).ready(function () {
  changeScrapers('getItems', 'Stock', '', '');
  changeScrapers('getItems', 'Crypto', '', '');
  updateCrypto();
});

// Interval forever
setInterval("updateCrypto()", 60000);