"use strict";

/*!

=========================================================
* Black Dashboard Pro - v1.1.1
=========================================================

* Product Page: https://themes.getbootstrap.com/product/black-dashboard-pro-premium-bootstrap-4-admin/
* Copyright 2019 Creative Tim (https://www.creative-tim.com)
* Coded by Creative Tim

=========================================================

* The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

*/

var transparent = true;
var transparentDemo = true;
var fixedTop = false;

var navbar_initialized = false;
var backgroundOrange = false;
var sidebar_mini_active = false;
var toggle_initialized = false;

var $html = $('html');
var $body = $('body');
var $navbar_minimize_fixed = $('.navbar-minimize-fixed');
var $collapse = $('.collapse');
var $navbar = $('.navbar');
var $tagsinput = $('.tagsinput');
var $selectpicker = $('.selectpicker');
var $navbar_color = $('.navbar[color-on-scroll]');
var $full_screen_map = $('.full-screen-map');
var $datetimepicker = $('.datetimepicker');
var $datepicker = $('.datepicker');
var $timepicker = $('.timepicker');

var seq = 0,
  delays = 80,
  durations = 500;
var seq2 = 0,
  delays2 = 80,
  durations2 = 500;

// Returns a function, that, as long as it continues to be invoked, will not
// be triggered. The function will be called after it stops being called for
// N milliseconds. If `immediate` is passed, trigger the function on the
// leading edge, instead of the trailing.

function debounce(func, wait, immediate) {
  var timeout;
  return function() {
    var context = this,
      args = arguments;
    clearTimeout(timeout);
    timeout = setTimeout(function() {
      timeout = null;
      if (!immediate) func.apply(context, args);
    }, wait);
    if (immediate && !timeout) func.apply(context, args);
  };
};

(function() {
  var isWindows = navigator.platform.indexOf('Win') > -1 ? true : false;

  if (isWindows) {
    // if we are on windows OS we activate the perfectScrollbar function
    if ($('.main-panel').length != 0) {
      var ps = new PerfectScrollbar('.main-panel', {
        wheelSpeed: 2,
        wheelPropagation: true,
        minScrollbarLength: 20,
        suppressScrollX: true
      });
    }

    if ($('.sidebar .sidebar-wrapper').length != 0) {

      var ps1 = new PerfectScrollbar('.sidebar .sidebar-wrapper');
      $('.table-responsive').each(function() {
        var ps2 = new PerfectScrollbar($(this)[0]);
      });
    }



    $html.addClass('perfect-scrollbar-on');
  } else {
    $html.addClass('perfect-scrollbar-off');
  }
})();

