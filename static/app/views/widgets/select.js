// Generated by CoffeeScript 1.10.0
(function() {
  define(["marionette"], function(Marionette) {
    var OptionView;
    OptionView = Marionette.ItemView.extend({
      tagName: "option",
      template: "{{text}}",
      templateHelpers: function() {
        return {
          text: this.model.get(this.nameAttr)
        };
      },
      initialize: function(options) {
        return this.mergeOptions(options, ["nameAttr", "valueAttr"]);
      },
      onRender: function() {
        return this.$el.attr("value", this.model.get(this.valueAttr));
      }
    });
    return Marionette.CollectionView.extend({
      tagName: "select",
      className: "form-control dropdown-toggle",
      childView: OptionView,
      childViewOptions: function() {
        return {
          valueAttr: this.valueAttr,
          nameAttr: this.nameAttr
        };
      },
      initialize: function(options) {
        this.mergeOptions(options, ["nameAttr", "valueAttr"]);
        return this.prefix = options.prefix || "select";
      },
      destroy: function() {
        return this.$el.off("change");
      },
      onRender: function() {
        var _this;
        _this = this;
        return this.$el.on("change", function() {
          var value;
          value = _this.$el.val();
          return _this.triggerMethod(_this.prefix + ":change", _this.findByValue(value));
        });
      },
      findByValue: function(value) {
        var query;
        query = {};
        query[this.valueAttr] = value;
        return this.collection.findWhere(query);
      }
    });
  });

}).call(this);
