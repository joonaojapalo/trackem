// Generated by CoffeeScript 1.10.0
(function() {
  define(["app/state", "app/store", "app/collections/races"], function(state, Store, Races) {
    var MapsStore;
    MapsStore = Store.extend({
      fetchableClass: Races,
      setup: function() {
        this.fetchable.group = state.get("group");
        return this.listenTo(state, "change:group", this.refetch);
      }
    });
    return new MapsStore;
  });

}).call(this);
