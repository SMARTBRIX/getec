odoo.define('property_management.Portal', function (require) {
'use strict';

const publicWidget = require('web.public.widget');

publicWidget.registry.PropertyDetailPortal = publicWidget.Widget.extend({
    selector: '.dr-portal-property-page',
    events: {
        'click .dr-protected-download': '_onClickProtectedDownload',
    },

    start: function () {
        this.leadID = this.$el.attr('data-lead-id');
        return this._super.apply(this, arguments);
    },

    _onClickProtectedDownload: function (ev) {
        ev.preventDefault();
        const $target = $(ev.currentTarget);

        const link = $target.attr('href');
        const ID = $target.attr('data-id');
        const model = $target.attr('data-model');

        return this._rpc({
            route: '/property_management/log_downloaded_protected_document',
            params: {
                lead_id: parseInt(this.leadID),
                attachment_id: parseInt(ID),
                model_name: model,
            }
        }).then(() => {
            window.location = link;
        });
    },
});

publicWidget.registry.DrPropertyTerms = publicWidget.Widget.extend({
    selector: '#termsModal',
    events: {
        'click .accept': '_onClick',
    },
    start: function () {
        this.$el.modal('show');
        this.$el.on('hidden.bs.modal', function () {
            window.location.href='/my/property_objects';
        });
        this.$el.on('hidden.bs.modal', function () {
            window.location.href='/my/tenancies';
        });
        return this._super.apply(this, arguments);
    },
    _onClick: function (ev) {
        const leadID = parseInt(this.el.dataset.leadId);
        const requiredCheckbox = this.$('.form-check-input[required]').length;
        const tickedRequiredCheckbox = this.$('.form-check-input[required]:checked').length;
        const accepedTermsIDs = _.map(this.$('.form-check-input:checked'), function (el) {
            return parseInt(el.getAttribute('id'));
        });

        if (requiredCheckbox == tickedRequiredCheckbox) {
            this._rpc({
                model: 'crm.lead',
                method: 'change_property_terms',
                args: [
                    [leadID],
                    {accepted_terms_ids: accepedTermsIDs},
                ]
            }).then(function () {
                window.location.reload();
            });
        }
    },
});

});
