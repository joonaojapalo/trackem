define ["underscore", "backbone", "app/models/map"], (_, Backbone, Map) ->

	Maps = Backbone.Collection.extend

		model: Map

		url: ->
			groupId = @group.get "id"
			"/api/groups/#{groupId}/maps"

		###initialize: (models, options) ->
			_.bindAll @, "url"
			@group = options.group###