$(document).ready(function() {

  var scroll_start = 0;
  var startchange = $('.row');
  var offset = startchange.offset();
  var scrollElement = navigator.platform.indexOf('Win') > -1 ? $(".ps") : $(window);
  scrollElement.scroll(function() {

    scroll_start = $(this).scrollTop();

    if (scroll_start > 50) {
      $navbar_minimize_fixed.css('opacity', '1');
    } else {
      $navbar_minimize_fixed.css('opacity', '0');
    }
  });

  // hide the siblings opened collapse

  $collapse.on('show.bs.collapse', function() {
    $(this).parent().siblings().children('.collapse').each(function() {
      $(this).collapse('hide');
    });
  });

  //  Activate the Tooltips
  $('[data-toggle="tooltip"], [rel="tooltip"]').tooltip();

  // Activate Popovers and set color for popovers
  $('[data-toggle="popover"]').each(function() {
    color_class = $(this).data('color');
    $(this).popover({
      template: '<div class="popover popover-' + color_class + '" role="tooltip"><div class="arrow"></div><h3 class="popover-header"></h3><div class="popover-body"></div></div>'
    });
  });

  var tagClass = $tagsinput.data('color');

  if ($tagsinput.length != 0) {
    $tagsinput.tagsinput();
  }

  $('.bootstrap-tagsinput').find('.tag').addClass('badge-' + tagClass);

  //    Activate bootstrap-select
  if ($selectpicker.length != 0) {
    $selectpicker.selectpicker({
      iconBase: "tim-icons",
      tickIcon: "icon-check-2"
    });
  }

  //when you click the modal search button the navbar will not be collapsed
  $("#search-button").click(function() {
    $(this).closest('.navbar-collapse').removeClass('show');
    $navbar.addClass('navbar-transparent').removeClass('bg-white');

  });



  blackDashboard.initMinimizeSidebar();

  var scroll_distance = $navbar_color.attr('color-on-scroll') || 500;

  // Check if we have the class "navbar-color-on-scroll" then add the function to remove the class "navbar-transparent" so it will transform to a plain color.
  if ($navbar_color.length != 0) {
    blackDashboard.checkScrollForTransparentNavbar();
    $(window).on('scroll', blackDashboard.checkScrollForTransparentNavbar)
  }

  if ($full_screen_map.length == 0 && $('.bd-docs').length == 0) {
    // On click navbar-collapse the menu will be white not transparent
    $('.navbar-toggler').click(function() {
      $collapse.on('show.bs.collapse', function() {
        $(this).closest('.navbar').removeClass('navbar-transparent').addClass('bg-white');
      }).on('hide.bs.collapse', function() {
        $(this).closest('.navbar').addClass('navbar-transparent').removeClass('bg-white');
      });
      $navbar.css('transition', '');

    });
  }

  $navbar.css({
    'top': '0',
    'transition': 'all .5s linear'
  });

  $('.form-control').on("focus", function() {
    $(this).parent('.input-group').addClass("input-group-focus");
  }).on("blur", function() {
    $(this).parent(".input-group").removeClass("input-group-focus");
  });

  // Activate bootstrapSwitch
  $('.bootstrap-switch').each(function() {
    var data_on_label = $(this).data('on-label') || '';
    var data_off_label = $(this).data('off-label') || '';

    $(this).bootstrapSwitch({
      onText: data_on_label,
      offText: data_off_label
    });
  });
});

$(document).on('click', '.navbar-toggle', function() {
  var $toggle = $(this);

  if (blackDashboard.misc.navbar_menu_visible == 1) {
    $html.removeClass('nav-open');
    blackDashboard.misc.navbar_menu_visible = 0;
    setTimeout(function() {
      $toggle.removeClass('toggled');
      $('.bodyClick').remove();
    }, 550);

  } else {
    setTimeout(function() {
      $toggle.addClass('toggled');
    }, 580);

    var div = '<div class="bodyClick"></div>';
    $(div).appendTo('body').click(function() {
      $html.removeClass('nav-open');
      blackDashboard.misc.navbar_menu_visible = 0;
      setTimeout(function() {
        $toggle.removeClass('toggled');
        $('.bodyClick').remove();
      }, 550);
    });

    $html.addClass('nav-open');
    blackDashboard.misc.navbar_menu_visible = 1;
  }
});

$(window).resize(function() {
  // reset the seq for charts drawing animations
  seq = seq2 = 0;

  if ($full_screen_map.length == 0 && $('.bd-docs').length == 0) {
    var isExpanded = $navbar.find('[data-toggle="collapse"]').attr("aria-expanded");
    if ($navbar.hasClass('bg-white') && $(window).width() > 991) {
      $navbar.removeClass('bg-white').addClass('navbar-transparent');
    } else if ($navbar.hasClass('navbar-transparent') && $(window).width() < 991 && isExpanded != "false") {
      $navbar.addClass('bg-white').removeClass('navbar-transparent');
    }
  }
});

