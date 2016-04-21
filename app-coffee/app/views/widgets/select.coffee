define ["marionette"], (Marionette) ->

	OptionView = Marionette.ItemView.extend
		tagName: "option"
		template: "{{text}}"

		templateHelpers: ->
			text: @model.get @nameAttr

		initialize: (options) ->
			@mergeOptions options, ["nameAttr", "valueAttr"]

		onRender: ->
			@$el.attr "value", @model.get @valueAttr


	Marionette.CollectionView.extend
		tagName: "select"
		className: "form-control dropdown-toggle"
		childView: OptionView
		childViewOptions: ->
			valueAttr: @valueAttr
			nameAttr: @nameAttr

		initialize: (options) ->
			@mergeOptions options, ["nameAttr", "valueAttr"]
			@prefix = options.prefix || "select"

		destroy: ->
			@$el.off "change"

		onRender: ->
			_this = @
			@$el.on "change", ->
				value = _this.$el.val()
				_this.triggerMethod _this.prefix + ":change", _this.findByValue value

		findByValue: (value) ->
			query = {}
			query[@valueAttr] = value
			@collection.findWhere query
