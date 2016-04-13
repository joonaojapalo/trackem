// Generated by CoffeeScript 1.10.0
(function() {
  define(["underscore", "backbone"], function(_, Backbone) {
    var Maps;
    return Maps = Backbone.Model.extend({
      urlRoot: function() {
        return "/api/groups/" + (this.get('group')) + "/maps";
      },
      initialize: function(attributes) {
        return _.bindAll(this, "urlRoot");
      }
    });
  });

}).call(this);
