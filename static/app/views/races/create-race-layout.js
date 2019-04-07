// Generated by CoffeeScript 1.10.0
(function() {
  define(["jquery", "underscore", "radio", "marionette", "text!templates/races/add-modal", "widgets/select", "stores/maps", "stores/races", "app/models/race", "app/state"], function($, _, Radio, Marionette, template, SelectView, mapsStore, racesStore, Race, state) {
    var CreateRaceLayout;
    return CreateRaceLayout = Marionette.LayoutView.extend({
      template: template,
      regions: {
        mapsRegion: '[data-region="maps-dropdown"]'
      },
      ui: {
        name: '[name="race-name"]',
        createBtn: '[data-action="create"]'
      },
      events: {
        'click @ui.createBtn': "onCreate",
        "keyup @ui.name": "onNameChange"
      },
      mountData: [mapsStore, racesStore],
      initialize: function() {
        _.bindAll(this, "mount", "onCreate", "onSelectMapChange", "onNameChange");
        this.race = new Race({
          group: state.get("group")
        });
        this.race.on("error", this.onInvalid);
        return this.promises = _.invoke(this.mountData, "fetch");
      },
      onBeforeShow: function() {
        var all;
        all = $.when.apply(this, this.promises);
        return all.done(this.mount);
      },
      mount: function(maps, races) {
        var select;
        this.races = races;
        select = new SelectView({
          prefix: "select:map",
          collection: maps,
          nameAttr: "name",
          valueAttr: "id"
        });
        select.on("select:map:change", this.onSelectMapChange);
        return this.mapsRegion.show(select);
      },
      onSelectMapChange: function(model) {
        return this.race.set("map", model.get("id"));
      },
      onNameChange: function() {
        return this.race.set("name", this.ui.name.val());
      },
      onInvalid: function(error) {
        return console.log("invalid", error);
      },
      onCreate: function() {
        if (this.race.validate) {
          return;
        }
        return this.races.create(this.race, {
          wait: true
        });
      }
    });
  });

}).call(this);
