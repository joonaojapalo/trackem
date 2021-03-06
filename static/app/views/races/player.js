// Generated by CoffeeScript 1.10.0
(function() {
  define(["radio", "app/state", "underscore", "marionette", "text!templates/races/player"], function(Radio, state, _, Marionette, template) {
    var RacePlayerView;
    return RacePlayerView = Marionette.ItemView.extend({
      className: function() {
        if ((this.model.get("status")) === "started") {
          return "race-player race-player-started";
        } else {
          return "race-player race-player-stopped";
        }
      },
      template: template,
      templateHelpers: function() {
        return {
          followUrl: state["const"].url.followAPI + "/" + (this.model.get("race_hash"))
        };
      },
      ui: {
        start: '[data-action="start"]',
        stop: '[data-action="stop"]'
      },
      events: {
        "click @ui.start": "start",
        "click @ui.stop": "stop"
      },
      modelEvents: {
        "change:status": "onStatusChange"
      },
      onRender: function() {
        return this.onStatusChange();
      },
      start: function() {
        var promise;
        return promise = this.model.save({
          status: "started"
        }, {
          wait: true
        });
      },
      stop: function() {
        var promise;
        return promise = this.model.save({
          status: "stopped"
        }, {
          wait: true
        });
      },
      onStatusChange: function() {
        var status;
        status = this.model.get("status");
        this.$el.removeClass();
        this.$el.addClass(this.className());
        if (status === "started") {
          this.ui.start.addClass("hidden");
        } else {
          this.ui.start.removeClass("hidden");
        }
        if (status === "stopped") {
          return this.ui.stop.addClass("hidden");
        } else {
          return this.ui.stop.removeClass("hidden");
        }
      }
    });
  });

}).call(this);