var blackDashboard = {
  misc: {
    navbar_menu_visible: 0
  },

  checkScrollForTransparentNavbar: debounce(function() {
    if ($(document).scrollTop() > scroll_distance) {
      if (transparent) {
        transparent = false;
        $navbar_color.removeClass('navbar-transparent');
      }
    } else {
      if (!transparent) {
        transparent = true;
        $navbar_color.addClass('navbar-transparent');
      }
    }
  }, 17),



  // Activate DateTimePicker

  initDateTimePicker: function() {
    if ($datetimepicker.length != 0) {
      $datetimepicker.datetimepicker({
        icons: {
          time: "tim-icons icon-watch-time",
          date: "tim-icons icon-calendar-60",
          up: "fa fa-chevron-up",
          down: "fa fa-chevron-down",
          previous: 'tim-icons icon-minimal-left',
          next: 'tim-icons icon-minimal-right',
          today: 'fa fa-screenshot',
          clear: 'fa fa-trash',
          close: 'fa fa-remove'
        }
      });
    }

    if ($datepicker.length != 0) {
      $datepicker.datetimepicker({
        format: 'MM/DD/YYYY',
        icons: {
          time: "tim-icons icon-watch-time",
          date: "tim-icons icon-calendar-60",
          up: "fa fa-chevron-up",
          down: "fa fa-chevron-down",
          previous: 'tim-icons icon-minimal-left',
          next: 'tim-icons icon-minimal-right',
          today: 'fa fa-screenshot',
          clear: 'fa fa-trash',
          close: 'fa fa-remove'
        }
      });
    }

    if ($timepicker.length != 0) {
      $timepicker.datetimepicker({
        // format: 'H:mm',    // use this format if you want the 24hours timepicker
        format: 'h:mm A', //use this format if you want the 12hours timpiecker with AM/PM toggle
        icons: {
          time: "tim-icons icon-watch-time",
          date: "tim-icons icon-calendar-60",
          up: "fa fa-chevron-up",
          down: "fa fa-chevron-down",
          previous: 'tim-icons icon-minimal-left',
          next: 'tim-icons icon-minimal-right',
          today: 'fa fa-screenshot',
          clear: 'fa fa-trash',
          close: 'fa fa-remove'
        }
      });
    }
  },

  initMinimizeSidebar: function() {
    if ($('.sidebar-mini').length != 0) {
      sidebar_mini_active = true;
    }

    $('.minimize-sidebar').click(function() {

      if (sidebar_mini_active == true) {
        $body.removeClass('sidebar-mini');
        sidebar_mini_active = false;
        blackDashboard.showSidebarMessage('Sidebar mini deactivated...');
      } else {
        $body.addClass('sidebar-mini');
        sidebar_mini_active = true;
        blackDashboard.showSidebarMessage('Sidebar mini activated...');
      }

      // we simulate the window Resize so the charts will get updated in realtime.
      var simulateWindowResize = setInterval(function() {
        window.dispatchEvent(new Event('resize'));
      }, 180);

      // we stop the simulation of Window Resize after the animations are completed
      setTimeout(function() {
        clearInterval(simulateWindowResize);
      }, 1000);
    });
  },

  startAnimationForLineChart: function(chart) {
    chart.on('draw', function(data) {
      if (data.type === 'line' || data.type === 'area') {
        data.element.animate({
          d: {
            begin: 600,
            dur: 700,
            from: data.path.clone().scale(1, 0).translate(0, data.chartRect.height()).stringify(),
            to: data.path.clone().stringify(),
            easing: Chartist.Svg.Easing.easeOutQuint
          }
        });
      } else if (data.type === 'point') {
        seq++;
        data.element.animate({
          opacity: {
            begin: seq * delays,
            dur: durations,
            from: 0,
            to: 1,
            easing: 'ease'
          }
        });
      }
    });

    seq = 0;
  },
  startAnimationForBarChart: function(chart) {

    chart.on('draw', function(data) {
      if (data.type === 'bar') {
        seq2++;
        data.element.animate({
          opacity: {
            begin: seq2 * delays2,
            dur: durations2,
            from: 0,
            to: 1,
            easing: 'ease'
          }
        });
      }
    });

    seq2 = 0;
  },
  showSidebarMessage: function(message) {
    try {
      $.notify({
        icon: "tim-icons icon-bell-55",
        message: message
      }, {
        type: 'primary',
        timer: 4000,
        placement: {
          from: 'top',
          align: 'right'
        }
      });
    } catch (e) {
      console.log('Notify library is missing, please make sure you have the notifications library added.');
    }

  }
};

function hexToRGB(hex, alpha) {
  var r = parseInt(hex.slice(1, 3), 16),
    g = parseInt(hex.slice(3, 5), 16),
    b = parseInt(hex.slice(5, 7), 16);

  if (alpha) {
    return "rgba(" + r + ", " + g + ", " + b + ", " + alpha + ")";
  } else {
    return "rgb(" + r + ", " + g + ", " + b + ")";
  }
}

