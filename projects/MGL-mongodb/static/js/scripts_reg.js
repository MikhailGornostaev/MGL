var reg1 = /[-._!"`'#%&,:;<>=@{}~\$\(\)\*\+\/\\\?\[\]\^\|А-я]+/
var reg2 = /[-_\*#]|A-z0-9]+/
var reg3 = /[.!"`'#%&,:;<>=@{}~\$\(\)\*\+\/\\\?\[\]\^\|А-я]+/
var reg4 = /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/

$(document).ready(function() {

    var validLgn = false;
    var validPass = false;

    $("form").submit(function(event) {
        event.preventDefault();

        var lgn = $("#login").val();
        var pass = $("#pass").val();
        var nick = $("#nick").val();
        var email = $("#email").val();

        if (nick == "" || reg3.test(nick) || nick.length <= 1 || nick.length >= 16) {
            $("#nick").parent().removeClass("has-success").addClass("has-error");
            validNick = false;
        } else {
            $("#nick").parent().removeClass("has-error").addClass("has-success");
            validNick = true;
        }

        if (lgn == "" || reg1.test(lgn) || lgn.length <= 4 || lgn.length >= 16) {
            $("#login").parent().removeClass("has-success").addClass("has-error");
            validLgn = false;
        } else {
            $("#login").parent().removeClass("has-error").addClass("has-success");
            validLgn = true;
        }

        if (pass == "" || !reg2.test(pass) || pass.length <= 5 || pass.length >= 21) {
            $("#pass").parent().removeClass("has-success").addClass("has-error");
            validPass = false;
        } else {
            $("#pass").parent().removeClass("has-error").addClass("has-success");

            validPass = true;
        }

        if (email == "" || !reg4.test(email) || email.length <= 6 || email.length >= 51) {
            $("#email").parent().removeClass("has-success").addClass("has-error");
            validEmail = false;
        } else {
            $("#email").parent().removeClass("has-error").addClass("has-success");

            validEmail = true;
        }

        if (validLgn == true && validNick == true && validPass == true && validEmail == true) {
            $("form").unbind('submit').submit();
        }

    });
        setTimeout(function() {
            $(".flash").fadeOut('fast');
        }, 3000)

});