//一周内访问总数折线图
//点击某天后的出现
	//每小时访问数  折线图
	//ios_version 饼状图
	//android 版本分布 饼状图
	//微信端,移动端分布 饼状图
	//每个api访问数 柱状图
	//总请求数

var currentIndex, //当前渲染的第几天的索引
	contents,	//存储7天的访问情况
	week = {},
	api,
	ios_distribute=[],
	android_distribute=[],
	device_distribute=[];

var week_chart = echarts.init(document.getElementById('week'));
var api_chart = echarts.init(document.getElementById("api_order"));
var ios_chart = echarts.init(document.getElementById('ios_version'));
var android_chart = echarts.init(document.getElementById('android_version'));
var hour_chart = echarts.init(document.getElementById('hour'));
var device_chart = echarts.init(document.getElementById('device_distribute'));

inital();

function transformDate(date){
	var y = date.getFullYear();
	var m = date.getMonth()+1;
	var d = date.getDate();
	if(m<10)
		m = '0'+m;
	else
		m+='';
	if(d<10)
		d = '0'+d;
	return y+m+d;
}

function inital(){
	week_chart.showLoading();
	
	var date = new Date();
	date.setDate( date.getDate()-7 );
	
	$.ajax({
		url: 'http://139.129.4.159:7000/herald/api/v1/log',
		type: 'POST',
		dataType: 'json',
		data: {
			date_start: transformDate(date),
			date_cnt: 7},
		timeout: 6000
	})
	.success(function(data){

		week_chart.showLoading();

		contents = data['content'];
		currentIndex = contents.length-1
		var date = contents[currentIndex]['date'] + '';
		title.innerHTML = date.slice(0,4)+'年'+date.slice(4,6)+'月'+date.slice(6,8)+'日'+'的具体访问情况';

		inital_week_chart();
		inital_api_chart(currentIndex);
		inital_ios_chart(currentIndex);
		inital_android_chart(currentIndex);
		inital_hour_chart(currentIndex);
		inital_device_chart(currentIndex);

		week_chart.hideLoading();

	})
	.fail(function() {
		console.log('request error');
	});
}

function updateDayInfo(i){
	inital_api_chart(i);
	inital_hour_chart(i);
	inital_ios_chart(i);
	inital_android_chart(i);
	inital_device_chart(i);
}

function inital_week_chart(){
	for(var i in contents){
		week[ contents[i]["date"] ] = contents[i]["call_count"];
	}

	week_chart.setOption({
		title: {
	    	text: '7天内访问量变化',
	    	x: 'center',
			y:'top'
		},
		tooltip: {},
		xAxis: {
		    data: Object.keys(week)
		},
		yAxis: {},
		series: [{
		    name: '访问量',
		    type: 'line',
		    data: Object.values(week)
		}]
	});
}

function inital_api_chart(i){

	api = contents[i]['api_order'];

	for( var i in api)
		if(api[i]<1000)
			delete api[i];

	api_chart.setOption({
		title: {
	    	text: 'API调用情况(没有展示数量较少的)',
	    	x: 'left',
			y:'top'
		},
		tooltip: {},
		xAxis: {
		    data: Object.keys(api),
		    axisLabel:{
		    	interval: 0
		    }
		},
		yAxis: {},
		series: [{
		    name: '访问量',
		    type: 'bar',
		    data: Object.values(api)
		}]
	});
}

function inital_ios_chart(i){
	var temp = contents[i]['ios_version'];
	ios_distribute.length = 0;

	for(var t in temp){
		ios_distribute.push({value: temp[t], name:t});
	}

	ios_chart.setOption({
			title: {
				text: 'iOS端访问版本分布',
				x: 'left',
				y:'top'
			},
			tooltip : {
                trigger: 'item',
                formatter: "{a} <br/>{b} : {c} ({d}%)"
            },
            legend: {
            	x:'left',
            	y: 'bottom',
            	data: Object.keys(temp)
            },
		    series : [
		        {
		            name: '访问量(百分比)',
		            type: 'pie',
		            radius: '55%',
		            data: ios_distribute
		        }
		    ]
	});
}

function inital_android_chart(i){
	var temp = contents[i]['android_version'];
	android_distribute.length = 0;

	if(temp['']){
		temp['<7']=temp[''];
		delete temp[''];
	}

	for(var t in temp){
		android_distribute.push({value: temp[t], name:t});
	}

	android_chart.setOption({
			title: {
				text: 'Android端访问版本分布',
	    		x: 'left',
	    		y: 'top'
			},
			tooltip : {
                trigger: 'item',
                formatter: "{a} <br/>{b} : {c} ({d}%)"
            },
            legend: {
            	y: 'bottom',
            	x:'center',
            	data: Object.keys(temp)
            },
		    series : [
		        {
		            name: '访问量(百分比)',
		            type: 'pie',
		            radius: '55%',
		            data:android_distribute
		        }
		    ]
	});
}

function inital_hour_chart(i){
	hour = contents[i]['every_hour_count'];
	hour_chart.setOption({
		title: {
	    	text: '一天内每时的访问变化',
	    	x:'left',
	    	y:'top'
		},
		tooltip: {},
		xAxis: {
		    data: Object.keys(hour)
		},
		yAxis: {},
		series: [{
		    name: '访问量',
		    type: 'line',
		    data: Object.values(hour)
		}]
	});
}

function inital_device_chart(i){
	var temp= contents[i]['device_distribute'];
	device_distribute.length = 0;
	
	for(var t in temp){
		device_distribute.push({value: temp[t], name:t});
	}

	device_chart.setOption({
			title: {
				text: '访问设备分布',
				x: 'left',
				y:'top'
			},
			tooltip : {
				trigger: 'item',
				formatter: "{a} <br/>{b} : {c} ({d}%)"
			},
			legend: {
				data: Object.keys(temp),
				y: 'bottom',
				x:'center'
            },
			series : [
				{
                    name:'访问量(百分比)',
                    type:'pie',
                    data:device_distribute
                }
			]
	});
}

week_chart.on('click', function (params) {
	if (params.componentType === 'series' && params.seriesType === 'line'){
            var i = params['dataIndex'];
            if( i!=currentIndex ){
				currentIndex=i;
				var date = params.name;
				title.innerHTML = date.slice(0,4)+'年'+date.slice(4,6)+'月'+date.slice(6,8)+'日'+'的具体访问情况';
            	updateDayInfo(i);
            }
        }
});