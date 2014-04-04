(function(){
var h=null;
(function(){var s,t={}.hasOwnProperty,u=[].slice;if(((s=this.google)!=h?s.maps:void 0)!=h)this.OverlappingMarkerSpiderfier=function(){function o(b,d){var a,g,e,f,c=this;this.map=b;d==h&&(d={});for(a in d)t.call(d,a)&&(g=d[a],this[a]=g);this.m=new this.constructor.c(this.map);this.i();this.b={};f=["click","zoom_changed","maptypeid_changed"];g=0;for(e=f.length;g<e;g++)a=f[g],l.addListener(this.map,a,function(){return c.unspiderfy()})}var l,p,n,q,k,c,r;c=o.prototype;c.VERSION="0.2.6";p=google.maps;l=
p.event;k=p.MapTypeId;r=2*Math.PI;c.keepSpiderfied=!1;c.markersWontHide=!1;c.markersWontMove=!1;c.nearbyDistance=20;c.circleSpiralSwitchover=9;c.circleFootSeparation=23;c.circleStartAngle=r/12;c.spiralFootSeparation=26;c.spiralLengthStart=11;c.spiralLengthFactor=4;c.spiderfiedZIndex=1E3;c.usualLegZIndex=10;c.highlightedLegZIndex=20;c.legWeight=1.5;c.legColors={usual:{},highlighted:{}};q=c.legColors.usual;n=c.legColors.highlighted;q[k.HYBRID]=q[k.SATELLITE]="#fff";n[k.HYBRID]=n[k.SATELLITE]="#f00";
q[k.TERRAIN]=q[k.ROADMAP]="#444";n[k.TERRAIN]=n[k.ROADMAP]="#f00";c.i=function(){this.a=[];this.f=[]};c.addMarker=function(b){var d,a=this;if(b._oms!=h)return this;b._oms=!0;d=[l.addListener(b,"click",function(){return a.B(b)})];this.markersWontHide||d.push(l.addListener(b,"visible_changed",function(){return a.k(b,!1)}));this.markersWontMove||d.push(l.addListener(b,"position_changed",function(){return a.k(b,!0)}));this.f.push(d);this.a.push(b);return this};c.k=function(b,d){if(b._omsData!=h&&(d||
!b.getVisible())&&!(this.p!=h||this.q!=h))return this.F(d?b:h)};c.getMarkers=function(){return this.a.slice(0)};c.removeMarker=function(b){var d,a,g,e,f;b._omsData!=h&&this.unspiderfy();d=this.h(this.a,b);if(0>d)return this;g=this.f.splice(d,1)[0];e=0;for(f=g.length;e<f;e++)a=g[e],l.removeListener(a);delete b._oms;this.a.splice(d,1);return this};c.clearMarkers=function(){var b,d,a,g,e,f,c,i;this.unspiderfy();i=this.a;b=g=0;for(f=i.length;g<f;b=++g){a=i[b];d=this.f[b];e=0;for(c=d.length;e<c;e++)b=
d[e],l.removeListener(b);delete a._oms}this.i();return this};c.addListener=function(b,d){var a,g;((g=(a=this.b)[b])!=h?g:a[b]=[]).push(d);return this};c.removeListener=function(b,d){var a;a=this.h(this.b[b],d);0>a||this.b[b].splice(a,1);return this};c.clearListeners=function(b){this.b[b]=[];return this};c.trigger=function(){var b,d,a,g,e,f;d=arguments[0];b=2<=arguments.length?u.call(arguments,1):[];d=(a=this.b[d])!=h?a:[];f=[];g=0;for(e=d.length;g<e;g++)a=d[g],f.push(a.apply(h,b));return f};c.r=function(b,
d){var a,g,e,f,c;e=this.circleFootSeparation*(2+b)/r;g=r/b;c=[];for(a=f=0;0<=b?f<b:f>b;a=0<=b?++f:--f)a=this.circleStartAngle+a*g,c.push(new p.Point(d.x+e*Math.cos(a),d.y+e*Math.sin(a)));return c};c.s=function(b,d){var a,g,e,c,j;e=this.spiralLengthStart;a=0;j=[];for(g=c=0;0<=b?c<b:c>b;g=0<=b?++c:--c)a+=this.spiralFootSeparation/e+5.0E-4*g,g=new p.Point(d.x+e*Math.cos(a),d.y+e*Math.sin(a)),e+=r*this.spiralLengthFactor/a,j.push(g);return j};c.B=function(b){var d,a,g,c,f,j,i,m,l;d=b._omsData!=h;(!d||
!this.keepSpiderfied)&&this.unspiderfy();if(d||this.map.getStreetView().getVisible())return this.trigger("click",b);c=[];f=[];j=this.nearbyDistance*this.nearbyDistance;g=this.j(b.position);l=this.a;i=0;for(m=l.length;i<m;i++)d=l[i],d.getVisible()&&d.map!=h&&(a=this.j(d.position),this.n(a,g)<j?c.push({v:d,l:a}):f.push(d));return 1===c.length?this.trigger("click",b):this.C(c,f)};c.u=function(b){var d=this;return{d:function(){return b._omsData.e.setOptions({strokeColor:d.legColors.highlighted[d.map.mapTypeId],
zIndex:d.highlightedLegZIndex})},g:function(){return b._omsData.e.setOptions({strokeColor:d.legColors.usual[d.map.mapTypeId],zIndex:d.usualLegZIndex})}}};c.C=function(b,d){var a,c,e,f,j,i,m,k,o,n;this.p=!0;n=b.length;a=this.z(function(){var a,d,c;c=[];a=0;for(d=b.length;a<d;a++)k=b[a],c.push(k.l);return c}());f=n>=this.circleSpiralSwitchover?this.s(n,a).reverse():this.r(n,a);a=function(){var a,d,k,n=this;k=[];a=0;for(d=f.length;a<d;a++)e=f[a],c=this.A(e),o=this.w(b,function(a){return n.n(a.l,e)}),
m=o.v,i=new p.Polyline({map:this.map,path:[m.position,c],strokeColor:this.legColors.usual[this.map.mapTypeId],strokeWeight:this.legWeight,zIndex:this.usualLegZIndex}),m._omsData={D:m.position,e:i},this.legColors.highlighted[this.map.mapTypeId]!==this.legColors.usual[this.map.mapTypeId]&&(j=this.u(m),m._omsData.t={d:l.addListener(m,"mouseover",j.d),g:l.addListener(m,"mouseout",j.g)}),m.setPosition(c),m.setZIndex(Math.round(this.spiderfiedZIndex+e.y)),k.push(m);return k}.call(this);delete this.p;this.o=
!0;return this.trigger("spiderfy",a,d)};c.unspiderfy=function(b){var d,a,c,e,f,j,i;b==h&&(b=h);if(this.o==h)return this;this.q=!0;e=[];c=[];i=this.a;f=0;for(j=i.length;f<j;f++)a=i[f],a._omsData!=h?(a._omsData.e.setMap(h),a!==b&&a.setPosition(a._omsData.D),a.setZIndex(h),d=a._omsData.t,d!=h&&(l.removeListener(d.d),l.removeListener(d.g)),delete a._omsData,e.push(a)):c.push(a);delete this.q;delete this.o;this.trigger("unspiderfy",e,c);return this};c.n=function(b,d){var a,c;a=b.x-d.x;c=b.y-d.y;return a*
a+c*c};c.z=function(b){var d,a,c,e,f;e=a=c=0;for(f=b.length;e<f;e++)d=b[e],a+=d.x,c+=d.y;b=b.length;return new p.Point(a/b,c/b)};c.j=function(b){return this.m.getProjection().fromLatLngToDivPixel(b)};c.A=function(b){return this.m.getProjection().fromDivPixelToLatLng(b)};c.w=function(b,c){var a,g,e,f,j,i;e=j=0;for(i=b.length;j<i;e=++j)if(f=b[e],f=c(f),!("undefined"!==typeof a&&a!==h)||f<g)g=f,a=e;return b.splice(a,1)[0]};c.h=function(b,c){var a,g,e,f;if(b.indexOf!=h)return b.indexOf(c);a=e=0;for(f=
b.length;e<f;a=++e)if(g=b[a],g===c)return a;return-1};o.c=function(b){return this.setMap(b)};o.c.prototype=new p.OverlayView;o.c.prototype.draw=function(){};return o}()}).call(this);}).call(this);

