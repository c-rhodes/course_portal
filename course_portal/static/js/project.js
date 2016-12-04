/* Project specific Javascript goes here. */

/*
Formatting hack to get around crispy-forms unfortunate hardcoding
in helpers.FormHelper:

    if template_pack == 'bootstrap4':
        grid_colum_matcher = re.compile('\w*col-(xs|sm|md|lg|xl)-\d+\w*')
        using_grid_layout = (grid_colum_matcher.match(self.label_class) or
                             grid_colum_matcher.match(self.field_class))
        if using_grid_layout:
            items['using_grid_layout'] = True

Issues with the above approach:

1. Fragile: Assumes Bootstrap 4's API doesn't change (it does)
2. Unforgiving: Doesn't allow for any variation in template design
3. Really Unforgiving: No way to override this behavior
4. Undocumented: No mention in the documentation, or it's too hard for me to find
*/
$('.form-group').removeClass('row');

function apply_form_field_error(fieldname, error) {
    $input = $('#id_' + fieldname);
    $container = $('#div_id_' + fieldname);
    var error_msg = $('<span />').addClass('error').text(error[0]);

    $container.addClass('has-error');
    error_msg.insertAfter($input);
}

function clear_form_field_errors(form) {
    $('.error', $(form)).remove();
    $('.has-error', $(form)).removeClass('has-error');
}

function add_success_message(message) {
    (function (el) {
        setTimeout(function () {
            el.children().remove('div');
        }, 5000);
    }($('#messages').append('<div class="alert alert-success">' + message + '</div>')));
}

function showModal(selector, bodyText, confirmFunction) {
    var $modal = $(selector);
    if (bodyText !== undefined) {
        $modal.find('.modal-body').html(bodyText);
    }
    $modal.modal('show');

    $modal.find('#confirm-no').click(function(event) {
        event.preventDefault();
        $modal.modal('hide');
    });

    $modal.find('#confirm-yes').click(function(event) {
        $modal.modal('hide');
        if (confirmFunction !== undefined) {
            confirmFunction(event);
        }
    });
}

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}