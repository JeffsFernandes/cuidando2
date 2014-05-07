<!DOCTYPE html>
<html lang="pt-BR">
    <head>
        <title>Cuidando da minha creche</title>
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
                    // Criando Ã­cones customizados

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
                       
        		//Criacao das creches                
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
                        var cmAttr = 'Map data &copy; 2011 OpenStreetMap contributors, Imagery &copy; 2011 CloudMade',
                                cmUrl = 'http://{s}.tile.cloudmade.com/0f41e16652a74c9ba844a8f1a2ffee54/{styleId}/256/{z}/{x}/{y}.png';
                        var minimal = L.tileLayer(cmUrl, {styleId: 22677, attribution: cmAttr});

                        //Criacao do Mapa e adicionar os distritos
                        var map = L.map('map', {
                            center: [-23.58098, -46.61293],
                            zoom: 11,
                            layers: [minimal, publica, privada]
                        });
                        var distritos = new L.KML("data/distritos.kml", {async: true});
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
                    <h2>EstatÃ­sticas</h2>
                </div>
                <div class="columns">
   
                    <div id = "containere" style = "min-width: 310px; height: 400px; margin: 0 auto"> </div>
                    <script>
                        /*
                        var dir = new Array(0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0); //diretorias de ensino
                        $.get("data/creches.csv", function(data) {
                            var creches = $.csv.toArrays(data);
                            for (var i = 1; i < creches.length - 1; i++) {
                                var a = creches[i];
                                dir[0] = dir[0] + 1;
                            }
       
*/                                $(function() {
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
                                                    data: [49.9, 71.5, 106.4, 129.2, 144.0, 176.0, 135.6, 148.5, 216.4, 194.1, 95.6, 54.4]

                                                }, {
                                                    name: 'Conveniadas',
                                                    data: [83.6, 78.8, 98.5, 93.4, 106.0, 84.5, 105.0, 104.3, 91.2, 83.5, 106.6, 92.3]

                                                }, {
                                                    name: 'Total',
                                                    data: [48.9, 38.8, 39.3, 41.4, 47.0, 48.3, 59.0, 59.6, 52.4, 65.2, 59.3, 51.2]
                                                }]
                                        });
                                 });
                     //   });




                    </script>
                </div>

            </section>

            <?php include("footer.inc.php"); ?>
    </body>
</html>
