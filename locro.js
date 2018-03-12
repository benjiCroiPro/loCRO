let vars = [],
	vars_fetched = false,
	varCheck = 5,
	finalCheck_complete = false

function fetchVars(i) {
	let url = '/variations/production/',
		variation_js = `${url}v${i}.js`,
		variation_css = `${url}v${i}.css`,
		links = []

	fetch(variation_js).then((response) => {
		// console.log('success:', response)
		if (response.status !== 404) {
			links.push(variation_js)
		} else {
			links.push('0')
		}
	}).then(fetch(variation_css).then((response) => {
		// console.log('success:', response)
		if (response.status !== 404) {
			links.push(variation_css)
		} else {
			links.push('0')
		}
	}).then(() => {
		if (links[0] !== '0' || links[1] !== '0') {
			let state = (parseInt(cookie('check')) === i),
				obj = {
					'links': links,
					'text': `Variation ${i}`,
					'state': state
				}
			vars.push(obj)
		}

		if (i == varCheck - 1) {
			finalCheck_complete = true
		}
	}))
}

function detectVars() {
	for (var i = 0; i < varCheck; i++) {
		fetchVars(i)
	}
}

function createSwitcher() {
	let target = document.body,
		vs = vars,
		variations = ''

	for (var i = 0; i < vs.length; i++) {
		if (vs[i].links[0] !== '0' || vs[i].links[1] !== '0') {
			variations += `<option value="${i+1}" data-js="${vs[i].links[0]}" data-css="${vs[i].links[1]}" ${ (vs[i].state === true) ? 'selected="selected"' : '' } >${vs[i].text}</option>`
		}
	}

	let element = `<div class="ip switcher">
						<label for="ip_switch_sel">Current Variation</label>
						<select name="ip_switch_sel" id="ip_switch_sel">${ variations }</select>
					</div>`

	target.innerHTML += element
	initSwitcher()
}

function cookie(method, value = false) {
	let cname = 'locro_active_variation',
		cvalue = value

	switch (method) {
		case 'check':
			var decodedCookie = decodeURIComponent(document.cookie);
			cname = cname+'='
			var ca = decodedCookie.split(';');
			for(var i = 0; i <ca.length; i++) {
				var c = ca[i];
				while (c.charAt(0) == ' ') {
					c = c.substring(1);
				}
				if (c.indexOf(cname) == 0) {
					return c.substring(cname.length, c.length);
				}
			}
			return false;
			break;
		case 'create':
			let d = new Date(),
				exdays = 1
			d.setTime(d.getTime() + (exdays*24*60*60*1000));
			var expires = "expires=Session";
			document.cookie = cname + "=" + cvalue + ";" + expires + ";path=/";
			break;
	}
}

function switchItUp(el) {
	cookie('create', $('#ip_switch_sel').val())
	window.location.reload()
}

function initSwitcher() {
	let c =  cookie('check')
	if (!c) {
		if($('#ip_switch_sel').find('[selected="selected"]').length === 0) {
			$('#ip_switch_sel').children().eq(0).attr('[selected="selected"]')	
			cookie('create', $('#ip_switch_sel').val())
		}
	}
	let curTar = $('#ip_switch_sel').find('[selected="selected"]'),
		js = curTar.attr('data-js'),
		css = curTar.attr('data-css')

	$('head').append(`<link rel="stylesheet" href="${css}" />`)
	$('body').append(`<script src="${js}"></script>`)

	$('body').on('change', '#ip_switch_sel', function(e) {
		event.preventDefault();
		/* Act on the event */
		switchItUp(e.currentTarget)
	});
}

function init() {
	detectVars()

	var poller = (e) => {
		if (finalCheck_complete) {
			createSwitcher()
		} else {
			window.setTimeout(poller, 5)
		}
	}

	window.setTimeout(poller, 5);   
}

function loadJQuery(){
  var waitForLoad = function () {
    if (typeof jQuery != "undefined") {
    	init()
    } else {
      window.setTimeout(waitForLoad, 5);
    }
  };
  window.setTimeout(waitForLoad, 5);   
}
loadJQuery()
