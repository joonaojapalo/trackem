// Generated by CoffeeScript 1.10.0
(function() {
  define(["underscore", "backbone", "app/models/user", "app/models/group"], function(_, Backbone, User, Group) {
    var State;
    State = Backbone.Model.extend({
      defaults: {
        user: new User,
        group: new Group,
        locale: "fi_FI"
      },
      initialize: function() {
        _.bindAll(this, "setDefaultGroup");
        return (this.get("user")).on("sync", this.setDefaultGroup);
      },
      setDefaultGroup: function(userModel) {
        var groups;
        groups = this.get("user").get("groups");
        if (groups && groups.length) {
          (this.get("group")).set(groups[0]);
          return console.log("default group set: ", (this.get("group")).get("id", (this.get("group")).get("name")));
        } else {
          (this.get("group")).save().done((this.get("user")).fetch);
          return console.log("creating default group...");
        }
      }
    });
    return new State;
  });

}).call(this);
