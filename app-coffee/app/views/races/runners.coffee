define ["radio", "marionette", "text!templates/races/runners", "views/races/runner-card", "app/state"], (Radio, Marionette, template, RunnerCardView, state) ->


	NoCardsView = Marionette.ItemView.extend
		template: '<div class="row"><div class="col-xs-12"><p>No runners. Share the <kbd>RACE CODE</kbd> and ask a runner to join.</p></div></div>'


	RunnerCardsView = Marionette.CollectionView.extend
		childView: RunnerCardView
		emptyView: NoCardsView


	RunnersView = Marionette.LayoutView.extend
		template: template

		regions:
			runnerCardsRegion: '[data-region="runner-cards"]'

		initialize: (options) ->
			@mergeOptions options, ["runners"]

		onBeforeShow: ->
			@runnerCardsRegion.show new RunnerCardsView
				collection: @runners

