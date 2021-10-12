$(document).ready(function() {
    $(".ajx").submit(function(e) {
        e.preventDefault();
        var form = $(this);
        var url = form.attr("action");
        var resp = $(this).children().children().attr("value")
        $.ajax({
            type: "POST",
            url: url,
            data: resp,
            success: function() {
                $('#Overlay').fadeIn(297, function() {
                    $('#Modal_confirm')
                        .css('display', 'block')
                        .animate({ opacity: 1 }, 198);

                    $('#Overlay').click(function() {
                        $('#Modal_confirm').animate({ opacity: 0 }, 198,
                            function() {
                                $(this).css('display', 'none');
                                $('#Overlay').fadeOut(297);

                            });

                    });

                    $('.modal_button_left').click(function(event) {
                        event.preventDefault();
                        $('#Overlay').fadeIn(297, function() {
                            $('#Modal_delete')
                                .css('display', 'block')
                                .animate({ opacity: 1 }, 198);
                            $.ajax({
                                type: "DELETE",
                                url: url
                            })
                        });
                    });

                    $('#Overlay, #close').click(function() {
                        $('#Modal_delete').animate({ opacity: 0 }, 5,
                            function() {
                                $(this).css('display', 'none');
                                $('#Modal_confirm').css('display', 'none');
                                $('#Overlay').fadeOut(297);
                                location.reload()
                            });
                    });

                    $('.modal_button_right').click(function(event) {
                        var url = $(this).attr('href');
                        window.location.href = url;
                    })

                });
            }
        })

    })
    setTimeout(function() {
        $(".flash").fadeOut('fast');
    }, 3000)
});