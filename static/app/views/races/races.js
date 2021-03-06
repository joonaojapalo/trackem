// Generated by CoffeeScript 1.10.0
(function() {
  define(["radio", "app/state", "marionette", "text!templates/races/race-item"], function(Radio, state, Marionette, template) {
    var RaceItemView, RacesView;
    RaceItemView = Marionette.ItemView.extend({
      tagName: "li",
      className: "list-group-item",
      template: template,
      events: {
        "click a": "selectRace"
      },
      selectRace: function(e) {
        (Radio.channel("races")).trigger("select", this.model);
        return e.preventDefault();
      }
    });
    return RacesView = Marionette.CollectionView.extend({
      childView: RaceItemView,
      tagName: "ul",
      className: "list-group"
    });
  });

}).call(this);
