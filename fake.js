/**
 * A simlpe javascript file that opens a new tab and closes it
 * immediately to run local tests.
 */
chrome.browserAction.onClicked.addListener(function() {
	chrome.tabs.getSelected(null,function(tab) {
		var curr = tab.url;
		var id;
		chrome.tabs.create({url: "http://127.0.0.1:5000/" + "?" + String(curr)}, function(tab) {
			id =  tab.id;
			chrome.tabs.remove(id);
		});
	});
});