/*!
 * jQuery twitter bootstrap wizard plugin
 * Examples and documentation at: http://github.com/VinceG/twitter-bootstrap-wizard
 * version 1.4.2
 * Requires jQuery v1.3.2 or later
 * Supports Bootstrap 2.2.x, 2.3.x, 3.0
 * Dual licensed under the MIT and GPL licenses:
 * http://www.opensource.org/licenses/mit-license.php
 * http://www.gnu.org/licenses/gpl.html
 * Authors: Vadim Vincent Gabriel (http://vadimg.com), Jason Gill (www.gilluminate.com)
 */
;
(function($) {
  var bootstrapWizardCreate = function(element, options) {
    var element = $(element);
    var obj = this;

    // selector skips any 'li' elements that do not contain a child with a tab data-toggle
    var baseItemSelector = 'li:has([data-toggle="tab"])';
    var historyStack = [];

    // Merge options with defaults
    var $settings = $.extend({}, $.fn.bootstrapWizard.defaults, options);
    var $activeTab = null;
    var $navigation = null;

    this.rebindClick = function(selector, fn) {
      selector.unbind('click', fn).bind('click', fn);
    }

    this.fixNavigationButtons = function() {
      // Get the current active tab
      if (!$activeTab.length) {
        // Select first one
        $navigation.find('a:first').tab('show');
        $activeTab = $navigation.find(baseItemSelector + ':first');
      }

      // See if we're currently in the first/last then disable the previous and last buttons
      $($settings.previousSelector, element).toggleClass('disabled', (obj.firstIndex() >= obj.currentIndex()));
      $($settings.nextSelector, element).toggleClass('disabled', (obj.currentIndex() >= obj.navigationLength()));
      $($settings.nextSelector, element).toggleClass('hidden', (obj.currentIndex() >= obj.navigationLength() && $($settings.finishSelector, element).length > 0));
      $($settings.lastSelector, element).toggleClass('hidden', (obj.currentIndex() >= obj.navigationLength() && $($settings.finishSelector, element).length > 0));
      $($settings.finishSelector, element).toggleClass('hidden', (obj.currentIndex() < obj.navigationLength()));
      $($settings.backSelector, element).toggleClass('disabled', (historyStack.length == 0));
      $($settings.backSelector, element).toggleClass('hidden', (obj.currentIndex() >= obj.navigationLength() && $($settings.finishSelector, element).length > 0));

      // We are unbinding and rebinding to ensure single firing and no double-click errors
      obj.rebindClick($($settings.nextSelector, element), obj.next);
      obj.rebindClick($($settings.previousSelector, element), obj.previous);
      obj.rebindClick($($settings.lastSelector, element), obj.last);
      obj.rebindClick($($settings.firstSelector, element), obj.first);
      obj.rebindClick($($settings.finishSelector, element), obj.finish);
      obj.rebindClick($($settings.backSelector, element), obj.back);

      if ($settings.onTabShow && typeof $settings.onTabShow === 'function' && $settings.onTabShow($activeTab, $navigation, obj.currentIndex()) === false) {
        return false;
      }
    };

    this.next = function(e) {
      // If we clicked the last then dont activate this
      if (element.hasClass('last')) {
        return false;
      }

      if ($settings.onNext && typeof $settings.onNext === 'function' && $settings.onNext($activeTab, $navigation, obj.nextIndex()) === false) {
        return false;
      }

      var formerIndex = obj.currentIndex();
      var $index = obj.nextIndex();

      // Did we click the last button
      if ($index > obj.navigationLength()) {} else {
        historyStack.push(formerIndex);
        $navigation.find(baseItemSelector + ($settings.withVisible ? ':visible' : '') + ':eq(' + $index + ') a').tab('show');
      }
    };

    this.previous = function(e) {
      // If we clicked the first then dont activate this
      if (element.hasClass('first')) {
        return false;
      }

      if ($settings.onPrevious && typeof $settings.onPrevious === 'function' && $settings.onPrevious($activeTab, $navigation, obj.previousIndex()) === false) {
        return false;
      }

      var formerIndex = obj.currentIndex();
      var $index = obj.previousIndex();

      if ($index < 0) {} else {
        historyStack.push(formerIndex);
        $navigation.find(baseItemSelector + ($settings.withVisible ? ':visible' : '') + ':eq(' + $index + ') a').tab('show');
      }
    };

    this.first = function(e) {
      if ($settings.onFirst && typeof $settings.onFirst === 'function' && $settings.onFirst($activeTab, $navigation, obj.firstIndex()) === false) {
        return false;
      }

      // If the element is disabled then we won't do anything
      if (element.hasClass('disabled')) {
        return false;
      }


      historyStack.push(obj.currentIndex());
      $navigation.find(baseItemSelector + ':eq(0) a').tab('show');
    };

    this.last = function(e) {
      if ($settings.onLast && typeof $settings.onLast === 'function' && $settings.onLast($activeTab, $navigation, obj.lastIndex()) === false) {
        return false;
      }

      // If the element is disabled then we won't do anything
      if (element.hasClass('disabled')) {
        return false;
      }

      historyStack.push(obj.currentIndex());
      $navigation.find(baseItemSelector + ':eq(' + obj.navigationLength() + ') a').tab('show');
    };

    this.finish = function(e) {
      if ($settings.onFinish && typeof $settings.onFinish === 'function') {
        $settings.onFinish($activeTab, $navigation, obj.lastIndex());
      }
    };

    this.back = function() {
      if (historyStack.length == 0) {
        return null;
      }

      var formerIndex = historyStack.pop();
      if ($settings.onBack && typeof $settings.onBack === 'function' && $settings.onBack($activeTab, $navigation, formerIndex) === false) {
        historyStack.push(formerIndex);
        return false;
      }

      element.find(baseItemSelector + ':eq(' + formerIndex + ') a').tab('show');
    };

    this.currentIndex = function() {
      return $navigation.find(baseItemSelector + ($settings.withVisible ? ':visible' : '')).index($activeTab);
    };

    this.firstIndex = function() {
      return 0;
    };

    this.lastIndex = function() {
      return obj.navigationLength();
    };

    this.getIndex = function(e) {
      return $navigation.find(baseItemSelector + ($settings.withVisible ? ':visible' : '')).index(e);
    };

    this.nextIndex = function() {
      var nextIndexCandidate = this.currentIndex();
      var nextTabCandidate = null;
      do {
        nextIndexCandidate++;
        nextTabCandidate = $navigation.find(baseItemSelector + ($settings.withVisible ? ':visible' : '') + ":eq(" + nextIndexCandidate + ")");
      } while ((nextTabCandidate) && (nextTabCandidate.hasClass("disabled")));
      return nextIndexCandidate;
    };
    this.previousIndex = function() {
      var prevIndexCandidate = this.currentIndex();
      var prevTabCandidate = null;
      do {
        prevIndexCandidate--;
        prevTabCandidate = $navigation.find(baseItemSelector + ($settings.withVisible ? ':visible' : '') + ":eq(" + prevIndexCandidate + ")");
      } while ((prevTabCandidate) && (prevTabCandidate.hasClass("disabled")));
      return prevIndexCandidate;
    };
    this.navigationLength = function() {
      return $navigation.find(baseItemSelector + ($settings.withVisible ? ':visible' : '')).length - 1;
    };
    this.activeTab = function() {
      return $activeTab;
    };
    this.nextTab = function() {
      return $navigation.find(baseItemSelector + ':eq(' + (obj.currentIndex() + 1) + ')').length ? $navigation.find(baseItemSelector + ':eq(' + (obj.currentIndex() + 1) + ')') : null;
    };
    this.previousTab = function() {
      if (obj.currentIndex() <= 0) {
        return null;
      }
      return $navigation.find(baseItemSelector + ':eq(' + parseInt(obj.currentIndex() - 1) + ')');
    };
    this.show = function(index) {
      var tabToShow = isNaN(index) ?
        element.find(baseItemSelector + ' a[href="#' + index + '"]') :
        element.find(baseItemSelector + ':eq(' + index + ') a');
      if (tabToShow.length > 0) {
        historyStack.push(obj.currentIndex());
        tabToShow.tab('show');
      }
    };
    this.disable = function(index) {
      $navigation.find(baseItemSelector + ':eq(' + index + ')').addClass('disabled');
    };
    this.enable = function(index) {
      $navigation.find(baseItemSelector + ':eq(' + index + ')').removeClass('disabled');
    };
    this.hide = function(index) {
      $navigation.find(baseItemSelector + ':eq(' + index + ')').hide();
    };
    this.display = function(index) {
      $navigation.find(baseItemSelector + ':eq(' + index + ')').show();
    };
    this.remove = function(args) {
      var $index = args[0];
      var $removeTabPane = typeof args[1] != 'undefined' ? args[1] : false;
      var $item = $navigation.find(baseItemSelector + ':eq(' + $index + ')');

      // Remove the tab pane first if needed
      if ($removeTabPane) {
        var $href = $item.find('a').attr('href');
        $($href).remove();
      }

      // Remove menu item
      $item.remove();
    };

    var innerTabClick = function(e) {
      // Get the index of the clicked tab
      var $ul = $navigation.find(baseItemSelector);
      var clickedIndex = $ul.index($(e.currentTarget).parent(baseItemSelector));
      var $clickedTab = $($ul[clickedIndex]);
      if ($settings.onTabClick && typeof $settings.onTabClick === 'function' && $settings.onTabClick($activeTab, $navigation, obj.currentIndex(), clickedIndex, $clickedTab) === false) {
        return false;
      }
    };

    var innerTabShown = function(e) {
      var $element = $(e.target).parent();
      var nextTab = $navigation.find(baseItemSelector).index($element);

      // If it's disabled then do not change
      if ($element.hasClass('disabled')) {
        return false;
      }

      if ($settings.onTabChange && typeof $settings.onTabChange === 'function' && $settings.onTabChange($activeTab, $navigation, obj.currentIndex(), nextTab) === false) {
        return false;
      }

      $activeTab = $element; // activated tab
      obj.fixNavigationButtons();
    };

    this.resetWizard = function() {

      // remove the existing handlers
      $('a[data-toggle="tab"]', $navigation).off('click', innerTabClick);
      $('a[data-toggle="tab"]', $navigation).off('show show.bs.tab', innerTabShown);

      // reset elements based on current state of the DOM
      $navigation = element.find('ul:first', element);
      $activeTab = $navigation.find(baseItemSelector + '.active', element);

      // re-add handlers
      $('a[data-toggle="tab"]', $navigation).on('click', innerTabClick);
      $('a[data-toggle="tab"]', $navigation).on('show show.bs.tab', innerTabShown);

      obj.fixNavigationButtons();
    };

    $navigation = element.find('ul:first', element);
    $activeTab = $navigation.find(baseItemSelector + '.active', element);

    if (!$navigation.hasClass($settings.tabClass)) {
      $navigation.addClass($settings.tabClass);
    }

    // Load onInit
    if ($settings.onInit && typeof $settings.onInit === 'function') {
      $settings.onInit($activeTab, $navigation, 0);
    }

    // Load onShow
    if ($settings.onShow && typeof $settings.onShow === 'function') {
      $settings.onShow($activeTab, $navigation, obj.nextIndex());
    }

    $('a[data-toggle="tab"]', $navigation).on('click', innerTabClick);

    // attach to both show and show.bs.tab to support Bootstrap versions 2.3.2 and 3.0.0
    $('a[data-toggle="tab"]', $navigation).on('show show.bs.tab', innerTabShown);
  };
  $.fn.bootstrapWizard = function(options) {
    //expose methods
    if (typeof options == 'string') {
      var args = Array.prototype.slice.call(arguments, 1)
      if (args.length === 1) {
        args.toString();
      }
      return this.data('bootstrapWizard')[options](args);
    }
    return this.each(function(index) {
      var element = $(this);
      // Return early if this element already has a plugin instance
      if (element.data('bootstrapWizard')) return;
      // pass options to plugin constructor
      var wizard = new bootstrapWizardCreate(element, options);
      // Store plugin object in this element's data
      element.data('bootstrapWizard', wizard);
      // and then trigger initial change
      wizard.fixNavigationButtons();
    });
  };

  // expose options
  $.fn.bootstrapWizard.defaults = {
    withVisible: true,
    tabClass: 'nav nav-pills',
    nextSelector: '.wizard li.next',
    previousSelector: '.wizard li.previous',
    firstSelector: '.wizard li.first',
    lastSelector: '.wizard li.last',
    finishSelector: '.wizard li.finish',
    backSelector: '.wizard li.back',
    onShow: null,
    onInit: null,
    onNext: null,
    onPrevious: null,
    onLast: null,
    onFirst: null,
    onFinish: null,
    onBack: null,
    onTabChange: null,
    onTabClick: null,
    onTabShow: null
  };

})(jQuery);