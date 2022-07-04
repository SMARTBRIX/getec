odoo.define('property_management.fields_widget', function (require) {
"use strict";

const fieldRegistry = require('web.field_registry');
const { FieldMany2ManyBinaryMultiFiles } = require('web.relational_fields');

const FieldMultiAttachments = FieldMany2ManyBinaryMultiFiles.extend({
    template: 'FieldMultiAttachments',
    template_files: 'CustomFieldBinaryFileUploader.files',
    init: function () {
        this._super.apply(this, arguments);
        this.image_only = this.nodeOptions.image_only;
    },
});

fieldRegistry.add('dr_field_multi_attachments', FieldMultiAttachments);

});
