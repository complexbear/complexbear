// Code for displaying & working with the blog posts

logger('blog.js loaded');

// Define blog object
Blog = (function() {
	var cls = function(element) {
		var head = document.getElementsByTagName('head')[0],
			css = document.createElement('link');
		// Load blog css
		css.setAttribute('href', 'css/blog.css');
		css.setAttribute('rel', 'stylesheet');
		css.setAttribute('type', 'text/css');
		head.appendChild(css);
		
		this.element = element;
		this.element.className = 'blog';
		this.element.setAttribute('id','blog');
		logger('loaded blog css');
	};
	
	cls.prototype = {
		loadPosts: function() {
			logger('loading blog posts');
			var req = new XMLHttpRequest(),
			formdata = new FormData();
			formdata.append('cmd','loadPosts');
			formdata.append('data', server.token);
			req.open(this.method, this.path, false);
			req.send(formdata);
			if(req.responseText != '') {
				debugger;
				var data = JSON.parse(req.responseText);
			}
		}
	};
	
	return cls;
})();

// Get active area div, remove drawing canvas and add blog panel
(function(){
	var canvas = document.getElementById('canvas'),
		active = document.getElementById('active'),
		blogElement = document.createElement('div');
	
	activearea(false);
	active.onmouseover = null;
	active.onmouseout = null;
	canvas.parentNode.removeChild(canvas);
		
	// global blog object
	blog = new Blog(blogElement);

	active.appendChild(blogElement);
	logger('blog active');
	
	blog.loadPosts();
})();