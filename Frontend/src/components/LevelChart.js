import React from 'react'
import d3 from 'd3'

import TimerMixin from 'react-timer-mixin';
var reactMixin = require('react-mixin');

import './LevelChart.css'

var sidePadding = 30;
var bottomPadding = 30;
var iconSize = 20;
var caffeineData = [];
var alcoholData = [];

var caffeineHistory = [];
var alcoholHistory = [];

var gridOpacity = 0.2;
var caffeineColor = "#22c";
var alcoholColor = "#2c2";

var optimalCaffeineLevel = [100, 250];
var optimalAlcoholLevel = [1.29, 1.38];

/*var m = (optimalCaffeineLevel[0]-optimalCaffeineLevel[1])/(optimalAlcoholLevel[0]-optimalAlcoholLevel[1]);
var n = optimalCaffeineLevel[0]-m*optimalAlcoholLevel[0];
var alcoholRange = [0, 3];
var caffeineRange = [m*alcoholRange[0]+n, m*alcoholRange[1]+n];*/

var alcoholRange = [0, 3];
var caffeineRange = [0, 500];

var caffeineLUT = [    
    ["mate", require("./../images/mate.svg")],
    ["tee", require("./../images/tea.svg")],
    ["monster energy", require("./../images/energy_drink.svg")]
];
var alcoholLUT = [
    ["bier", require("./../images/beer.svg")],
    ["wein", require("./../images/wine.svg")],
    ["sekt", require("./../images/wine.svg")],
    ["likör", require("./../images/wine.svg")],
    ["rum", require("./../images/wine.svg")],
    ["schnaps", require("./../images/wine.svg")],
    ["wodka", require("./../images/wine.svg")]
];

export default class LevelChart extends React.Component {

	constructor(props){
		super(props);

        this.setInterval(this.tick, 250);

        this.tick();

	}

    tick(){
        console.log("tick");

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
        
        this.getJSON('https://hpi.de/naumann/sites/ingestion/hackhpi/caffeine/history',
            function(err, data) {
                caffeineHistory = data.results;
                this.readCSV();
            }.bind(this)
        );
        
        this.getJSON('https://hpi.de/naumann/sites/ingestion/hackhpi/alcohol/history',
            function(err, data) {
                alcoholHistory = data.results;
                this.readCSV();
            }.bind(this)
        );
    }

