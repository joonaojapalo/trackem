// Generated by CoffeeScript 1.10.0
(function() {
  var slice = [].slice;

  define(["handlebars", "radio", "app/state", "views/app-layout", "app/locales/locale", "widgets/loader"], function(Handlebars, Radio, state, AppLayoutView, locale, LoaderView) {
    var $, AppRouter, Backbone, Marionette, RacesRouter, RequireRouter, appLayout, appRouter, navChannel, racesRouter, requireStores, userChannel;
    $ = require("jquery");
    Backbone = require("backbone");
    Marionette = require("marionette");
    Marionette.Renderer.render = function(template, data) {
      return Handlebars.compile(template)(data);
    };
    Handlebars.registerHelper("_", function(keyword, options) {
      var ref;
      return new Handlebars.SafeString((ref = locale[state.get("locale")][keyword]) != null ? ref : keyword);
    });
    navChannel = Radio.channel("navigation");
    userChannel = Radio.channel("user");
    appLayout = new AppLayoutView;
    Radio.tuneIn("map");
    requireStores = function(storeModules, success, fail) {
      return require(storeModules, function() {
        var promise, store, stores;
        stores = 1 <= arguments.length ? slice.call(arguments, 0) : [];
        promise = $.when.apply(this, (function() {
          var i, len, results;
          results = [];
          for (i = 0, len = stores.length; i < len; i++) {
            store = stores[i];
            results.push(store.fetch());
          }
          return results;
        })());
        promise.done(function() {
          var models;
          models = 1 <= arguments.length ? slice.call(arguments, 0) : [];
          return success.apply(this, models);
        });
        return promise.fail(function() {
          var models;
          models = 1 <= arguments.length ? slice.call(arguments, 0) : [];
          if (fail) {
            return fail.apply(this, models);
          }
        });
      });
    };
    RequireRouter = Backbone.Router.extend({
      requireAndShow: function(layoutName, options) {
        var isReady;
        isReady = false;
        setTimeout((function() {
          if (!isReady) {
            return appLayout.contentRegion.show(new LoaderView);
          }
        }), 200);
        return require(["app/views/" + layoutName + "/layout"], function(LayoutView) {
          var layout;
          layout = new LayoutView(options != null ? options : {
            options: {}
          });
          layout.on("show", function() {
            return navChannel.trigger(layoutName);
          });
          isReady = true;
          return appLayout.contentRegion.show(layout);
        });
      }
    });
    AppRouter = RequireRouter.extend({
      routes: {
        "": "dashboard",
        "maps": "maps",
        "maps/:id": "map",
        "groups": "groups",
        "user": "user"
      },
      dashboard: function() {
        return this.requireAndShow("dashboard");
      },
      user: function() {
        return this.requireAndShow("user");
      },
      maps: function() {
        return this.requireAndShow("maps");
      },
      map: function(id) {
        return this.requireAndShow("maps", {
          mapId: id
        });
      },
      groups: function() {
        return this.requireAndShow("groups");
      }
    });
    RacesRouter = RequireRouter.extend({
      routes: {
        "races": "races",
        "races/:id": "races"
      },
      races: function(id) {
        var _this;
        _this = this;
        return requireStores(["stores/races", "stores/runners"], function(races, runners) {
          return _this.requireAndShow("races", {
            races: races,
            raceId: parseInt(id, {
              runners: runners
            })
          });
        });
      }
    });
    appRouter = new AppRouter();
    racesRouter = new RacesRouter();
    return ($.when((state.get("user")).fetch())).then(function() {
      appLayout.on("render", function() {
        return Backbone.history.start();
      });
      return appLayout.render();
    });
  });

}).call(this);
