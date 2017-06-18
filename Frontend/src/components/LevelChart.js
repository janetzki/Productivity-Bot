import React from 'react'
import d3 from 'd3'

import './LevelChart.css'

var sidePadding = 30;
var bottomPadding = 30;
var dotRadius = 4;

export default class LevelChart extends React.Component {

	constructor(props){
		super(props);

        this.getJSON('https://hpi.de/naumann/sites/ingestion/hackhpi/caffeine/chart',
            function(err, data) {
                this.readCSV(data.results);
            }.bind(this)
        );
	}

	readCSV(csv){
		console.log(csv);

		this.w = this.refs.chartContainer.offsetWidth;
		this.h = 300;

        d3.selectAll("svg > *").remove();
        var chart = this.refs.levelChart;
        this.svg = d3.select(chart);

        this.dateFormat = d3.time.format("%H:%M");
        this.timeScale = d3.time.scale()
                .domain([new Date(csv[0][0]), new Date(csv[csv.length-1][0])])
                .range([0, this.w - 2 * sidePadding]);

        this.valueScale = d3.scale.linear()
        		.domain([500, 0])
        		.range([0, this.h - bottomPadding]);

        var xAxis = d3.svg.axis()
            .scale(this.timeScale)
            .orient('bottom')
            .ticks(d3.time.houres, 1)
            .tickSize(this.h - bottomPadding, 0)
            .tickFormat(d3.time.format('%H:%M'));

        this.svg.append('g')
            .attr('class', 'grid')
            .attr('transform', 'translate(' + sidePadding + ', ' + -bottomPadding + ')')
            .call(xAxis)
            .selectAll("text")
            .style("text-anchor", "middle")
            .attr("fill", "#000")
            .attr("stroke", "none")
            .attr("font-size", 10)
            .attr("dy", "1em");

        var yAxis = d3.svg.axis()
            .scale(this.valueScale)
            .orient('left')
            //.ticks(d3.ti, 1)
            .tickSize(this.w - sidePadding, 0);
            //.tickFormat(d3.time.format('%H:%M'));

        this.svg.append('g')
            .attr('class', 'grid')
            .attr('transform', 'translate(' + this.w + ', ' + -sidePadding + ')')
            .call(yAxis)
            .selectAll("text")
            .style("text-anchor", "middle")
            .attr('transform', 'translate(' + -10 + ', ' + -8 + ')')
            .attr("fill", "#000")
            .attr("stroke", "none")
            .attr("font-size", 10)
            .attr("dy", "1em");

        /*var valueline = d3.svg.line()
            .x(function(d) { return this.timeScale(this.dateFormat.parse(d.time)); }.bind(this))
            .y(function(d) { return this.valueScale(d.alcohol); }.bind(this));/**/

        var valueline = d3.svg.line()
            .x(function(d) { return this.timeScale(new Date(d[0])) + sidePadding; }.bind(this))
            .y(function(d) { return this.valueScale(d[1]) - bottomPadding; }.bind(this));

        this.svg.append("path")
          //.data(csv)
          .attr("class", "line")
          .attr("d", valueline(csv));

        var dots = this.svg.append('g')
            .selectAll("rect")
            .data(csv)
            .enter();

        var innerRects = dots.append("rect")
            .attr("rx", 3)
            .attr("ry", 3)
            .attr("x", function(d) {
                return this.timeScale(new Date(d[0])) + sidePadding - dotRadius / 2;
            }.bind(this))
            .attr("y", function(d, i) {
                console.log(d[1]);
                return this.valueScale(d[1]) - bottomPadding - dotRadius / 2;
                //return this.valueScale(d.alcohol);
            }.bind(this))
            .attr("width", dotRadius)
            .attr("height", dotRadius)
            .attr("stroke", "none")
            .attr("fill", "#ff0000");

        this.forceUpdate();
	}

    getJSON(url, callback) {
        var xhr = new XMLHttpRequest();
        xhr.open('GET', url, true);
        xhr.responseType = 'json';
        xhr.onload = function() {
          var status = xhr.status;
          if (status == 200) {
            callback(null, xhr.response);
          } else {
            callback(status);
          }
        };
        xhr.send();
    }


	render() {
        return (
            <div id="chartContainer" ref="chartContainer">
            	<svg id="levelChart" ref="levelChart"  width={ this.w } height={ this.h } />
            </div>
        );
    }
}
