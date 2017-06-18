import React from 'react'
import d3 from 'd3'

import TimerMixin from 'react-timer-mixin';
var reactMixin = require('react-mixin');

import './LevelChart.css'

var sidePadding = 30;
var bottomPadding = 30;
var dotRadius = 4;
var caffeineData = [];
var alcoholData = [];

var gridOpacity = 0.2;
var caffeineColor = "#c22";
var alcoholColor = "#2c2";

export default class LevelChart extends React.Component {

	constructor(props){
		super(props);

        this.setInterval(this.tick, 1000);

        this.tick();

	}

    tick(){
        //console.log("tick");

        this.getJSON('https://hpi.de/naumann/sites/ingestion/hackhpi/caffeine/chart',
            function(err, data) {
                caffeineData = data.results;
                this.readCSV();
            }.bind(this)
        );
        
        this.getJSON('https://hpi.de/naumann/sites/ingestion/hackhpi/alcohol/chart',
            function(err, data) {
                alcoholData = data.results;
                this.readCSV();
            }.bind(this)
        );
        
        this.getJSON('https://hpi.de/naumann/sites/ingestion/hackhpi/alcohol/history',
            function(err, data) {
                //alcoholData = data.results;
                //this.readCSV();
                //console.log(data);
            }.bind(this)
        );
    }

	readCSV(){

		this.w = this.refs.chartContainer.offsetWidth;
		this.h = 300;

        d3.selectAll("svg > *").remove();
        var chart = this.refs.levelChart;
        this.svg = d3.select(chart);

        this.dateFormat = d3.time.format("%H:%M");
        this.timeScale = d3.time.scale()
                .domain([new Date(caffeineData[0][0]), new Date(caffeineData[caffeineData.length-1][0])])
                .range([0, this.w - 2 * sidePadding]);

        this.caffeineScale = d3.scale.linear()
                .domain([500, 0])
                .range([0, this.h - bottomPadding]);

        this.alcoholScale = d3.scale.linear()
                .domain([3, 0])
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

        var yAxisCaffeine = d3.svg.axis()
            .scale(this.caffeineScale)
            .orient('left')
            .tickSize(this.w - 2 * sidePadding, 0);

        var yAxisCaffeineEntries = this.svg.append('g')
            .attr('class', 'caffeineGrid')
            .attr('transform', 'translate(' + (this.w - sidePadding) + ', ' + -bottomPadding + ')')
            .call(yAxisCaffeine);

        yAxisCaffeineEntries.selectAll("line")
            .attr("stroke", caffeineColor)
            .attr("opacity", gridOpacity);

        yAxisCaffeineEntries.selectAll("text")
            .style("text-anchor", "middle")
            .attr('transform', 'translate(' + -10 + ', ' + -8 + ')')
            .attr("fill", caffeineColor)
            .attr("stroke", "none")
            .attr("font-size", 10)
            .attr("dy", "1em");

        var yAxisAlcohol = d3.svg.axis()
            .scale(this.alcoholScale)
            .orient('right')
            .tickSize(this.w - 2 * sidePadding, 0);

        var yAxisAlcoholEntries = this.svg.append('g')
            .attr('class', 'grid')
            .attr('transform', 'translate(' + sidePadding + ', ' + -sidePadding + ')')
            .call(yAxisAlcohol);

        yAxisAlcoholEntries.selectAll("line")
            .attr("stroke", alcoholColor)
            .attr("opacity", gridOpacity);

        yAxisAlcoholEntries.selectAll("text")
            .style("text-anchor", "middle")
            .attr('transform', 'translate(' + (-20 + sidePadding) + ', ' + -8 + ')')
            .attr("fill", alcoholColor)
            .attr("stroke", "none")
            .attr("font-size", 10)
            .attr("dy", "1em");

        /*var valueline = d3.svg.line()
            .x(function(d) { return this.timeScale(this.dateFormat.parse(d.time)); }.bind(this))
            .y(function(d) { return this.valueScale(d.alcohol); }.bind(this));/**/

        var caffeineLine = d3.svg.line()
            .x(function(d) { return this.timeScale(new Date(d[0])) + sidePadding; }.bind(this))
            .y(function(d) { return this.caffeineScale(d[1]) - bottomPadding; }.bind(this));

        var alcoholLine = d3.svg.line()
            .x(function(d) { return this.timeScale(new Date(d[0])) + sidePadding; }.bind(this))
            .y(function(d) { return this.alcoholScale(d[1]) - bottomPadding; }.bind(this));

        this.svg.append("path")
          .attr("class", "caffeineLine")
          .attr("d", caffeineLine(caffeineData))
          .attr("stroke", caffeineColor);

        this.svg.append("path")
          .attr("class", "alcoholLine")
          .attr("d", alcoholLine(alcoholData))
          .attr("stroke", alcoholColor);

        /*var dots = this.svg.append('g')
            .selectAll("rect")
            .data(csv)
            .enter();

        dots.append("rect")
            .attr("rx", 3)
            .attr("ry", 3)
            .attr("x", function(d) {
                return this.timeScale(new Date(d[0])) + sidePadding - dotRadius / 2;
            }.bind(this))
            .attr("y", function(d, i) {
                return this.valueScale(d[1]) - bottomPadding - dotRadius / 2;
                //return this.valueScale(d.alcohol);
            }.bind(this))
            .attr("width", dotRadius)
            .attr("height", dotRadius)
            .attr("stroke", "none")
            .attr("fill", "#ff0000");*/

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

reactMixin(LevelChart.prototype, TimerMixin);