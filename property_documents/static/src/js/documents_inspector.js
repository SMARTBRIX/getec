odoo.define('property_documents.DocumentsInspector', function (require) {
'use strict';

/**
 * This file defines the DocumentsInspector Widget, which is displayed next to
 * the KanbanRenderer in the DocumentsKanbanView.
 */

const DocumentsInspector = require('documents.DocumentsInspector');

DocumentsInspector.include({
    /**
     * Render and append a field widget for the given field and the current
     * records.
     *
     * @private
     * @param {string} fieldName
     * @param {Object} [options] options to pass to the field
     * @param {string} [options.icon] optional icon to display
     * @param {string} [options.label] the label to display
     * @return {Promise}
     */
    /**
     * @private
     * @return {Promise}
     */
    _renderFields: function () {
        const parentPromise = this._super(...arguments);
        const options = {mode: 'edit'};
        const proms = [];
        if (this.records.length > 0) {
            proms.push(this._renderField('property_id', options));
        }
        return Promise.all([proms, parentPromise])
    },
});

return DocumentsInspector;

});
