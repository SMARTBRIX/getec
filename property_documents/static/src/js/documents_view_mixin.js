odoo.define('property_documents.viewMixin', function (require) {
'use strict';

    const DocumentsViewMixin = require('documents.viewMixin');
    DocumentsViewMixin.inspectorFields.push('property_id');
    
    return DocumentsViewMixin;

});
