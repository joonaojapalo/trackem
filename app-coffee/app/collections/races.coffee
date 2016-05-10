define ["underscore", "backbone", "app/models/race"], (_, Backbone, Race) ->

	Races = Backbone.Collection.extend

		model: Race

		url: ->
			groupId = @group.get "id"
			"/api/groups/#{groupId}/races"
