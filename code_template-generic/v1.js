// "This is not the script you are looking for..."
function conditions() {
	let cond = typeof $ != "undefined";
	return cond
}

function pollElements(){
  var waitForLoad = function () {
    if (conditions()) {
    	//  Do Things
		init()
    } else {
      window.setTimeout(waitForLoad, 5);
    }
  };
  window.setTimeout(waitForLoad, 5);   
}
pollElements()