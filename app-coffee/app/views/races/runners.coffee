define ["radio", "marionette", "text!templates/races/runners", "views/races/runner-card", "app/state"], (Radio, Marionette, template, RunnerCardView, state) ->


	NoCardsView = Marionette.ItemView.extend
		template: '<div class="panel"><div class="panel-body palette-coastal-surf"><strong>{{_ "No runners."}}</strong> {{_ "Share the RACE CODE and ask a runner to join."}}</div></div>'


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

