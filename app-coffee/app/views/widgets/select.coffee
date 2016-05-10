define ["underscore", "marionette", "app/translate"], (_, Marionette, __) ->

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
			_.bindAll @, "findByValue", "onChange"
			@mergeOptions options, ["nameAttr", "valueAttr"]
			@prefix = options.prefix || "select"

		destroy: ->
			@$el.off "change"

		onRender: ->
			@$el.on "change", @onChange
			@$el.prepend '<option val="" selected="1" disabled="1">'+__("Select..")+'</option>'

		onChange: ->
			# find model
			value = @$el.val()
			model = @findByValue parseInt(value)

			# fire event
			eventName = @prefix + ":change"
			@trigger eventName, model

		findByValue: (value) ->
			query = {}
			query[@valueAttr] = value
			@collection.findWhere query
