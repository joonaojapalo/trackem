define ["underscore", "backbone"], (_, Backbone) ->

	Runners = Backbone.Collection.extend

		url: ->
			groupId = @group.get "id"
			raceId = @raceId
			"/api/groups/#{groupId}/races/#{raceId}/runners"
