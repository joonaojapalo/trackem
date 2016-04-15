define ["underscore", "backbone"], (_, Backbone) ->

	Maps = Backbone.Model.extend

		urlRoot: ->
			console.log "attr",@attributes
			"/api/groups/#{@get 'group'}/maps"

		initialize: (attributes) ->
			_.bindAll @, "urlRoot"
