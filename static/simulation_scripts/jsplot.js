function point_scale(min, scale, offset, value){
	return (value - min) * scale + offset;
}

var jsplot_margin = 4;
var jsplot_draw_grid = true;
var jsplot_grid_dash = [5, 5];

function jsplot_step_table(axis_range, power, max_labels){
    var scaled_axis_range = axis_range / 10**power;
    if(scaled_axis_range < max_labels / 10){
        return 0.1;
	}
    else if(scaled_axis_range < max_labels / 5){
        return 0.2;
	}
    else if(scaled_axis_range < max_labels / 2){
        return 0.5;
	}
    else if(scaled_axis_range < max_labels){
        return 1;
	}
    else if(scaled_axis_range < 2 * max_labels){
        return 2;
	}
    else if(scaled_axis_range < 5 * max_labels){
        return 5;
	}
    else if(scaled_axis_range < 10 * max_labels){
        return 10;
	}
    else if(scaled_axis_range < 20 * max_labels){
        return 20;
	}
    else{
        return 50;
	}
}

function jsplot_x_axis_labels(canvas_ctx, graph_width, graph_height,
								label_x_offset, x_data){
	var x_min = Math.min(...x_data);
	var x_max = Math.max(...x_data);

	var x_axis_range = x_max - x_min;
	if(x_axis_range == 0){
		x_axis_range = 2;
	}

	var x_label_range = x_axis_range;

	var label_height = canvas_ctx.measureText("-10.00").actualBoundingBoxAscent;
	var inner_graph_height = graph_height - label_height;
	var inner_graph_width = graph_width - label_x_offset;

	var x_power = Math.floor(Math.log10(Math.max(Math.abs(x_max), Math.abs(x_min))));
	if(x_power < -1 || x_power > 3){
		x_power = x_power - 1;
	}
	else{
		x_power = 0;
	}

	var x_label_width = canvas_ctx.measureText((-888.88).toFixed(1)).width;

	var x_label_spacing = x_label_width + 2 * jsplot_margin;
	var max_labels = Math.ceil(inner_graph_width / x_label_spacing);

	var label_step = jsplot_step_table(x_axis_range, x_power, max_labels);
	var label_power_step = label_step * 10**x_power;

	var x_min_label = Math.round((x_min / 10**x_power) / label_step + 0.5);
	var x_max_label = Math.round((x_max / 10**x_power) / label_step - 0.5);

	for(var i = Math.floor(x_min_label); i < Math.ceil(x_max_label); i++){
		var val = i * label_power_step;
		var pos = ((val - x_min) / (x_max - x_min)) * inner_graph_width;
		var val_txt = (val / 10**x_power).toFixed(1);

		canvas_ctx.fillText(val_txt, label_x_offset + pos,
							inner_graph_height + label_height);
		if(jsplot_draw_grid){
			canvas_ctx.beginPath();
			canvas_ctx.setLineDash(jsplot_grid_dash);
			canvas_ctx.moveTo(label_x_offset + pos, 0);
			canvas_ctx.lineTo(label_x_offset + pos, inner_graph_height);
			canvas_ctx.stroke();
			canvas_ctx.setLineDash([]);
		}
	}

	if(x_power != 0){
		var x_power_label = "e" + x_power.toString();
		var x_power_label_width = canvas_ctx.measureText(x_power_label).width;
		canvas_ctx.fillText(x_power_label, graph_width - x_power_label_width,
							graph_height - label_height);
	}

	return [x_min, x_max, x_axis_range];
}