	readCSV(){

		this.w = this.refs.chartContainer.offsetWidth-2;
		this.h = this.refs.chartContainer.offsetHeight-20;

        d3.selectAll("svg > *").remove();
        var chart = this.refs.levelChart;
        this.svg = d3.select(chart);

        this.dateFormat = d3.time.format("%H:%M");
        this.timeScale = d3.time.scale()
                .domain([new Date(caffeineData[0][0]), new Date(caffeineData[caffeineData.length-1][0])])
                .range([0, this.w - 2 * sidePadding]);

        this.caffeineScale = d3.scale.linear()
                .domain(caffeineRange)
                .range([this.h - bottomPadding, 0]);

        this.alcoholScale = d3.scale.linear()
                .domain(alcoholRange)
                .range([this.h - bottomPadding, 0]);

        /*this.svg.append("rect")
            .attr("width", this.w - 2 * sidePadding)
            .attr("height", this.alcoholScale(optimalAlcoholLevel[0])-this.alcoholScale(optimalAlcoholLevel[1]))
            .attr("fill", "#0f0")
            .attr("opacity", 0.1)
            .attr("x", sidePadding)
            .attr("y", this.alcoholScale(optimalAlcoholLevel[1]) - bottomPadding);*/

        this.svg.append("rect")
            .attr("width", this.w - 2 * sidePadding)
            .attr("height", this.alcoholScale(optimalAlcoholLevel[0])-this.alcoholScale(optimalAlcoholLevel[1]))
            .attr("fill", alcoholColor)
            .attr("opacity", 0.1)
            .attr("x", sidePadding)
            .attr("y", this.alcoholScale(optimalAlcoholLevel[1]) - bottomPadding);

        this.svg.append("rect")
            .attr("width", this.w - 2 * sidePadding)
            .attr("height", this.caffeineScale(optimalCaffeineLevel[0])-this.caffeineScale(optimalCaffeineLevel[1]))
            .attr("fill", caffeineColor)
            .attr("opacity", 0.1)
            .attr("x", sidePadding)
            .attr("y", this.caffeineScale(optimalCaffeineLevel[1]) - bottomPadding);

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
            .tickSize(10/*this.w - 2 * sidePadding/**/, 0);

        var yAxisCaffeineEntries = this.svg.append('g')
            .attr('class', 'caffeineGrid')
            .attr('transform', 'translate(' + (sidePadding) + ', ' + -bottomPadding + ')')
            .call(yAxisCaffeine);

        yAxisCaffeineEntries.selectAll("line")
            .attr("stroke", caffeineColor)
            .attr("opacity", gridOpacity);

        yAxisCaffeineEntries.selectAll("text")
            .style("text-anchor", "middle")
            .attr('transform', 'translate(' + -8 + ', ' + -8 + ')')
            .attr("fill", caffeineColor)
            .attr("stroke", "none")
            .attr("font-size", 10)
            .attr("dy", "1em");

        var yAxisAlcohol = d3.svg.axis()
            .scale(this.alcoholScale)
            .orient('right')
            .tickSize(10/*this.w - 2 * sidePadding/**/, 0);

        var yAxisAlcoholEntries = this.svg.append('g')
            .attr('class', 'grid')
            .attr('transform', 'translate(' + (this.w - sidePadding) + ', ' + -sidePadding + ')')
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

        var caffeineIcons = this.svg.append('g')
            .selectAll("rect")
            .data(caffeineHistory)
            .enter();

        caffeineIcons.append("image")
            .attr("xlink:href", function(d){
                    var src = "";
                    caffeineLUT.forEach(function(lutEntry){
                        if(lutEntry[0] == d.drink) src = lutEntry[1];
                    }.bind(this))
                    return src;
                }.bind(this))
            .attr("x", function(d) {
                return this.timeScale(new Date(d.timestamp)) + sidePadding - iconSize / 2;
            }.bind(this))
            .attr("y", function(d, i) {
                return this.caffeineScale(d.total_caffeine) - bottomPadding - iconSize / 2;
            }.bind(this))
            .attr("width", iconSize)
            .attr("height", iconSize);

        var alcoholIcons = this.svg.append('g')
            .selectAll("rect")
            .data(alcoholHistory)
            .enter();

        alcoholIcons.append("image")
            .attr("xlink:href", function(d){
                    var src = "";
                    alcoholLUT.forEach(function(lutEntry){
                        if(lutEntry[0] == d.drink) src = lutEntry[1];
                    }.bind(this))
                    return src;
                }.bind(this))
            .attr("x", function(d) {
                return this.timeScale(new Date(d.timestamp)) + sidePadding - iconSize / 2;
            }.bind(this))
            .attr("y", function(d, i) {
                return this.alcoholScale(d.total_alcohol) - bottomPadding - iconSize / 2;
            }.bind(this))
            .attr("width", iconSize)
            .attr("height", iconSize);

        this.svg.append("rect")
            .attr("width", 2)
            .attr("height", this.h - 2 * bottomPadding)
            .attr("fill", "#f4b342")
            .attr("x", this.timeScale(Date.now()) + sidePadding)
            .attr("y", 0);

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

    //<svg id="levelChart" ref="levelChart"  width={ this.w } height={ this.h } />
	render() {
        return (
            <div id="chartContainer" ref="chartContainer">
                <svg id="levelChart" ref="levelChart"  width={ this.w } height={ this.h } />
            </div>
        );
    }
}

reactMixin(LevelChart.prototype, TimerMixin);