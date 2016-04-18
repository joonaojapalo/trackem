define ["radio", "marionette", "text!templates/maps/dropdown"], (Radio, Marionette, template) ->


	EmptyListView = Marionette.ItemView.extend
		template: '{{_ "No maps yet. Begin adding one."}}'

	ListItemView = Marionette.ItemView.extend
#		tagName: "li"
		template: '<button class="btn btn-default btn-block" data-action="select">{{name}} ({{id}})</button><br>'

		events:
			"click [data-action='select']": "onClickSelect"

		onRender: ->
#			@$el.addClass("list-group-item")
			@model.once "change:name", @render

		onClickSelect: ->
			channel = Radio.channel("maps")
			channel.trigger "map:select", @model

	ListView = Marionette.CollectionView.extend
#		tagName: "ul"
		childView: ListItemView
		emptyView: EmptyListView
#		onRender: ->
#			@$el.addClass("list-group")


	Dropdown = Marionette.LayoutView.extend
		template: template

		regions:
			itemsRegion: '[data-region="items"]'

		initialize: (options) ->
			@mergeOptions options, ["dropdownGroups"] # [{name: "", comparator: func, limit: 1, filter: func}, ...]

		onBeforeShow: ->
			# create collection views
			@itemsRegion.show new ListView
				collection: @collection

