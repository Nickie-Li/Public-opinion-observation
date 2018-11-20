
$(document).ready(function () {
    $.extend($.easing, {
        easeOutExpo: function (x, t, b, c, d) {
            return (t == d) ? b + c : c * (-Math.pow(2, -10 * t / d) + 1) + b;
        }
    });
    $("#gotop").click(function () {
        jQuery("html,body").animate({
            scrollTop: 0
        }, 1000, "easeOutExpo");
    });

});