function jsplot_y_axis_labels(canvas_ctx, graph_width, graph_height, y_data){
	var y_mins = [];
	var y_maxs = [];
	for(var i = 0; i < y_data.length; i++){
		y_mins.push(Math.min(...y_data[i]));
		y_maxs.push(Math.max(...y_data[i]));
	}
	var y_min = Math.min(...y_mins);
	var y_max = Math.max(...y_maxs);

	var y_axis_range = y_max - y_min;
	if(y_axis_range == 0){
		y_axis_range = 2;
	}

	y_max = y_max + y_axis_range * jsplot_margin / graph_height;
	y_min = y_min + y_axis_range * jsplot_margin / graph_height;
	y_axis_range = y_max - y_min;

	var label_height = canvas_ctx.measureText("-10.00").actualBoundingBoxAscent;
	var inner_graph_height = graph_height - label_height;

	var y_power = Math.floor(Math.log10(Math.max(Math.abs(y_max), Math.abs(y_min))));
	if(y_power < -1){
		y_power = y_power;
	}
	else if(y_power > 2){
		y_power = y_power - 1;
	}
	else{
		y_power = 0;
	}

	var y_label_spacing = 3 * label_height;
	var max_labels = Math.ceil(inner_graph_height / y_label_spacing);

	var label_step = jsplot_step_table(y_axis_range, y_power, max_labels);
	var label_power_step = label_step * 10**y_power;

	var y_min_label = Math.round((y_min / 10**y_power) / label_step - 0.5);
	var y_max_label = Math.round((y_max / 10**y_power) / label_step + 0.5);

	var label_x_offset = 0;

	for(var i = Math.floor(y_min_label); i < Math.floor(y_max_label) + 1; i++){
		var val = i * label_power_step;
		var pos = ((y_max_label * label_power_step - val)
				   / (y_max_label * label_power_step - y_min_label * label_power_step)
				   * inner_graph_height);
		var val_txt = (val / 10**y_power).toFixed(1);

		canvas_ctx.fillText(val_txt, 0, pos + label_height);
		var val_txt_width = canvas_ctx.measureText(val_txt).width;
		if(val_txt_width > label_x_offset){
			label_x_offset = val_txt_width;
		}
		if(jsplot_draw_grid){
			canvas_ctx.beginPath();
			canvas_ctx.setLineDash(jsplot_grid_dash);
			canvas_ctx.moveTo(label_x_offset, pos);
			canvas_ctx.lineTo(graph_width, pos);
			canvas_ctx.stroke();
			canvas_ctx.setLineDash([]);
		}
	}

	if(y_power != 0){
		var y_power_label = "e" + y_power.toString();
		var y_power_label_width = canvas_ctx.measureText(y_power_label).width;
		canvas_ctx.fillText(y_power_label, label_x_offset + jsplot_margin, label_height);
	}

	return [y_min_label * label_power_step, y_max_label * label_power_step,
			(y_max_label - y_min_label) * label_power_step, label_x_offset];
}

function jsplot_plot(canvas, x_data, y_data, title){
	var width = canvas.width;
	var height = canvas.height;
	canvas.style.width = width + "px";
	canvas.style.height = height + "px";

	var ctx = canvas.getContext("2d");
	ctx.clearRect(0, 0, width, height);
	
	ctx.fillStyle = "rgb(0,0,0)";
	ctx.font = "normal 12px sans-serif";
	var title_width = ctx.measureText(title).width;
	ctx.fillText(title, (width - title_width) / 2, 12);

	if(x_data.length === 0){
		console.log("No x_data");
		return;
	}
	for(var i = 0; i < y_data.length; i++){
		if(x_data.length != y_data[i].length){
			console.log("y_data length mismatch");
			return;
		}
	}

	var x_label_height = ctx.measureText("-10.00").actualBoundingBoxAscent;

	var y_axis_data = jsplot_y_axis_labels(ctx, width, height - jsplot_margin, y_data);
	var y_min = y_axis_data[0];
	var y_max = y_axis_data[1];
	var y_axis_range = y_axis_data[2];
	var label_x_offset = y_axis_data[3] + jsplot_margin;

	var x_axis_data = jsplot_x_axis_labels(ctx, width, height, label_x_offset, x_data);
	var x_min = x_axis_data[0];
	var x_max = x_axis_data[1];
	var x_axis_range = x_axis_data[2];

	if(x_axis_range == 0 || y_axis_range == 0){
		console.log("axis range empty");
		return;
	}

	var inner_graph_height = height - x_label_height - jsplot_margin;
	var inner_graph_width = width - label_x_offset;

	var x_scale = inner_graph_width / x_axis_range;
	var y_scale = inner_graph_height / y_axis_range;

	ctx.beginPath();
	ctx.moveTo(label_x_offset, 0);
	ctx.lineTo(label_x_offset, inner_graph_height);
	ctx.lineTo(width, inner_graph_height);
	ctx.stroke();

	var graph_xs = [];
	for(var i = 0; i < x_data.length; i++){
		graph_xs.push((x_data[i] - x_min) * x_scale + label_x_offset);
	}

	for(var j = 0; j < y_data.length; j++){
		ctx.beginPath();

		ctx.moveTo(graph_xs[0], inner_graph_height - (y_data[j][0] - y_min) * y_scale);
		for(var i = 1; i < y_data[j].length; i++){
			ctx.lineTo(graph_xs[i], inner_graph_height - (y_data[j][i] - y_min) * y_scale);
		}
		ctx.stroke();
	}
}
