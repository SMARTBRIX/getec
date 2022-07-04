odoo.define('theme_realestate.frontend', function (require) {
'use strict';
console.log("dddddddddddddddd")
var publicWidget = require('web.public.widget');
var core = require('web.core');

require('web.dom_ready');

var _t = core._t;
var QWeb = core.qweb;

// Enable bootstrap tooltip
$('[data-toggle="tooltip"]').tooltip({
    delay: {
        show: 100,
        hide: 100,
    },
});

publicWidget.registry.DrPropertySearch = publicWidget.Widget.extend({
    selector: '.dr-property-search-container',
    read_events: {
        'click .dr-properties-search-btn': '_onClickSearchBtn',
        'change #property-location-collapse input': '_onClickPropertyLocation',
    },
    start: function () {
        var self = this;
        this.$el.on('show.bs.collapse', '.dr-root-collapse', function (ev) {
            if (!$(ev.target).hasClass('dr-child-collapse')) {
                self.$('.dr-root-collapse').collapse('hide');
            }
        });
        this.$el.on('hidden.bs.collapse', '.dr-root-collapse', function (ev) {
            if (!$(ev.target).hasClass('dr-child-collapse')) {
                self._applySelected();
            }
        });
        return this._super.apply(this, arguments);
    },
    _onClickSearchBtn: function (ev) {
        ev.preventDefault();
        var params = this._getParams(ev);
        var newUrl = $.param.querystring(window.location.origin + '/real_estate/properties', params);
        window.location = newUrl;
    },
    _applySelected: function () {
        var sellTypeChecked = this.$('#sell-type-collapse [name=sell-type]:checked');
        if (sellTypeChecked.length) {
            // this.$('[data-target="#sell-type-collapse"] span').text(_t(sellTypeChecked.val() == 'buy' ? $('#buy').text() :  $('#rent').text()));

            this.$('[data-target="#sell-type-collapse"] span').text(_t(sellTypeChecked.val() == 'buy' ? $('#buy').text() : (_t(sellTypeChecked.val() == 'rent' ? $('#rent').text() : $('#tolease').text()))));

        } else {
            this.$('[data-target="#sell-type-collapse"] span').text(_t('Select'));
        }

        var selectedPropertyType = [];
        this.$('#property-type-collapse input:checked').each(function () {
            selectedPropertyType.push($(this).attr('string'));
        });
        if (selectedPropertyType.length) {
            this.$('[data-target="#property-type-collapse"] span').text(_t(selectedPropertyType.slice(0, 2).join(', ')));
        } else {
            this.$('[data-target="#property-type-collapse"] span').text(_t('Select'));
        }

        var selectedPropertyLocation = [];
        this.$('#property-location-collapse [id^="property-sub-location"]:checked').each(function () {
            selectedPropertyLocation.push($(this).attr('string'));
        });
        if (selectedPropertyLocation.length) {
            this.$('[data-target="#property-location-collapse"] span').text(_t(selectedPropertyLocation.slice(0, 2).join(', ')));
        } else {
            this.$('[data-target="#property-location-collapse"] span').text(_t('Select'));
        }

        var actualMinPrice = parseInt(this.$('div#price-range-collapse .dr-range-slider').data('min') || 0);
        var actualMaxPrice = parseInt(this.$('div#price-range-collapse .dr-range-slider').data('max') || 0);
        var minPrice = parseInt(this.$('div#price-range-collapse input[name=min_value]').val() || 0);
        var maxPrice = parseInt(this.$('div#price-range-collapse input[name=max_value]').val() || 0);
        if (actualMinPrice !== minPrice || actualMaxPrice !== maxPrice) {
            this.$('[data-target="#price-range-collapse"] span').text(_t(this.$('.dr-currency-symbol').text() + ' ' + minPrice + ' - ' + maxPrice));
        } else {
            this.$('[data-target="#price-range-collapse"] span').text(_t('Select'));
        }
    },
    _getParams: function (ev) {
        var params = {};

        if (this.$('input[name=reference]').val()) {
            params['reference'] = this.$('input[name=reference]').val();
        }

        var sellTypeChecked = this.$('#sell-type-collapse [name=sell-type]:checked');
        if (sellTypeChecked.length) {
            params['sell_type'] = sellTypeChecked.val();
        }

        var selectedPropertyType = [];
        this.$('#property-type-collapse input:checked').each(function () {
            selectedPropertyType.push($(this).val());
        });
        if (selectedPropertyType.length) {
            params['property_type'] = selectedPropertyType.join(',');
        }

        var selectedPropertySublocation = [];
        this.$('#property-location-collapse [id^="property-sub-location"]:checked').each(function () {
            selectedPropertySublocation.push($(this).val());
        });
        if (selectedPropertySublocation.length) {
            params['property_sublocation'] = selectedPropertySublocation.join(',');
        }

        var bedroomsChecked = this.$('#bedrooms-collpase [name=bedroom]:checked');
        if (bedroomsChecked.length) {
            params['bedrooms'] = bedroomsChecked.val();
        }

        var bathroomsChecked = this.$('#bathrooms-collpase [name=bathroom]:checked');
        if (bathroomsChecked.length) {
            params['bathrooms'] = bathroomsChecked.val();
        }

        var parkingsChecked = this.$('#parkings-collpase [name=parking]:checked');
        if (parkingsChecked.length) {
            params['parkings'] = parkingsChecked.val();
        }

        var garagesChecked = this.$('#garages-collpase [name=garage]:checked');
        if (garagesChecked.length) {
            params['garages'] = garagesChecked.val();
        }

        var actualMinPrice = parseInt(this.$('div#price-range-collapse .dr-range-slider').data('min') || 0);
        var actualMaxPrice = parseInt(this.$('div#price-range-collapse .dr-range-slider').data('max') || 0);
        var minPrice = parseInt(this.$('div#price-range-collapse input[name=min_value]').val() || 0);
        var maxPrice = parseInt(this.$('div#price-range-collapse input[name=max_value]').val() || 0);
        if (actualMinPrice !== minPrice || actualMaxPrice !== maxPrice) {
            params['from_price'] = minPrice;
            params['to_price'] = maxPrice;
        }

        var actualLivingSpaceMinValue = parseInt(this.$('div#living-space-collpase .dr-range-slider').data('min') || 0);
        var actualLivingSpaceMaxValue = parseInt(this.$('div#living-space-collpase .dr-range-slider').data('max') || 0);
        var livingSpaceMinValue = parseInt(this.$('div#living-space-collpase input[name=min_value]').val() || 0);
        var livingSpaceMaxValue = parseInt(this.$('div#living-space-collpase input[name=max_value]').val() || 0);
        if (actualLivingSpaceMinValue !== livingSpaceMinValue || actualLivingSpaceMaxValue !== livingSpaceMaxValue) {
            params['property_living_space_from_value'] = livingSpaceMinValue;
            params['property_living_space_to_value'] = livingSpaceMaxValue;
        }

        var actualPlotAreaMinValue = parseInt(this.$('div#plot-area-collpase .dr-range-slider').data('min') || 0);
        var actualPlotAreaMaxValue = parseInt(this.$('div#plot-area-collpase .dr-range-slider').data('max') || 0);
        var plotAreaMinValue = parseInt(this.$('div#plot-area-collpase input[name=min_value]').val() || 0);
        var plotAreaMaxValue = parseInt(this.$('div#plot-area-collpase input[name=max_value]').val() || 0);
        if (actualPlotAreaMinValue !== plotAreaMinValue || actualPlotAreaMaxValue !== plotAreaMaxValue) {
            params['property_plot_area_from_value'] = plotAreaMinValue;
            params['property_plot_area_to_value'] = plotAreaMaxValue;
        }
        return params;
    },
    _onClickPropertyLocation: function (ev) {
        const isParent = ev.currentTarget.getAttribute('id').startsWith('property-location');
        if (isParent) {
            const childs = this.$el[0].querySelectorAll('[data-parent-id="' + ev.currentTarget.value + '"]');
            _.each(childs, function (child) {
                child.checked = ev.currentTarget.checked;
            });
        } else {
            const childs = this.$el[0].querySelectorAll('[data-parent-id="' + ev.currentTarget.getAttribute('data-parent-id') + '"]');
            let isParentSelectable = true;
            _.each(childs, function (child) {
                if (!child.checked) {
                    isParentSelectable = false;
                }
            });
            this.$el[0].querySelector('#property-location-' + ev.currentTarget.getAttribute('data-parent-id')).checked = isParentSelectable;
        }
    },
});

publicWidget.registry.DrPropertyCoverImages = publicWidget.Widget.extend({
    selector: '.dr-property-page',
    start: function () {
        var $owlCover = this.$('.dr-property-cover-carousel');
        var $owlThumb = this.$('.dr-property-cover-thumb-carousel');

        $owlCover.owlCarousel({
            items: 1,
            dots: false,
            autoplay: true,
            lazyLoad: true,
            autoplayTimeout: 5000,
            autoplayHoverPause: true,
            rewind: true,
        }).on('changed.owl.carousel', function (el) {
            var current = el.item.index;
            $owlThumb.find('.owl-item').removeClass('current').eq(current).addClass('current');
            $owlThumb.data('owl.carousel').to(current, 300, true);
        });
        this.$('.dr-owl-carousel-prev').click(function() {
            $owlCover.trigger('prev.owl.carousel');
        });
        this.$('.dr-owl-carousel-next').click(function() {
            $owlCover.trigger('next.owl.carousel');
        });

        $owlThumb.on('initialized.owl.carousel', function () {
            $owlThumb.find('.owl-item').eq(0).addClass('current');
        });
        $owlThumb.owlCarousel({
            items: 12,
            dots: false,
            margin: 6,
            stagePadding: 6,
        }).on('changed.owl.carousel', function (el) {
            var number = el.item.index;
            $owlCover.data('owl.carousel').to(number, 300, true);
        });
        $owlThumb.on('click', '.owl-item', function (e) {
            e.preventDefault();
            var number = $(this).index();
            $owlCover.data('owl.carousel').to(number, 300, true);
        });
        return this._super.apply(this, arguments);
    },
});

publicWidget.registry.DrPropertyGrid = publicWidget.Widget.extend({
    selector: '.dr-property-grid-image',
    read_events: {
        'click img': '_onClickImage',
    },
    start: function () {
        this.items = _.map(this.$('img'), function (img) {
            var $img = $(img);
            return {
                src: $img.attr('src'),
                w: $img[0].naturalWidth,
                h: $img[0].naturalHeight,
            }
        });
        return this._super.apply(this, arguments);
    },
    _onClickImage: function (ev) {
        var photoSwipe = new PhotoSwipe($('.pswp')[0], PhotoSwipeUI_Default, this.items, {
            shareButtons: [
                {id: 'download', label: _t('Download image'), url: '{{raw_image_url}}', download: true},
            ],
            index: $(ev.currentTarget).parent().index(),
            closeOnScroll: false,
            bgOpacity: 0.8,
            tapToToggleControls: false,
            clickToCloseNonZoomable: false,
        });
        photoSwipe.init();
    },
});

publicWidget.registry.s_real_estate_search = publicWidget.Widget.extend({
    selector: '.s_real_estate_search',
    disabledInEditableMode: false,
    read_events: {
        'click .dr-search': '_onClickSearch',
    },
    xmlDependencies: ['/theme_realestate/static/src/xml/theme_realestate.xml'],
    willStart: function () {
        var self = this;
        var def = self._rpc({
            route:'/real_estate/get_search_snippet_data',
        }).then(function (data) {
            self.data = data;
        });
        return Promise.all([def, this._super.apply(this, arguments)]);
    },
    start: function () {
        this._initStructure();
        return this._super.apply(this, arguments);
    },
    _initStructure: function () {
        this.$target.children().remove();
        var $selector = QWeb.render('theme_realestate.s_real_estate_search_template', this.data);
        this.$el.append($selector);
        this.trigger_up('widgets_start_request', {$target: this.$('.o_wsale_products_searchbar_form')});
        this.trigger_up('widgets_start_request', {$target: this.$('.dr-range-slider-container')});
    },
    _onClickSearch: function (ev) {
        ev.preventDefault();
        var params = {};

        if (this.$('input[name=reference]').val()) {
            params['reference'] = this.$('input[name=reference]').val();
        }

        if (this.$('select[name=sell_type]').val()) {
            params['sell_type'] = this.$('select[name=sell_type]').val();
        }

        if (this.$('select[name=property_type]').val()) {
            params['property_type'] = this.$('select[name=property_type]').val();
        }

        if (this.$('select[name=property_location]').val()) {
            params['property_location'] = this.$('select[name=property_location]').val();
        }

        var actualMinPrice = parseInt(this.$('.dr-range-slider').data('min') || 0);
        var actualMaxPrice = parseInt(this.$('.dr-range-slider').data('max') || 0);
        var minPrice = parseInt(this.$('input[name=min_value]').val() || 0);
        var maxPrice = parseInt(this.$('input[name=max_value]').val() || 0);
        if (actualMinPrice !== minPrice || actualMaxPrice !== maxPrice) {
            params['from_price'] = minPrice;
            params['to_price'] = maxPrice;
        }

        var newUrl = $.param.querystring(window.location.origin + '/real_estate/properties', params);
        window.location = newUrl;
    },
});

publicWidget.registry.DrAddToFavorite = publicWidget.Widget.extend({
    selector: '.dr-add-to-favorite-btn',
    events: {
        'click': '_onClickBtn',
    },
    _onClickBtn: function (ev) {
        var self = this;
        ev.preventDefault();
        $(ev.currentTarget).addClass('disabled');
        this._rpc({
            route: '/real_estate/add_to_favorite/' + $(ev.currentTarget).attr('property-id'),
        }).then(function (res) {
            if (res) {
                self.displayNotification({
                    type: 'success',
                    title: _t('Success'),
                    message: _t('Added to Favorite'),
                });
            }
        });
    },
});

publicWidget.registry.DrLeafletMap = publicWidget.Widget.extend({
    selector: '#leaflet_map',
    start: function () {
        var latitude = this.$el.data('latitude') || 0;
        var longitude = this.$el.data('longitude') || 0;
        var map = L.map('leaflet_map', {
            attributionControl: false,
            doubleClickZoom: false,
            maxZoom: 18,
            boxZoom: false,
            touchZoom: false,
        }).setView([latitude, longitude], 16);
        L.marker([latitude, longitude]).addTo(map);
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(map);
        return this._super.apply(this, arguments);
    },
});

//------------------------------------------------------------------------------
// General
//------------------------------------------------------------------------------
publicWidget.registry.DrPropertyCardImages = publicWidget.Widget.extend({
    selector: '.dr-property-card-images',
    start: function () {
        var $owlSlider = this.$('.owl-carousel').owlCarousel({
            margin: 4,
            items: 1,
            dots: false,
            lazyLoad: true,
            rewind: true,
        });
        this.$('.dr-owl-carousel-prev').click(function() {
            $owlSlider.trigger('prev.owl.carousel');
        });
        this.$('.dr-owl-carousel-next').click(function() {
            $owlSlider.trigger('next.owl.carousel');
        });
        // Prevent conflict with parent owl slider
        $owlSlider.on('next.owl.carousel', function(event) {
            event.stopPropagation();
        })
        $owlSlider.on('prev.owl.carousel', function(event) {
            event.stopPropagation();
        })
        $owlSlider.on('mousedown.owl.core', function (event) {
            event.preventDefault()
            event.stopPropagation()
        });
        return this._super.apply(this, arguments);
    },
});

publicWidget.registry.DrRangeSlider = publicWidget.Widget.extend({
    selector: '.dr-range-slider-container',
    events: {
        'change input[name=min_value]': '_onChangeValue',
        'change input[name=max_value]': '_onChangeValue',
    },
    start: function () {
        var self = this;
        this.$('.dr-range-slider').ionRangeSlider({
            skin: 'square',
            prettify_separator: ',',
            type: 'double',
            onChange: function (ev) {
                self.$('input[name=min_value]').val(ev.from);
                self.$('input[name=max_value]').val(ev.to);
                self.$('.dr-range-validate').text('');
                self.$('[type=submit]').removeClass('d-none');
            },
        });
        this.rangeSlider = this.$('.dr-range-slider').data('ionRangeSlider');
        return this._super.apply(this, arguments);
    },
    _onChangeValue: function (ev) {
        ev.preventDefault();
        var minValue = this.$('input[name=min_value]').val();
        var maxValue = this.$('input[name=max_value]').val();
        if (isNaN(minValue) || isNaN(maxValue)) {
            this.$('.dr-range-validate').text(_t('Enter valid value'));
            this.$('[type=submit]').addClass('d-none');
            return false;
        }
        if (parseInt(minValue) > parseInt(maxValue)) {
            this.$('.dr-range-validate').text(_t('Invalid Range'));
            this.$('[type=submit]').addClass('d-none');
            return false;
        }
        this.rangeSlider.update({
            from: minValue,
            to: maxValue,
        });
        this.$('.dr-range-validate').text('');
        this.$('[type=submit]').removeClass('d-none');
        return false;
    },
});

//------------------------------------------------------------------------------
// Snippets
//------------------------------------------------------------------------------
publicWidget.registry.s_real_estate_search_2 = publicWidget.Widget.extend({
    selector: '.s_real_estate_search_2',
    disabledInEditableMode: false,
    willStart: function () {
        var self = this;
        var def = this._rpc({
            route: '/real_estate/get_search_2_snippet_data',
        }).then(function (template) {
            self.$template = $(template);
        });
        return Promise.all([def, this._super.apply(this, arguments)]);
    },
    start: function () {
        this.$target.empty();
        this.$el.append(this.$template);
        this.trigger_up('widgets_start_request', {$target: this.$('.dr-property-search-container')});
        return this._super.apply(this, arguments);
    },
    destroy: function () {
        this.$el.empty();
        this._super.apply(this, arguments);
    }
});

publicWidget.registry.s_real_estate_cover = publicWidget.Widget.extend({
    selector: '.s_real_estate_cover',
    disabledInEditableMode: false,
    willStart: function () {
        var self = this;
        var def = this._rpc({
            route: '/real_estate/get_cover_snippet_data',
        }).then(function (template) {
            self.$template = $(template);
        });
        return Promise.all([def, this._super.apply(this, arguments)]);
    },
    start: function () {
        this.$target.empty();
        this.$el.append(this.$template);
        this.$('.owl-carousel').owlCarousel({
            autoplay: true,
            autoplayTimeout: 9500,
            autoplayHoverPause: true,
            rewind: true,
            lazyLoad: true,
            items: 1,
            nav: true,
            navText: ['<span class="fa fa-chevron-left fa-2x"></span>','<span class="fa fa-chevron-right fa-2x"></span>'],
        });
        return this._super.apply(this, arguments);
    },
    destroy: function () {
        this.$el.empty();
        this._super.apply(this, arguments);
    }
});

publicWidget.registry.s_real_estate_categories = publicWidget.Widget.extend({
    selector: '.s_real_estate_categories',
    disabledInEditableMode: false,
    willStart: function () {
        var self = this;
        var def = this._rpc({
            route: '/real_estate/get_categories_snippet_data',
        }).then(function (template) {
            self.$template = $(template);
        });
        return Promise.all([def, this._super.apply(this, arguments)]);
    },
    start: function () {
        this._initStructure();
        return this._super.apply(this, arguments);
    },
    _initStructure: function () {
        this.$target.empty();
        this.$el.append(this.$template);
        _.each(this.$('.dr-property-category-box'), function (categoryBox) {
            var $categoryBox = $(categoryBox);
            var $owlSlider = $categoryBox.find('.dr-property-category').owlCarousel({
                dots: false,
                margin: 15,
                stagePadding: 5,
                rewind: true,
                responsive: {
                    0: {
                        items: 1,
                    },
                    576: {
                        items: 1,
                    },
                    768: {
                        items: 2,
                    },
                    992: {
                        items: 3,
                    },
                    1200: {
                        items: 3,
                    }
                },
            });
            $categoryBox.find('.dr-owl-category-carousel-prev').click(function() {
                $owlSlider.trigger('prev.owl.carousel');
            });
            $categoryBox.find('.dr-owl-category-carousel-next').click(function() {
                $owlSlider.trigger('next.owl.carousel');
            });
        });
        this.trigger_up('widgets_start_request', {$target: this.$('.dr-property-card-images')});
    },
    destroy: function () {
        this.$el.empty();
        this._super.apply(this, arguments);
    }
});

});
