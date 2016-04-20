define ["underscore", "marionette"], (_, Marionette) ->

	Store = Marionette.Object.extend

		fetchableClass: null

		initialize: (options) ->
			_.bindAll @, "setup"
			@dfd = null
			@fetchable = new @fetchableClass

		setup: ->
			null

		_fetch: ->
			dfd = new $.Deferred

			# fetch dependecies
			deps = _.result @, "setupDeps", []

			depsPromise = $.when.apply _.map deps, (dep) ->
				dep.fetch()

			_this = @
			depsPromise.done ->

				# setup fetchable
				_this.setup arguments

				# fetch
				promise = _this.fetchable.fetch()

				promise.done ->
					dfd.resolve(_this.fetchable)

				promise.fail ->
					dfd.reject()

			depsPromise.fail ->
				dfd.reject()

			dfd

		fetch: ->
			if !@dfd
				@dfd = @_fetch()

			@dfd.promise()


		refetch: ->
			@dfd = null
			return @fetch

	Store