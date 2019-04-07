// Generated by CoffeeScript 1.10.0
(function() {
  define(["underscore", "backbone", "models/user", "models/group"], function(_, Backbone, User, Group) {
    var State;
    State = Backbone.Model.extend({
      defaults: {
        user: new User,
        group: new Group,
        locale: "fi_FI"
      },
      constants: {
        url: {
          followAPI: "https://trackem.com/follow/"
        }
      },
      initialize: function() {
        _.bindAll(this, "setDefaultGroup");
        (this.get("user")).on("sync", this.setDefaultGroup);
        return this["const"] = this.constants;
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