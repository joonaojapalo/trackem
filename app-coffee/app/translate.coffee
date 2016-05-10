define ["app/state", "app/locales/locale"], (state, locale) ->
	__ = (msgid) ->
		currentLocale = state.get "locale"
		locale[currentLocale][msgid]
