function logger(msg) {
	if( window.console !== undefined ) {
		window.console.log(msg);
	}
}

function activearea(show) {
	logger('activearea: ' + show);
	var a = document.getElementById('active'),
		c = document.getElementById('canvas');
	if(show) {
		a.className = 'active';
		c.onmousedown = function(e){ draw.start(e); };
		c.onmouseup = function(e){ draw.stop(e); };
		c.onmousemove = function(e){ draw.draw(e); };
	} else {
		a.className = '';
		c.onmousedown = null;
		c.onmouseup = null;
		c.onmousemove = null;
	}
}


/// DRAWING ///
window.onload = function() {
	draw = new Draw();
	server = new Server();
	blog = null;
};


/////////////////// SERVER FUNCTIONS //////////////////
Server = (function() {
	
	var cls = function() {
		this.path = '/blogserver';
		this.method = 'POST';
	};
	
	cls.prototype = {
			
		authenticate: function(data) {
			var req = new XMLHttpRequest(),
				points = JSON.stringify(data),
				formdata = new FormData();
			try {
				formdata.append('cmd','authenticate');
				formdata.append('data',points);
			
				req.open(this.method, this.path, false);
	            req.send(formdata);
				if(req.responseText != '') return JSON.parse(req.responseText);
			} catch (err) {
				logger('ERROR: ' + err);
			}
			return null;
		},
		
		loadContent: function() {
			var req = new XMLHttpRequest(),
				formdata = new FormData();
			formdata.append('cmd','loadContent');
			formdata.append('data', server.token);
			req.open(this.method, this.path, false);
			req.send(formdata);
			if(req.responseText != '') eval(req.responseText);
		}
	};
	
	return cls;
})();


////////////////// DRAWING FUNCTIONS ////////////////
Draw = (function() {
		
	var cls = function() {
		this.trace = [];
		this.origin = null;
		this.tolerance = 5;
		
		this.active = document.getElementById('active');
		this.canvas = document.getElementById('canvas');
		
		this.context = this.canvas.getContext('2d');
		this.context.strokeStyle = '#000';
		this.context.lineWidth   = 10;
		
		this.canvas.width = active.clientWidth;
		this.canvas.height = active.clientHeight;
		this.context.width = active.clientWidth;
		this.context.height = active.clientHeight;
	};
		
	
	cls.prototype = {
		
		atOrigin: function(x, y) {
			var xOk, yOk;
			if(this.origin !== null) {
				xOk = (this.origin.x <= x + this.tolerance) &&
					  (this.origin.x >= x - this.tolerance);
				yOk = (this.origin.y <= y + this.tolerance) &&
				  	  (this.origin.y >= y - this.tolerance);
				return xOk && yOk;
			}
			return true; // causes drawing to stop & reset
		},

		start: function(event) {
			this.trace = []; 	
			this.origin = {x: event.offsetX,
						   y: event.offsetY};
			logger('origin: ' + this.origin.x + ',' + this.origin.y);
			this.context.beginPath();
			this.context.moveTo(event.offsetX, event.offsetY);
		},
		
		stop: function(event) {
			logger('draw stop');
			// Send points to server for verification
			var self = this,
			    result = server.authenticate(this.trace);
			
			if( result ) {
				try {
					this.context.strokeStyle = result.valid ? '#0a0' : '#a00';
					this.context.beginPath();
					this.context.arc(result.origin[0], result.origin[1], result.inner, 0, Math.PI*2, true);
					this.context.stroke();
					this.context.beginPath();
					this.context.arc(result.origin[0], result.origin[1], result.outer, 0, Math.PI*2, true);
					this.context.stroke();
				} finally {
					self.reset();
					if( result.valid ) {
						server.token = result.token;
						server.loadContent();
					}
				}				
			} else {
				self.reset();
			}
		},
	
		reset: function() {
			var self = this;
			logger('reset');
			this.trace = [];
			this.origin = null;
			this.context.strokeStyle = '#000';
			window.setTimeout(function() {
				self.context.clearRect(0, 0, self.canvas.width, self.canvas.height);
				self.context.width = self.canvas.width;
			}, 1000);			
		},
	
		draw: function(event) {
			var x = event.offsetX,
				y = event.offsetY;
			
			if( this.origin !== null ) {
				//logger('draw: ' + x + ',' + y);
				this.context.lineTo(x,y);
				this.context.stroke();
				this.trace.push([x,y]);
			}
		}
	}
	return cls;
})();
