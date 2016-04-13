define ["underscore", "backbone", "app/models/user", "app/models/group"], (_, Backbone, User, Group) ->
	State = Backbone.Model.extend
		defaults:
			user: 		new User
			group: 		new Group
			locale: 	"fi_FI"

		initialize: ->
			_.bindAll @, "setDefaultGroup"
			(@get "user").on "sync", @setDefaultGroup

		setDefaultGroup: (userModel) ->

			groups = @get("user").get("groups")

			if groups and groups.length
				(@get "group").set groups[0]
				console.log "default group set: ", (@get "group").get "id", (@get "group").get "name"
			else
				# create a new group, once saved, (re)fetch user
				(@get "group").save().done (@get "user").fetch

				console.log "creating default group..."

	new State
