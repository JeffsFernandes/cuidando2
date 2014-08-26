<!DOCTYPE html>
<html lang="pt-BR">
    <head>
        <title>Cuidando do meu bairro Creches</title>
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
        <meta charset="utf-8"/>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">

        <!-- Le HTML5 shim, for IE6-8 support of HTML5 elements -->
        <!--[if lte IE 9]><link rel="stylesheet" href="http://cdn.leafletjs.com/leaflet-0.7.2/leaflet.ie.css" /><![endif]-->

        <!--favicon-->
        <link rel="shortcut icon" href="img/favicon.ico" type="image/x-icon"/>

        <!--Leaflet APIs-->
        <script src="http://cdn.leafletjs.com/leaflet-0.7.2/leaflet.js"></script>
        <script src="js/leaflet.markercluster-src.js"></script>
        <script src="js/KML.js"></script>  


        <!--CSS Styles-->
        <link rel="stylesheet" href="http://cdn.leafletjs.com/leaflet-0.7.2/leaflet.css" />
        <link href="css/MarkerCluster.css" rel="stylesheet" />
        <link href="css/MarkerCluster.Default.css" rel="stylesheet" />
        <link href="css/table.css" rel="stylesheet">
        <link href="css/bootstrap.min.css" rel="stylesheet">
        <link href="css/bootstrap-responsive.min.css" rel="stylesheet">
        <link href="css/docs.css" rel="stylesheet">
        <link href="css/l.geosearch.css" rel="stylesheet"/>

        <!--Javascript-->
        <script src="http://ajax.googleapis.com/ajax/libs/jquery/1.8.2/jquery.min.js"></script>
        <script src="http://code.highcharts.com/highcharts.js"></script>
        <script src="http://code.highcharts.com/modules/exporting.js"></script>
        <script src="js/l.control.geosearch.js"></script>
        <script src="js/l.geosearch.provider.openstreetmap.js"></script>

        <!--JQuery-->        
        <script src="js/jquery.csv-0.71.min.js"></script>

        <!--Bootstrap-->
        <script src="js/bootstrap.min.js"></script>
        <script src="js/application.js"></script>
        <script src="data/distritos.json"></script>

    </head>
    <body>   
        <?php include("header.inc.php"); ?>
        <div class="container">

            <header class="jumbotron subhead" id="overview">
                <div class="subnav">
                    <ul class="nav nav-pills">
                        <li><a href="#mapa">Mapa</a></li>
                        <li><a href="#label">Legenda</a></li>
                        <li><a href="#char">Estatísticas</a></li>
                    </ul>
                </div>
            </header>

            <section id="mapa">
                <div class="page-header" style>
                    <h2>Mapa das Creches</h2>
                </div>
                
                <div id="map" style="width: 1170px; height: 700px"></div>
			
                <script>

                    //Icones
                    // Criando ícones customizados

                    $.get("data/creches.csv", function(data) {
                        var creches = $.csv.toArrays(data);

                        var blueIcon = L.Icon.Default.extend({
                            options: {
                                iconUrl: 'img/pin-blue.png',
                                iconSize: [50, 41],
                                popupAnchor: [15, -41],
                            }
                        });
                        var greenIcon = L.Icon.Default.extend({
                            options: {
                                iconUrl: 'img/pin-green.png',
                                iconSize: [50, 41],
                                popupAnchor: [15, -41],
                            }
                        });
                        var orangeIcon = L.Icon.Default.extend({
                            options: {
                                iconUrl: 'img/pin-orange.png',
                                iconSize: [50, 41],
                                popupAnchor: [15, -41],
                            }
                        });

                        var blueIcon = new blueIcon();
                        var greenIcon = new greenIcon();
                        var orangeIcon = new orangeIcon();

                        //Layers
                        var publica = L.markerClusterGroup();
                        var privada = L.markerClusterGroup();

                        //Adiciona Creches e verifica pontos


                        function popUp(feature, layer) {
                            layer.bindPopup(feature.properties.name);
                        }
                        //Verifica pontos na layer e plota as creches
                        
                            for (var i = 1; i < creches.length - 1; i++) {
                                var a = creches[i];                     

                                    //Separa as creches
                                    if (a[4] == 'Privada') {
                                        var marker = L.marker([a[2], a[1]], {icon: greenIcon}).bindPopup(a[3] + "<br>" + "Administração: " + a[4] + "<br>" + "Dependencia Administrativa: " + a[58] + "<br>" + "Tipo: " + a[59] + "<br>" + "Distrito: " + a[6] + "<br>" + "Endereço: " + a[7] + " Nº " + a[8] + "<br>" + "Bairro: " + a[9] + "<br>" + "CEP: " + a[10] + " Telefone: 11 " + a[11] + "<br>" + "Fax: " + a[12] + "<br>" + "e-mail: " + a[13] + "<br>" + "Situação: " + a[14] + "<br>" + " Matriculados: " + a[57] + "<br>" + "Abre aos Finais de semana: " + a[55] + "<br><br>" + "Infraestrutura: " + "<br>" + "Número de Salas: " + a[40] + "<br>" + "Número de Funcionários: " + a[43] + "<br>" + "Acessibilidade: " + a[15] + "<br>" + "Dependencias PNE: " + a[16] + "<br>" + "Sanitário PNE: " + a[17] + "<br>" + "Cozinha: " + a[30] + "<br>" + "Refeitório: " + a[18] + "<br>" + "Despensa: " + a[19] + "<br>" + "Lavanderia: " + a[37] + "<br>" + "Chuveiro: " + a[36] + "Auditorio: " + a[21] + "<br>" + "Laboratório de Informática: " + a[22] + "<br>" + "Laboratório de Ciências: " + a[23] + "<br>" + "Quadra de esportes coberta: " + a[25] + " Descoberta: " + a[26] + "<br>" + "Pátio coberto: " + a[27] + " Descoberto: " + a[28] + "<br>" + "Parque Infantil: " + a[29] + "<br>" + "Biblioteca: " + a[36] + "<br>" + "Berçário: " + a[31] + "<br>" + "Sala de Leitura: " + a[41] + "<br>" + "Area verde: " + a[42] + "Internet: " + a[45] + "<b>" + "TV: " + a[53] + "<br>" + "Multimídia: " + a[52]).addTo(privada);
                                    } else { //Publica
                                        var marker = L.marker([a[2], a[1]], {icon: blueIcon}).bindPopup(a[3] + "<br>" + "Distrito: " + a[6] + "<br>" + "Endereço: " + a[7] + " Nº " + a[8] + "<br>" + "Bairro: " + a[9] + "<br>" + "CEP: " + a[10] + " Telefone: 11 " + a[11] + "<br>" + "Fax: " + a[12] + "<br>" + "e-mail: " + a[13] + "<br>" + "Situação: " + a[14] + "<br>" + "Matriculados: " + a[57] + "<br>" + "Abre aos Finais de semana: " + a[55] + "<br><br>" + "Infraestrutura: " + "<br>" + "Número de Salas: " + a[40] + "<br>" + "Número de Funcionários: " + a[43] + "<br>" + "Acessibilidade: " + a[15] + "<br>" + "Dependencias PNE: " + a[16] + "<br>" + "Sanitário PNE: " + a[17] + "<br>" + "Cozinha: " + a[30] + "<br>" + "Refeitório: " + a[18] + "<br>" + "Despensa: " + a[19] + "<br>" + "Lavanderia: " + a[37] + "<br>" + "Chuveiro: " + a[36] + "<br>" + "Auditorio: " + a[21] + "<br>" + "Laboratório de Informática: " + a[22] + "<br>" + "Laboratório de Ciências: " + a[23] + "<br>" + "Quadra de esportes coberta: " + a[25] + " Descoberta: " + a[26] + "<br>" + "Pátio coberto: " + a[27] + " Descoberto: " + a[28] + "<br>" + "Parque Infantil: " + a[29] + "<br>" + "Biblioteca: " + a[36] + "<br>" + "Berçário: " + a[31] + "<br>" + "Sala de Leitura: " + a[41] + "<br>" + "Area verde: " + a[42] + "<br>" + "Internet: " + a[45] + "<br>" + "TV: " + a[53] + "<br>" + "Multimídia: " + a[52]).addTo(publica);
                                    }

                            }
                       

                        //Configuração tile do mapa
                        var cmAttr = '&copy; Mapbox &copy OpenStreetMap',
                                cmUrl = 'http://{s}.tiles.mapbox.com/v3/renansfs.ia0j96ji/{z}/{x}/{y}.png';
                        var minimal = L.tileLayer(cmUrl, {styleId: 22677, attribution: cmAttr});

                        //Criacao do Mapa e adicionar os distritos
                        var map = L.map('map', {
                            center: [-23.58098, -46.61293],
                            zoom: 11,
                            layers: [minimal, publica, privada]
                        });
                        
                        //var distritos = new L.KML("data/distritos.kml", {async: true});
                        //map.addLayer(distritos);
                        
                        function getColor(d) {
                            return d > 1000 ? '#800026' :
                                   d > 500  ? '#BD0026' :
                                   d > 200  ? '#E31A1C' :
                                   d > 100  ? '#FC4E2A' :
                                   d > 50   ? '#FD8D3C' :
                                   d > 20   ? '#FEB24C' :
                                   d > 10   ? '#FED976' :
                                              '#FFEDA0';
                        }

                        function style(feature) {
                            var distritosHash = {};
                            $.get("data/filas.csv", function(data) {
                                var creches = $.csv.toArrays(data);
                                for(i = 1; i < creches.length; i++){
                                    var distrito = creches[i].toString();
                                    var indexComma = distrito.indexOf(",");
                                    var fila = distrito.substr(indexComma + 1);
                                    var distrito = distrito.substr(0, indexComma);
                                    distritosHash[distrito] = fila;                                
                                }
                            });
                            console.log(distritosHash);
                            
                            return {
                                fillColor: getColor(1200),
                                weight: 2,
                                opacity: 1,
                                color: 'white',
                                dashArray: '3',
                                fillOpacity: 0.7
                            };
                        }

                        var distritos = new L.GeoJSON(distritoData, {style: style});
                        map.addLayer(distritos);
                        
                        
                        //adiciona busca por endereco
                        new L.Control.GeoSearch({
                            provider: new L.GeoSearch.Provider.OpenStreetMap(),
			    position: 'topright',
			    showMarker: false
                        }).addTo(map);


                        //Adicionado Layers
                        var baseLayers = {
                            "Minimal": minimal,
                        };

                        //Overlays
                        var overlays = {
                            "Públicas": publica,
                            "Privadas": privada,
                            "Distritos": distritos
                        };

                        L.control.layers(baseLayers, overlays).addTo(map);


                    });
                </script>


            </section>

            <section id="label">
                <div class="page-header">
                    <h2>Legenda dos Marcadores</h2>
                </div>
                <div class="row">
                    <div style="width:397px; margin:0 auto;">
                        <table id="label" cellspacing="0">
                            <tr>
                                <th scope="col" class="nobg"></th>
                                <th scope="col">Significado</th>
                            </tr>

                            <tr>
                                <th scope="row" class="spec" style="text-align: left"><img src="img/pin-green.png" width="22" height="32"></img></th>
                                <td>As creches são <b>Conveniadas</b>.</td>
                            </tr>

                            <tr>
                                <th scope="row" class="specalt" style="text-align: left"><img src="img/pin-blue.png" width="22" height="32"></img></th>
                                <td class="alt">As creches são <b>Públicas</b>.</td>
                            </tr>


                        </table>
                    </div>
                </div>
            </section>

            <section id="char">
                <div class="page-header">
                    <h2>Estatísticas</h2>
                </div>
                <div class="columns">
   
                    <div id = "containere" style = "min-width: 310px; height: 400px; margin: 0 auto"> </div>
                    <script>
                        var a = 0;
                        var pub = new Array(12); //diretorias de ensino publicas
			var conv = new Array(12);
			while(a<13){
				pub[a] = 0;
				conv[a] = 0;				
				a++;
			}                        
			$.get("data/creches.csv", function(data) {
                            var creches = $.csv.toArrays(data);
			
                            for (var i = 1; i < creches.length - 1; i++) {
                                var a = creches[i];
				if(a[6] == 'JARDIM PAULISTA' || a[6] == 'ITAIM BIBI' || a[6] == 'BUTANTA' || a[6] == 'RIO PEQUENO' || a[6] == 'PINHEIROS' || a[6] == 'ALTO DE PINHEIROS' || a[6] == 'MORUMBI' || a[6] == 'RAPOSO TAVARES' || 					a[6] == 'VILA SONIA'){ //BUTANTA
					if(a[4] == 'Privada') conv[0] = conv[0] + 1;
					else pub[0] = pub[0]+1;
				}else if(a[6] == 'CAMPO LIMPO' || a[6] == 'JARDIM SAO LUIS' || a[6] == 'VILA ANDRADE' || a[6] == 'CAPAO REDONDO' || a[6] == 'JARDIM ANGELA'){ //CAMPO LIMPO
					if(a[4] == 'Privada') conv[1] = conv[1] + 1;
					else pub[1] = pub[1]+1;
				}
				else if(a[6] == 'CIDADE DUTRA' || a[6] == 'GRAJAU' || a[6] == 'MARSILAC' || a[6] == 'PARELHEIROS' || a[6] == 'SOCORRO'){ //CAPELA DO SOCORRO
					if(a[4] == 'Privada') conv[2] = conv[2] + 1;
					else pub[2] = pub[2]+1;
				}
				else if(a[6] == 'LIMAO' || a[6] == 'BRASILANDIA' || a[6] == 'FREGUESIA DO O' || a[6] == 'CASA VERDE' || a[6] == 'CACHOEIRINHA'){  //FREQUESIA/BRASILANDIA
					if(a[4] == 'Privada') conv[3] = conv[3] + 1;
					else pub[3] = pub[3]+1;
				}
				else if(a[6] == 'GUAIANASES' || a[6] == 'LAJEADO' || a[6] == 'CIDADE TIRADENTES'){ //GUAIANASES
					if(a[4] == 'Privada') conv[4] = conv[4] + 1; 
					else pub[4] = pub[4]+1;
				}
				else if(a[6] == 'REPUBLICA' || a[6] == 'BELA VISTA' || a[6] == 'BOM RETIRO' || a[6] == 'CAMBUCI' || a[6] == 'CONSOLACAO' ||	a[6] == 'CURSINO' || a[6] == 'IPIRANGA' || a[6] == 'LIBERDADE' || a[6] == 'MOEMA' || a[6] == 'SACOMA' || a[6] == 'SANTA CECILIA' || a[6] == 'SAO LUCAS' || a[6] == 'SAUDE' || a[6] == 'SE' || a[6] == 'VILA MARIANA' || a[6] == 'VILA PRUDENTE'){ //IPIRANGA
					if(a[4] == 'Privada') conv[5] = conv[5] + 1;
					else pub[5] = pub[5]+1;
				}
				else if(a[6] == 'ARICANDUVA' || a[6] == 'CARRAO' || a[6] == 'CIDADE LIDER' || a[6] == 'ITAQUERA' || a[6] == 'JOSE BONIFACIO' || a[6] == 'PARQUE DO CARMO' || a[6] == 'VILA FORMOSA'){ //ITAQUERA
					if(a[4] == 'Privada') conv[6] = conv[6] + 1;
					else pub[6] = pub[6]+1;
				}
				else if(a[6] == 'JACANA' || a[6] == 'MANDAQUI' || a[6] == 'SANTANA' || a[6] == 'TREMEMBE' || a[6] == 'TUCURUVI' || a[6] == 'VILA GUILHERME' || a[6] == 'VILA MARIA' || a[6] == 'VILA MEDEIROS'){ 
					if(a[4] == 'Privada') conv[7] = conv[7] + 1;
					else pub[7] = pub[7]+1; //JACANA - TREMEMBE
				}
				else if(a[6] == 'ITAIM PAULISTA' || a[6] == 'JARDIM HELENA' || a[6] == 'SAO MIGUEL' || a[6] == 'VILA CURUCA' || a[6] == 'VILA JACUI'){ //SAO MIGUEL PAULISTA
					if(a[4] == 'Privada') conv[8] = conv[8] + 1;
					else pub[8] = pub[8]+1;
				}
				else if(a[6] == 'AGUA RASA' || a[6] == 'ARTUR ALVIM' || a[6] == 'BELEM' || a[6] == 'BRAS' || a[6] == 'CANGAIBA' || a[6] == 'ERMELINO MATARAZZO' || a[6] == 'MOOCA' || a[6] == 'PARI' || a[6] == 'PENHA' ||
				a[6] == 'PONTE RASA' || a[6] == 'TATUAPE' || a[6] == 'VILA MATILDE'){ //PENHA
					if(a[4] == 'Privada') conv[9] = conv[9] + 1;
					else pub[9] = pub[9]+1;
				}
				else if(a[6] == 'ANHANGUERA' || a[6] == 'BARRA FUNDA' || a[6] == 'JAGUARA' || a[6] == 'JAGUARE' || a[6] == 'JARAGUA' || a[6] == 'LAPA' || a[6] == 'PERDIZES' || a[6] == 'PERUS' || a[6] == 'PIRITUBA' ||
				a[6] == 'SAO DOMINGOS' || a[6] == 'VILA LEOPOLDINA'){ //PIRITUBA
					if(a[4] == 'Privada') conv[10] = conv[10] + 1;
					else pub[10] = pub[10]+1;
				}
				else if(a[6] == 'CAMPO BELO' || a[6] == 'CAMPO GRANDE' || a[6] == 'CIDADE ADEMAR' || a[6] == 'JABAQUARA' || a[6] == 'PEDREIRA' || a[6] == 'SANTO AMARO'){ //SANTO AMARO
					if(a[4] == 'Privada') conv[11] = conv[11] + 1;
					else pub[11] = pub[11]+1;
				}
				else if(a[6] == 'IGUATEMI' || a[6] == 'SAO MATEUS' || a[6] == 'SAO RAFAEL' || a[6] == 'SAPOPEMBA'){
					if(a[4] == 'Privada') conv[12] = conv[12] + 1; //SAO MATEUS
					else pub[12] = pub[12]+1;
				}else{
					console.log(a[6]);
				}
                            }
    
                             $(function() {
                                        $('#containere').highcharts({
                                            chart: {
                                                type: 'column'
                                            },
                                            title: {
                                                text: 'Creches por diretoria de ensino: Publicas, Privadas e Total'
                                            },
                                            subtitle: {
                                                text: ' '
                                            },
                                            xAxis: {
                                                categories: [
                                                    'Butantã',
                                                    'Campo Limpo',
                                                    'Capela do Socorro',
                                                    'Frequesia/Brasilêndia',
                                                    'Guaianazes',
                                                    'Ipiranga',
                                                    'Itaquera',
                                                    'Jaçaba/Tremembé',
                                                    'São Miguel Paulista',
                                                    'Penha',
                                                    'Pirituba',
						    'Santo Amaro',
                                                    'Sao Mateus'
                                                ]
                                            },
                                            yAxis: {
                                                min: 0,
                                                title: {
                                                    text: 'Quantidade de Creches'
                                                }
                                            },
                                            tooltip: {
                                                headerFormat: '<span style="font-size:10px">{point.key}</span><table>',
                                                pointFormat: '<tr><td style="color:{series.color};padding:0">{series.name}: </td>' +
                                                             '<td style="padding:0"><b>{point.y:.1f} </b></td></tr>',
                                                footerFormat: '</table>',
                                                shared: true,
                                                useHTML: true
                                            },
                                            plotOptions: {
                                                column: {
                                                    pointPadding: 0.2,
                                                    borderWidth: 0
                                                }
                                            },
                                            series: [{
                                                    name: 'Públicas',
                                                    data: [pub[0], pub[1], pub[2], pub[3], pub[4], pub[5], pub[6], pub[7], pub[8], pub[9], pub[10], pub[11], pub[12]]

                                                }, {
                                                    name: 'Conveniadas',
                                                    data: [conv[0], conv[1], conv[2], conv[3], conv[4], conv[5], conv[6], conv[7], conv[8], conv[9], conv[10], conv[11], conv[12]]

                                                }, {
                                                    name: 'Total',
                                                    data: [(pub[0]+conv[0]),(pub[1]+conv[1]), (pub[2]+conv[2]), (pub[3]+conv[3]), 							   (pub[4]+conv[4]), (pub[5]+conv[5]), (pub[6]+conv[6]), (pub[7]+conv[7]), (pub[8]+conv[8]), (pub[9]+conv[9]), (pub[10]+conv[10]), (pub[11]+conv[11]), (pub[12]+conv[12])]
                                                }]
                                        });
                                 });
                        });




                    </script>
                </div>

            </section>

            <?php include("footer.inc.php"); ?>
    </body>
</html>
