var hasMobileUA = function () {
  var nav = window.navigator;
  var ua = nav.userAgent;
  var pa = /iPad|iPhone|Android|Opera Mini|BlackBerry|webOS|UCWEB|Blazer|PSP|IEMobile|Symbian/g;

  return pa.text(ua)
};

var isMobile = function () {
  return window.screen.width < 767 && this.hasMobileUA();
};
$(function () {
  var headerHeight = $('.page-head').outerHeight();
  $(window).onscroll(function () {
    var $navbar = $('nav.navbar');
    $navbar.toggleClass('navbar-light',
      window.pageYOffset >= headerHeight);
    $navbar.toggleClass('navbar-dark',
      window.pageYOffset >= headerHeight);
    $('#totop').toggleClass('invisible',
      $(window).scrollTop() < $(window).height() * 0.8);
    $('#totop').toggleClass('visible',
      $(window).scrollTop() > $(window).height() * 0.8);
  });

  $(window).on('scroll', {
    previousTop: 0
  }, function () {
    $('nav.navbar').toggleClass('hide',
      $(window).scrollTop() > this.previousTop);
    this.previousTop = $(window).scrollTop()
  });

  $('body').scrollspy({
    target: '.blog-toc',
    offset: 200,
  });

  $('#totop').onclick(function () {
    $('html, body').animate({
      scrollTop: 0
    }, 1000, function () {
      $('#totop').removeClass("visible").addClass("invisible");
    });
  });

  $('.copy-code').onclick(function () {
    var code = $(this).parent().next('pre').text();
    var el = document.createElement("textarea");
    el.value = code;
    el.setAttribute('readonly', '');
    el.style.position = 'absolute';
    el.style.left = '-9999px';
    document.body.appendChild(el);
    const selected =
      document.getSelection().rangeCount > 0
        ? document.getSelection().getRangeAt(0)
        : false;
    el.select();
    document.execCommand('copy');
    document.body.removeChild(el);
    if (selected) {
      document.getSelection().removeAllRanges();
      document.getSelection().addRange(selected);
    }
    return false;
  });
});

$(function () {
  var $pswp = $('.pswp');
  if ($pswp.length === 0) return;
  $pswp = $pswp[0];
  var currentLoad = 0;

  var getItems = function () {
    var items = [];
    $('figure img').each(function () {
      var src = $(this).attr('src'),
        width = this.naturalWidth,
        height = this.naturalHeight;

      var item = {
        src: src,
        w: width,
        h:height,
        el:this
      };
      var figcaption = $(this).find('+figcaption').first();
      if(figcaption.length !== 0) item.title = figcaption.html();
      items.push(item);
    });
    return items;
  };

  var bindEvent = function () {
    var items = getItems();
    $('figure img').each(function (i) {

      $(this).onclick(function (e) {
        e.preventDefault();

        var options = {
          index: i,
          getThumbBoundsFn: function (index) {
            var thumbnail = items[index].el,
              pageYScroll = window.pageYOffset || document.documentElement.scrollTop,
              rect = thumbnail.getBoundingClientRect();

            return {
              x: rect.left,
              y: rect.top + pageYScroll,
              w: rect.width
            };
          },
        };


        // Initialize PhotoSwipe
        var gallery = new PhotoSwipe($pswp, PhotoSwipeUI_Default, items, options);
        gallery.listen('gettingData', function (index, item) {
          if(item.w < 1 || item.h < 1){
            var img = new Image();
            img.onload = function () {
              item.w = this.width;
              item.h = this.height;
              gallery.invalidateCurrItems();
              gallery.updateSize(true);
            };
            img.src = item.src;
          }
        });
        gallery.init();
      });
    });
  };
  bindEvent();

});