google.load("visualization", "1", {packages:["corechart"]});
window.onload = function() {
	var mapOptions = {
		mapTypeId: google.maps.MapTypeId.ROADMAP,
		center: new google.maps.LatLng(-23.55052330, -46.63429820),
		// scrollwheel: false,
		zoom: 12
	}

	var spiderfierOptions = {
		markersWontMove: true,
		markersWontHide: true
	}

	var iw = new google.maps.InfoWindow();
	var map = new google.maps.Map(document.getElementById('map-wrapper'), mapOptions);
	var oms = new OverlappingMarkerSpiderfier(map, spiderfierOptions);

	oms.addListener('click', function(marker) {
		iw.setContent(marker.desc);
		iw.open(map, marker);
	});

	oms.addListener('spiderfy', function(markers) {
		for(var i = 0; i < markers.length; i ++) {
			//markers[i].setIcon(iconWithColor(spiderfiedColor));
			markers[i].setShadow(null);
		}
		iw.close();
	});

	oms.addListener('unspiderfy', function(markers) {
		for(var i = 0; i < markers.length; i ++) {
			//markers[i].setIcon(iconWithColor(usualColor));
			markers[i].setShadow(shadow);
		}
	});
	
	function getlocation(coordenadas) {
		if("cep" in coordenadas) {
			return coordenadas['cep'];
		}
		
		var more_priority = [];
		var less_priority = [];
		var keys = Object.keys(coordenadas);
		$.each(keys, function(index, key) {
			var priorities = ["bairro", "cidade", "comunidade", "conjunto", "distrito", "favela", "jardim",
												"loteamento", "morro", "recanto", "sitio", "subprefeitura", "vila"];
												
			if($.inArray(key, priorities) != -1) {
			 	less_priority = less_priority.concat(coordenadas[key]);
			 } else {
			 	more_priority = more_priority.concat(coordenadas[key]);
			 }
		});
		if(more_priority.length != 0) {
			return more_priority;
		} else {
			return less_priority;
		}
	}
	
	function getdescription(entry) {
		var description = 'ID: ' + entry.id +
				'<br>' + entry.descricao +
				'<br>Orçado: ' + entry.orcado +
				'<br>Atualizado: ' + entry.atualizado +
				'<br>Empenhado: ' + entry.empenhado +
				'<br>Liquidado: ' + entry.liquidado +
				'<br>Órgão: ' + entry.orgao +
				'<br>Unidade: ' + entry.unidade +
				'<br>Função: ' + entry.funcao +
				'<br>Subfunção: ' + entry.subfuncao +
				'<br>Programa: ' + entry.programa;
		return description;
	}
	
	function getcolor(entry) {
		if(entry.atualizado == "0,00" && entry.empenhado == "0,00" && entry.liquidado == "0,00") {
			// return 'FE7569'; // Red
			return 'red';
		} else if(entry.empenhado == "0,00" && entry.liquidado == "0,00") {
			// return 'FFFF57'; // Yellow
			return 'yellow';
		} else if(entry.liquidado == "0,00") {
			// return '34BA46'; // Green
			return 'green';
		} else {
			// return '87AEC5'; // Blue
			return 'blue';
		}
	}

	var shadow = new google.maps.MarkerImage(
		'https://www.google.com/intl/en_ALL/mapfiles/shadow50.png',
		new google.maps.Size(40, 34),  // size   - for sprite clipping
		new google.maps.Point(0, 0),   // origin - ditto
		new google.maps.Point(10, 34)  // anchor - where to meet map location
	);

	var markersArray = [];
	var mapped_list_html = '<table cellspacing="0"><tr><th scope="col" class="nobg">ID</th><th scope="col">Descrição</th><th scope="col">Orçado</th><th scope="col">Atualizado</th><th scope="col">Empenhado</th><th scope="col">Liquidado</th><th scope="col">Órgão</th></tr>';
	var notmapped_list_html = mapped_list_html;
	
	function appendTableEntry(list, entry, rowclass) {
		var html = '<tr>';
		html += '<th scope="row" class="spec' + rowclass +'">' + entry.id + '</th>';
		if(list == 'mapped') {
			html += '<td class="' + rowclass + '">' + '<a onclick="gotoMarker(' + (markersArray.length-1) + ')">' + entry.descricao + '</a></td>';		
		} else {
			html += '<td class="' + rowclass + '">' + entry.descricao + '</td>';
		}
		html += '<td class="' + rowclass + '">' + entry.orcado + '</td>';
		html += '<td class="' + rowclass + '">' + entry.atualizado + '</td>';
		html += '<td class="' + rowclass + '">' + entry.empenhado + '</td>';
		html += '<td class="' + rowclass + '">' + entry.liquidado + '</td>';
		html += '<td class="' + rowclass + '">' + entry.orgao + '</td>';
		html += '</tr>';
		if(list == 'mapped') {
			mapped_list_html += html;
		} else {
			notmapped_list_html += html;
		}
	}

	function drawMarkers(data) {
		var mappedRowClass = '', notMappedRowClass = '';
		$.each(data, function(index, entry) {
			if(Object.keys(entry.coordenadas).length != 0) {
				var description = getdescription(entry);
				var color = getcolor(entry);
				$.each(getlocation(entry.coordenadas), function(index, location) {
					var marker = new google.maps.Marker({	
						position: new google.maps.LatLng(location.localizacoes[0].lat, location.localizacoes[0].lng),
						map: map,
						shadow: shadow,
						// icon: 'http://chart.googleapis.com/chart?chst=d_map_xpin_letter&chld=pin|+|' + color + '|000000|ffff00'
						icon: 'img/pin-' + color + '.png'
					});
					marker.desc = description;
					oms.addMarker(marker);
					markersArray.push(marker);
					appendTableEntry('mapped', entry, mappedRowClass);
				});
			} else {
				appendTableEntry('notmapped', entry, notMappedRowClass);
			}
		});
	}

	function drawCharts(metadata) {
		var options_chart1 = {
			title: 'Quantidade de cada tipo de despesa',
			colors: ['#3FB1FC', '#C9C3C3'],
			height: 400
		};
		
		var options_chart2 = {
			title: 'Distribuição de recursos por tipo de despesa',
			hAxis: {
				title: 'Tipo',
				viewWindowMode: 'pretty'
			},
			vAxis: {
				viewWindowMode: 'pretty'
//				logScale: true
			},
			colors: ['#C9C3C3', '#3FB1FC'],
			isStacked: true,
			height: 400
		};
		
		var data_chart1 = [
			['Tipo', 'Quantidade']
		];
	
		var data_chart2 = [
			['Varíavel', 'Não Mapeado', 'Mapeado']
		];
		
		var tipo1 = metadata.tipo_1;
		var tipo2 = metadata.tipo_2;
		var tipo3 = metadata.tipo_3;
		var tipo4 = metadata.tipo_4;
		
		data_chart1.push(['Mapeado', tipo3.quantidade + tipo4.quantidade]);
		data_chart1.push(['Não Mapeado', tipo1.quantidade + tipo2.quantidade]);
		
		data_chart2.push(['Orçado', tipo1.orcado + tipo2.orcado, tipo3.orcado + tipo4.orcado]);
		data_chart2.push(['Atualizado', tipo1.atualizado + tipo2.atualizado, tipo3.atualizado + tipo4.atualizado]);
		data_chart2.push(['Empenhado', tipo1.empenhado + tipo2.empenhado, tipo3.empenhado + tipo4.empenhado]);
		data_chart2.push(['Liquidado', tipo1.liquidado + tipo2.liquidado, tipo3.liquidado + tipo4.liquidado]);
		
		var data_chart1 = google.visualization.arrayToDataTable(data_chart1);
		var data_chart2 = google.visualization.arrayToDataTable(data_chart2);
		
		var formatter = new google.visualization.NumberFormat({prefix: 'R$'});
		formatter.format(data_chart2, 1);
		formatter.format(data_chart2, 2);
		
		var chart1 = new google.visualization.PieChart(document.getElementById('chart-quantity-wrapper'));
		var chart2 = new google.visualization.ColumnChart(document.getElementById('chart-values-wrapper'));
		chart1.draw(data_chart1, options_chart1);
		chart2.draw(data_chart2, options_chart2);
	}

	// Code starts here
	$.getJSON(path + 'geocoded.json', function(data) {
		drawMarkers(data.data);
		$('#mapped-list-wrapper').html(mapped_list_html + '</table>');
		$('#notmapped-list-wrapper').html(notmapped_list_html + '</table>');
		drawCharts(data.metadata);
	});
	
	window.markersArray = markersArray;
	window.map = map;
}

function gotoMarker(i) {
	map.setCenter(new google.maps.LatLng(markersArray[i].position.lat(), markersArray[i].position.lng()));
        map.setZoom(16);
	google.maps.event.trigger(markersArray[i], 'click');
	$('html, body').animate({ scrollTop: $('#map-wrapper').offset().top }, 'slow' );
}












var bounds;


var geocoder;
function initialize() {
  geocoder = new google.maps.Geocoder();

   var ne = new google.maps.LatLng(-19.779320,-44.160561);
   var sw = new google.maps.LatLng(-25.250469,-53.109612);
   var bounds = new google.maps.LatLngBounds(sw, ne);
}

function codeAddress() {
  var address = document.getElementById('address').value;
  geocoder.geocode( { 'address': address+'+"são paulo, sp"', 'bounds': bounds }, function(results, status) {
    if (status == google.maps.GeocoderStatus.OK) {
      map.setCenter(results[0].geometry.location);
      map.setZoom(16);
//      var marker = new google.maps.Marker({
//          map: map,
//          position: results[0].geometry.location
//      });
    } else {
      alert('Geocode was not successful for the following reason: ' + status);
    }
  });
}

google.maps.event.addDomListener(window, 'load', initialize);

