define ["marionette"], (Marionette) ->

	OptionView = Marionette.ItemView.extend
		tagName: "option"
		template: "{{text}}"

		templateHelpers: ->
			text: @model.get @nameAttr

		initialize: (options) ->
			@mergeOptions options, ["nameAttr", "valueAttr"]
			console.log @nameAttr, @valueAttr

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

		destroy: ->
			@$el.off "change"

		onRender: ->
			_this = @
			@$el.on "change", ->
				_this.trigger "change"

		getValue: ->
			@$el.val()