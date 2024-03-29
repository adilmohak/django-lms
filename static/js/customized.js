$(document).ready(function () {
    $('#login-form').submit(function (e) {
        // e.preventDefault();
        $('#login-btn').addClass('disabled')
        $('#login-btn').html(`Signing you in`)
    });
    $('#username').on("input", function () {
        username = $(this).val();

        $.ajax({
            url: "/accounts/ajax/validate-username/",
            data: {
                username: username
            },
            dataType: 'json',
            success: function (data) {
                if (data.is_token) {
                    console.log(data.is_taken);
                    $('#message-wrapper').html(`<p class="my-2 text-danger"><span class="bg-error p-2"><b>${username}</b> already taken :( try another one </span></p>)`)
                }
                else {
                    $('#message-wrapper').html(`<p class="my-2 text-success"><span class="bg-correct p-2"><b>${username}</b> is valid </span></p>`)
                }
            }
        })
    });
});