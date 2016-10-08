if ($.carApp === undefined) {
        $.carApp = {};
    }

$.carApp.Car = Backbone.RelationalModel.extend({
    urlRoot: '/api/v1/Car/'
    // relations: [{
    //     type: Backbone.HasOne,
    //     key: 'user',
    //     relatedModel: '$.tutorsApp.PrivateUser',
    //     includeInJSON: 'resource_uri'
    // }]
});

$.carApp.CarCollection = Backbone.Collection.extend({
    model: $.carApp.Car,
    url: '/api/v1/Car/'
});
