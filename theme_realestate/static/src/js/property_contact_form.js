odoo.define('theme_realestate.property_contact_form', function (require) {
'use strict';

var publicWidget = require('web.public.widget');


publicWidget.registry.RealestatePropertyContactForm = publicWidget.Widget.extend({
    selector: '.s_webiste_form_property_contact',
    events: {
        'change #t_and_c': '_onChangeTermConditions',
        'change select[id="country_id"]': '_onChangeCountry',
    },
    _onChangeTermConditions: function (ev) {
        if ($(ev.currentTarget).prop('checked')) {
            this.$('.o_website_form_send').removeAttr('disabled');
        } else {
            this.$('.o_website_form_send').attr('disabled', '1');
        }
    },
    _onChangeCountry: function () {
        const $state = this.$("select[id='state_id']");
        const $country = this.$("select[id='country_id']");
        $state.html('');

        if (!$country.val()) {
            return;
        }

        this._rpc({
            route: '/real_estate/country_infos/' + $country.val(),
        }).then(function (data) {
            if (data.states.length) {
                _.each(data.states, function (x) {
                    var opt = $('<option>').text(x[1])
                        .attr('value', x[0])
                        .attr('data-code', x[2]);
                    $state.append(opt);
                });
            }
        });
    },
});

});
