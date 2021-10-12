// var reg1 = /[-._!"`'#%&,:;<>=@{}~\$\(\)\*\+\/\\\?\[\]\^\|А-я]+/
var reg1 = /[._!"`#%&,:;<>=@{}~\$\(\)\*\+\/\\\?\[\]\^\|]+/

$(document).ready(function() {

    var validTitle = false;

    $("form").submit(function(event) {
        event.preventDefault();

        var title = $("#titleg").val();
        var select = $("#selg").val();
        const optValues = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10'];

        if (title == "" || reg1.test(title) || title.length <= 1 || title.length >= 73) {
            $("#titleg").parent().removeClass("has-success").addClass("has-error");
            validTitle = false;
        } else {
            $("#titleg").parent().removeClass("has-error").addClass("has-success");
            validTitle = true;
        }

        if (!optValues.includes(select)) {
            $("#selg").parent().removeClass("has-success").addClass("has-error");
            validSelect = false;
        } else {
            $("#selg").parent().removeClass("has-error").addClass("has-success");
            validSelect = true;
        }

        if (validTitle == true && validSelect == true) {
            $("form").unbind('submit').submit();
        }
        setTimeout(function() {
            $(".flash").fadeOut('fast');
        }, 3000)
    });


});